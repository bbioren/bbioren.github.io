---
layout: post
title: why the gradient points uphill
date: 2026-02-09
description: a list of partial derivatives somehow knows the steepest direction, and a cosine explains why
tags: visual-proofs calculus optimization
categories: math
related_posts: false
---

The way the gradient usually shows up in a calculus class is as bookkeeping. You take the partial derivative in each coordinate, stack them into a vector, and call it $$\nabla f$$. Then a few pages later you're told this vector points in the direction of steepest ascent, and also that it's perpendicular to the level curves. That seems like a weird thing to just accept. The coordinate axes are an arbitrary choice, so why would slopes measured along them know anything about the best direction overall?

The answer comes from one formula. If $$f : \mathbb{R}^n \to \mathbb{R}$$ is differentiable at $$p$$ and $$u$$ is a unit vector, the rate of change of $$f$$ in the direction $$u$$ is

$$
D_u f(p) = \lim_{t \to 0} \frac{f(p + tu) - f(p)}{t} = \nabla f(p) \cdot u .
$$

This comes from what differentiability means in the first place, which is that up close $$f$$ looks like a plane:

$$
f(p + h) = f(p) + \nabla f(p) \cdot h + o(\Vert h \Vert).
$$

So near $$p$$, the function is basically the linear map $$h \mapsto \nabla f(p) \cdot h$$. The partials are just the coefficients of that map written in the coordinate basis, and the map itself doesn't care what basis you used. That's why the axes stop mattering.

## The picture

Let's make this concrete with $$f(x,y) = x^2 + 3y^2$$, whose level sets are ellipses. Pick the point $$p = (1, \tfrac12)$$, which sits on the level set $$f = 1.75$$, and where $$\nabla f(p) = (2, 3)$$. Now fan out a bunch of unit vectors around $$p$$ and color each one by how fast $$f$$ changes in that direction.

<div class="row justify-content-center mt-3">
  <div class="col-sm-10 mt-3 mt-md-0">
    {% include figure.liquid loading="eager" path="assets/img/blog/why-the-gradient-points-uphill/gradient-fan-on-contours.svg" class="img-fluid rounded" zoomable=true %}
  </div>
</div>
<div class="caption">
  Left: sixteen directions around p on the ellipses of f = x² + 3y², colored orange (uphill), gray (flat), or blue (downhill). Right: those same sixteen rates plotted against the angle to ∇f, which gives a cosine.
</div>

Each spoke has rate $$\nabla f(p) \cdot u$$, and if $$\theta$$ is the angle between $$u$$ and the gradient, that dot product is

$$
D_u f(p) = \Vert \nabla f(p) \Vert \cos\theta .
$$

So all the colors on the left are samples of one cosine curve, which is what the right panel plots. Once you've written it this way, everything falls out. The cosine is biggest at $$\theta = 0$$, so the steepest direction is along the gradient, and the rate there is $$\Vert \nabla f(p) \Vert$$. (If you want a name for this step, it's Cauchy–Schwarz.) The cosine is most negative at $$\theta = \pi$$, so straight downhill is $$-\nabla f$$. And it's zero at $$\theta = \pm \pi/2$$, which are the gray spokes.

Those gray spokes are where $$f$$ doesn't change to first order, so they should be the directions along the level set. You can check this directly. Take any curve $$\gamma(t)$$ that stays on the level set with $$\gamma(0) = p$$. Then $$f(\gamma(t)) = 1.75$$ for all $$t$$, and differentiating with the chain rule gives

$$
0 = \frac{d}{dt} f(\gamma(t)) \Big\vert_{t=0} = \nabla f(p) \cdot \gamma'(0).
$$

So every tangent direction to the level set is orthogonal to the gradient, which is the right angle drawn in the figure. This does need $$\nabla f(p) \neq 0$$, since at a critical point the level set can pinch or cross itself and there isn't a single normal direction anymore.

I like this picture because steepest ascent and perpendicularity stop being two separate facts. They're the max and the zeros of the same cosine.

The obvious use of all this is gradient descent. If you get one small step and want $$f$$ to go down as much as possible, the plane approximation tells you to step along $$-\nabla f$$, and so the update $$x_{k+1} = x_k - \alpha \nabla f(x_k)$$ is just the greedy move for that plane. The perpendicularity fact is also what makes Lagrange multipliers work, since at a constrained optimum both $$\nabla f$$ and the constraint's gradient are normal to the constraint surface, so they have to be parallel.

## Steepest according to whom

There's one thing hiding in the argument above. When we maximized $$\nabla f \cdot u$$, we took $$u$$ from the ordinary unit circle, $$\Vert u \Vert_2 = 1$$. That's a choice about how to measure step length, and if you measure it differently, "steepest" changes too.

Say you use a quadratic norm $$\Vert u \Vert_P = (u^\top P u)^{1/2}$$ with $$P$$ symmetric positive definite. Substituting $$w = P^{1/2} u$$ turns it back into the Euclidean problem, and the same cosine argument says the steepest direction is

$$
u^\star \propto P^{-1} \nabla f .
$$

This is the steepest descent direction for a quadratic norm in Boyd and Vandenberghe §9.4, and it's a nice way to think about Newton's method. Pick $$P = \nabla^2 f(x)$$ and you get the Newton step $$-\nabla^2 f(x)^{-1} \nabla f(x)$$, which is steepest descent measured in the function's own curvature. You can see it on our ellipses. With $$P = \mathrm{diag}(2, 6)$$, $$P^{-1} \nabla f$$ at a point $$(x, y)$$ is exactly $$(x, y)$$, so $$-P^{-1}\nabla f$$ aims straight at the minimum. Plain $$-\nabla f$$ doesn't, because it's perpendicular to a squashed ellipse and the ellipse's normal mostly doesn't point at the center.

There's a more abstract version of this about the derivative really being a covector, which needs an inner product before you can draw it as an arrow, but I'll skip it. The short version is that the level sets are fixed and the vector of partials is what you get once you've decided to use the dot product.
