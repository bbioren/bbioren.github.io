---
layout: post
title: jensen's inequality is a picture
date: 2026-01-14
description: if you can draw a bowl and a line, you can remember which way jensen goes
tags: visual-proofs probability convexity
categories: math
related_posts: false
---

Jensen's inequality says that if $$f$$ is convex and $$X$$ is a random variable with a finite mean, then

$$
f\big(\mathbb{E}[X]\big) \le \mathbb{E}\big[f(X)\big].
$$

In words, applying $$f$$ to the average gives you something smaller than averaging the values of $$f$$. I think most people learn this as a formula and then spend a while unsure which side the $$f$$ goes on. There's a picture behind it, though, and it's easy enough to redraw on the spot whenever you forget.

Here's a quick example to get the direction in your head. Take $$f(x) = x^2$$ and let $$X$$ be $$+1$$ or $$-1$$ with equal probability. The average of $$X$$ is $$0$$, so $$f(\mathbb{E}[X]) = 0$$. But $$X^2$$ is always $$1$$, so $$\mathbb{E}[X^2] = 1$$. Squaring after averaging loses the spread, and squaring before averaging keeps it. (This example is also why variance is never negative, since $$\mathbb{E}[X^2] - \mathbb{E}[X]^2 \ge 0$$ is exactly Jensen with $$x^2$$.)

## Two points

Start with the case where $$X$$ only takes two values, $$x$$ with probability $$\lambda$$ and $$y$$ with probability $$1 - \lambda$$. Then Jensen says

$$
f\big(\lambda x + (1-\lambda) y\big) \le \lambda f(x) + (1-\lambda) f(y),
$$

and if you've seen the definition of a convex function, this is it, word for word. So Jensen is what you get when you take the definition of convexity and let the average be over any distribution instead of just two points.

Here's what it looks like. In the figure, $$f(x) = e^{x/2}$$, and $$X$$ is $$-1$$ with probability $$0.6$$ and $$4$$ with probability $$0.4$$, so $$\mathbb{E}[X] = 1$$.

<div class="row justify-content-center mt-3">
  <div class="col-sm-10 mt-3 mt-md-0">
    {% include figure.liquid loading="eager" path="assets/img/blog/jensens-inequality/chord-above-curve.svg" class="img-fluid rounded" zoomable=true %}
  </div>
</div>
<div class="caption">
  The weighted average of the two points on the curve lands on the chord, above the curve at E[X].
</div>

Put the two outcomes on the graph, at $$(-1, f(-1))$$ and $$(4, f(4))$$, and think of each one as a weight equal to its probability. Their center of mass is

$$
\big(0.6 \cdot (-1) + 0.4 \cdot 4,\; 0.6\, f(-1) + 0.4\, f(4)\big) = \big(\mathbb{E}[X],\; \mathbb{E}[f(X)]\big).
$$

A center of mass of two points sits somewhere on the segment between them, so this point is on the chord, right above $$\mathbb{E}[X]$$. The curve at the same spot is $$f(\mathbb{E}[X])$$, and a convex curve sags below its chords, so the curve point is lower. With these numbers it's about $$1.65$$ on the curve versus about $$3.32$$ on the chord. That vertical gap is what people call the Jensen gap.

So if you forget the direction, draw a bowl, pick two points on it, and connect them. The line is above the bowl, and the line is the average of $$f$$.

## Any distribution

With more than two outcomes, the center of mass ends up somewhere inside the region above the curve instead of on one chord, which is still fine but a little annoying to make precise. There's a cleaner argument that works for every distribution at once. Let $$\mu = \mathbb{E}[X]$$ and draw the tangent line to $$f$$ at $$\mu$$:

$$
\ell(x) = f(\mu) + f'(\mu)(x - \mu).
$$

<div class="row justify-content-center mt-3">
  <div class="col-sm-10 mt-3 mt-md-0">
    {% include figure.liquid loading="eager" path="assets/img/blog/jensens-inequality/tangent-line-below.svg" class="img-fluid rounded" zoomable=true %}
  </div>
</div>
<div class="caption">
  A convex function stays above its tangent line at the mean.
</div>

A convex function lies above all of its tangent lines, so $$f(X) \ge \ell(X)$$ no matter what value $$X$$ takes. Now take expectations of both sides. The line is linear, so its expectation is easy:

$$
\mathbb{E}[f(X)] \ge f(\mu) + f'(\mu)\big(\mathbb{E}[X] - \mu\big) = f(\mu).
$$

The slope term drops out because we put the line at the mean, and we're done. (If $$f$$ has a corner at $$\mu$$, use any line through $$(\mu, f(\mu))$$ that stays below the graph. Convexity guarantees there is one.)

Let's do one application. Since $$\log$$ is concave, the inequality flips. Put weight $$\lambda_i$$ on positive numbers $$a_i$$ and you get

$$
\log\Big(\sum_i \lambda_i a_i\Big) \ge \sum_i \lambda_i \log a_i \quad\Longrightarrow\quad \sum_i \lambda_i a_i \ge \prod_i a_i^{\lambda_i},
$$

which is the AM-GM inequality. The same move, pushing a $$\log$$ inside an expectation, is also how you get the evidence lower bound in variational inference, but I'll skip the details here.

## When it's an equality

One more thing the tangent-line proof gives you for free is when the two sides are equal. Equality means $$f(X) = \ell(X)$$ with probability one, so every value $$X$$ takes has to sit exactly where the curve touches the line. For something strictly convex like $$x^2$$ or $$e^{x/2}$$, the curve only touches its tangent line at one point, so $$X$$ has to be constant. If $$f$$ has flat (linear) stretches, $$X$$ can move around inside one of those stretches and you still get equality, since there the chord and the curve are the same thing. I like this because it tells you what the gap is measuring: roughly, how much $$X$$ spreads out over the part of the curve that actually bends.
