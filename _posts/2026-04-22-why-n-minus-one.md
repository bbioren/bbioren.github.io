---
layout: post
title: why n minus one
date: 2026-04-22
description: the degree of freedom you lose to the sample mean is literally a dimension
tags: visual-proofs statistics linear-algebra
categories: math
related_posts: false
---

"You lose a degree of freedom" gets said in just about every intro stats class, right when the sample variance shows up with an $$n-1$$ where everyone expected an $$n$$. It's almost never explained. It sounds like a bookkeeping rule, but it's really a statement about geometry: the degree of freedom you lose is an actual dimension of $$\mathbb{R}^n$$, and once you see the picture the $$n-1$$ is the only number that makes sense.

## the statement

Let $$X_1, \dots, X_n$$ be iid with mean $$\mu$$ and finite variance $$\sigma^2$$, with $$n \ge 2$$. Write $$\bar X = \frac{1}{n}\sum_i X_i$$. Then the sample variance

$$
S^2 = \frac{1}{n-1} \sum_{i=1}^n (X_i - \bar X)^2
$$

satisfies $$\mathbb{E}[S^2] = \sigma^2$$. Dividing by $$n$$ would underestimate $$\sigma^2$$ on average.

Here's why you should expect a correction, and why it should push the estimate up. If we knew $$\mu$$, we would just average $$(X_i - \mu)^2$$, and that average is exactly unbiased. We don't know $$\mu$$, so we use $$\bar X$$ in its place. But $$\bar X$$ is not just some estimate of the center. It's the number $$c$$ that _minimizes_ $$\sum_i (X_i - c)^2$$ (set the derivative $$-2\sum_i (X_i - c)$$ to zero). So the squared deviations around $$\bar X$$ are never larger than the ones around the true $$\mu$$, and they're usually smaller. Measuring spread around a center you fit to the same data flatters the data, and dividing by something smaller than $$n$$ makes up for it.

## the two-line derivation

Write $$X_i - \mu = (X_i - \bar X) + (\bar X - \mu)$$, square it, and sum. The cross term is $$2(\bar X - \mu)\sum_i (X_i - \bar X) = 0$$, because deviations from the mean sum to zero. So

$$
\sum_{i=1}^n (X_i - \mu)^2 = \sum_{i=1}^n (X_i - \bar X)^2 + n(\bar X - \mu)^2 .
$$

Now take expectations. The left side is $$n\sigma^2$$. Since $$\operatorname{Var}(\bar X) = \sigma^2/n$$, the last term has expectation $$n \cdot \sigma^2/n = \sigma^2$$. So

$$
\mathbb{E}\Big[\sum_{i=1}^n (X_i - \bar X)^2\Big] = n\sigma^2 - \sigma^2 = (n-1)\sigma^2 .
$$

Divide by $$n-1$$ and you're done (this is Bessel's correction). Note where the missing $$\sigma^2$$ went: it's the variance of the sample mean, which the data can't see because it measured spread around $$\bar X$$, not around $$\mu$$. The decomposition above should look familiar, though, because it's Pythagoras.

## the picture

Think of the whole sample as one vector $$X = (X_1, \dots, X_n) \in \mathbb{R}^n$$, and let $$\mathbf{1} = (1, \dots, 1)$$. The vector $$\bar X \mathbf{1}$$ is the orthogonal projection of $$X$$ onto the line spanned by $$\mathbf{1}$$, since the projection coefficient is $$\langle X, \mathbf{1}\rangle / \langle \mathbf{1}, \mathbf{1} \rangle = \sum_i X_i / n = \bar X$$. The residual $$X - \bar X \mathbf{1}$$ is then orthogonal to $$\mathbf{1}$$. That's the same fact as "deviations sum to zero," written as $$\langle X - \bar X\mathbf{1}, \mathbf{1} \rangle = 0$$. So the residual lives in $$\mathbf{1}^\perp$$, a subspace of dimension $$n-1$$.

Here is the picture for $$n = 2$$, where $$\operatorname{span}(\mathbf{1})$$ is the diagonal.

<div class="row justify-content-center mt-3">
  <div class="col-sm-10 mt-3 mt-md-0">
    {% include figure.liquid loading="eager" path="assets/img/blog/why-n-minus-one/projection-onto-ones.svg" class="img-fluid rounded" zoomable=true %}
  </div>
</div>
<div class="caption">
  The error vector X − μ1 splits into a piece along the diagonal span(1) (blue) and a piece orthogonal to it (orange). The sample variance only sees the orange piece.
</div>

The vector we wish we could measure is the black one, $$X - \mu\mathbf{1}$$, running from the true center $$\mu\mathbf{1}$$ to the data. Both $$\mu\mathbf{1}$$ and $$\bar X\mathbf{1}$$ sit on the diagonal, so the blue leg $$(\bar X - \mu)\mathbf{1}$$ lies along $$\mathbf{1}$$. The orange leg $$X - \bar X\mathbf{1}$$ is perpendicular to it. That gives a right triangle, and Pythagoras says

$$
\Vert X - \mu\mathbf{1} \Vert^2 = \Vert (\bar X - \mu)\mathbf{1} \Vert^2 + \Vert X - \bar X\mathbf{1} \Vert^2 ,
$$

which is exactly the identity from the last section: $$\sum_i (X_i - \mu)^2 = n(\bar X - \mu)^2 + \sum_i (X_i - \bar X)^2$$.

Now the counting. The noise vector $$X - \mu\mathbf{1}$$ has independent coordinates, each with variance $$\sigma^2$$, so its covariance is $$\sigma^2 I$$. That noise has no preferred direction: projected onto _any_ unit vector $$u$$, it has variance $$u^\top (\sigma^2 I) u = \sigma^2$$. So if you pick an orthonormal basis made of $$\mathbf{1}/\sqrt{n}$$ plus $$n-1$$ vectors spanning $$\mathbf{1}^\perp$$, each of the $$n$$ directions carries $$\sigma^2$$ of expected squared length. The blue leg gets one direction, so its expected squared length is $$\sigma^2$$. The orange leg gets the other $$n-1$$, so its expected squared length is $$(n-1)\sigma^2$$. In symbols, if $$P$$ is the projection onto $$\mathbf{1}^\perp$$, then $$\mathbb{E}\Vert P(X - \mu\mathbf{1})\Vert^2 = \sigma^2 \operatorname{tr}(P) = (n-1)\sigma^2$$. Since $$P\mu\mathbf{1} = 0$$, the residual we can compute, $$X - \bar X\mathbf{1}$$, is exactly $$P(X - \mu\mathbf{1})$$.

That's the lost degree of freedom. It's literally the dimension along $$\mathbf{1}$$. Fitting the mean uses up that direction, and the residuals are stuck in the remaining $$n-1$$. This argument only needs the covariance to be $$\sigma^2 I$$, not Gaussianity. If the data are Gaussian, the noise is fully rotation-invariant, and you get more: the two legs are independent, $$\sum_i (X_i - \bar X)^2 / \sigma^2 \sim \chi^2_{n-1}$$, and $$\bar X$$ is independent of $$S^2$$. That's where the $$n-1$$ in the $$t$$-distribution comes from.

## the part that gets missed

Unbiased for $$\sigma^2$$ doesn't mean unbiased for $$\sigma$$. Since the square root is strictly concave, Jensen gives $$\mathbb{E}[S] = \mathbb{E}\big[\sqrt{S^2}\big] \lt \sqrt{\mathbb{E}[S^2]} = \sigma$$ whenever $$S^2$$ isn't a constant. For Gaussian data with $$n = 2$$, $$\mathbb{E}[S] = \sqrt{2/\pi}\,\sigma \approx 0.80\,\sigma$$. So the $$n-1$$ that gets drilled into you doesn't even fix the sample standard deviation, which is the number people actually report. The deeper point is that "unbiased" isn't the same as "better." Consider estimators $$c \sum_i (X_i - \bar X)^2$$ for Gaussian data. Using the $$\chi^2_{n-1}$$ distribution, the mean squared error is minimized at $$c = 1/(n+1)$$, not $$1/(n-1)$$. Even the biased $$1/n$$ estimator, which is the maximum likelihood estimator, has MSE $$(2n-1)\sigma^4/n^2$$, less than the unbiased estimator's $$2\sigma^4/(n-1)$$ for every $$n$$. Shrinking toward zero trades a little bias for a real cut in variance. (Outside the Gaussian case the ranking depends on the fourth moment, so it isn't universal.) So $$n-1$$ is the right answer to one specific question, "what makes the average come out exactly right?", and the geometry shows why it's that number. Whether that's the question you should be asking is a different matter.
