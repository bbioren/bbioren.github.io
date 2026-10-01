---
layout: post
title: why the gradient points uphill
date: 2026-02-09
description: where the directional derivative formula comes from and what it says about steepest ascent
tags: visual-proofs calculus optimization
categories: math
related_posts: false
---

If $$f : \mathbb{R}^n \to \mathbb{R}$$ is differentiable at a point $$p$$ and $$u$$ is a unit vector, then the rate at which $$f$$ changes as you move away from $$p$$ in the direction $$u$$ is

$$
D_u f(p) = \lim_{t \to 0} \frac{f(p + tu) - f(p)}{t} = \nabla f(p) \cdot u .
$$

So to get the slope in any direction at all, you take the gradient (the vector of partial derivatives) and dot it with the direction you care about. That's a strange thing to be true if you stop and look at it. The partial derivatives are slopes along the coordinate axes, and the coordinate axes are a pretty arbitrary choice. Why should slopes along those particular directions know anything about every other direction? And why should the gradient end up pointing in the direction of steepest ascent, and be perpendicular to the level curves on top of that?

The answer comes from what it means for $$f$$ to be differentiable in the first place. Differentiability says that close to $$p$$ the function looks like a plane. More precisely, it says that

$$
f(p + h) = f(p) + \nabla f(p) \cdot h + o(\Vert h \Vert).
$$

(I'm being a little loose with the $$o(\Vert h \Vert)$$ notation. It just means some error term that goes to zero faster than $$\Vert h \Vert$$ does.) If we plug in $$h = tu$$, subtract $$f(p)$$ and divide by $$t$$, we get

$$
\frac{f(p + tu) - f(p)}{t} = \nabla f(p) \cdot u + \frac{o(\Vert tu \Vert)}{t}.
$$

Since $$u$$ has length one, the last term goes to zero as $$t \to 0$$, and we're left with the formula from the top. So near $$p$$ the function is basically the linear map $$h \mapsto \nabla f(p) \cdot h$$. The partial derivatives are just the coefficients of that map when you write it out in the coordinate basis. The map itself doesn't depend on which basis you picked, so the choice of axes ends up not mattering.

## Sixteen directions on an ellipse

To see this on an actual function, take $$f(x,y) = x^2 + 3y^2$$, whose level sets are ellipses around the origin. At the point $$p = (1, \tfrac12)$$ we have $$f(p) = 1 + \tfrac34 = 1.75$$, so $$p$$ sits on the level set $$f = 1.75$$. The gradient is $$\nabla f = (2x, 6y)$$, which at $$p$$ gives $$\nabla f(p) = (2, 3)$$. In the figure I drew a fan of unit vectors coming out of $$p$$ and colored each one by how fast $$f$$ changes when you move in that direction.

<div class="row justify-content-center mt-3">
  <div class="col-sm-10 mt-3 mt-md-0">
    {% include figure.liquid loading="eager" path="assets/img/blog/why-the-gradient-points-uphill/gradient-fan-on-contours.svg" class="img-fluid rounded" zoomable=true %}
  </div>
</div>
<div class="caption">
  Left: sixteen directions around p on the ellipses of f = x² + 3y², colored orange (uphill), gray (flat), or blue (downhill). Right: the same sixteen rates plotted against the angle to ∇f, which gives a cosine.
</div>

The rate along each spoke is $$\nabla f(p) \cdot u$$. If $$\theta$$ is the angle between $$u$$ and the gradient, we can rewrite this dot product as

$$
D_u f(p) = \Vert \nabla f(p) \Vert \Vert u \Vert \cos\theta = \Vert \nabla f(p) \Vert \cos\theta ,
$$

where the $$\Vert u \Vert$$ drops out because $$u$$ is a unit vector. So the colors on the left are all samples of one cosine curve, and the right panel just plots that curve against the angle.

Most of what you'd want to know about the gradient can be read off this curve. Where is the cosine largest? At $$\theta = 0$$, so the steepest direction is the gradient itself, and the rate of increase along it is $$\Vert \nabla f(p) \Vert$$. (This is really just Cauchy–Schwarz, but I find the cosine easier to remember.) Where is it most negative? At $$\theta = \pi$$, so the steepest way down is $$-\nabla f$$. And it's zero at $$\theta = \pm \pi/2$$, which are the gray spokes in the figure.

Along the gray spokes $$f$$ doesn't change to first order, so they ought to be the directions that run along the level set. We can check this directly. Take any curve $$\gamma(t)$$ that stays on the level set and has $$\gamma(0) = p$$. Then $$f(\gamma(t)) = 1.75$$ for every $$t$$. Differentiating both sides with the chain rule gives

$$
0 = \frac{d}{dt} f(\gamma(t)) \Big\vert_{t=0} = \nabla f(p) \cdot \gamma'(0).
$$

So every tangent direction to the level set is orthogonal to the gradient, which is the right angle drawn in the figure. This does need $$\nabla f(p) \neq 0$$. At a critical point the level set can pinch or cross itself, and then there isn't a single normal direction anymore.

The obvious use of all this is gradient descent. If you're allowed one small step and want $$f$$ to go down as much as possible, the plane approximation says to step along $$-\nabla f$$. The update $$x_{k+1} = x_k - \alpha \nabla f(x_k)$$ is just that greedy move, made over and over. The perpendicular fact is also why Lagrange multipliers work. At a constrained optimum, $$\nabla f$$ and the gradient of the constraint are both normal to the constraint surface, so they have to be parallel.

## Measuring step length a different way

When I maximized $$\nabla f \cdot u$$ above, I took $$u$$ from the ordinary unit circle, $$\Vert u \Vert_2 = 1$$. That's actually a choice about how to measure the length of a step. If you measure length some other way, the steepest direction changes too. Say you use a quadratic norm $$\Vert u \Vert_P = (u^\top P u)^{1/2}$$, where $$P$$ is symmetric positive definite. Substituting $$w = P^{1/2} u$$ turns the problem back into the Euclidean one. We have that

$$
\nabla f \cdot u = \nabla f \cdot P^{-1/2} w = (P^{-1/2} \nabla f) \cdot w ,
$$

and $$\Vert w \Vert_2 = \Vert u \Vert_P = 1$$. So the same cosine argument says the best $$w$$ points along $$P^{-1/2} \nabla f$$, and going back with $$u = P^{-1/2} w$$ gives

$$
u^\star \propto P^{-1} \nabla f .
$$

Flip the sign and this is the steepest descent direction for a quadratic norm in §9.4 of Boyd and Vandenberghe. It also gives a nice way to think about Newton's method. If you pick $$P = \nabla^2 f(x)$$, you get the Newton step $$-\nabla^2 f(x)^{-1} \nabla f(x)$$. So Newton's method is steepest descent where the length of a step is measured using the function's own curvature.

The ellipses from before show the difference. The Hessian of our $$f$$ is $$P = \mathrm{diag}(2, 6)$$, and at a point $$(x, y)$$ we have that

$$
P^{-1} \nabla f = \left( \tfrac{2x}{2}, \tfrac{6y}{6} \right) = (x, y).
$$

So $$-P^{-1}\nabla f$$ aims straight at the minimum at the origin. Plain $$-\nabla f$$ doesn't do that. It's perpendicular to a squashed ellipse, and the normal to a squashed ellipse mostly doesn't point at the center.
