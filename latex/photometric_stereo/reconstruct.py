"""Recreate the monkey-head figures from the CC BY 4.0 Strathclyde archive.

Usage: python reconstruct.py Out_of_plane_configuration_monkey_head.zip
Data: https://doi.org/10.15129/44b337ab-9fd9-4983-9079-a0dcfaae1d84
Acquisition geometry: Le Francois et al., https://doi.org/10.1364/OE.408658
The data authors released four grayscale display exports from decoded video.
We use their shared display scale, with no per-image rescaling or gamma change.
Dependencies: matplotlib, numpy, Pillow, scipy.
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
from PIL import Image
from scipy import ndimage


ZIP_HASH = "b51629acc9110f772ed3e073afa2ba7b51e57ade7b6c2f81853395271e8f2ce9"
LIGHTS_CM = np.array([[-27, 42, 10], [-14, 42, 35], [14, 42, 35], [27, 42, 10]])
# Coordinates in the decoded 219 by 389 image, after removing the export margins.
VIEW = np.s_[45:174, 98:261]
EXAMPLE_PIXEL = (95, 160)
OUTPUT = Path(__file__).resolve().parents[2] / "images" / "photometric_stereo"


def read_intensities(archive):
    if hashlib.sha256(archive.read_bytes()).hexdigest() != ZIP_HASH:
        raise ValueError("The archive checksum differs from the published example used here.")
    images = []
    with zipfile.ZipFile(archive) as source:
        for index in range(1, 5):
            path = f"Out_of_plane_configuration_monkey_head/LED{index}.png"
            with Image.open(io.BytesIO(source.read(path))) as im:
                # All four exports have the same image rectangle and colorbar limits.
                image = np.asarray(im.convert("RGB"))[93:312, 65:454, 0].copy()
                images.append(image)
    return np.stack(images, axis=-1).astype(float)


def surface_slopes(intensity):
    light = LIGHTS_CM / np.linalg.norm(LIGHTS_CM, axis=1, keepdims=True)
    g = intensity @ np.linalg.pinv(light).T
    rho = np.linalg.norm(g, axis=-1)
    normal = np.divide(g, rho[..., None], out=np.zeros_like(g), where=rho[..., None] > 0)

    bright = np.zeros(rho.shape, dtype=bool)
    bright[VIEW] = intensity[VIEW].max(axis=-1) >= 18
    labels, _ = ndimage.label(bright)  # Four-connected foreground.
    largest = 1 + np.bincount(labels.ravel())[1:].argmax()
    silhouette = ndimage.binary_fill_holes(labels == largest)
    retained = (silhouette & (normal[..., 2] >= 0.2)
                & ((intensity >= 8).sum(axis=-1) >= 3))
    # Row increases down the picture, while the lighting frame has y upwards.
    p = np.zeros_like(rho)
    q_row = np.zeros_like(rho)
    p[retained] = -normal[..., 0][retained] / normal[..., 2][retained]
    q_row[retained] = normal[..., 1][retained] / normal[..., 2][retained]
    return light, g, rho, normal, silhouette, retained, p, q_row


def integrate(p, q_row):
    rows, cols = p.shape
    # Unit pixel spacing. Use exact zeros at the constant and any Nyquist modes.
    def symbol(size):
        d = 1j * np.sin(2 * np.pi * np.fft.fftfreq(size))
        d[0] = 0
        if size % 2 == 0:
            d[size // 2] = 0
        return d

    dx, dr = symbol(cols)[None, :], symbol(rows)[:, None]
    denominator = np.abs(dx) ** 2 + np.abs(dr) ** 2
    numerator = dx.conj() * np.fft.fft2(p) + dr.conj() * np.fft.fft2(q_row)
    coeff = np.divide(numerator, denominator, out=np.zeros_like(numerator),
                      where=denominator > 0)
    return np.fft.ifft2(coeff).real


def save_figures(out, intensity, rho, normal, silhouette, retained, p, q_row, height):
    out.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
                         "savefig.facecolor": "white", "figure.facecolor": "white"})
    fig, axes = plt.subplots(1, 4, figsize=(8.2, 2.2), layout="constrained")
    for j, ax in enumerate(axes):
        ax.imshow(intensity[VIEW][..., j], cmap="gray", vmin=0, vmax=255,
                  interpolation="nearest")
        row, col = EXAMPLE_PIXEL
        ax.plot(col - VIEW[1].start, row - VIEW[0].start, marker="o",
                markersize=5, markerfacecolor="none", markeredgecolor="#ffc85b",
                markeredgewidth=0.85)
        ax.set_title(f"LED {j + 1}", weight="bold")
        ax.set_xlabel("({:d}, {:d}, {:d}) cm".format(*LIGHTS_CM[j]))
        ax.set(xticks=[], yticks=[])
    fig.savefig(out / "monkey_inputs.png", dpi=240, bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)

    def show_only(values, mask):
        return np.ma.masked_where(~mask[VIEW], values[VIEW])

    def horizontal_bar(fig, axis, mappable, ticks=None):
        bar = fig.colorbar(mappable, ax=axis, orientation="horizontal", pad=0.06,
                           aspect=24, shrink=0.90, ticks=ticks)
        bar.ax.tick_params(labelsize=8, length=2)
        return bar

    fig, axes = plt.subplots(1, 4, figsize=(8.4, 2.25), layout="constrained")
    for ax in axes:
        ax.set(xticks=[], yticks=[], frame_on=False)
    rmax = np.ceil(rho[retained].max() / 25) * 25
    im = axes[0].imshow(show_only(rho, retained), cmap="cividis", vmin=0, vmax=rmax)
    axes[0].set_title(r"Amplitude $\hat\rho$")
    horizontal_bar(fig, axes[0], im)
    rgb = (normal[VIEW] + 1) / 2
    rgb[~retained[VIEW]] = 1
    axes[1].imshow(rgb, interpolation="nearest")
    axes[1].set_title("Unit normal")
    axes[1].set_xlabel(r"RGB = $(\mathbf{n}+1)/2$", fontsize=9)
    for ax, v, title in zip(axes[2:], [p, q_row], [r"Across $p$", r"Down $q_{\rm row}$"]):
        im = ax.imshow(show_only(v, retained), cmap="RdBu_r", vmin=-2, vmax=2,
                       interpolation="nearest")
        ax.set_title(title)
        horizontal_bar(fig, ax, im, [-2, 0, 2]).set_label("slope", fontsize=8)
    fig.savefig(out / "monkey_maps.png", dpi=240, bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)

    z = np.where(silhouette[VIEW], height[VIEW], np.nan)
    norm = Normalize(vmin=np.nanmin(z), vmax=np.nanmax(z))
    rows, cols = np.indices(z.shape)
    y = z.shape[0] - 1 - rows
    fig = plt.figure(figsize=(8.3, 3.0), layout="constrained")
    gs = fig.add_gridspec(1, 3, width_ratios=[1, 1.3, 0.045])
    ax = fig.add_subplot(gs[0])
    ax.imshow(z, cmap="viridis", norm=norm, interpolation="nearest",
              extent=(-0.5, z.shape[1] - 0.5, -0.5, z.shape[0] - 0.5))
    ax.set(xlabel="x (crop pixels)", ylabel="y (crop pixels)", title="Relative height")
    surface = fig.add_subplot(gs[1], projection="3d")
    # An explicit triangle list prevents bridges or artificial walls at the silhouette.
    idx = np.arange(z.size).reshape(z.shape)
    a, b, c, d = idx[:-1, :-1], idx[:-1, 1:], idx[1:, :-1], idx[1:, 1:]
    triangles = np.concatenate([np.stack([a, c, b], axis=-1).reshape(-1, 3),
                                np.stack([b, c, d], axis=-1).reshape(-1, 3)])
    triangles = triangles[np.isfinite(z.ravel()[triangles]).all(axis=1)]
    surface.plot_trisurf(cols.ravel(), y.ravel(), z.ravel(), triangles=triangles,
                         cmap="viridis", norm=norm, linewidth=0, antialiased=False)
    surface.set(xlim=(0, z.shape[1] - 1), ylim=(0, z.shape[0] - 1),
                zlim=(norm.vmin, norm.vmax), title="Oblique view",
                xticks=[0, 40, 80, 120, 160], yticks=[0, 40, 80, 120], zticks=[-10, 0, 10])
    surface.set_box_aspect((z.shape[1] - 1, z.shape[0] - 1, norm.vmax - norm.vmin))
    surface.view_init(elev=32, azim=-66)
    surface.set_xlabel("x", labelpad=-2)
    surface.set_ylabel("y", labelpad=-2)
    surface.tick_params(labelsize=7, pad=0)
    fig.colorbar(plt.cm.ScalarMappable(norm, cmap="viridis"), cax=fig.add_subplot(gs[2]),
                 label="Relative height (pixel units)")
    fig.savefig(out / "monkey_surface.png", dpi=240, bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    intensity = read_intensities(args.archive)
    light, g, rho, normal, silhouette, retained, p, q_row = surface_slopes(intensity)
    height = integrate(p, q_row)
    save_figures(args.output, intensity, rho, normal, silhouette, retained, p, q_row, height)
    np.set_printoptions(precision=5, suppress=True)
    rc = EXAMPLE_PIXEL
    print("Example full-frame (row, column)", rc, "I", intensity[rc], "g", g[rc],
          "rho", rho[rc], "n", normal[rc], "p, q_row", p[rc], q_row[rc],
          "predicted", light @ g[rc])
    print("Light rank, condition", np.linalg.matrix_rank(light), np.linalg.cond(light))
    print("Foreground pixels, retained slopes", silhouette.sum(), retained.sum())
    print("Global mean, foreground height min/max", height.mean(),
          height[silhouette].min(), height[silhouette].max())
    dx = (np.roll(height, -1, axis=1) - np.roll(height, 1, axis=1)) / 2
    dr = (np.roll(height, -1, axis=0) - np.roll(height, 1, axis=0)) / 2
    print("Squared slope residual relative to zero height (full domain)",
          ((dx-p)**2 + (dr-q_row)**2).sum() / (p**2 + q_row**2).sum())


if __name__ == "__main__":
    main()
