---
layout: post
title: jensen's inequality is a picture
date: 2026-01-14
description: why the average of a convex function sits above the function of the average
tags: visual-proofs probability convexity
categories: math
related_posts: false
thumbnail: /assets/img/blog/jensens-inequality/chord-above-curve.svg
---

Take $$f(x) = x^2$$ and let $$X$$ be $$+1$$ or $$-1$$, each with probability one half. The average of $$X$$ is $$0$$, so if you average first and then square, you get $$f(\mathbb{E}[X]) = 0$$. If you square first, $$X^2$$ is $$1$$ no matter which value comes up, so the average of the squares is $$\mathbb{E}[X^2] = 1$$. Why do the two orders give different answers? Because averaging first throws away the fact that $$X$$ was spread out, and squaring first keeps it. Jensen's inequality says the square-first number is always at least as big, as long as $$f$$ is convex and $$X$$ is a random variable with a finite mean:

$$
f\big(\mathbb{E}[X]\big) \le \mathbb{E}\big[f(X)\big].
$$

(This is also why a variance can't be negative. The statement $$\mathbb{E}[X^2] - \mathbb{E}[X]^2 \ge 0$$ is just Jensen with $$f(x) = x^2$$.)

What does the inequality say when $$X$$ only takes two values? Say $$X$$ is $$x$$ with probability $$\lambda$$ and $$y$$ with probability $$1 - \lambda$$. Both expectations are then just weighted sums, and the inequality becomes

$$
f\big(\lambda x + (1-\lambda) y\big) \le \lambda f(x) + (1-\lambda) f(y),
$$

which is exactly the definition of a convex function. So Jensen is really the definition of convexity, except that the average is allowed to be over any distribution and not only over two points. To draw the two point case, I'll use $$f(x) = e^{x/2}$$ and let $$X$$ be $$-1$$ with probability $$0.6$$ and $$4$$ with probability $$0.4$$. In our example, we have that $$\mathbb{E}[X] = 0.6 \cdot (-1) + 0.4 \cdot 4 = 1$$.

<div class="row justify-content-center mt-3">
  <div class="col-sm-10 mt-3 mt-md-0">
    {% include figure.liquid loading="eager" path="assets/img/blog/jensens-inequality/chord-above-curve.svg" class="img-fluid rounded" zoomable=true %}
  </div>
</div>
<div class="caption">
  The two outcomes, weighted by their probabilities. Their center of mass sits on the chord, above the curve at E[X].
</div>

Put the two outcomes on the graph at $$(-1, f(-1))$$ and $$(4, f(4))$$, and think of each one as a weight equal to its probability. Where is the center of mass of the two weights? Its first coordinate is the weighted average of the $$x$$ values, and its second coordinate is the weighted average of the heights, so it is

$$
\big(0.6 \cdot (-1) + 0.4 \cdot 4,\; 0.6\, f(-1) + 0.4\, f(4)\big) = \big(\mathbb{E}[X],\; \mathbb{E}[f(X)]\big).
$$

The center of mass of two points always lies on the segment between them, so this point is on the chord, directly above $$\mathbb{E}[X]$$. The curve at that same spot has height $$f(\mathbb{E}[X])$$. A convex curve sags below its chords, so the curve is the lower of the two. Plugging in, the curve is at about $$1.65$$ and the chord is at about $$3.32$$. The vertical distance between them is usually called the Jensen gap. If you forget which way the inequality goes, it's enough to draw a bowl and connect two points on it with a line. The line is the average of $$f$$, and it sits above the bowl. I find this picture a lot easier to remember than any of the proofs.

What happens with more than two outcomes? The center of mass then lands somewhere inside the region above the curve, not on a single chord. Of course, a drawing with two dots on it isn't a proof, and making the many-point version precise is more fiddly than it looks. I'm not going to try, because there is a cleaner argument that handles every distribution at once. Let $$\mu = \mathbb{E}[X]$$ and draw the tangent line to $$f$$ at $$\mu$$,

$$
\ell(x) = f(\mu) + f'(\mu)(x - \mu).
$$

<div class="row justify-content-center mt-3">
  <div class="col-sm-10 mt-3 mt-md-0">
    {% include figure.liquid loading="eager" path="assets/img/blog/jensens-inequality/tangent-line-below.svg" class="img-fluid rounded" zoomable=true %}
  </div>
</div>
<div class="caption">
  The convex function stays above its tangent line at the mean.
</div>

A convex function lies above every one of its tangent lines, so $$f(X) \ge \ell(X)$$ for whatever value $$X$$ takes. Now take the expectation of both sides. The expectation of a line is easy to compute, since a line is linear, and we get

$$
\mathbb{E}[f(X)] \ge f(\mu) + f'(\mu)\big(\mathbb{E}[X] - \mu\big) = f(\mu).
$$

The slope term drops out because $$\mathbb{E}[X] - \mu = 0$$. That's the whole reason for putting the line at the mean. If $$f$$ has a corner at $$\mu$$ then there's no derivative there, which sounds like a problem, but it isn't really one. Convexity still gives some line through $$(\mu, f(\mu))$$ that stays below the graph, and the same argument works with that line.

For a concave function the inequality goes the other way, and $$\log$$ is concave. Put weights $$\lambda_i$$ on positive numbers $$a_i$$. Applying the flipped inequality to $$\log$$, and then exponentiating both sides, we have that

$$
\log\Big(\sum_i \lambda_i a_i\Big) \ge \sum_i \lambda_i \log a_i \quad\Longrightarrow\quad \sum_i \lambda_i a_i \ge \prod_i a_i^{\lambda_i},
$$

which is the AM-GM inequality. Moving a $$\log$$ inside an expectation like this is also how the evidence lower bound in variational inference gets derived.

When are the two sides equal? The tangent line proof tells you this too. Equality needs $$f(X) = \ell(X)$$ with probability one, which means every value $$X$$ takes has to be a point where the curve touches the line. A strictly convex function like $$x^2$$ or $$e^{x/2}$$ only touches its tangent line at one point, so in that case $$X$$ has to be constant. If $$f$$ is linear on some stretch, then $$X$$ can move around inside that stretch and the two sides are still equal, because on that stretch the chord and the curve are the same line.
