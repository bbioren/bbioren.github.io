---
layout: post
title: where the root pi comes from
date: 2026-06-11
description: the gaussian integral, and the circle hiding inside every bell curve
tags: visual-proofs calculus probability
categories: math
related_posts: false
---

Everyone who has taken a statistics class has memorized the normal density, and with it the odd constant out front: $$\frac{1}{\sqrt{2\pi}}$$. The $$e^{-x^2/2}$$ part makes sense, since it's a bump that dies off fast. But what is $$\pi$$ doing there? There are no circles anywhere in sight. The usual answer is "it makes the total area equal to 1," which is true and explains nothing. The real answer is that there _is_ a circle in the bell curve. You just have to look at it from above.

## the statement

The fact underneath everything is the Gaussian integral:

$$
I = \int_{-\infty}^{\infty} e^{-x^2}\, dx = \sqrt{\pi}.
$$

A quick sanity check: $$e^{-x^2}$$ is at most 1 and is already below $$0.02$$ by $$x = 2$$, so the area should be a bit less than 2, roughly the area of a box of height 1 over $$[-1, 1]$$. And $$\sqrt{\pi} \approx 1.772$$. Plausible.

The trouble is actually proving it. The obvious attack is to find an antiderivative and plug in the endpoints, but $$e^{-x^2}$$ has no elementary antiderivative, so that's a dead end. The trick is to stop working in one dimension. Multiply two copies together:

$$
e^{-x^2} \cdot e^{-y^2} = e^{-(x^2+y^2)}.
$$

The right-hand side depends on $$(x, y)$$ only through $$x^2 + y^2$$, the squared distance from the origin. That's where the circle comes from.

## why it matters

First, the payoff for probability. To normalize $$e^{-(x-\mu)^2/(2\sigma^2)}$$, substitute $$t = (x-\mu)/(\sigma\sqrt{2})$$, so that $$dx = \sigma\sqrt{2}\, dt$$:

$$
\int_{-\infty}^{\infty} e^{-(x-\mu)^2/(2\sigma^2)}\, dx = \sigma\sqrt{2} \int_{-\infty}^{\infty} e^{-t^2}\, dt = \sigma\sqrt{2\pi}.
$$

Dividing by that gives the density of $$N(\mu, \sigma^2)$$:

$$
\frac{1}{\sigma\sqrt{2\pi}}\, e^{-(x-\mu)^2/(2\sigma^2)}.
$$

So the $$\sqrt{2\pi}$$ is just $$\sqrt{\pi}$$ from the Gaussian integral, plus a $$\sqrt{2}$$ that comes from the convention of writing $$2\sigma^2$$ in the exponent.

A bonus one-liner: substituting $$t = x^2$$ in the Gamma function gives

$$
\Gamma\left(\tfrac{1}{2}\right) = \int_0^\infty t^{-1/2} e^{-t}\, dt = 2\int_0^\infty e^{-x^2}\, dx = \sqrt{\pi}.
$$

That's why $$\sqrt{\pi}$$ keeps turning up in the volumes of high-dimensional balls, which are full of half-integer Gamma values.

## the proof, from above

Square the integral and write the square as a double integral:

$$
I^2 = \left(\int_{-\infty}^{\infty} e^{-x^2}\, dx\right)\left(\int_{-\infty}^{\infty} e^{-y^2}\, dy\right) = \iint_{\mathbb{R}^2} e^{-(x^2+y^2)}\, dx\, dy.
$$

Now $$I^2$$ is the volume under the surface $$z = e^{-(x^2+y^2)}$$, a bell curve spun around the $$z$$-axis. Look straight down on that surface. Since the height depends only on distance from the origin, the level sets are concentric circles. So instead of slicing the volume into the usual grid of squares, slice it into thin rings.

<div class="row justify-content-center mt-3">
  <div class="col-sm-10 mt-3 mt-md-0">
    {% include figure.liquid loading="eager" path="assets/img/blog/where-the-root-pi-comes-from/rings-top-down.svg" class="img-fluid rounded" zoomable=true %}
  </div>
</div>
<div class="caption">
  Looking down on the surface e^(−(x²+y²)), whose level sets are circles. A thin ring of radius r and width dr, cut and straightened out, is nearly a rectangle of length 2πr. On that ring the surface has height e^(−r²) all the way around.
</div>

Take the ring between radius $$r$$ and $$r + dr$$ (orange in the figure). Cut it at one point and straighten it out. What you get is almost a rectangle: its length is the circumference, $$2\pi r$$, and its width is $$dr$$, so its area is about $$2\pi r\, dr$$. Its exact area is $$\pi(r+dr)^2 - \pi r^2 = 2\pi r\, dr + \pi\, dr^2$$, and the second term vanishes in the limit. On the whole ring the surface sits at the same height, $$e^{-r^2}$$, up to an error that also goes away as $$dr \to 0$$. So the slab of volume above the ring is

$$
e^{-r^2} \cdot 2\pi r\, dr.
$$

Add up the rings from the center outward:

$$
I^2 = \int_0^\infty e^{-r^2}\, 2\pi r\, dr.
$$

That extra factor of $$r$$ is usually introduced as "the Jacobian of polar coordinates," and it's easy to treat as something you just have to remember. The figure shows what it really is: rings farther out are longer. A ring at radius 2 has twice as much ground under it as a ring at radius 1, so it gets twice the weight.

And that factor of $$r$$ is exactly what makes the integral solvable. $$e^{-r^2}$$ on its own has no elementary antiderivative, but $$2r\, e^{-r^2}$$ is the derivative of $$-e^{-r^2}$$. With $$u = r^2$$:

$$
I^2 = \pi \int_0^\infty e^{-u}\, du = \pi.
$$

<div class="row justify-content-center mt-3">
  <div class="col-sm-10 mt-3 mt-md-0">
    {% include figure.liquid loading="eager" path="assets/img/blog/where-the-root-pi-comes-from/radial-integrand.svg" class="img-fluid rounded" zoomable=true %}
  </div>
</div>
<div class="caption">
  How much volume each ring contributes, as a function of its radius: 2πr e^(−r²). The total shaded area is exactly π. The dashed curve is the height e^(−r²) alone. Near the center the rings are too short to contribute much; far out the surface is too low.
</div>

Since $$I \gt 0$$, we get $$I = \sqrt{\pi}$$. The $$\pi$$ is the circumference of a circle, $$2\pi r$$, carried through the calculation. The square root is there because we squared $$I$$ to bring the circle into view.

## the part that gets missed

Two things usually get skipped. The small one is the step $$I^2 = \iint e^{-(x^2+y^2)}\, dx\, dy$$, which uses Fubini's theorem on an infinite domain. It's fine here because the integrand is positive, and Tonelli's theorem lets you swap or merge integrals of nonnegative functions without any further conditions. Positivity is also why you can add up the plane in rings instead of squares and get the same total. The bigger one is that the trick isn't a lucky coincidence, and it doesn't work for other bumps. Try it on $$e^{-\vert x \vert}$$: the product $$e^{-\vert x \vert - \vert y \vert}$$ has diamond-shaped level sets, not circles, and the rings don't help. In fact the Gaussian is essentially the only function where it works. If $$f(x) f(y)$$ depends only on $$x^2 + y^2$$, then $$h(s) = \log f(\sqrt{s}) - \log f(0)$$ must satisfy Cauchy's equation $$h(s) + h(t) = h(s + t)$$ (for a positive $$f$$, which is the case for a density like this). Under a mild regularity assumption like continuity, that forces $$f(x) = C e^{-a x^2}$$. In probability terms, this is the Herschel–Maxwell theorem: if a random vector's coordinates are independent and its distribution is unchanged by rotations, those coordinates must be centered Gaussians with equal variance (as I understand it, that's essentially how Maxwell derived the distribution of molecular velocities). Read the other way, it's why a vector of i.i.d. standard normals looks the same from every direction in any dimension, which is the fact behind random projections and sampling uniformly on spheres. The circle in the bell curve isn't a trick. It's the defining property of the Gaussian.
