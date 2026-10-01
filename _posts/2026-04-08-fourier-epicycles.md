---
layout: post
title: fourier epicycles
date: 2026-04-08
description: spinning circles stacked end to end that trace any closed curve
tags: visual-proofs interactive
categories: math
kind: interactive
thumbnail: /assets/img/projects/fourier-epicycles.svg
related_posts: false
---

<div class="viz" id="fourier-epicycles"></div>
<script src="{{ '/assets/notebook/viz/fourier-epicycles.js' | relative_url | bust_file_cache }}" defer></script>

Think of a closed curve as a point $$z(t)$$ moving in the complex plane, going once around as $$t$$ runs from 0 to 1. Any such curve can be written as a sum of rotating vectors:

$$
z(t) = \sum_{k} c_k e^{2\pi i k t}.
$$

Each term is an arrow of length $$\vert c_k \vert$$ spinning $$k$$ times per lap. Positive $$k$$ spins counterclockwise and negative $$k$$ spins clockwise, and you need both. Put the arrows tip to tail and the last tip draws the curve. The circles are just the paths each arrow sweeps out.

Where do the $$c_k$$ come from? Sample the curve at $$N$$ evenly spaced points $$z_0, \dots, z_{N-1}$$ and take the discrete Fourier transform:

$$
c_k = \frac{1}{N} \sum_{n=0}^{N-1} z_n e^{-2\pi i k n / N}.
$$

The page sorts the terms by $$\vert c_k \vert$$ and keeps the biggest ones, so the slider adds circles from largest to smallest. The constant term $$c_0$$ is the center of the curve and is always kept. "Energy captured" is $$\sum \vert c_k \vert^2$$ over the kept terms divided by the total, which by Parseval is how much of the curve's spread you have accounted for.

The square preset is a triangle wave in $$x$$ and a square wave in $$y$$, so the tip slides along the top, jumps down, slides back along the bottom, and jumps up. The jumps are where the Gibbs phenomenon shows up. Add circles and the wiggles get squeezed toward the corners, but the peak stays about 9% of the jump above the edge. It never goes away.

For your own drawing, the path is resampled to 256 points evenly spaced by arc length before the transform.

Source: [assets/notebook/viz/fourier-epicycles.js](https://github.com/bbioren/bbioren.github.io/blob/main/assets/notebook/viz/fourier-epicycles.js)
