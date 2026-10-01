---
layout: post
title: which way does kl point?
date: 2026-07-08
description: forward and reverse kl fit the same bimodal target in very different ways, and ml uses both
tags: visual-proofs information-theory machine-learning
categories: math
related_posts: false
---

KL divergence usually gets introduced as a distance between distributions, and then the next sentence says it isn't really one because it isn't symmetric. Then everyone moves on. I think that asymmetry deserves more attention than it gets, because which way you write it changes what your fitted model looks like, and the two most common objectives in machine learning use opposite directions.

Here's the definition. For distributions $$p$$ and $$q$$,

$$
\mathrm{KL}(p \Vert q) = \mathbb{E}_{x \sim p}\left[\log \frac{p(x)}{q(x)}\right] \ge 0,
$$

with equality only when $$p = q$$. The thing to remember is that the expectation is under the _first_ argument. You only pay where $$p$$ puts mass. Wherever $$p(x) = 0$$ the integrand gets weighted by zero, and $$q$$ can do whatever it wants there. So if you swap the arguments, you swap whose support counts.

## Two directions in the wild

Say you have data $$x_1, \dots, x_n$$ from $$p_{\text{data}}$$ and a model $$q_\theta$$. The average log-likelihood estimates an expectation under the data, and you can split it up like this:

$$
\begin{aligned}
\frac{1}{n}\sum_{i=1}^n \log q_\theta(x_i) \;\approx\; \mathbb{E}_{p_{\text{data}}}[\log q_\theta(x)]
&= \mathbb{E}_{p_{\text{data}}}[\log p_{\text{data}}(x)] - \mathbb{E}_{p_{\text{data}}}\left[\log \frac{p_{\text{data}}(x)}{q_\theta(x)}\right] \\
&= -H(p_{\text{data}}) - \mathrm{KL}(p_{\text{data}} \Vert q_\theta).
\end{aligned}
$$

The entropy term doesn't depend on $$\theta$$, so maximum likelihood is the same as minimizing $$\mathrm{KL}(p_{\text{data}} \Vert q_\theta)$$. That's forward KL, with the data in the first slot.

Now think about variational inference. You want a posterior $$p(z \mid x)$$ that you can't compute, so you pick some tractable $$q(z)$$ to approximate it. If you expand $$\log p(x,z) = \log p(z \mid x) + \log p(x)$$ inside an expectation over $$q$$, you get

$$
\log p(x) = \underbrace{\mathbb{E}_{q}\left[\log \frac{p(x,z)}{q(z)}\right]}_{\text{ELBO}} + \mathrm{KL}\big(q(z) \Vert p(z \mid x)\big).
$$

The left side is a fixed number, so pushing the ELBO up pushes $$\mathrm{KL}(q \Vert p)$$ down. This is reverse KL, with the approximation first. And it pretty much has to go this way, since the expectation needs to be under $$q$$, which is the only thing you can sample from. So fitting a model and approximating a posterior minimize the same quantity with the arguments flipped. Does that matter?

## One target, two fits

Let's try it. Take a bimodal target

$$
p = \tfrac12 \mathcal{N}(-2, 0.6^2) + \tfrac12 \mathcal{N}(2, 0.6^2),
$$

and fit a single Gaussian $$q = \mathcal{N}(\mu, \sigma^2)$$ to it, once in each direction.

<div class="row justify-content-center mt-3">
  <div class="col-sm-10 mt-3 mt-md-0">
    {% include figure.liquid loading="eager" path="assets/img/blog/which-way-kl/forward-vs-reverse-kl-fits.svg" class="img-fluid rounded" zoomable=true %}
  </div>
</div>
<div class="caption">
  The bimodal target (black) and the best single Gaussian in each direction. Forward KL is blue, reverse KL is orange and dashed.
</div>

Start with forward, $$\mathrm{KL}(p \Vert q)$$, where the integrand is $$p \log(p/q)$$. If $$q$$ were tiny on either black bump, $$\log(p/q)$$ would blow up, and it's being weighted by $$p$$, which isn't small there. So $$q$$ can't go near zero anywhere $$p$$ has mass. Putting mass in the empty valley around $$x = 0$$ is free, though, because $$p \approx 0$$ there. People call this mass-covering, and you can see it in the blue curve, which stretches over both modes and spills into the gap.

For Gaussian $$q$$ you can actually solve this. Up to a constant,

$$
\mathrm{KL}(p \Vert q) = \log \sigma + \frac{\mathbb{E}_p[(x - \mu)^2]}{2\sigma^2},
$$

which is minimized at $$\mu = \mathbb{E}_p[x]$$ and $$\sigma^2 = \mathrm{Var}_p(x)$$, so it's just moment matching. Here the mean is $$0$$ and the variance is $$0.6^2 + 2^2 = 4.36$$, giving $$\sigma \approx 2.09$$.

Reverse, $$\mathrm{KL}(q \Vert p)$$, has integrand $$q \log(q/p)$$, and now the danger is somewhere else. Anywhere $$q \gt 0$$ but $$p \approx 0$$ costs you a lot, so the valley becomes the worst place to put mass. Meanwhile missing a mode entirely costs nothing, since the integrand is weighted by $$q \approx 0$$ there. With only one bump to work with, the cheapest option is to sit inside a single mode. Minimizing numerically gives $$\mu \approx 2$$ and $$\sigma \approx 0.6$$, which is the orange curve. The mirror image at $$-2$$ is just as good, so which mode you land on depends on where you start.

The numbers match the picture. The blue fit has forward KL about $$0.555$$ and reverse KL about $$1.27$$. The orange fit has reverse KL about $$0.692$$, which is basically $$\log 2$$ (on its mode, $$p \approx q/2$$), but its forward KL is around $$10.4$$ because it gives almost no probability to half the data.

## Overconfident posteriors

Neither fit is wrong. Forward KL wants a $$q$$ that never misses anything $$p$$ could produce, which is what you'd want from a density model. Reverse KL wants a $$q$$ that never produces anything $$p$$ wouldn't, which is closer to what you'd want from a sampler.

The thing I'd keep in mind is that reverse KL tends to underestimate uncertainty, and you don't need multiple modes for that to happen. Take a correlated Gaussian posterior with precision matrix $$\Lambda$$ and fit a mean-field (fully factorized) $$q$$. The means come out exactly right, but each variance comes out as $$1/\Lambda_{ii}$$, the conditional variance, and that's never bigger than the true marginal variance $$(\Lambda^{-1})_{ii}$$ and is usually smaller. So variational posteriors tend to look tighter than they should, and if one looks surprisingly confident, remember which direction the KL went.
