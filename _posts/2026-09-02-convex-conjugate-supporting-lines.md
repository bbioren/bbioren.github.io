---
layout: post
title: the convex conjugate is a list of supporting lines
date: 2026-09-02
description: for each slope, how far down a line has to go before it fits under the graph
tags: visual-proofs convex-optimization duality
categories: math
related_posts: false
---

The convex conjugate shows up in Boyd and Vandenberghe (§3.3) as a one-line definition,

$$
f^*(y) = \sup_x \big( y^T x - f(x) \big).
$$

What is this thing supposed to be? On its own the definition doesn't say much. It makes a lot more sense once you draw it. The short version is that $$f^*$$ describes the same convex function as $$f$$, but by its tangent lines instead of by its points.

## Supporting lines of a fixed slope

To keep everything in a picture, I'm going to stay in one dimension. Fix a slope $$y$$ and look at the lines $$yx + b$$ with that slope. If $$b$$ is very negative, the line sits below the graph of $$f$$. As you raise $$b$$, it eventually runs into the graph. So how high can it go? Well, the line $$yx + b$$ is below $$f$$ when $$yx + b \le f(x)$$ for every $$x$$. We can rewrite that as $$b \le f(x) - yx$$ for every $$x$$, so the largest $$b$$ that works is

$$
b = \inf_x \big( f(x) - yx \big) = -\sup_x \big( yx - f(x) \big) = -f^*(y).
$$

So the highest supporting line of slope $$y$$ is

$$
\ell_y(x) = yx - f^*(y),
$$

and $$f^*(y)$$ is just minus its intercept. You can think of the conjugate as a table. You give it a slope, and it tells you how far down a line of that slope has to be pushed before it fits under the graph.

The figure below shows this for $$f(x) = e^x$$ with slope $$4$$.

<div class="row justify-content-center mt-3">
  <div class="col-sm-10 mt-3 mt-md-0">
    {% include figure.liquid loading="eager" path="assets/img/blog/convex-conjugate-supporting-lines/supporting-line-exp.svg" class="img-fluid rounded" zoomable=true %}
  </div>
</div>
<div class="caption">
  Lines of slope 4 next to e^x. The orange segment is the biggest gap 4x − e^x, at x* = ln 4. Shifting the orange line down by that much gives the blue supporting line, with intercept 4 − 4 ln 4 ≈ −1.55.
</div>

Start with the orange line $$4x$$ through the origin. On the shaded stretch it is above $$e^x$$. The vertical gap at a point $$x$$ is $$4x - e^x$$, which is exactly the expression inside the sup, so $$f^*(4)$$ is the length of the tallest gap. Setting the derivative $$4 - e^x$$ to zero puts the tallest gap at $$x^* = \log 4$$, and there the gap is $$4 \log 4 - 4 \approx 1.55$$. Pushing the orange line down by that amount gives the blue line, which touches the curve at $$x^*$$ and stays under it everywhere else. If you push it down any less, it still cuts into the graph (that's the upper dashed line). If you push it down any more, there's room to spare (the lower dashed line).

Notice that the blue line touches the curve exactly at the point that maximized the gap. When $$f$$ is differentiable, that's the point where $$y - f'(x) = 0$$, which is where $$f$$ has slope $$y$$. So the supporting line of slope $$y$$ is just the tangent line at that point. This works because every tangent line of a convex function lies below the graph.

Doing this for every slope gives the whole conjugate of $$e^x$$. For $$y \gt 0$$, the tangent point is $$x = \log y$$, and plugging in gives $$f^*(y) = y \log y - y$$. For $$y \lt 0$$ the conjugate is $$+\infty$$. A line with negative slope keeps climbing as you go left, while $$e^x$$ flattens out toward zero, so no amount of pushing down gets it under the curve. For $$f(x) = x^2/2$$, the gap $$yx - x^2/2$$ peaks at $$x = y$$, so $$f^*(y) = y^2/2$$. This function is its own conjugate, which is kind of nice.

## Building f back from the lines

The conjugate is a sup over $$x$$, so it's at least as big as the value at any particular $$x$$. That gives

$$
f(x) + f^*(y) \ge xy \quad \text{for all } x, y.
$$

This is the Fenchel–Young inequality. It's really just the statement that $$\ell_y$$ lies below $$f$$, with the terms moved around. For $$x^2/2$$ it says $$\tfrac{1}{2}x^2 + \tfrac{1}{2}y^2 \ge xy$$, which is the usual AM–GM inequality.

You can also run the construction backwards. Taking the conjugate of $$f^*$$ gives

$$
f^{**}(x) = \sup_y \big( xy - f^*(y) \big) = \sup_y \ell_y(x),
$$

which is the upper envelope of all the supporting lines. If $$f$$ is convex and closed, the supporting lines hug the graph everywhere, and the envelope is just $$f$$ again. (I'm not going to prove that part.)

What if $$f$$ isn't convex? The definition still makes sense, and $$f^*$$ still comes out convex. For each fixed $$x$$ the expression $$yx - f(x)$$ is affine in $$y$$, and a sup of affine functions is convex. But $$f^{**}$$ is no longer equal to $$f$$. A double well is a good example.

<div class="row justify-content-center mt-3">
  <div class="col-sm-10 mt-3 mt-md-0">
    {% include figure.liquid loading="eager" path="assets/img/blog/convex-conjugate-supporting-lines/convex-envelope-double-well.svg" class="img-fluid rounded" zoomable=true %}
  </div>
</div>
<div class="caption">
  The double well f(x) = (x² − 1)² with a few supporting lines. None of them can get into the bump between the minima, so f** is 0 on [−1, 1] and equals f outside. The shaded region never shows up in f*.
</div>

Every supporting line has to stay under the whole graph, so none of them can reach up into the bump between the two wells. The conjugate never sees that part of $$f$$. What comes back as $$f^{**}$$ is the convex envelope, which is flat across the middle and matches $$f$$ outside. In particular, any two functions with the same convex envelope have the same conjugate.

This is, I think, the clearest way to see why Lagrange duality gives lower bounds. Boyd writes the dual function in terms of conjugates (§5.1.6), so the dual problem only ever sees $$f^{**}$$. That sits below $$f$$, so in effect the dual is solving the convexified problem. When $$f$$ is convex nothing is lost, and with a constraint qualification the bound is tight. When it isn't, the dual can come out strictly below the true optimum. In the picture above, that difference comes from the shaded bump.
