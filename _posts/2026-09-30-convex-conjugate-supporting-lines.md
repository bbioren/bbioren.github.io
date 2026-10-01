---
layout: post
title: the convex conjugate is a list of supporting lines
date: 2026-09-30
description: for each slope, how far down do you have to push a line so it supports the graph?
tags: visual-proofs convex-optimization duality
categories: math
related_posts: false
---

The convex conjugate shows up in Boyd and Vandenberghe (§3.3) as a one-line definition, $$f^*(y) = \sup_x \left( y^T x - f(x) \right)$$, and it looks like it came out of nowhere. Why subtract $$f$$ from a linear function? Why take a sup? The answer is that the conjugate isn't really a new function. It's the same convex function written down a different way: you describe it by its tangent lines instead of by its points.

## The statement

Stay in one dimension so you can picture everything. For a function $$f : \mathbb{R} \to \mathbb{R}$$, the conjugate is

$$
f^*(y) = \sup_{x} \big( yx - f(x) \big).
$$

Here's the heuristic I'll spend the rest of the post justifying. Fix a slope $$y$$. Among all lines of slope $$y$$ that lie entirely below the graph of $$f$$, take the highest one. Its equation is

$$
\ell_y(x) = yx - f^*(y),
$$

so **the intercept of the best supporting line of slope $$y$$ is $$-f^*(y)$$**. The conjugate is a table that maps each slope to how far you have to slide a line of that slope to make it touch the graph from below.

As a quick sanity check, the units work out. $$yx$$ and $$f(x)$$ are both measured in "height," so $$f^*(y)$$ is a height too, which is exactly what an intercept should be.

## Why it matters

Take $$f(x) = x^2/2$$. Then $$yx - x^2/2$$ is a downward parabola in $$x$$ with its peak at $$x = y$$, so

$$
f^*(y) = y \cdot y - \tfrac{1}{2} y^2 = \tfrac{1}{2} y^2.
$$

The function is its own conjugate. Read geometrically, the supporting line of slope $$y$$ touches the parabola at $$x = y$$, and its intercept is $$-y^2/2$$.

Now take $$f(x) = e^x$$, where something more interesting happens. For $$y \gt 0$$, set the derivative of $$yx - e^x$$ to zero to get $$x = \log y$$, so $$f^*(y) = y \log y - y$$. For $$y = 0$$ the supremum of $$-e^x$$ is $$0$$, which you approach as $$x \to -\infty$$ but never reach. For $$y \lt 0$$, $$yx - e^x \to +\infty$$ as $$x \to -\infty$$, so $$f^*(y) = +\infty$$. That last case has a picture: no line with negative slope fits under $$e^x$$, however far down you push it, because the curve flattens out toward $$0$$ on the left while the line keeps climbing.

You also get one inequality for free. Since $$f^*(y)$$ is a supremum over $$x$$, it is at least the value at any particular $$x$$:

$$
f(x) + f^*(y) \ge xy \quad \text{for all } x, y.
$$

That's the Fenchel–Young inequality. It's the statement "the supporting line lies below the graph" with the terms moved around. With $$f = x^2/2$$ it becomes $$\tfrac{1}{2}x^2 + \tfrac{1}{2}y^2 \ge xy$$, which is AM–GM.

Do it twice and something even better happens: if $$f$$ is closed and convex, then $$f^{**} = f$$. You can rebuild the function from its table of supporting lines alone. And this is the engine of Lagrange duality. In §5.1.6, Boyd writes the dual function of a linearly constrained problem directly in terms of $$f_0^*$$.

## The visual proof

Here is the picture for $$f(x) = e^x$$ and slope $$y = 4$$.

<div class="row justify-content-center mt-3">
  <div class="col-sm-10 mt-3 mt-md-0">
    {% include figure.liquid loading="eager" path="assets/img/blog/convex-conjugate-supporting-lines/supporting-line-exp.svg" class="img-fluid rounded" zoomable=true %}
  </div>
</div>
<div class="caption">
  Lines of slope 4 next to the graph of e^x. The orange vertical segment is the largest gap 4x − e^x, reached at x* = ln 4. Pushing the orange line y = 4x down by exactly that gap gives the blue supporting line, which is tangent at x* and has intercept −f*(4) = 4 − 4 ln 4 ≈ −1.55.
</div>

Start with the orange line $$y = 4x$$ through the origin. Over the shaded region it sits above $$e^x$$, and the vertical gap between them at a point $$x$$ is $$4x - e^x$$. That expression is the thing inside the sup. So $$f^*(4)$$ is literally the tallest vertical segment you can fit between the line and the curve, and it's drawn in orange at $$x^* = \log 4$$, where it has length $$4 \log 4 - 4 \approx 1.55$$.

Now slide the line down. A line $$4x + b$$ lies below the graph exactly when $$4x + b \le e^x$$ for every $$x$$, which means $$b \le e^x - 4x$$ for every $$x$$, which means

$$
b \le \inf_x \big( e^x - 4x \big) = -\sup_x \big( 4x - e^x \big) = -f^*(4).
$$

So the highest admissible intercept is $$-f^*(4)$$. Getting there means pushing the orange line down by exactly the length of the largest gap, which closes that gap to zero. The result is the blue line. It lies below the curve and touches it at $$x^*$$. Lines above it, like the upper dashed one, cut into the graph. Lines below it, like the lower dashed one, leave room to spare.

Where does it touch? At the point that maximized the gap, and for differentiable $$f$$ that's where $$\frac{d}{dx}(yx - f(x)) = 0$$, that is, $$f'(x^*) = y$$. The supporting line of slope $$y$$ is the tangent line at the point where the curve has slope $$y$$. For a convex function every tangent line is a supporting line, so this always works. That's why the conjugate re-encodes $$f$$ by its tangents.

Running the argument in reverse gives $$f^{**}$$:

$$
f^{**}(x) = \sup_y \big( xy - f^*(y) \big) = \sup_y \ell_y(x).
$$

That is the upper envelope of all the supporting lines. For a closed convex function, the supporting hyperplane theorem says those lines hug the graph everywhere, so their envelope is $$f$$ itself.

## The part that gets missed

Two facts usually get skipped, and both come straight from the picture. First, **$$f^*$$ is always convex, even when $$f$$ is not.** For each fixed $$x$$, the expression $$yx - f(x)$$ is an affine function of $$y$$, and a pointwise supremum of affine functions is convex. You never need to check convexity of $$f$$ to know $$f^*$$ is convex. Second, $$f^{**} = f$$ needs $$f$$ to be closed and convex. Drop that and you get the largest closed convex function lying below $$f$$, which is the (closed) convex envelope:

<div class="row justify-content-center mt-3">
  <div class="col-sm-10 mt-3 mt-md-0">
    {% include figure.liquid loading="eager" path="assets/img/blog/convex-conjugate-supporting-lines/convex-envelope-double-well.svg" class="img-fluid rounded" zoomable=true %}
  </div>
</div>
<div class="caption">
  The double well f(x) = (x² − 1)² and a few of its supporting lines (blue). Every line that stays below f also stays below the flat segment joining the two minima. So the envelope of supporting lines, f**, is 0 on [−1, 1] and agrees with f outside that interval. The shaded bump is information that f* never records.
</div>

Supporting lines have to stay under the whole graph, so none of them can climb into the bump between the two wells. The conjugate simply never sees that part of $$f$$. Two functions with the same convex envelope have the same conjugate. That's the real content behind duality giving *lower bounds*. Through the conjugate, the dual problem sees only $$f^{**} \le f$$, so in effect it solves the convexified problem, and the best it can certify is a value at or below the true optimum. When $$f$$ is convex, the convexification loses nothing and (under a constraint qualification) the bound is tight. When it isn't, the shaded region is exactly what gets lost, and the space between $$f$$ and $$f^{**}$$ is where duality gaps come from.
