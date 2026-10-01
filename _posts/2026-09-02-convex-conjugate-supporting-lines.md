---
layout: post
title: the convex conjugate is a list of supporting lines
date: 2026-09-02
description: for each slope, how far down do you push a line before it fits under the graph?
tags: visual-proofs convex-optimization duality
categories: math
related_posts: false
---

The convex conjugate shows up in Boyd and Vandenberghe (§3.3) as a one-line definition,

$$
f^*(y) = \sup_x \big( y^T x - f(x) \big),
$$

and on first read it's hard to see why anyone would write that down. Why subtract $$f$$ from a linear function, and why take a sup? I think the definition makes a lot more sense once you draw it. The short version is that $$f^*$$ describes the same convex function as $$f$$, except by its tangent lines instead of by its points.

## Pushing a line down

Let's stay in one dimension so everything fits in a picture. Fix a slope $$y$$ and look at all the lines $$yx + b$$ with that slope. If $$b$$ is very negative the line sits below the graph of $$f$$, and as you raise $$b$$ it eventually bumps into the graph. So what's the highest line of slope $$y$$ that still stays below?

A line $$yx + b$$ is below $$f$$ when $$yx + b \le f(x)$$ for every $$x$$, so when $$b \le f(x) - yx$$ for every $$x$$. The largest such $$b$$ is

$$
b = \inf_x \big( f(x) - yx \big) = -\sup_x \big( yx - f(x) \big) = -f^*(y).
$$

So the highest supporting line of slope $$y$$ is

$$
\ell_y(x) = yx - f^*(y),
$$

and $$f^*(y)$$ is minus its intercept. You can think of the conjugate as a table where you give it a slope and it tells you how far down a line of that slope has to go to fit under the graph.

Here's what that looks like for $$f(x) = e^x$$ with slope $$4$$.

<div class="row justify-content-center mt-3">
  <div class="col-sm-10 mt-3 mt-md-0">
    {% include figure.liquid loading="eager" path="assets/img/blog/convex-conjugate-supporting-lines/supporting-line-exp.svg" class="img-fluid rounded" zoomable=true %}
  </div>
</div>
<div class="caption">
  Lines of slope 4 next to e^x. The orange segment is the biggest gap 4x − e^x, at x* = ln 4. Shifting the orange line down by that much gives the blue supporting line, with intercept 4 − 4 ln 4 ≈ −1.55.
</div>

Start with the orange line $$4x$$ through the origin. On the shaded stretch it's above $$e^x$$, and the vertical gap at a point $$x$$ is $$4x - e^x$$, which is exactly the thing inside the sup. So $$f^*(4)$$ is the length of the tallest vertical segment you can fit between the line and the curve. That happens at $$x^* = \log 4$$, where the gap is $$4 \log 4 - 4 \approx 1.55$$. If you push the orange line down by that amount, the biggest gap closes to zero and you get the blue line, which touches the curve at $$x^*$$ and stays under it everywhere else. Push it down any less and it still cuts into the graph (the upper dashed line), and push it more and there's room to spare (the lower one).

Where does the line touch? At the point that maximized the gap, and if $$f$$ is differentiable that's where $$y - f'(x) = 0$$. So the supporting line of slope $$y$$ is the tangent line at the point where $$f$$ has slope $$y$$. For a convex function every tangent line lies below the graph, which is why this works out so cleanly.

Doing this for every slope gives the whole conjugate of $$e^x$$. For $$y \gt 0$$ the tangent point is $$x = \log y$$, and $$f^*(y) = y \log y - y$$. For $$y \lt 0$$ you get $$+\infty$$, and the picture tells you why. A line with negative slope keeps climbing as you go left while $$e^x$$ flattens out toward zero, so no amount of pushing down gets it under the curve. (The borderline case is $$y = 0$$, where $$f^*(0) = 0$$ and the supporting line is the asymptote.)

Let's do one more. For $$f(x) = x^2/2$$, the gap $$yx - x^2/2$$ peaks at $$x = y$$, so $$f^*(y) = y^2/2$$ and the function is its own conjugate.

## Going back

Since the conjugate is a sup over $$x$$, it's at least as big as the value at any particular $$x$$, which gives

$$
f(x) + f^*(y) \ge xy \quad \text{for all } x, y.
$$

This is the Fenchel–Young inequality, and it's the statement "$$\ell_y$$ lies below $$f$$" with the terms moved around. For $$x^2/2$$ it says $$\tfrac{1}{2}x^2 + \tfrac{1}{2}y^2 \ge xy$$, which is the usual AM–GM inequality.

You can also run the construction backwards. Taking the conjugate of $$f^*$$ gives

$$
f^{**}(x) = \sup_y \big( xy - f^*(y) \big) = \sup_y \ell_y(x),
$$

which is the upper envelope of all the supporting lines. If $$f$$ is convex (and closed, which rules out some bad behavior at the edge of its domain), those lines hug the graph everywhere and the envelope is $$f$$ again. So you really can rebuild the function from its table of slopes and intercepts.

## When f isn't convex

What happens if $$f$$ isn't convex? The definition still makes sense, and $$f^*$$ still comes out convex, because for each fixed $$x$$ the expression $$yx - f(x)$$ is affine in $$y$$ and a sup of affine functions is convex. But now $$f^{**}$$ isn't $$f$$ anymore. Here's a double well:

<div class="row justify-content-center mt-3">
  <div class="col-sm-10 mt-3 mt-md-0">
    {% include figure.liquid loading="eager" path="assets/img/blog/convex-conjugate-supporting-lines/convex-envelope-double-well.svg" class="img-fluid rounded" zoomable=true %}
  </div>
</div>
<div class="caption">
  The double well f(x) = (x² − 1)² with a few supporting lines. None of them can get into the bump between the minima, so f** is 0 on [−1, 1] and equals f outside. The shaded region never shows up in f*.
</div>

A supporting line has to stay under the whole graph, so none of them can reach up into the bump between the two wells. The conjugate never sees that part of $$f$$, and what you get back as $$f^{**}$$ is the convex envelope, which is flat across the middle and matches $$f$$ outside. Any two functions with the same convex envelope have the same conjugate.

I think this is the clearest way to see why Lagrange duality gives lower bounds. Boyd writes the dual function in terms of conjugates (§5.1.6), so the dual problem only ever sees $$f^{**}$$, which sits below $$f$$, and in effect it's solving the convexified problem. When $$f$$ is convex nothing is lost, and with a constraint qualification the bound is tight. When it isn't, the dual can come out strictly below the true optimum, and in this picture the difference comes from that shaded bump.
