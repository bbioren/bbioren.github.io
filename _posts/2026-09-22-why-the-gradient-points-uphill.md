---
layout: post
title: why the gradient points uphill
date: 2026-09-22
description: the vector of partials is the steepest direction because, up close, every function is a plane
tags: visual-proofs calculus optimization
categories: math
related_posts: false
---

The gradient is usually introduced as bookkeeping: take the partial derivative in each coordinate and stack them into a vector. A few pages later comes the claim that this vector points in the direction of steepest ascent and sits perpendicular to the level curves. Presented that way, it sounds like a lucky coincidence. Why would a list of slopes along the coordinate axes, which are an arbitrary choice, know anything about the best direction overall? It isn't luck, and the reason fits in one line.

## The statement

Let $$f : \mathbb{R}^n \to \mathbb{R}$$ be differentiable at $$p$$, and let $$u$$ be a unit vector. The directional derivative of $$f$$ at $$p$$ in direction $$u$$ is

$$
D_u f(p) = \lim_{t \to 0} \frac{f(p + tu) - f(p)}{t} = \nabla f(p) \cdot u .
$$

The heuristic is that differentiability means that, up close, $$f$$ is a plane:

$$
f(p + h) = f(p) + \nabla f(p) \cdot h + o(\Vert h \Vert).
$$

Near $$p$$, then, $$f$$ acts like the linear function $$h \mapsto g \cdot h$$ with $$g = \nabla f(p)$$. A linear function $$g \cdot h$$ grows fastest when you walk along its own coefficient vector $$g$$, and doesn't change at all when you walk perpendicular to it. The partials happen to be the coefficients of that linear map in the coordinate basis, and the map itself doesn't depend on which basis you used to write it down. That's why the coordinate axes stop mattering.

## Why it matters

The obvious use is gradient descent. If you're allowed one small step and want $$f$$ to drop as much as possible, the first-order model says to step along $$-\nabla f$$. So the update $$x_{k+1} = x_k - \alpha \nabla f(x_k)$$ is just the greedy choice for the plane that approximates $$f$$ at $$x_k$$.

The less obvious use is finding normal vectors for free. Take the sphere $$x^2 + y^2 + z^2 = r^2$$, which is a level set of $$F(x,y,z) = x^2 + y^2 + z^2$$. Since $$\nabla F = (2x, 2y, 2z)$$, the normal at a point $$(x_0, y_0, z_0)$$ is parallel to $$(x_0, y_0, z_0)$$, and the tangent plane there is

$$
x_0 x + y_0 y + z_0 z = r^2 .
$$

The radius is perpendicular to the sphere, which is exactly what you'd expect, and you get it without parametrizing the surface. The same trick gives the tangent plane to any surface $$F = c$$, and it's the geometric fact under Lagrange multipliers: at a constrained optimum, $$\nabla f$$ and $$\nabla g$$ are both normal to the constraint surface, so they're parallel.

## The visual proof

Here's the whole argument in one picture. The function is $$f(x,y) = x^2 + 3y^2$$, whose level sets are ellipses. Fix the point $$p = (1, \tfrac12)$$ on the level set $$f = 1.75$$, where $$\nabla f(p) = (2, 3)$$.

<div class="row justify-content-center mt-3">
  <div class="col-sm-10 mt-3 mt-md-0">
    {% include figure.liquid loading="eager" path="assets/img/blog/why-the-gradient-points-uphill/gradient-fan-on-contours.svg" class="img-fluid rounded" zoomable=true %}
  </div>
</div>
<div class="caption">
  Left: level sets of f = x² + 3y², with sixteen unit directions u fanned around p = (1, ½), colored by the directional derivative (orange is uphill, gray is flat, blue is downhill). The gradient arrow is shortened and drawn perpendicular to the dashed tangent line. Right: the same sixteen directional derivatives plotted against the angle θ between u and ∇f trace out exactly |∇f| cos θ.
</div>

**Step 1: every direction is a dot product.** Each spoke in the fan on the left is a unit vector $$u$$. By the statement above, the rate at which $$f$$ changes along that spoke is $$\nabla f(p) \cdot u$$. Writing $$\theta$$ for the angle between $$u$$ and $$\nabla f(p)$$, this is

$$
D_u f(p) = \Vert \nabla f(p) \Vert \, \Vert u \Vert \cos\theta = \Vert \nabla f(p) \Vert \cos\theta .
$$

So the spoke colors on the left are just samples of a single cosine, which is what the right panel shows.

**Step 2: read off the maximum.** Since $$\cos\theta \le 1$$, with equality only at $$\theta = 0$$, the best rate available is $$\Vert \nabla f(p) \Vert$$, and you get it only by pointing $$u$$ along $$\nabla f(p)$$. This is Cauchy–Schwarz, $$\nabla f \cdot u \le \Vert \nabla f \Vert \, \Vert u \Vert$$, with equality exactly when the two vectors are positively parallel. The worst rate is $$-\Vert \nabla f(p) \Vert$$, at $$\theta = \pi$$. In the picture, the brightest orange spoke lies under the gradient arrow and the darkest blue one points the opposite way.

**Step 3: the flat directions are the tangent.** The gray spokes at $$\theta = \pm \pi/2$$ are the directions where $$D_u f(p) = 0$$, so to first order $$f$$ doesn't change along them. Those are exactly the directions you move in when you slide along the level set. To check this, take any smooth curve $$\gamma(t)$$ lying in the level set with $$\gamma(0) = p$$. Then $$f(\gamma(t)) = 1.75$$ for every $$t$$, and the chain rule gives

$$
0 = \frac{d}{dt} f(\gamma(t)) \Big\vert_{t=0} = \nabla f(p) \cdot \gamma'(0).
$$

Every tangent vector to the level set is therefore orthogonal to $$\nabla f(p)$$, so the gradient is normal to the level set. That's the right-angle mark in the figure. (This needs $$\nabla f(p) \neq 0$$. At a critical point, the level set can pinch or cross itself, and "the normal direction" stops making sense.)

Steepest ascent and perpendicularity come out of the same cosine: the maximum is at $$\theta = 0$$, and the zeros are at $$\theta = \pm\pi/2$$.

## The part that gets missed

"Steepest" quietly depends on how you measure step length. Step 2 maximized $$\nabla f \cdot u$$ over the Euclidean unit sphere $$\Vert u \Vert_2 = 1$$. If you measure steps in a different norm, you get a different answer. Take a quadratic norm $$\Vert u \Vert_P = (u^\top P u)^{1/2}$$ with $$P$$ symmetric positive definite. Substituting $$w = P^{1/2} u$$ turns the constraint into $$\Vert w \Vert_2 = 1$$ and the objective into $$(P^{-1/2} \nabla f) \cdot w$$. By the same Cauchy–Schwarz argument, the best $$w$$ is parallel to $$P^{-1/2}\nabla f$$, which means the steepest direction is

$$
u^\star \propto P^{-1} \nabla f .
$$

This is the steepest descent direction for a quadratic norm in Boyd and Vandenberghe §9.4. Choosing $$P = \nabla^2 f(x)$$ gives the Newton direction $$-\nabla^2 f(x)^{-1} \nabla f(x)$$, and choosing some other $$P$$ is what "preconditioning" means. Newton's method isn't a different idea from gradient descent. It's steepest descent in the geometry the function's own curvature suggests. On the ellipses above, $$P = \mathrm{diag}(2, 6)$$ makes $$P^{-1}\nabla f$$ at any point $$(x, y)$$ equal to $$(x, y)$$ itself, so the step $$-P^{-1}\nabla f$$ points straight at the minimum. Plain $$-\nabla f$$ doesn't, because it's perpendicular to a squashed ellipse. The deeper version of the same point is that the derivative is fundamentally a covector, the linear map $$h \mapsto df_p(h)$$ that eats a direction and returns a rate. Turning it into an arrow you can draw takes an inner product: $$\nabla f$$ is the vector $$g$$ with $$\langle g, h \rangle = df_p(h)$$ for all $$h$$. With the dot product that's the vector of partials. With $$\langle u, v \rangle_P = u^\top P v$$ it's $$P^{-1}\nabla f$$, and that arrow is $$P$$-perpendicular to the level sets. The level sets themselves never change. What changes is your choice of what "perpendicular" and "steepest" mean, and the vector of partials is just the answer you get for the Euclidean choice.
