---
layout: post
title: lagrange multipliers are a tangency condition
date: 2026-03-03
description: why the gradients line up at a constrained optimum, and what lambda is measuring
tags: visual-proofs optimization calculus
categories: math
related_posts: false
---

Lagrange multipliers usually get taught as a recipe. You write down $$\mathcal{L} = f - \lambda\,(g - c)$$, set $$\nabla \mathcal{L} = 0$$, and solve. The $$\lambda$$ shows up out of nowhere, helps you find the answer, and then nobody mentions it again. I think that's a shame, because the recipe is just a picture written as an equation, and once you've seen the picture there isn't much left to memorize.

Here's the setup. We want to maximize (or minimize) a smooth function $$f(x,y)$$ while staying on the curve $$g(x,y) = c$$. The theorem says that if $$(x^*, y^*)$$ is a local optimum on the curve and $$\nabla g(x^*, y^*) \neq 0$$, then there's some number $$\lambda$$ with

$$
\nabla f(x^*, y^*) = \lambda\, \nabla g(x^*, y^*).
$$

Setting $$\nabla \mathcal{L} = 0$$ gives you exactly this equation, plus the constraint. So why should the two gradients be parallel?

## The picture

Let's do an example where you can see everything. Maximize $$f(x,y) = x + y$$ on the unit circle $$x^2 + y^2 = 1$$. The level sets of $$f$$ are the parallel lines $$x + y = k$$, so we're looking for the biggest $$k$$ whose line still touches the circle.

<div class="row justify-content-center mt-3">
  <div class="col-sm-10 mt-3 mt-md-0">
    {% include figure.liquid loading="eager" path="assets/img/blog/lagrange-multipliers-tangency/level-lines-kiss-circle.svg" class="img-fluid rounded" zoomable=true %}
  </div>
</div>
<div class="caption">
  Level lines of f = x + y and the unit circle. At P the line cuts through the circle and ∇f has a tangential part (orange). At Q the line just touches the circle, and ∇f and ∇g point the same way.
</div>

Start at $$P = (1, 0)$$, where $$f = 1$$. The line $$x + y = 1$$ cuts right through the circle at $$P$$, so if you walk counterclockwise a little you end up on higher level lines. You can see the same thing with vectors. Split $$\nabla f = (1,1)$$ into a piece pointing along $$\nabla g = (2, 0)$$ (normal to the circle) and a piece tangent to the circle:

$$
\nabla f = \underbrace{(1, 0)}_{\text{normal}} + \underbrace{(0, 1)}_{\text{tangent}}.
$$

That tangent piece is the orange arrow, and as long as it's nonzero you can slide along the circle in its direction and make $$f$$ bigger. So $$P$$ isn't the max.

Now keep sliding. You cross higher and higher lines until you reach $$Q = (1/\sqrt{2}, 1/\sqrt{2})$$, where the line $$x + y = \sqrt{2}$$ only touches the circle at one point, and the whole circle sits on the side where $$f \le \sqrt{2}$$. The level line and the circle are tangent there. In vector terms, the tangent piece of $$\nabla f$$ has disappeared, so all that's left is the normal piece, which points along $$\nabla g$$. Checking, $$\nabla f = (1, 1)$$ and $$\nabla g = (\sqrt{2}, \sqrt{2})$$, so $$\lambda = 1/\sqrt{2}$$.

The same argument works for any curve. Parametrize the curve near the optimum as $$\gamma(t)$$ with $$\gamma(0) = \mathbf{x}^*$$ and $$\gamma'(0) \neq 0$$. Since $$f(\gamma(t))$$ has a local max at $$t = 0$$, its derivative $$\nabla f \cdot \gamma'(0)$$ is zero. And since $$g(\gamma(t)) = c$$ for all $$t$$, we also get $$\nabla g \cdot \gamma'(0) = 0$$. In the plane, two vectors that are both perpendicular to the same nonzero vector have to be parallel, and $$\nabla g \neq 0$$, so $$\nabla f = \lambda \nabla g$$.

(The bottom of the circle, $$(-1/\sqrt{2}, -1/\sqrt{2})$$, satisfies the same equation with $$\lambda = -1/\sqrt{2}$$. It's the minimum. The equation finds the tangent points, and you still have to check which one is which.)

## What λ is measuring

So far $$\lambda$$ is just a proportionality constant. Let's do one more example and see if it means anything. Maximize $$xy$$ subject to $$x + y = 10$$. We get $$\nabla f = (y, x)$$ and $$\nabla g = (1, 1)$$, so $$y = \lambda$$ and $$x = \lambda$$. That means $$x = y = 5$$, the max is $$25$$, and $$\lambda = 5$$.

Now redo it with $$x + y = c$$ instead of $$10$$. The optimum is $$x = y = c/2$$, so the best value is $$f^*(c) = c^2/4$$, and

$$
\frac{d f^*}{dc} = \frac{c}{2} = 5 \quad \text{at } c = 10.
$$

Hey, that's $$\lambda$$. And it's not a coincidence. If the optimizer $$\mathbf{x}^*(c)$$ moves smoothly as you change $$c$$, the chain rule gives

$$
\frac{d f^*}{dc} = \nabla f \cdot \frac{d\mathbf{x}^*}{dc} = \lambda\, \nabla g \cdot \frac{d\mathbf{x}^*}{dc} = \lambda\, \frac{d}{dc}\, g(\mathbf{x}^*(c)) = \lambda\, \frac{d}{dc}\, c = \lambda.
$$

So $$\lambda$$ tells you how fast the best possible value improves as you loosen the constraint. Economists call this the shadow price. If $$c$$ is your budget, $$\lambda$$ is how much one more dollar is worth to you at the margin, which is a pretty useful number to get for free.

## Where it breaks

The one hypothesis I'd actually pay attention to is $$\nabla g \neq 0$$. In the proof, that's what makes the constraint set a nice smooth curve near the optimum, with a tangent direction and a normal direction. If you drop it, things can go wrong.

Here's an example. Minimize $$f(x,y) = x$$ subject to $$y^2 - x^3 = 0$$. On this curve $$x^3 = y^2 \ge 0$$, so $$x \ge 0$$, and the minimum is $$0$$ at the origin, which is the tip of a cusp. But at the origin $$\nabla f = (1, 0)$$ and $$\nabla g = (-3x^2, 2y) = (0, 0)$$, and there's no $$\lambda$$ with $$(1, 0) = \lambda\,(0, 0)$$. So if you just run the recipe, it has no solutions at all, and you'd never find the actual minimum. A cusp doesn't have a tangent line, so there's nothing for the level curve to be tangent to. In practice this means you should check the points where $$\nabla g = 0$$ separately, since the recipe can't see them.
