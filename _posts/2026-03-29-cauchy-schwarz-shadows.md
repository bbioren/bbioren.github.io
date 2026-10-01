---
layout: post
title: cauchy–schwarz is a shadow
date: 2026-03-29
description: why a projection is never longer than the vector it came from
tags: visual-proofs linear-algebra inequalities
categories: math
related_posts: false
---

Cauchy–Schwarz is probably the most-used inequality in analysis, and its standard proof is a trick: "consider $$\Vert u - t v \Vert^2 \ge 0$$, expand, and look at the discriminant." It works, but it gives no hint of why anyone would write it down. My favorite way to see the inequality is as a statement about shadows, and once you have that picture the trick turns out to be the same argument in algebra.

## The statement

Let $$V$$ be a real inner product space. For any $$u, v \in V$$,

$$
\vert \langle u, v \rangle \vert \le \Vert u \Vert \, \Vert v \Vert,
$$

where $$\Vert u \Vert = \sqrt{\langle u, u \rangle}$$. Equality holds exactly when $$u$$ and $$v$$ are linearly dependent.

In $$\mathbb{R}^2$$ there's nothing to prove: $$\langle u, v \rangle = \Vert u \Vert \Vert v \Vert \cos\theta$$, so the inequality says $$\vert \cos\theta \vert \le 1$$, with equality when $$\theta = 0$$ or $$\pi$$. Both sides also double when $$u$$ does, so the inequality is about directions, not sizes.

The point is that it holds in *any* inner product space: functions with $$\langle f, g \rangle = \int f g$$, random variables, matrices. There nobody hands you an angle. You *define* it by

$$
\cos\theta = \frac{\langle u, v \rangle}{\Vert u \Vert \, \Vert v \Vert},
$$

and Cauchy–Schwarz is exactly what makes that legal, by putting the right-hand side in $$[-1, 1]$$.

## Why it matters

**Correlation.** Take random variables $$X, Y$$ with finite variance, and use $$\langle X, Y \rangle = \mathbb{E}[XY]$$. Apply Cauchy–Schwarz to the centered variables $$X - \mathbb{E}X$$ and $$Y - \mathbb{E}Y$$:

$$
\vert \operatorname{Cov}(X, Y) \vert \le \sigma_X \, \sigma_Y .
$$

So the correlation $$\rho = \operatorname{Cov}(X,Y) / (\sigma_X \sigma_Y)$$ lies in $$[-1, 1]$$. Hey, $$\rho$$ is just the cosine of the angle between the centered variables!

**The triangle inequality.** Bound the cross term:

$$
\Vert u + v \Vert^2 = \Vert u \Vert^2 + 2\langle u, v \rangle + \Vert v \Vert^2 \le \Vert u \Vert^2 + 2\Vert u \Vert \Vert v \Vert + \Vert v \Vert^2 = \left(\Vert u \Vert + \Vert v \Vert\right)^2.
$$

Take square roots. This is the step that makes $$\Vert \cdot \Vert$$ a norm.

**Averages.** In $$\mathbb{R}^n$$, take $$u = (a_1, \dots, a_n)$$ and $$v = (1, \dots, 1)$$. Then $$\langle u, v \rangle = \sum a_i$$ and $$\Vert v \Vert^2 = n$$, so

$$
\Big( \sum_{i=1}^n a_i \Big)^2 \le n \sum_{i=1}^n a_i^2 .
$$

Divide by $$n^2$$: the squared mean is at most the mean of the squares. That's the AM–QM inequality.

## The proof is a shadow

If $$v = 0$$ both sides are zero, so assume $$v \ne 0$$. Shine a light straight down onto the line through $$v$$. The shadow of $$u$$ is its orthogonal projection,

$$
p = \frac{\langle u, v \rangle}{\Vert v \Vert^2} \, v .
$$

<div class="row justify-content-center mt-3">
  <div class="col-sm-10 mt-3 mt-md-0">
    {% include figure.liquid loading="eager" path="assets/img/blog/cauchy-schwarz-shadows/projection-shadow.svg" class="img-fluid rounded" zoomable=true %}
  </div>
</div>
<div class="caption">
  The shadow p of u on the line through v (orange, labeled proj) and the leftover u − p (dashed) are perpendicular, so u is the hypotenuse of a right triangle and p is a leg.
</div>

The leftover piece $$u - p$$ really is perpendicular to $$v$$:

$$
\langle u - p, v \rangle = \langle u, v \rangle - \frac{\langle u, v \rangle}{\Vert v \Vert^2} \langle v, v \rangle = 0 .
$$

So $$u = p + (u - p)$$ is an orthogonal split, and Pythagoras holds in any inner product space (expand $$\Vert a + b \Vert^2$$ with $$\langle a, b \rangle = 0$$). That gives

$$
\Vert u \Vert^2 = \Vert p \Vert^2 + \Vert u - p \Vert^2 \ge \Vert p \Vert^2 .
$$

The shadow is never longer than the object. Measure the shadow, $$\Vert p \Vert = \vert \langle u, v \rangle \vert / \Vert v \Vert$$, multiply through by $$\Vert v \Vert^2$$, and that's Cauchy–Schwarz.

Now go back to the trick. For every real $$t$$,

$$
f(t) = \Vert u - t v \Vert^2 = \Vert u \Vert^2 - 2t \langle u, v \rangle + t^2 \Vert v \Vert^2 \ge 0 .
$$

A quadratic that never goes negative has discriminant $$4\langle u, v \rangle^2 - 4\Vert u \Vert^2 \Vert v \Vert^2 \le 0$$, which is the inequality again. But ask where the parabola bottoms out:

$$
t^* = \frac{\langle u, v \rangle}{\Vert v \Vert^2},
$$

the coefficient of the projection, so $$t^* v = p$$. The minimum value is

$$
f(t^*) = \Vert u \Vert^2 - \frac{\langle u, v \rangle^2}{\Vert v \Vert^2} = \Vert u - p \Vert^2 ,
$$

the squared dashed leg. Minimizing $$\Vert u - t v \Vert$$ finds the point on the line closest to $$u$$, the foot of the perpendicular, and "discriminant $$\le 0$$" just says that leg has nonnegative squared length.

<div class="row justify-content-center mt-3">
  <div class="col-sm-10 mt-3 mt-md-0">
    {% include figure.liquid loading="eager" path="assets/img/blog/cauchy-schwarz-shadows/quadratic-above-axis.svg" class="img-fluid rounded" zoomable=true %}
  </div>
</div>
<div class="caption">
  The quadratic t ↦ ‖u − tv‖² for u = (3, 2), v = (4, 0). It starts at ‖u‖² = 13, bottoms out at t* = 3/4 (the projection coefficient), and its minimum value 4 is the squared length of u − p from the first figure.
</div>

## The part that gets missed

So the trick proof isn't a trick: it's the projection argument with the picture removed, and $$t^* v$$ is the foot of the perpendicular. That also makes the equality case obvious, which the discriminant version usually states without explanation. Equality holds exactly when $$\Vert u - p \Vert = 0$$, i.e. the dashed leg vanishes and $$u$$ already lies on the line through $$v$$, so $$u$$ and $$v$$ are linearly dependent. One more subtlety is often skipped: the inequality never uses that $$\langle w, w \rangle = 0$$ forces $$w = 0$$, only that $$\langle w, w \rangle \ge 0$$. (If $$\Vert v \Vert = 0$$, the "quadratic" is linear in $$t$$, and a nonnegative line is flat, so $$\langle u, v \rangle = 0$$.) The equality case does use definiteness, which is why $$\vert \rho \vert = 1$$ only gives $$Y - \mathbb{E}Y = c\,(X - \mathbb{E}X)$$ *almost surely*: a leg of length zero in $$L^2$$ is zero only almost everywhere.
