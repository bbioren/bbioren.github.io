---
layout: post
title: jensen's inequality is a picture
date: 2026-01-14
description: chords lie above convex curves, and that is the whole inequality
tags: visual-proofs probability convexity
categories: math
related_posts: false
---

jensen's inequality is usually handed over as a formula to memorize, and then half the room spends the rest of the course unsure which side of the inequality the $$f$$ goes on. that is a strange way to treat it, because jensen is not really a formula at all. it is a picture: a chord drawn between two points on a convex curve lies above the curve. everything else is bookkeeping.

## the statement

let $$X$$ be a random variable with finite mean, and let $$f$$ be convex. then

$$
f\big(\mathbb{E}[X]\big) \le \mathbb{E}\big[f(X)\big].
$$

the smallest case is a random variable that takes only two values: $$x$$ with probability $$\lambda$$ and $$y$$ with probability $$1-\lambda$$. then jensen says

$$
f\big(\lambda x + (1-\lambda) y\big) \le \lambda f(x) + (1-\lambda) f(y),
$$

which is word for word the definition of convexity. so the general inequality is the definition of convexity, extended from two-point averages to arbitrary averages.

the slogan i like is: **the output of the average is at most the average of the outputs.** a quick sanity check shows why the direction can't be the other way. take $$f(x) = x^2$$ and let $$X$$ be $$\pm 1$$ with equal probability. the average input is $$0$$, so the output of the average is $$0$$. but every output is $$1$$, so the average output is $$1$$. a convex function bends upward, which punishes spread: inputs that sit far from the center get blown up, and averaging after applying $$f$$ keeps that inflation, while averaging first throws it away.

## why it matters

jensen turns up all over the place in disguise. three one-liners:

**variance is nonnegative.** with $$f(x) = x^2$$, jensen gives $$\mathbb{E}[X]^2 \le \mathbb{E}[X^2]$$, that is, $$\operatorname{Var}(X) = \mathbb{E}[X^2] - \mathbb{E}[X]^2 \ge 0$$.

**am–gm.** $$\log$$ is concave, so the inequality flips. put mass $$\lambda_i$$ on the positive number $$a_i$$:

$$
\log\Big(\sum_i \lambda_i a_i\Big) \ge \sum_i \lambda_i \log a_i \quad\Longrightarrow\quad \sum_i \lambda_i a_i \ge \prod_i a_i^{\lambda_i}.
$$

the weighted arithmetic mean beats the weighted geometric mean. hey, that's am–gm!

**the elbo.** for any distribution $$q(z)$$ whose support covers that of $$p(z \mid x)$$, write the evidence as an expectation under $$q$$ and push the concave $$\log$$ inside:

$$
\log p(x) = \log \mathbb{E}_{q}\left[\frac{p(x,z)}{q(z)}\right] \ge \mathbb{E}_{q}\left[\log \frac{p(x,z)}{q(z)}\right].
$$

that right-hand side is the evidence lower bound that variational inference maximizes, and the same step is the lower bound that em climbs at each iteration. a lot of modern machine learning rests on this one application of jensen.

## the proof is the picture

start with the two-point case, since it is the whole idea. in the figure below, $$f(x) = e^{x/2}$$ and $$X$$ takes the value $$x_1 = -1$$ with probability $$0.6$$ and $$x_2 = 4$$ with probability $$0.4$$, so $$\mathbb{E}[X] = 1$$.

<div class="row justify-content-center mt-3">
  <div class="col-sm-10 mt-3 mt-md-0">
    {% include figure.liquid loading="eager" path="assets/img/blog/jensens-inequality/chord-above-curve.svg" class="img-fluid rounded" zoomable=true %}
  </div>
</div>
<div class="caption">
  the two outcomes, lifted onto the curve and weighted by their probabilities, have their center of mass on the chord, directly above E[X]. the curve at E[X] sits below it.
</div>

here is how to read it. lift each outcome onto the graph, giving the points $$(x_1, f(x_1))$$ and $$(x_2, f(x_2))$$, and give each point its probability as a mass. their center of mass is

$$
\big(0.6\,x_1 + 0.4\,x_2,\; 0.6\,f(x_1) + 0.4\,f(x_2)\big) = \big(\mathbb{E}[X],\; \mathbb{E}[f(X)]\big).
$$

a center of mass of two points always lies on the segment between them, so this point is on the chord, directly above $$\mathbb{E}[X]$$. meanwhile the point $$(\mathbb{E}[X], f(\mathbb{E}[X]))$$ is on the curve at that same horizontal position. convexity says the curve lies below its chords, so the curve point is lower: $$f(\mathbb{E}[X]) \approx 1.65$$ against $$\mathbb{E}[f(X)] \approx 3.32$$. the vertical gap between them is the jensen gap. with more than two outcomes the same picture holds, except that the center of mass lands somewhere inside the convex region above the graph rather than on a single chord.

for a general distribution there is a cleaner argument that avoids centers of mass entirely. let $$\mu = \mathbb{E}[X]$$ and draw the tangent line to $$f$$ at $$\mu$$:

$$
\ell(x) = f(\mu) + f'(\mu)(x - \mu).
$$

<div class="row justify-content-center mt-3">
  <div class="col-sm-10 mt-3 mt-md-0">
    {% include figure.liquid loading="eager" path="assets/img/blog/jensens-inequality/tangent-line-below.svg" class="img-fluid rounded" zoomable=true %}
  </div>
</div>
<div class="caption">
  a convex function lies above its tangent line at the mean. every outcome contributes a nonnegative gap f(x) − ℓ(x), and the line itself averages to exactly f(μ).
</div>

a convex function lies above every one of its tangent lines, so $$f(x) \ge \ell(x)$$ for every $$x$$, and in particular $$f(X) \ge \ell(X)$$ for every outcome of $$X$$. take expectations of both sides. the right side is linear in $$X$$, so

$$
\mathbb{E}[f(X)] \ge f(\mu) + f'(\mu)\big(\mathbb{E}[X] - \mu\big) = f(\mu) + f'(\mu)\cdot 0 = f(\mathbb{E}[X]).
$$

the linear term vanishes because we drew the line at the mean, and that's the proof. if $$f$$ has a corner at $$\mu$$, any supporting line through $$(\mu, f(\mu))$$ with slope between the left and right derivatives works just as well. convexity guarantees at least one exists.

## the part that gets missed

the usual presentation treats the direction of the inequality as a fact to memorize, when the picture hands it to you: for convex $$f$$ the curve sags below its chords, so the curve value $$f(\mathbb{E}[X])$$ is the smaller one. if you forget, draw a bowl and two points. for concave $$f$$, such as $$\log$$ or $$\sqrt{x}$$, the curve bulges above its chords and the inequality flips to $$f(\mathbb{E}[X]) \ge \mathbb{E}[f(X)]$$, which is the version the am–gm and elbo examples used. the tangent-line proof also tells you exactly when equality holds. equality forces $$f(X) = \ell(X)$$ with probability one, meaning every outcome lands where the curve touches its supporting line. for strictly convex $$f$$ like $$x^2$$ or $$e^{x/2}$$ that happens only when $$X$$ is constant. for a general convex $$f$$ it happens exactly when $$f$$ is linear on the smallest interval containing the values $$X$$ takes, so a chord there doesn't lie above the curve, it lies on it. the size of the jensen gap is a measure of how much $$X$$ spreads out across the region where $$f$$ actually bends.
