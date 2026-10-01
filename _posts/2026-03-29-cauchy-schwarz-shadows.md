---
layout: post
title: cauchy–schwarz is a shadow
date: 2026-03-29
description: a projection is never longer than the vector it came from
tags: visual-proofs linear-algebra inequalities
categories: math
related_posts: false
thumbnail: /assets/img/blog/cauchy-schwarz-shadows/projection-shadow.svg
---

In $$\mathbb{R}^2$$ the Cauchy–Schwarz inequality $$\vert \langle u, v \rangle \vert \le \Vert u \Vert \, \Vert v \Vert$$ is just the statement that $$\vert \cos\theta \vert \le 1$$, since $$\langle u, v \rangle = \Vert u \Vert \Vert v \Vert \cos\theta$$. There isn't much there to prove. (I'm writing $$\langle u, v \rangle$$ for the inner product, which in $$\mathbb{R}^2$$ is the plain dot product.)

So why does anyone care about it? Well, it holds in every real inner product space, with equality exactly when $$u$$ and $$v$$ are linearly dependent. That includes spaces like functions with $$\langle f, g \rangle = \int f g$$, where nobody gives you an angle to begin with. In those spaces you define the angle by

$$
\cos\theta = \frac{\langle u, v \rangle}{\Vert u \Vert \, \Vert v \Vert},
$$

and Cauchy–Schwarz is what makes sure the right side lands in $$[-1, 1]$$. Without it the definition wouldn't make sense.

For random variables you can use $$\langle X, Y \rangle = \mathbb{E}[XY]$$. Applying the inequality to the centered variables $$X - \mathbb{E}X$$ and $$Y - \mathbb{E}Y$$, we have that

$$
\vert \operatorname{Cov}(X, Y) \vert \le \sigma_X \, \sigma_Y .
$$

So the correlation $$\rho = \operatorname{Cov}(X,Y) / (\sigma_X \sigma_Y)$$ is between $$-1$$ and $$1$$. In fact it's just the cosine of the angle between the two centered variables.

The proof that usually gets shown expands $$\Vert u - t v \Vert^2 \ge 0$$ and looks at the discriminant. It works, but nothing in it explains why you would write that quantity down in the first place. I prefer to think of the inequality as a statement about shadows. The discriminant proof turns out to be the same argument with the picture taken out.

If $$v = 0$$ both sides are zero, so assume it isn't. Shine a light straight down onto the line through $$v$$. The shadow of $$u$$ is its orthogonal projection onto that line,

$$
p = \frac{\langle u, v \rangle}{\Vert v \Vert^2} \, v .
$$

<div class="row justify-content-center mt-3">
  <div class="col-sm-10 mt-3 mt-md-0">
    {% include figure.liquid loading="eager" path="assets/img/blog/cauchy-schwarz-shadows/projection-shadow.svg" class="img-fluid rounded" zoomable=true %}
  </div>
</div>
<div class="caption">
  The shadow p of u on the line through v, with the leftover piece u − p dashed. The two meet at a right angle, so u is the hypotenuse.
</div>

The leftover piece $$u - p$$ is perpendicular to $$v$$. We can check this directly:

$$
\langle u - p, v \rangle = \langle u, v \rangle - \frac{\langle u, v \rangle}{\Vert v \Vert^2} \langle v, v \rangle = 0 .
$$

So $$u = p + (u - p)$$ splits $$u$$ into two perpendicular pieces. Now we want Pythagoras, but does it still work in an arbitrary inner product space? It does. Expanding gives $$\Vert a + b \Vert^2 = \Vert a \Vert^2 + 2\langle a, b \rangle + \Vert b \Vert^2$$, and when $$\langle a, b \rangle = 0$$ the cross term drops out. Taking $$a = p$$ and $$b = u - p$$, we have that

$$
\Vert u \Vert^2 = \Vert p \Vert^2 + \Vert u - p \Vert^2 \ge \Vert p \Vert^2 .
$$

The hypotenuse is at least as long as either leg, so the shadow can't be longer than the vector casting it. The shadow has length $$\Vert p \Vert = \vert \langle u, v \rangle \vert / \Vert v \Vert$$. Plugging that in gives $$\Vert u \Vert^2 \ge \langle u, v \rangle^2 / \Vert v \Vert^2$$, and multiplying through by $$\Vert v \Vert^2$$ and taking square roots gives Cauchy–Schwarz.

## The discriminant proof is the same picture

The usual proof says that for every real $$t$$,

$$
f(t) = \Vert u - t v \Vert^2 = \Vert u \Vert^2 - 2t \langle u, v \rangle + t^2 \Vert v \Vert^2 \ge 0 .
$$

A quadratic that never goes negative has discriminant at most zero. So $$4\langle u, v \rangle^2 - 4\Vert u \Vert^2 \Vert v \Vert^2 \le 0$$, which is the inequality again.

What this proof doesn't tell you is where the quadratic bottoms out. Setting $$f'(t) = -2\langle u, v \rangle + 2t \Vert v \Vert^2$$ equal to zero, the minimum is at

$$
t^* = \frac{\langle u, v \rangle}{\Vert v \Vert^2}.
$$

That's exactly the coefficient from the projection, so $$t^* v = p$$. Plugging it back in, the minimum value is

$$
f(t^*) = \Vert u \Vert^2 - \frac{\langle u, v \rangle^2}{\Vert v \Vert^2} = \Vert u - p \Vert^2 ,
$$

which is the squared length of the dashed leg. So minimizing $$\Vert u - t v \Vert$$ over $$t$$ is the same as finding the point on the line closest to $$u$$, and that point is the foot of the perpendicular. The discriminant condition is just saying that the dashed leg has a nonnegative squared length.

<div class="row justify-content-center mt-3">
  <div class="col-sm-10 mt-3 mt-md-0">
    {% include figure.liquid loading="eager" path="assets/img/blog/cauchy-schwarz-shadows/quadratic-above-axis.svg" class="img-fluid rounded" zoomable=true %}
  </div>
</div>
<div class="caption">
  The quadratic t ↦ ‖u − tv‖² for u = (3, 2) and v = (4, 0). It starts at 13 and bottoms out at t* = 3/4, where the minimum value 4 is the squared length of u − p.
</div>

The picture also gives the equality case, which the discriminant version usually just states. Equality means $$\Vert u - p \Vert = 0$$. In other words, the dashed leg has collapsed and $$u$$ was already sitting on the line through $$v$$, which is what linearly dependent means here. For correlation, this is why $$\vert \rho \vert = 1$$ forces $$Y - \mathbb{E}Y$$ to be a constant multiple of $$X - \mathbb{E}X$$ almost surely.
