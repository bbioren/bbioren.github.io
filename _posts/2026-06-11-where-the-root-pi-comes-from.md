---
layout: post
title: where the root pi comes from
date: 2026-06-11
description: why there's a pi in the normal distribution, and the circle you can see from above
tags: visual-proofs calculus probability
categories: math
related_posts: false
---

If you've taken a stats class, you've seen the normal density, and you've probably wondered at some point about the constant out front, $$\frac{1}{\sqrt{2\pi}}$$. The $$e^{-x^2/2}$$ part is reasonable enough, it's a bump that dies off fast. But why $$\pi$$? Nothing about a bell curve looks like it has anything to do with circles. The usual explanation is that the constant makes the area come out to 1, which is true, but it doesn't tell you why that number in particular has a $$\pi$$ in it.

Everything comes down to one integral:

$$
I = \int_{-\infty}^{\infty} e^{-x^2}\, dx = \sqrt{\pi}.
$$

Before proving it, is that even a believable number? $$e^{-x^2}$$ is at most 1, and by $$x = 2$$ it's already under $$0.02$$, so the area should be somewhere a bit under 2. And $$\sqrt{\pi} \approx 1.772$$, so that seems about right.

Once you know this, the normal density follows from a substitution. Setting $$t = (x-\mu)/(\sigma\sqrt{2})$$, so $$dx = \sigma\sqrt{2}\, dt$$, gives

$$
\int_{-\infty}^{\infty} e^{-(x-\mu)^2/(2\sigma^2)}\, dx = \sigma\sqrt{2} \int_{-\infty}^{\infty} e^{-t^2}\, dt = \sigma\sqrt{2\pi}.
$$

So the $$\sqrt{2\pi}$$ is the $$\sqrt{\pi}$$ from $$I$$, along with a $$\sqrt{2}$$ that's only there because we like writing $$2\sigma^2$$ in the exponent. The question is where the $$\sqrt{\pi}$$ comes from.

## Going up a dimension

The first thing you'd try is finding an antiderivative of $$e^{-x^2}$$, and that doesn't work, because there isn't an elementary one. So instead we do something that seems like it should make things worse, which is to square the integral and write it as a double integral:

$$
I^2 = \left(\int_{-\infty}^{\infty} e^{-x^2}\, dx\right)\left(\int_{-\infty}^{\infty} e^{-y^2}\, dy\right) = \iint_{\mathbb{R}^2} e^{-(x^2+y^2)}\, dx\, dy.
$$

Now $$I^2$$ is the volume under the surface $$z = e^{-(x^2+y^2)}$$, which is a bell curve spun around the $$z$$-axis. The height only depends on $$x^2 + y^2$$, the squared distance from the origin, so if you look straight down at it, the level sets are circles. That's where the circle is. And since the surface is round, it makes more sense to chop the plane into thin rings than into the usual grid of little squares.

<div class="row justify-content-center mt-3">
  <div class="col-sm-10 mt-3 mt-md-0">
    {% include figure.liquid loading="eager" path="assets/img/blog/where-the-root-pi-comes-from/rings-top-down.svg" class="img-fluid rounded" zoomable=true %}
  </div>
</div>
<div class="caption">
  The surface e^(−(x²+y²)) seen from above. A thin ring of radius r, cut open and straightened, is nearly a rectangle of length 2πr, and the surface has height e^(−r²) all the way around it.
</div>

Take the ring between radius $$r$$ and $$r + dr$$, the orange one in the picture. If you cut it at one point and straighten it out, you get something that's almost a rectangle, with length $$2\pi r$$ (the circumference) and width $$dr$$. So its area is about $$2\pi r\, dr$$, and the surface sits at height $$e^{-r^2}$$ over the whole ring, which means the volume above it is

$$
e^{-r^2} \cdot 2\pi r\, dr.
$$

(The ring isn't exactly a rectangle and the height isn't exactly constant across it, but those errors are higher order in $$dr$$ and go away in the limit.) Adding up all the rings from the center out,

$$
I^2 = \int_0^\infty e^{-r^2}\, 2\pi r\, dr.
$$

That factor of $$r$$ is what you'd normally call the Jacobian for polar coordinates, and I think it's usually presented as something to memorize. The picture makes it obvious, though. Rings farther out are longer, so a ring at radius 2 has twice as much area as one at radius 1 and should count twice as much.

It's also exactly what saves us. We couldn't integrate $$e^{-r^2}$$ by itself, but $$2r\, e^{-r^2}$$ is the derivative of $$-e^{-r^2}$$. With $$u = r^2$$,

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

The plot above shows the tradeoff. Rings near the center are too short to hold much volume, and rings far out are too low, so most of it comes from somewhere in between. Anyway, $$I$$ is positive, so $$I = \sqrt{\pi}$$. The $$\pi$$ is the $$\pi$$ from the circumference $$2\pi r$$, and the square root is there because we had to square $$I$$ to get a circle to show up at all.

## Why only the Gaussian

You might wonder if this works for other bumps. Try $$e^{-\vert x \vert}$$. The product $$e^{-\vert x \vert - \vert y \vert}$$ has level sets shaped like diamonds, not circles, so slicing into rings doesn't buy you anything.

In fact the Gaussian is basically the only function where the trick works. Suppose $$f$$ is positive and $$f(x) f(y)$$ only depends on $$x^2 + y^2$$. If you set $$h(s) = \log f(\sqrt{s}) - \log f(0)$$, you can check that $$h(s) + h(t) = h(s + t)$$, and with a mild assumption like continuity that forces $$h$$ to be linear, so $$f(x) = C e^{-a x^2}$$. In probability language, if a random vector has independent coordinates and its distribution looks the same in every direction, the coordinates have to be centered Gaussians with the same variance (this is called the Herschel–Maxwell theorem). So the circle we used to compute the integral was always going to be there, and you'd get the same kind of rings if you tried this with independent Gaussians in three or more dimensions.
