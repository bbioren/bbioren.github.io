---
layout: post
title: where the root pi comes from
date: 2026-06-11
description: where the pi in the normal distribution comes from
tags: visual-proofs calculus probability
categories: math
related_posts: false
thumbnail: /assets/img/blog/where-the-root-pi-comes-from/rings-top-down.svg
---

The integral of $$e^{-x^2}$$ over the whole real line comes out to exactly $$\sqrt{\pi}$$:

$$
I = \int_{-\infty}^{\infty} e^{-x^2}\, dx = \sqrt{\pi}.
$$

Why would there be a $$\pi$$ in there? The function is just a bump that dies off fast, and nothing about it looks like it has anything to do with circles. Before worrying about that, it's worth checking that the number is at least reasonable. The function $$e^{-x^2}$$ is never bigger than 1, and by $$x = 2$$ it's already under $$0.02$$. So the area should be a bit under 2, and $$\sqrt{\pi} \approx 1.772$$ fits.

This integral is also where the $$\frac{1}{\sqrt{2\pi}}$$ in front of the normal density comes from. If we set $$t = (x-\mu)/(\sigma\sqrt{2})$$, then $$dx = \sigma\sqrt{2}\, dt$$, and we have that

$$
\int_{-\infty}^{\infty} e^{-(x-\mu)^2/(2\sigma^2)}\, dx = \sigma\sqrt{2} \int_{-\infty}^{\infty} e^{-t^2}\, dt = \sigma\sqrt{2\pi}.
$$

So the $$\sqrt{2\pi}$$ in the normal distribution is really just the $$\sqrt{\pi}$$ from $$I$$. The extra $$\sqrt{2}$$ only shows up because people like to write the exponent with a $$2\sigma^2$$ in it. That means if we can figure out where the $$\sqrt{\pi}$$ in $$I$$ comes from, we've also figured it out for the normal distribution.

## Squaring the integral

The obvious first thing to try is finding an antiderivative of $$e^{-x^2}$$. Well, there isn't an elementary one, so that goes nowhere. What works instead looks like it should only make things worse. We multiply the integral by itself and write the product as a double integral:

$$
I^2 = \left(\int_{-\infty}^{\infty} e^{-x^2}\, dx\right)\left(\int_{-\infty}^{\infty} e^{-y^2}\, dy\right) = \iint_{\mathbb{R}^2} e^{-(x^2+y^2)}\, dx\, dy.
$$

Calling the variable $$y$$ in the second copy doesn't change its value, but it lets us treat the product as one integral over the plane.

Now $$I^2$$ is the volume under the surface $$z = e^{-(x^2+y^2)}$$, which is the bell curve spun around the $$z$$-axis. The height only depends on $$x^2 + y^2$$, the squared distance from the origin. So if you look down at the surface from above, its level sets are circles. The surface is round, so it makes more sense to chop the plane into thin rings than into the usual grid of little squares.

<div class="row justify-content-center mt-3">
  <div class="col-sm-10 mt-3 mt-md-0">
    {% include figure.liquid loading="eager" path="assets/img/blog/where-the-root-pi-comes-from/rings-top-down.svg" class="img-fluid rounded" zoomable=true %}
  </div>
</div>
<div class="caption">
  The surface e^(−(x²+y²)) seen from above. A thin ring of radius r, cut open and straightened, is nearly a rectangle of length 2πr, and the surface has height e^(−r²) all the way around it.
</div>

Take the ring between radius $$r$$ and $$r + dr$$ (the orange one in the picture). If you cut the ring at one point and straighten it out, you get something that's almost a rectangle. Its length is the circumference $$2\pi r$$ and its width is $$dr$$, so its area is about $$2\pi r\, dr$$. The surface has the same height $$e^{-r^2}$$ all the way around the ring. So the volume sitting above the ring is about

$$
e^{-r^2} \cdot 2\pi r\, dr.
$$

The ring isn't exactly a rectangle, and the height isn't exactly constant across it. Both of these errors are higher order in $$dr$$, so they go away in the limit. I'm not going to be more careful than that here. Adding up all the rings from the center outward, we get

$$
I^2 = \int_0^\infty e^{-r^2}\, 2\pi r\, dr.
$$

The factor of $$r$$ in there is what's usually called the Jacobian for polar coordinates. In a class it's often something you're just told to memorize. In the picture it says that rings farther out are longer. A ring at radius 2 has twice the area of a ring at radius 1, so it should count for twice as much volume.

That same factor of $$r$$ is also what lets us finish. We couldn't integrate $$e^{-r^2}$$ on its own, but $$2r\, e^{-r^2}$$ is the derivative of $$-e^{-r^2}$$. So if we pull the $$\pi$$ out front and substitute $$u = r^2$$, so that $$du = 2r\, dr$$, we have that

$$
I^2 = \pi \int_0^\infty e^{-u}\, du = \pi.
$$

<div class="row justify-content-center mt-3">
  <div class="col-sm-10 mt-3 mt-md-0">
    {% include figure.liquid loading="eager" path="assets/img/blog/where-the-root-pi-comes-from/radial-integrand.svg" class="img-fluid rounded" zoomable=true %}
  </div>
</div>
<div class="caption">
  How much volume each ring contributes, 2πr e^(−r²), as a function of r. The shaded area is π. The dashed curve is the height e^(−r²) on its own.
</div>

The plot above shows how much volume each ring contributes. Rings near the center are too short to hold much, and rings far out are too low, so most of the volume comes from somewhere in between. Since $$I$$ is positive, taking the square root gives $$I = \sqrt{\pi}$$.

So where did the $$\pi$$ come from? It's the same $$\pi$$ that's in the circumference $$2\pi r$$ of each ring. The square root is there because we had to square $$I$$ before any circles showed up.

## Why it only works for the Gaussian

You might wonder if the same trick works for other bumps, like $$e^{-\vert x \vert}$$. It doesn't, at least not with rings. The product $$e^{-\vert x \vert - \vert y \vert}$$ has level sets shaped like diamonds instead of circles, so cutting the plane into rings doesn't help at all.

In fact the Gaussian is pretty much the only function this works for. Suppose $$f$$ is positive and $$f(x) f(y)$$ only depends on $$x^2 + y^2$$. Set $$h(s) = \log f(\sqrt{s}) - \log f(0)$$. Then you can check that $$h(s) + h(t) = h(s + t)$$. With a mild assumption like continuity, this forces $$h$$ to be linear, which means $$f(x) = C e^{-a x^2}$$.

In probability language, this says the following. If a random vector has independent coordinates and its distribution looks the same in every direction, then the coordinates have to be centered Gaussians with the same variance. This is called the Herschel–Maxwell theorem.
