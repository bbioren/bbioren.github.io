---
layout: post
title: why n minus one
date: 2026-04-22
description: the degree of freedom you lose is a direction you can draw
tags: visual-proofs statistics linear-algebra
categories: math
related_posts: false
---

Every intro stats class gets to the sample variance and puts an $$n-1$$ in the denominator where everyone expected an $$n$$. Then someone says "you lose a degree of freedom," and the class moves on. I don't think that phrase means much the first time you hear it. It does mean something, though, and it's pretty concrete. The degree of freedom is an actual direction in $$\mathbb{R}^n$$, and you can draw a picture of it.

Here's the setup. Let $$X_1, \dots, X_n$$ be iid with mean $$\mu$$ and variance $$\sigma^2$$, with $$n \ge 2$$, and write $$\bar X = \frac{1}{n}\sum_i X_i$$. The claim is that

$$
S^2 = \frac{1}{n-1} \sum_{i=1}^n (X_i - \bar X)^2
$$

has $$\mathbb{E}[S^2] = \sigma^2$$, and that dividing by $$n$$ would come out too small on average.

Before doing any math, you can guess which way the correction should go. If we knew $$\mu$$, we'd average $$(X_i - \mu)^2$$ and that would be exactly unbiased. We don't know $$\mu$$, so we plug in $$\bar X$$. But $$\bar X$$ is the number $$c$$ that minimizes $$\sum_i (X_i - c)^2$$ (set the derivative to zero and see). So the squared deviations around $$\bar X$$ are never bigger than the ones around $$\mu$$, and usually they're smaller. You're measuring spread around a center you fit to the same data, so the data looks a bit tighter than it really is, and dividing by something less than $$n$$ makes up for that. The question is why it's exactly $$n-1$$.

## Pythagoras

Write $$X_i - \mu = (X_i - \bar X) + (\bar X - \mu)$$, square it, and sum over $$i$$. The cross term is $$2(\bar X - \mu)\sum_i (X_i - \bar X)$$, which is zero because deviations from the mean add up to zero. So

$$
\sum_{i=1}^n (X_i - \mu)^2 = \sum_{i=1}^n (X_i - \bar X)^2 + n(\bar X - \mu)^2 .
$$

Take expectations. The left side is $$n\sigma^2$$. Since $$\operatorname{Var}(\bar X) = \sigma^2/n$$, the last term has expectation $$\sigma^2$$. That leaves

$$
\mathbb{E}\Big[\sum_{i=1}^n (X_i - \bar X)^2\Big] = (n-1)\sigma^2 ,
$$

and you divide by $$n-1$$. So the missing $$\sigma^2$$ is the variance of the sample mean. The residuals can't see how far $$\bar X$$ landed from $$\mu$$, because they're measured from $$\bar X$$.

That identity is Pythagoras, and I think it's much easier to believe once you draw it.

## Counting directions

Treat the whole sample as one vector $$X = (X_1, \dots, X_n)$$ in $$\mathbb{R}^n$$, and let $$\mathbf{1} = (1, \dots, 1)$$. Projecting $$X$$ onto the line through $$\mathbf{1}$$ gives coefficient $$\langle X, \mathbf{1}\rangle / \langle \mathbf{1}, \mathbf{1}\rangle = \bar X$$, so $$\bar X\mathbf{1}$$ is that projection. The residual $$X - \bar X\mathbf{1}$$ is then perpendicular to $$\mathbf{1}$$, which is the same fact as "deviations sum to zero." For $$n = 2$$ the line through $$\mathbf{1}$$ is the diagonal, and it looks like this.

<div class="row justify-content-center mt-3">
  <div class="col-sm-10 mt-3 mt-md-0">
    {% include figure.liquid loading="eager" path="assets/img/blog/why-n-minus-one/projection-onto-ones.svg" class="img-fluid rounded" zoomable=true %}
  </div>
</div>
<div class="caption">
  The error X − μ1 splits into a blue piece along the diagonal and an orange piece perpendicular to it. The sample variance only sees the orange one.
</div>

The black vector $$X - \mu\mathbf{1}$$ is the one we'd like to measure. Both $$\mu\mathbf{1}$$ and $$\bar X\mathbf{1}$$ sit on the diagonal, so the blue leg runs along $$\mathbf{1}$$ and the orange leg is perpendicular to it. That's a right triangle, and

$$
\Vert X - \mu\mathbf{1} \Vert^2 = \Vert (\bar X - \mu)\mathbf{1} \Vert^2 + \Vert X - \bar X\mathbf{1} \Vert^2
$$

is the same identity as before, just written with lengths.

Now count. The noise $$X - \mu\mathbf{1}$$ has independent coordinates with variance $$\sigma^2$$ each, so its covariance is $$\sigma^2 I$$, and it doesn't prefer any direction. Pick any unit vector $$u$$ and the noise has variance $$\sigma^2$$ along it. So take an orthonormal basis made of $$\mathbf{1}/\sqrt{n}$$ plus $$n-1$$ vectors perpendicular to it. Each direction carries $$\sigma^2$$ of expected squared length. The blue leg gets one direction, so it has expected squared length $$\sigma^2$$, and the orange leg gets the other $$n-1$$, so it has $$(n-1)\sigma^2$$. If you like it in one line, with $$P$$ the projection onto $$\mathbf{1}^\perp$$,

$$
\mathbb{E}\Vert P(X - \mu\mathbf{1})\Vert^2 = \sigma^2 \operatorname{tr}(P) = (n-1)\sigma^2 ,
$$

and $$P(X - \mu\mathbf{1})$$ is exactly the residual $$X - \bar X\mathbf{1}$$, since $$P$$ kills $$\mu\mathbf{1}$$.

So that's the lost degree of freedom. It's the direction along $$\mathbf{1}$$. Fitting the mean uses it up, and the residuals are stuck living in the other $$n-1$$ dimensions. This only needed the covariance to be $$\sigma^2 I$$, nothing Gaussian. (With Gaussian data you get more, like the $$\chi^2_{n-1}$$ distribution and the $$n-1$$ in the $$t$$-test, but I'll skip that.)

## What it doesn't fix

One thing that bugs me is that the $$n-1$$ makes $$S^2$$ unbiased, but almost nobody reports $$S^2$$. They report $$S$$. And the square root is concave, so by Jensen

$$
\mathbb{E}[S] \lt \sqrt{\mathbb{E}[S^2]} = \sigma
$$

whenever $$S^2$$ is actually random. For tiny samples the gap is pretty big. For Gaussian data with $$n = 2$$, $$\mathbb{E}[S] = \sqrt{2/\pi}\,\sigma \approx 0.80\,\sigma$$. So the correction gets the average of the variance exactly right and the standard deviation still comes out low. It's also not obvious that unbiased is what you want in the first place. For Gaussian data the plain $$1/n$$ version has smaller mean squared error than the $$1/(n-1)$$ one, for every $$n$$.
