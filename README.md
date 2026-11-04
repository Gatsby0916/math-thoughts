# math-thoughts

A living notebook for my math flashing ideas 💡

## Why this repo exists

I am a math student, and I get idea bursts all the time.
Some are rough, some are weird, many are unfinished, but they often contain something worth keeping.

This repo is where I catch those thoughts before they disappear.
Not a museum of perfect results, but a workshop for growing ideas 🧠

## What I store here

- quick sparks, questions, analogies, counterexamples
- topic notes I keep refining
- informal write-ups when ideas come
- project materials and experiments


## Write-ups

| Topic | Note | Source |
|---|---|---|
| Functional analysis | From a Single Jump to a Point Mass: A Story of Heaviside and Dirac | [PDF](docs/functional_analysis/dirac_heaviside_measure_story.pdf) · [LaTeX](latex/functional_analysis/dirac_heaviside_measure_story.tex) |
| Stochastic processes | Understanding Diffusion Through Probability Flux and Multi-Sample Paths | [PDF](docs/stochastic_diffusion/probability_flux_multisample_paths.pdf) · [LaTeX](latex/stochastic_diffusion/probability_flux_multisample_paths.tex) · [Markdown](markdown/2026-06-17_stochastic_reaction_diffusion_reflection.md) |
| Complex analysis | A Variational Path to Laplace's Equation via Complex Analysis | [Markdown](markdown/2026-10-07_variational_path_to_laplace.md) |
| Machine learning | Activation Functions: Sigmoid, tanh, arctan, ReLU and Softmax | [PDF](docs/activation_functions/activation_functions.pdf) · [LaTeX](latex/activation_functions/activation_functions.tex) |
| Computer vision and variational calculus | From Four Lights to One Surface | [PDF](docs/photometric_stereo/frankot_chellappa.pdf) · [LaTeX](latex/photometric_stereo/frankot_chellappa.tex) · [Figure script](latex/photometric_stereo/reconstruct.py) |

The monkey-head photographs and the figures derived from them are credited to the University of Strathclyde dataset by Emma Le Francois and colleagues, used under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The note crops and annotates the lighting images and computes new normal, slope and height maps. [Dataset and attribution](https://doi.org/10.15129/44b337ab-9fd9-4983-9079-a0dcfaae1d84)

## How I add ideas

1. **Catch it** — add one line to [`inbox.md`](inbox.md). No polishing.
2. **Grow it** — when an idea has a shape, copy [`templates/note.md`](templates/note.md) to `markdown/YYYY-MM-DD_topic.md`.
3. **Write it up** — ideas that deserve full proofs and numbered equations get a LaTeX version in `latex/<topic>/`, with the compiled PDF in `docs/<topic>/`.

## Folder map

- `inbox.md` - one-line idea capture
- `markdown/` - notes in Markdown
- `latex/` - LaTeX sources, one folder per topic
- `docs/` - compiled PDFs, one folder per topic
- `images/` - figures used by notes
- `resources/` - book notes and references
- `templates/` - note template

Please feel free to discuss with me and share your ideas!
