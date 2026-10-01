---
layout: post
title: cauchy–schwarz is a shadow
date: 2026-03-29
description: a projection is never longer than the vector it came from
tags: visual-proofs linear-algebra inequalities
categories: math
related_posts: false
---

Cauchy–Schwarz shows up all over analysis, and the proof most people see goes something like "consider $$\Vert u - t v \Vert^2 \ge 0$$, expand it, and look at the discriminant." That works fine, but I've never liked it much, because nothing in it tells you why you'd write down $$\Vert u - t v \Vert^2$$ in the first place. I think the inequality makes a lot more sense as a statement about shadows. And once you have that picture, the discriminant proof turns out to be the same argument with the picture taken away.

Here's the statement. In a real inner product space, for any vectors $$u$$ and $$v$$,

$$
\vert \langle u, v \rangle \vert \le \Vert u \Vert \, \Vert v \Vert,
$$

with equality exactly when $$u$$ and $$v$$ are linearly dependent.

In $$\mathbb{R}^2$$ there isn't much to prove. We have $$\langle u, v \rangle = \Vert u \Vert \Vert v \Vert \cos\theta$$, so the inequality just says $$\vert \cos\theta \vert \le 1$$. The interesting part is that it holds in every inner product space, including ones like functions with $$\langle f, g \rangle = \int f g$$, where nobody hands you an angle. In those spaces you define the angle by

$$
\cos\theta = \frac{\langle u, v \rangle}{\Vert u \Vert \, \Vert v \Vert},
$$

and Cauchy–Schwarz is what guarantees the right-hand side lands in $$[-1, 1]$$, so that this definition makes any sense.

Random variables are a nice example. Use $$\langle X, Y \rangle = \mathbb{E}[XY]$$ and apply the inequality to the centered variables $$X - \mathbb{E}X$$ and $$Y - \mathbb{E}Y$$. You get

$$
\vert \operatorname{Cov}(X, Y) \vert \le \sigma_X \, \sigma_Y ,
$$

so the correlation $$\rho = \operatorname{Cov}(X,Y) / (\sigma_X \sigma_Y)$$ is between $$-1$$ and $$1$$. So the correlation coefficient is literally the cosine of the angle between the centered variables, which is a nice way to remember what it measures.

## Shadows

OK, so why is it true? If $$v = 0$$ both sides are zero, so assume it isn't. Shine a light straight down onto the line through $$v$$. The shadow of $$u$$ is its orthogonal projection onto that line,

$$
p = \frac{\langle u, v \rangle}{\Vert v \Vert^2} \, v .
$$

<div class="row justify-content-center mt-3">
  <div class="col-sm-10 mt-3 mt-md-0">
    {% include figure.liquid loading="eager" path="assets/img/blog/cauchy-schwarz-shadows/projection-shadow.svg" class="img-fluid rounded" zoomable=true %}
  </div>
</div>
<div class="caption">
  The shadow p of u on the line through v, and the dashed leftover u − p. They meet at a right angle, so u is the hypotenuse.
</div>

The leftover piece $$u - p$$ is perpendicular to $$v$$, which you can check directly:

$$
\langle u - p, v \rangle = \langle u, v \rangle - \frac{\langle u, v \rangle}{\Vert v \Vert^2} \langle v, v \rangle = 0 .
$$

So $$u = p + (u - p)$$ splits $$u$$ into two perpendicular pieces, and Pythagoras works in any inner product space (expand $$\Vert a + b \Vert^2$$ when $$\langle a, b \rangle = 0$$ and the cross term drops out). That gives

$$
\Vert u \Vert^2 = \Vert p \Vert^2 + \Vert u - p \Vert^2 \ge \Vert p \Vert^2 .
$$

In words, the hypotenuse is at least as long as a leg, so a shadow can't be longer than the thing casting it. The shadow has length $$\Vert p \Vert = \vert \langle u, v \rangle \vert / \Vert v \Vert$$, and if you plug that in and multiply through by $$\Vert v \Vert^2$$, you get Cauchy–Schwarz.

## Where the discriminant comes from

Now let's go back to the usual proof. For every real $$t$$,

$$
f(t) = \Vert u - t v \Vert^2 = \Vert u \Vert^2 - 2t \langle u, v \rangle + t^2 \Vert v \Vert^2 \ge 0 .
$$

A quadratic that never goes negative has discriminant at most zero, so $$4\langle u, v \rangle^2 - 4\Vert u \Vert^2 \Vert v \Vert^2 \le 0$$, and that's the inequality again. But what is this quadratic actually doing? Ask where it bottoms out. The minimum is at

$$
t^* = \frac{\langle u, v \rangle}{\Vert v \Vert^2},
$$

which is exactly the coefficient in the projection, so $$t^* v = p$$. And the minimum value is

$$
f(t^*) = \Vert u \Vert^2 - \frac{\langle u, v \rangle^2}{\Vert v \Vert^2} = \Vert u - p \Vert^2 ,
$$

the squared length of the dashed leg. So minimizing $$\Vert u - t v \Vert$$ over $$t$$ is just finding the point on the line closest to $$u$$, which is the foot of the perpendicular. The discriminant condition says that the dashed leg has a nonnegative squared length, which is the same thing the shadow picture told us.

<div class="row justify-content-center mt-3">
  <div class="col-sm-10 mt-3 mt-md-0">
    {% include figure.liquid loading="eager" path="assets/img/blog/cauchy-schwarz-shadows/quadratic-above-axis.svg" class="img-fluid rounded" zoomable=true %}
  </div>
</div>
<div class="caption">
  The quadratic t ↦ ‖u − tv‖² for u = (3, 2), v = (4, 0). It starts at 13, bottoms out at t* = 3/4, and the minimum value 4 is the squared length of u − p.
</div>

The picture also explains the equality case, which the discriminant version usually just states. Equality means $$\Vert u - p \Vert = 0$$, so the dashed leg has collapsed and $$u$$ was already sitting on the line through $$v$$. That's what linearly dependent means here. For correlation, this is why $$\vert \rho \vert = 1$$ forces $$Y - \mathbb{E}Y$$ to be a constant multiple of $$X - \mathbb{E}X$$. (Technically only almost surely, since a random variable with zero length in this inner product is zero only with probability one, but that doesn't change the picture.)
