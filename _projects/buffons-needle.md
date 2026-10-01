---
layout: page
title: Buffon's Needle
description: drop needles on lined paper and watch them count out pi
img: assets/img/projects/buffons-needle.svg
importance: 2
category: include
math: true
---

<div class="viz" id="buffons-needle"></div>
<script src="{{ '/assets/notebook/viz/buffons-needle.js' | relative_url | bust_file_cache }}" defer></script>

Draw parallel lines $$d$$ apart and drop a needle of length $$\ell \le d$$ on them. Its center lands at a uniform random spot and it points in a uniform random direction. Needles that cross a line are orange, the rest are blue. What is the chance a needle crosses a line?

Let $$x$$ be the distance from the needle's center to the nearest line, so $$x$$ is uniform on $$[0, d/2]$$, and let $$\theta$$ be the angle between the needle and the lines, uniform on $$[0, \pi]$$. The needle reaches $$\frac{\ell}{2}\sin\theta$$ above and below its center, so it crosses exactly when $$x \le \frac{\ell}{2}\sin\theta$$. For a fixed angle that happens with probability $$\frac{\ell \sin\theta}{d}$$. Averaging over the angle,

$$
P(\text{cross}) = \frac{1}{\pi}\int_0^\pi \frac{\ell \sin\theta}{d}\, d\theta = \frac{2\ell}{\pi d}.
$$

So $$\pi$$ shows up in a question about needles and lines, and we can solve for it. After $$N$$ drops with $$C$$ crossings, $$C/N$$ estimates $$P(\text{cross})$$, which gives

$$
\hat\pi = \frac{2\ell N}{d\,C}.
$$

The plot under the board tracks $$\hat\pi$$ as $$N$$ grows. It wanders a lot early and settles slowly. Why so slow? $$C$$ is a binomial count, so the fraction $$C/N$$ has standard deviation $$\sqrt{p(1-p)/N}$$, and the error in $$\hat\pi$$ shrinks like $$1/\sqrt{N}$$. To get one more correct digit you need about 100 times as many needles. With $$\ell = d$$ the error after $$N$$ drops is roughly $$2.37/\sqrt{N}$$, so ten thousand needles typically gets you within about $$0.02$$ of $$\pi$$. Longer needles cross more often and give a slightly better estimate, which you can see by moving the slider.

Source: [assets/notebook/viz/buffons-needle.js](https://github.com/bbioren/bbioren.github.io/blob/main/assets/notebook/viz/buffons-needle.js)
