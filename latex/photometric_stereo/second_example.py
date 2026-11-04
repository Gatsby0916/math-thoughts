"""Draw the cube-corner sequence from four real decoded LED images.

Usage: python second_example.py Out_of_plane_configuration_cube_corner.zip
Data: Emma Le Francois et al., University of Strathclyde, CC BY 4.0.
https://doi.org/10.15129/44b337ab-9fd9-4983-9079-a0dcfaae1d84
Archive: https://pure.strath.ac.uk/ws/portalfiles/portal/99603606/Out_of_plane_configuration_cube_corner.zip
Acquisition and LED coordinates: https://doi.org/10.1364/OE.408658

All four display exports share a grayscale range. Crop their common image
rectangle, then fit the same three unknowns as in the monkey example. On this
object one side is in deep shadow in either LED 1 or LED 4. Omit each pixel's
darkest channel and use the three remaining measurements with equal gains.
Use only the outlined, wholly interior rectangle. Convert normals with
n_z >= 0.2 to slopes and fill the few remaining slopes from the nearest
retained pixel before integration. Draw missing observations white on maps.
For a free-standing patch, keep its mean tilt by reflecting the patch before
periodic FC integration: a slope normal to the reflection axis changes sign,
while the tangential slope retains its sign. Display the original quadrant.
"""

import argparse
import hashlib
import io
import zipfile
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import Normalize
from matplotlib.patches import Rectangle
from PIL import Image
from scipy.ndimage import distance_transform_edt

from reconstruct import LIGHTS_CM, OUTPUT, integrate


ZIP_HASH = "bb76690a957d4c0348ecce02d10b05c8bcaf320779a20000768f814ae2e4dcff"
FRAME = np.s_[93:312, 65:454]
VIEW = np.s_[58:179, 105:256]
PATCH = np.s_[80:150, 127:234]


def read_images(archive):
    if hashlib.sha256(archive.read_bytes()).hexdigest() != ZIP_HASH:
        raise ValueError("This figure uses the Strathclyde out-of-plane cube-corner archive.")
    stack = []
    with zipfile.ZipFile(archive) as src:
        for j in range(1, 5):
            with Image.open(io.BytesIO(src.read(f"Out_of_plane_configuration_cube_corner/LED{j}.png"))) as im:
                stack.append(np.asarray(im.convert("RGB"))[FRAME][..., 0])
    return np.stack(stack, axis=-1).astype(float)


def fit_patch(images):
    obs = images[PATCH]
    light = LIGHTS_CM / np.linalg.norm(LIGHTS_CM, axis=1, keepdims=True)
    darkest = np.argmin(obs, axis=-1)
    g = np.empty((*obs.shape[:2], 3))
    for j in range(4):
        retained_lights = np.arange(4) != j
        pixels = darkest == j
        g[pixels] = obs[pixels][:, retained_lights] @ np.linalg.pinv(light[retained_lights]).T
    normal = g / np.linalg.norm(g, axis=-1, keepdims=True)
    valid = normal[..., 2] >= 0.2
    nearest = tuple(distance_transform_edt(~valid, return_distances=False, return_indices=True))
    n = normal[nearest]
    p = -n[..., 0] / n[..., 2]
    q = n[..., 1] / n[..., 2]
    p_x = np.concatenate([p, -p[:, ::-1]], axis=1)
    q_x = np.concatenate([q, q[:, ::-1]], axis=1)
    p_xy = np.concatenate([p_x, p_x[::-1]], axis=0)
    q_xy = np.concatenate([q_x, -q_x[::-1]], axis=0)
    z = integrate(p_xy, q_xy)[:p.shape[0], :p.shape[1]]
    return normal, valid, p, q, z


def draw(out, images, normal, valid, p, q, z):
    plt.rcParams.update({"font.size": 10, "savefig.facecolor": "white"})
    fig = plt.figure(figsize=(8.0, 7.15))
    # Each strip follows the same left margin, with a step title above it.
    ink = "#22343f"
    for y, title in [(0.968, "1   Illuminate the same corner"),
                     (0.670, "2   Estimate the tilt on the outlined patch"),
                     (0.384, "3   Integrate the two slopes")]:
        fig.text(0.045, y, title, va="top", fontsize=12.2, fontweight="semibold", color=ink)
    for j in range(4):
        ax = fig.add_axes([0.045 + j * 0.232, 0.727, 0.214, 0.196])
        ax.imshow(images[VIEW][..., j], cmap="gray", vmin=0, vmax=255, interpolation="nearest")
        ax.add_patch(Rectangle((PATCH[1].start - VIEW[1].start - 0.5,
                                PATCH[0].start - VIEW[0].start - 0.5),
                               z.shape[1], z.shape[0], fill=False, linewidth=0.7,
                               edgecolor="#ffd679", linestyle=(0, (3.5, 2.5))))
        ax.set_axis_off()
        ax.text(0.5, -0.05, f"LED {j + 1}", ha="center", va="top", transform=ax.transAxes)

    rgb = (normal + 1) / 2
    rgb[~valid] = 1
    panels = [(rgb, "Normal"), (np.ma.masked_where(~valid, p), "Across"),
              (np.ma.masked_where(~valid, q), "Down")]
    for j, (data, title) in enumerate(panels):
        ax = fig.add_axes([0.05 + j * 0.306, 0.464, 0.284, 0.158])
        if j == 0:
            ax.imshow(data, interpolation="nearest")
        else:
            im = ax.imshow(data, cmap="RdBu_r", vmin=-4.5, vmax=4.5, interpolation="nearest")
        ax.set_axis_off()
        ax.text(0.5, -0.07, title, va="top", ha="center", transform=ax.transAxes)
    bar = fig.colorbar(im, cax=fig.add_axes([0.945, 0.465, 0.011, 0.156]),
                       ticks=[-4, 0, 4])
    bar.ax.tick_params(length=2, labelsize=8)

    # Common height scale and equal x, y, z data-unit lengths in the oblique view.
    norm = Normalize(z.min(), z.max())
    rows, cols = np.indices(z.shape)
    ax = fig.add_axes([0.072, 0.083, 0.365, 0.25])
    im = ax.imshow(z, cmap="viridis", norm=norm, interpolation="nearest")
    ax.set_axis_off()
    ax.text(0.5, -0.08, "Height map", va="top", ha="center", transform=ax.transAxes)
    ax = fig.add_axes([0.45, 0.040, 0.46, 0.318], projection="3d")
    ax.plot_surface(cols, z.shape[0] - 1 - rows, z, cmap="viridis", norm=norm,
                    rstride=1, cstride=1, linewidth=0, antialiased=False)
    ax.plot_wireframe(cols, z.shape[0] - 1 - rows, z, rstride=10, cstride=9,
                      color="#183c48", linewidth=0.45, alpha=0.55)
    ax.set_box_aspect((z.shape[1] - 1, z.shape[0] - 1, np.ptp(z)), zoom=1.22)
    ax.view_init(elev=65, azim=125)
    ax.set_axis_off()
    ax.text2D(0.5, -0.005, "Oblique view", ha="center", transform=ax.transAxes)
    cb = fig.colorbar(im, cax=fig.add_axes([0.924, 0.076, 0.012, 0.246]))
    cb.ax.tick_params(labelsize=8, length=2)
    cb.set_label("Height (pixel units)", fontsize=9)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=255, bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--output", type=Path, default=OUTPUT / "second_example.png")
    args = parser.parse_args()
    images = read_images(args.archive)
    normal, valid, p, q, z = fit_patch(images)
    draw(args.output, images, normal, valid, p, q, z)
    print(f"Patch {z.shape}. Fitted slopes at {valid.sum()} of {valid.size} pixels.")
