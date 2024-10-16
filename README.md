![Tests](https://github.com/turczyneq/pypesh/actions/workflows/test.yml/badge.svg)

FEM advection diffusion solver
==============================

This repository attempts to find a solution to advection diffusion problem

$$ 0 = \Delta \phi - \mathrm{Pe} (u \cdot \nabla \phi) $$

with $\phi = 1$ for $z \to \infty$ and $\phi = 0$ on a surface of the sphere and $\mathrm{Pe}$ denoting Peclet number. Final determined value is Sherwood number defined as 

$$ \mathrm{Sh} = \frac{\Phi}{ 4 \pi D R}$$

Where $D$ is diffusion constant and $\Phi$ is flux falling onto the sphere.

![Some solution of advection diffusion type problem](/graphics/sample_image.png)

We use two approaches: `scikit-fem` package to handle solving which requires rewriting equations in weak form for smaller peclets and `pychastic` to generate and trace trajcetories of single particles and .

License
-------
Copyright (C) 2024  Radost Waszkiewicz and Jan Turczynowicz.
This repository is published under GPL3.0 license.

Bibliography
------------
 - *Bubbles, Drops and Particles*; R. Clift, J. Grace, M. Weber (1978)
 - *Electrochemical measurements of mass transfer between a sphere and liquid in motion at high Peclet numbers*; S. Kutateladze, V. Nakoryakov, M. Iskakov (1982)
 - *Mass and heat transfer from fluid spheres at low Reynolds numbers*; Z. Feng, E. Michaelides (2000)
 - *Heat transfer from spheres to flowing media*; H. Kramers (1946)
