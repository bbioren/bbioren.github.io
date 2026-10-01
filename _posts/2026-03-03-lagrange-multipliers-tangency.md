---
layout: post
title: lagrange multipliers are a tangency condition
date: 2026-03-03
description: why the gradients line up at a constrained optimum, and what lambda means
tags: visual-proofs optimization calculus
categories: math
related_posts: false
thumbnail: /assets/img/blog/lagrange-multipliers-tangency/level-lines-kiss-circle.svg
---

Suppose you want to make $$x + y$$ as big as possible, but the point $$(x, y)$$ has to stay on the unit circle $$x^2 + y^2 = 1$$. What does the answer look like? Well, the level sets of $$f(x,y) = x + y$$ are the parallel lines $$x + y = k$$. So the problem is really asking for the largest $$k$$ where the line $$x + y = k$$ still touches the circle. If you draw it, the answer is pretty clear. The line slides up and to the right until it is just barely touching the circle, and any bigger $$k$$ misses the circle completely.

<div class="row justify-content-center mt-3">
  <div class="col-sm-10 mt-3 mt-md-0">
    {% include figure.liquid loading="eager" path="assets/img/blog/lagrange-multipliers-tangency/level-lines-kiss-circle.svg" class="img-fluid rounded" zoomable=true %}
  </div>
</div>
<div class="caption">
  Level lines of f = x + y and the unit circle. At P the line cuts through the circle and ∇f has a tangential part (orange). At Q the line just touches the circle, and ∇f and ∇g point the same way.
</div>

## Sliding along the circle

Start at $$P = (1, 0)$$, where $$f = 1$$. The line $$x + y = 1$$ goes through the circle at $$P$$ instead of just touching it. So if you walk counterclockwise a little bit, you end up on higher level lines.

We can see the same thing with vectors. Write the constraint as $$g(x,y) = x^2 + y^2 = 1$$, so that $$\nabla g = (2x, 2y)$$. At $$P$$ we have $$\nabla f = (1,1)$$ and $$\nabla g = (2, 0)$$. The vector $$\nabla g$$ is normal to the circle, so we can split $$\nabla f$$ into a piece along $$\nabla g$$ and a piece tangent to the circle:

$$
\nabla f = \underbrace{(1, 0)}_{\text{normal}} + \underbrace{(0, 1)}_{\text{tangent}}.
$$

The tangent piece is the orange arrow in the figure. Why do we care? Because as long as it is nonzero, you can move along the circle in its direction and $$f$$ goes up. So $$P$$ can't be the max.

If you keep sliding, you cross higher and higher lines until you get to $$Q = (1/\sqrt{2}, 1/\sqrt{2})$$. There the line $$x + y = \sqrt{2}$$ touches the circle at only one point, and the whole circle sits on the side where $$f \le \sqrt{2}$$. In terms of vectors, the tangent piece of $$\nabla f$$ is gone. All that's left is the normal piece, which points along $$\nabla g$$. At $$Q$$ we have that $$\nabla f = (1, 1)$$ and $$\nabla g = (\sqrt{2}, \sqrt{2})$$, so

$$
\nabla f = \frac{1}{\sqrt{2}}\, \nabla g.
$$

## What the theorem says

The Lagrange multiplier theorem says that the picture above is what happens in general. Suppose we want to maximize or minimize a smooth function $$f(x,y)$$ on the curve $$g(x,y) = c$$. If $$(x^*, y^*)$$ is a local optimum on the curve and $$\nabla g(x^*, y^*) \neq 0$$, then there is some number $$\lambda$$ with

$$
\nabla f(x^*, y^*) = \lambda\, \nabla g(x^*, y^*).
$$

In the circle example $$\lambda = 1/\sqrt{2}$$. The recipe most people learn is to write $$\mathcal{L} = f - \lambda\,(g - c)$$ and set $$\nabla \mathcal{L} = 0$$. The $$x$$ and $$y$$ partials of $$\mathcal{L}$$ give you exactly the equation above, and the $$\lambda$$ partial gives you back the constraint. So the recipe is just the tangency condition written in a different form. (Some people use a plus sign in front of $$\lambda$$, which just flips its sign. The minus makes the last section a little cleaner.)

Why should this work for any curve? The argument is the same as for the circle. Parametrize the curve near the optimum as $$\gamma(t)$$ with $$\gamma(0) = \mathbf{x}^*$$ and $$\gamma'(0) \neq 0$$. Since $$f(\gamma(t))$$ has a local max (or min) at $$t = 0$$, its derivative there is zero. By the chain rule that derivative is $$\nabla f \cdot \gamma'(0)$$, so

$$
\nabla f \cdot \gamma'(0) = 0.
$$

We also know $$g(\gamma(t)) = c$$ for every $$t$$. Differentiating that gives

$$
\nabla g \cdot \gamma'(0) = 0.
$$

So $$\nabla f$$ and $$\nabla g$$ are both perpendicular to the same nonzero vector $$\gamma'(0)$$. In the plane that forces them to be parallel, and since $$\nabla g \neq 0$$ we can write $$\nabla f = \lambda \nabla g$$. I'm not going to prove that the curve can be parametrized like this. That's where $$\nabla g \neq 0$$ comes in.

The equation doesn't tell you whether you found a max or a min. The bottom of the circle, $$(-1/\sqrt{2}, -1/\sqrt{2})$$, satisfies it too, with $$\lambda = -1/\sqrt{2}$$, and that point is the minimum. All the equation does is find the points of tangency. You still have to check which one is which.

The hypothesis the proof really needs is $$\nabla g \neq 0$$. It's what makes the constraint set a smooth curve near the optimum, with a tangent direction and a normal direction. If you drop it, the method can fail. For example, minimize $$f(x,y) = x$$ subject to $$y^2 - x^3 = 0$$. On this curve $$x^3 = y^2 \ge 0$$, so $$x \ge 0$$, and the minimum is $$0$$ at the origin. The origin is the tip of a cusp. There $$\nabla f = (1, 0)$$, but $$\nabla g = (-3x^2, 2y) = (0, 0)$$, and no $$\lambda$$ satisfies $$(1, 0) = \lambda\,(0, 0)$$. Running the recipe gives no solutions at all, so you would never find the real minimum this way. In the picture, a cusp has no tangent line, so there is nothing for the level curve to be tangent to. That's why the points where $$\nabla g = 0$$ have to be checked separately.

## What λ measures

So far $$\lambda$$ has only been a proportionality constant, but it does mean something. Take the problem of maximizing $$xy$$ subject to $$x + y = 10$$. Here $$\nabla f = (y, x)$$ and $$\nabla g = (1, 1)$$, so the equation $$\nabla f = \lambda \nabla g$$ says $$y = \lambda$$ and $$x = \lambda$$. Plugging into the constraint gives $$x = y = 5$$. The max is $$25$$, and $$\lambda = 5$$.

Now do the same problem with $$x + y = c$$ in place of $$10$$. The optimum is $$x = y = c/2$$ and the best value is $$f^*(c) = c^2/4$$. Taking the derivative with respect to $$c$$, we get

$$
\frac{d f^*}{dc} = \frac{c}{2} = 5 \quad \text{at } c = 10.
$$

Hey, that's $$\lambda$$! The same thing happens in general. If the optimizer $$\mathbf{x}^*(c)$$ moves smoothly as $$c$$ changes, the chain rule gives

$$
\frac{d f^*}{dc} = \nabla f \cdot \frac{d\mathbf{x}^*}{dc} = \lambda\, \nabla g \cdot \frac{d\mathbf{x}^*}{dc} = \lambda\, \frac{d}{dc}\, g(\mathbf{x}^*(c)) = \lambda\, \frac{d}{dc}\, c = \lambda.
$$

So $$\lambda$$ is how fast the best possible value goes up as you loosen the constraint. Economists call it the shadow price. If $$c$$ is a budget, then $$\lambda$$ is how much one more dollar is worth to you at the margin.
