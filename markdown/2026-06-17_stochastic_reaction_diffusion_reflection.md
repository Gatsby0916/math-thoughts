# Stochastic Modelling of Reaction-Diffusion Processes: A Post-Exam Reflection

Date: 2026-06-17

After finishing the exam, I feel that this course changed my understanding of stochastic modelling in a very concrete way. Before this course, I often treated differential equations, probability distributions, and simulation algorithms as separate tools. Now I see them as different languages for describing the same evolving system.

The central lesson is that a model is not only a formula. It is a choice about which uncertainty matters, which scale is being observed, and which mathematical object is carrying the state of the system.

## 1. From deterministic rates to random events

In a deterministic reaction model, concentration changes smoothly according to an ODE. This is powerful, but it hides the fact that reactions are discrete events. The stochastic simulation viewpoint makes this visible:

- a reaction channel has a propensity;
- the next event time is random;
- the next reaction type is random;
- one trajectory is only one possible history.

This helped me understand why the same chemical system can have both a deterministic description and a stochastic description. The ODE is not "wrong"; it is a large-scale or averaged view. But when copy numbers are small, or when switching between states is important, the randomness is not just noise around the truth. It can become the mechanism.

## 2. The chemical master equation as probability flow

The chemical master equation gave me a new way to think about probability distributions. A distribution is not just a static summary such as a mean or variance. It is an evolving object whose mass moves between states.

This was an important shift for me:

- the state variable can be a molecule count;
- the unknown can be the whole probability distribution;
- the mean and variance are projections of a deeper object;
- long-time limits describe where probability mass eventually settles.

The probability generating function was especially useful because it connects discrete probability with calculus. It turns an infinite collection of probabilities into one function, and then questions about moments or steady states become analytic questions.

## 3. Mean, variance, and the limits of averages

This course also made me more careful about means. In many applied problems, the mean trajectory can look simple while the actual distribution is broad, skewed, or even multimodal.

That matters because a mean can hide:

- rare but important events;
- switching between favourable states;
- stochastic focusing;
- self-induced stochastic resonance;
- the time scale of escape from a stable region.

So one of my biggest takeaways is that "compute the expectation" is not always the same as "understand the system". Sometimes variance, hitting time, switching time, or full distributional shape carries the real modelling insight.

## 4. SDEs and diffusion as local uncertainty

The diffusion part clarified the connection between microscopic random movement and macroscopic equations. Brownian motion and stochastic differential equations describe local uncertain motion, while the Fokker-Planck equation describes how density evolves.

The same process can therefore be viewed in at least two ways:

- path view: where is this particle likely to move next?
- density view: how does a cloud of many particles spread over time?

This changed how I think about PDEs. A diffusion equation is not only a deterministic smoothing equation. It can be the collective shadow of many random paths.

## 5. Boundaries are part of the model

Reaction-diffusion problems made boundary conditions feel more meaningful. Reflecting, absorbing, and partially absorbing boundaries are not just technical details added after writing down an equation. They encode physical assumptions:

- can the particle leave the domain?
- is the boundary reactive?
- is absorption immediate or probabilistic?
- what is the expected time before capture?

Mean exit time problems made this especially clear. The geometry of the domain, the dimension, and the boundary behaviour all become part of the probability calculation.

## 6. Algorithms are mathematical viewpoints

I also learned that simulation algorithms are not just implementation details. The naive stochastic simulation algorithm, Gillespie's algorithm, first-reaction method, next-reaction method, and multiscale methods each express a different way of organizing randomness and computational effort.

The practical question is not only "can this simulate the model?" but also:

- which events are frequent or rare?
- which time scale dominates?
- which variables need exact stochastic treatment?
- where is an approximation acceptable?

This made algorithmic efficiency feel like part of modelling, not something separate from it.

## 7. A personal modelling principle

The course leaves me with a principle I want to keep:

> Start by asking what object should evolve: a state, a trajectory, a distribution, a density, or a moment.

Once that is clear, the mathematical tools become much easier to place:

- ODEs describe averaged deterministic state change;
- CMEs describe probability flow over discrete states;
- PGFs compress discrete distributions into analytic functions;
- SDEs describe random continuous paths;
- Fokker-Planck equations describe evolving densities;
- backward equations answer hitting-time and switching-time questions;
- simulation algorithms generate sample histories when closed forms are hard.

This is why I feel the course improved my stochastic modelling ability. It connected differential equations and probability distributions into one modelling framework. More importantly, it made me more sensitive to when randomness should be averaged away and when it must be kept.

## Questions I want to keep thinking about

1. How can we decide, before simulating, whether a deterministic approximation will miss the key behaviour?
2. When is it better to study a full distribution rather than only moments?
3. How should multiscale models choose which variables remain stochastic?
4. Can mean switching time be used as a practical diagnostic for model stability?
5. How do reaction-diffusion models change when spatial heterogeneity is not just background, but the main driver?

These questions feel worth carrying forward into future work on stochastic processes, applied probability, mathematical biology, and simulation-based modelling.
