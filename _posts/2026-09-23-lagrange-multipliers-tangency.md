---
layout: post
title: lagrange multipliers are a tangency condition
date: 2026-09-23
description: why the gradients line up at a constrained optimum, and what the multiplier is actually measuring
tags: visual-proofs optimization calculus
categories: math
related_posts: false
---

Lagrange multipliers are usually handed over as a recipe: write down $$\mathcal{L} = f - \lambda\,(g - c)$$, set $$\nabla \mathcal{L} = 0$$, solve. The variable $$\lambda$$ shows up from nowhere, does its job, and gets thrown away. But the recipe is a compressed picture, and once you see the picture, neither the equation nor $$\lambda$$ is mysterious.

## The statement

Suppose we want to maximize (or minimize) a smooth $$f(x,y)$$ subject to a smooth constraint $$g(x,y) = c$$. If $$(x^*, y^*)$$ is a local optimum on the constraint curve and $$\nabla g(x^*, y^*) \neq 0$$, then there is a number $$\lambda$$ with

$$
\nabla f(x^*, y^*) = \lambda\, \nabla g(x^*, y^*).
$$

(Setting $$\nabla \mathcal{L} = 0$$ says exactly this, plus the constraint itself.) Why should it be true? The gradient $$\nabla f$$ points in the direction where $$f$$ increases fastest. If it had any component *along* the constraint curve, you could slide a little along the curve in that direction and make $$f$$ bigger, all while staying feasible. So at an optimum, $$\nabla f$$ has no component along the curve, which means it is perpendicular to the curve. And $$\nabla g$$ is perpendicular to the curve too, since the curve is a level set of $$g$$. Two vectors that are both perpendicular to the same curve in the plane are parallel.

## What it buys you

Take the classic: maximize $$xy$$ subject to $$x + y = 10$$. We have $$\nabla f = (y, x)$$ and $$\nabla g = (1, 1)$$, so the condition reads $$y = \lambda$$ and $$x = \lambda$$. Then $$x = y$$, the constraint forces $$x = y = 5$$, the maximum is $$25$$, and $$\lambda = 5$$.

That $$5$$ is not a throwaway. Redo the problem with $$x + y = c$$: the optimum is $$x = y = c/2$$, so the optimal value is $$f^*(c) = c^2/4$$, and

$$
\frac{d f^*}{dc} = \frac{c}{2} = 5 \quad \text{at } c = 10.
$$

Hey, that's $$\lambda$$. This is true in general. Write the optimizer as $$\mathbf{x}^*(c)$$ and assume it moves smoothly with $$c$$. Then

$$
\frac{d f^*}{dc} = \nabla f \cdot \frac{d\mathbf{x}^*}{dc} = \lambda\, \nabla g \cdot \frac{d\mathbf{x}^*}{dc} = \lambda\, \frac{d}{dc}\, g(\mathbf{x}^*(c)) = \lambda \cdot \frac{d}{dc}\, c = \lambda.
$$

So $$\lambda$$ is the rate at which the best achievable value improves when you loosen the constraint. Economists call it the shadow price: if $$c$$ is a budget, $$\lambda$$ is what one more dollar is worth at the margin.

## The picture

My favorite way to see the theorem is a second example: maximize $$f(x,y) = x + y$$ on the unit circle $$g(x,y) = x^2 + y^2 = 1$$. The level sets of $$f$$ are the parallel lines $$x + y = k$$, and maximizing $$f$$ means finding the largest $$k$$ whose line still touches the circle.

<div class="row justify-content-center mt-3">
  <div class="col-sm-10 mt-3 mt-md-0">
    {% include figure.liquid loading="eager" path="assets/img/blog/lagrange-multipliers-tangency/level-lines-kiss-circle.svg" class="img-fluid rounded" zoomable=true %}
  </div>
</div>
<div class="caption">
  Level lines of f = x + y and the constraint circle. At P the level line f = 1 cuts across the circle, and ∇f has a nonzero tangential part (orange), so sliding up the circle increases f. At Q the level line f = √2 just touches the circle, and ∇f and ∇g point the same way.
</div>

Start at $$P = (1, 0)$$, where $$f = 1$$. The line $$x + y = 1$$ *crosses* the circle there, so on one side of $$P$$ the circle climbs into territory where $$f$$ is bigger. In terms of vectors, split $$\nabla f = (1,1)$$ into a part normal to the circle and a part tangent to it. At $$P$$ the normal direction is $$\nabla g = (2, 0)$$, so

$$
\nabla f = \underbrace{(1, 0)}_{\text{normal}} + \underbrace{(0, 1)}_{\text{tangent}}.
$$

The tangential part $$(0,1)$$ is the orange arrow. Moving counterclockwise from $$P$$ at unit speed, $$f$$ increases at rate $$1$$, so $$P$$ is not a maximum.

Keep sliding, crossing higher and higher level lines, until you reach $$Q = (1/\sqrt{2}, 1/\sqrt{2})$$ on the line $$x + y = \sqrt{2}$$. That line touches the circle at a single point, with the whole circle on the side where $$f \le \sqrt{2}$$: the level curve and the constraint are tangent. Equivalently, the tangential part of $$\nabla f$$ is zero, so all that is left is its normal part, which points along $$\nabla g$$. Indeed $$\nabla f = (1, 1)$$ and $$\nabla g = (\sqrt{2}, \sqrt{2})$$, so

$$
\nabla f(Q) = \tfrac{1}{\sqrt{2}}\, \nabla g(Q), \qquad \lambda = \tfrac{1}{\sqrt{2}}.
$$

That is the whole proof, and it works for any constraint curve. Parametrize the curve near the optimum by $$\gamma(t)$$ with $$\gamma(0) = \mathbf{x}^*$$ and $$\gamma'(0) \neq 0$$. Since $$f(\gamma(t))$$ has a local max at $$t = 0$$, its derivative $$\nabla f \cdot \gamma'(0)$$ vanishes: the tangential part of $$\nabla f$$ is zero. Differentiating $$g(\gamma(t)) = c$$ gives $$\nabla g \cdot \gamma'(0) = 0$$ as well. In the plane, two vectors orthogonal to the same nonzero vector $$\gamma'(0)$$ are parallel, and since $$\nabla g \neq 0$$ we can write $$\nabla f = \lambda \nabla g$$.

## The part that gets missed

Look at where the proof used $$\nabla g \neq 0$$: it is what guarantees that the constraint set really is a smooth curve near the optimum, with a tangent direction $$\gamma'(0)$$ and a normal direction we can call $$\nabla g$$. Drop it and the theorem fails. Minimize $$f(x,y) = x$$ subject to $$g(x,y) = y^2 - x^3 = 0$$. Feasibility forces $$x^3 = y^2 \ge 0$$, so $$x \ge 0$$, and the minimum is $$0$$, attained only at the origin, which is the tip of a cusp. There $$\nabla f = (1, 0)$$ but $$\nabla g = (-3x^2, 2y) = (0, 0)$$, and no $$\lambda$$ makes $$(1, 0) = \lambda (0, 0)$$. The recipe $$\nabla \mathcal{L} = 0$$ has no solutions at all here, so the true minimizer is invisible to it; points where $$\nabla g = 0$$ must always be checked separately. The other half of the fine print is that the condition is necessary, not sufficient. On the unit circle, $$Q' = (-1/\sqrt{2}, -1/\sqrt{2})$$ also satisfies $$\nabla f = \lambda \nabla g$$, with $$\lambda = -1/\sqrt{2}$$, and it is the minimum. The condition can even hold at a point that is neither: maximize $$f = y^3$$ on the line $$x = 0$$, and the origin satisfies $$\nabla f = (0,0) = 0 \cdot \nabla g$$ while $$f$$ keeps increasing straight through it. The equation $$\nabla f = \lambda \nabla g$$ finds the places where the level curve kisses the constraint; deciding which kiss is the maximum is still up to you.
