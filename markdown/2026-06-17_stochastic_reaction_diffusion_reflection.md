# Understanding Diffusion Through Probability Flux and Multi-Sample Paths

Date: 2026-06-17

Diffusion appears in molecular motion, chemical transport, cell migration, ecological spread, financial perturbations, heat flow, and contaminant transport. In these settings diffusion is more than the operator \(D\Delta\). It is a modelling language that connects microscopic random paths to macroscopic probability distributions.

This note develops diffusion from the viewpoint of multi-sample paths, empirical measures, probability density, Fokker--Planck equations, probability flux, and expected absorption time. The full LaTeX version with numbered equations is stored in:

- `latex/stochastic_diffusion/probability_flux_multisample_paths.tex`
- `latex/stochastic_diffusion/probability_flux_multisample_paths.pdf`

## Main Thought

A single diffusion path gives one possible microscopic history:

$$
dX_t=\mu(X_t)\,dt+\sigma(X_t)\,dW_t.
$$

Many independent sample paths produce an empirical measure:

$$
\mu_t^N=\frac{1}{N}\sum_{m=1}^N\delta_{X_t^{(m)}}.
$$

For a test function \(\varphi\),

$$
\int_{\mathbb{R}}\varphi(x)\,d\mu_t^N(x)
=\frac{1}{N}\sum_{m=1}^N\varphi(X_t^{(m)})
\longrightarrow
\mathbb{E}[\varphi(X_t)].
$$

If \(X_t\) has density \(p(x,t)\), then

$$
\mathbb{E}[\varphi(X_t)]
=\int_{\mathbb{R}}\varphi(x)p(x,t)\,dx.
$$

Thus the stable large-sample object is not a single path but a probability density. The density evolves according to the Fokker--Planck equation:

$$
\frac{\partial p}{\partial t}
=-\frac{\partial}{\partial x}\big(\mu(x)p\big)
+\frac{1}{2}\frac{\partial^2}{\partial x^2}\big(\sigma^2(x)p\big).
$$

For Brownian diffusion,

$$
dX_t=\sqrt{2D}\,dW_t,
$$

this reduces to the heat equation:

$$
\frac{\partial p}{\partial t}=D\Delta p.
$$

The probability flux form is

$$
\frac{\partial p}{\partial t}+\nabla\cdot J=0.
$$

For pure diffusion,

$$
J=-D\nabla p.
$$

This gives a direct interpretation of boundary conditions. Reflecting boundaries impose zero flux. Absorbing boundaries remove probability mass. Partially absorbing boundaries can be expressed through Robin-type conditions such as

$$
-D\frac{\partial p}{\partial n}=\kappa p.
$$

The expected absorption time connects diffusion paths to boundary events. If

$$
\tau=\inf\{t:X_t\in\partial\Omega_{\mathrm{abs}}\},
$$

then

$$
T(x)=\mathbb{E}_x[\tau]
$$

satisfies the backward equation

$$
\mathcal{L}T(x)=-1.
$$

For Brownian diffusion,

$$
D\Delta T(x)=-1.
$$

On the interval \([0,L]\) with both endpoints absorbing,

$$
DT''(x)=-1,\qquad T(0)=T(L)=0,
$$

and therefore

$$
T(x)=\frac{x(L-x)}{2D}.
$$

This shows the core mathematical structure:

$$
X_t
\quad\longleftrightarrow\quad
\mu_t^N
\quad\longleftrightarrow\quad
p(x,t)
\quad\longleftrightarrow\quad
J(x,t)
\quad\longleftrightarrow\quad
T(x).
$$

The path gives microscopic random motion, the empirical measure gives multi-sample statistics, the density gives probability distribution, the flux gives probability movement, and the expected absorption time gives the average time scale of a boundary event.
