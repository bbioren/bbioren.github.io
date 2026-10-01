---
layout: post
title: which way does kl point?
date: 2026-07-08
description: fitting one gaussian to a two-bump distribution with forward and reverse kl gives two very different answers
tags: visual-proofs information-theory machine-learning
categories: math
related_posts: false
thumbnail: /assets/img/blog/which-way-kl/forward-vs-reverse-kl-fits.svg
---

Take a distribution with two bumps, one centered at $$-2$$ and one at $$2$$, and try to fit a single Gaussian to it. What does the best Gaussian look like? Well, it depends on which way you point the KL divergence. If the target goes in the first slot, you get a wide Gaussian that sits over both bumps and the gap between them. If the Gaussian goes in the first slot, you get a narrow one that sits on just one bump. Maximum likelihood uses one direction and variational inference uses the other. So it's worth working out why the two fits differ.

For distributions $$p$$ and $$q$$ the KL divergence is

$$
\mathrm{KL}(p \Vert q) = \mathbb{E}_{x \sim p}\left[\log \frac{p(x)}{q(x)}\right] \ge 0,
$$

with equality only when $$p = q$$. Notice that the expectation is taken under the _first_ argument. So you only pay for the places where $$p$$ puts mass. Wherever $$p(x) = 0$$ the integrand gets multiplied by zero, and $$q$$ can do whatever it wants there. Swapping the arguments swaps whose support counts.

## Where each direction comes from

Say you have data $$x_1, \dots, x_n$$ from $$p_{\text{data}}$$ and a model $$q_\theta$$. The average log-likelihood is an estimate of an expectation under the data. If we add and subtract $$\log p_{\text{data}}(x)$$ inside that expectation, it splits up like this:

$$
\begin{aligned}
\frac{1}{n}\sum_{i=1}^n \log q_\theta(x_i) \;\approx\; \mathbb{E}_{p_{\text{data}}}[\log q_\theta(x)]
&= \mathbb{E}_{p_{\text{data}}}[\log p_{\text{data}}(x)] - \mathbb{E}_{p_{\text{data}}}\left[\log \frac{p_{\text{data}}(x)}{q_\theta(x)}\right] \\
&= -H(p_{\text{data}}) - \mathrm{KL}(p_{\text{data}} \Vert q_\theta).
\end{aligned}
$$

The entropy term doesn't depend on $$\theta$$. So maximizing likelihood is the same thing as minimizing $$\mathrm{KL}(p_{\text{data}} \Vert q_\theta)$$. This direction is called forward KL, and the data goes in the first slot.

Variational inference goes the other way. You have a posterior $$p(z \mid x)$$ that you can't compute, so you pick some tractable $$q(z)$$ to approximate it. Write $$\log p(x,z) = \log p(z \mid x) + \log p(x)$$ and take the expectation over $$q$$. Since $$\log p(x)$$ doesn't depend on $$z$$, we have that

$$
\log p(x) = \underbrace{\mathbb{E}_{q}\left[\log \frac{p(x,z)}{q(z)}\right]}_{\text{ELBO}} + \mathrm{KL}\big(q(z) \Vert p(z \mid x)\big).
$$

The left side is a fixed number. So pushing the ELBO up is the same as pushing $$\mathrm{KL}(q \Vert p)$$ down. This is reverse KL, with the approximation in the first slot. Why this direction and not the other one? Because the expectation has to be under something you can sample from, and that's $$q$$. So fitting a model and approximating a posterior end up minimizing the same quantity, just with the arguments flipped.

## Fitting the two bumps

The target is

$$
p = \tfrac12 \mathcal{N}(-2, 0.6^2) + \tfrac12 \mathcal{N}(2, 0.6^2),
$$

and $$q = \mathcal{N}(\mu, \sigma^2)$$ gets fit to it once in each direction.

<div class="row justify-content-center mt-3">
  <div class="col-sm-10 mt-3 mt-md-0">
    {% include figure.liquid loading="eager" path="assets/img/blog/which-way-kl/forward-vs-reverse-kl-fits.svg" class="img-fluid rounded" zoomable=true %}
  </div>
</div>
<div class="caption">
  The two-bump target (black) with the best single Gaussian in each direction. The forward KL fit is blue and the reverse KL fit is orange and dashed.
</div>

Start with the forward direction, $$\mathrm{KL}(p \Vert q)$$. The integrand is $$p \log(p/q)$$. What happens if $$q$$ is very small on one of the black bumps? Then $$\log(p/q)$$ blows up, and it gets weighted by $$p$$, which is not small on the bumps. So the cost is large, and $$q$$ can't get close to zero anywhere that $$p$$ has mass. Putting mass in the empty valley around $$x = 0$$ costs nothing, though, because $$p \approx 0$$ there. This is usually called mass-covering, and it's what the blue curve does. It stretches out over both modes and spills into the gap in the middle.

When $$q$$ is Gaussian this case can be solved by hand. Plugging in $$\log q(x) = -\log \sigma - (x - \mu)^2 / (2\sigma^2) + \text{const}$$, we have that, up to a constant,

$$
\mathrm{KL}(p \Vert q) = \log \sigma + \frac{\mathbb{E}_p[(x - \mu)^2]}{2\sigma^2}.
$$

The numerator splits as $$\mathbb{E}_p[(x - \mu)^2] = \mathrm{Var}_p(x) + (\mathbb{E}_p[x] - \mu)^2$$, so the best $$\mu$$ is $$\mathbb{E}_p[x]$$. Then setting the derivative in $$\sigma$$ to zero gives $$1/\sigma = \mathrm{Var}_p(x)/\sigma^3$$, or $$\sigma^2 = \mathrm{Var}_p(x)$$. So forward KL with a Gaussian $$q$$ is just matching the first two moments. For this target the mean is $$0$$ and the variance is $$0.6^2 + 2^2 = 4.36$$. That gives $$\sigma \approx 2.09$$.

The reverse direction, $$\mathrm{KL}(q \Vert p)$$, has integrand $$q \log(q/p)$$, and now the expensive places are different. Anywhere that $$q \gt 0$$ but $$p \approx 0$$ costs a lot, so the valley is now the worst place to put mass. Missing a mode completely is free, because over there the integrand is weighted by $$q \approx 0$$. A Gaussian only has one bump of its own, so the cheapest thing it can do is sit inside one mode of $$p$$. There's no nice closed form this time, but minimizing numerically gives $$\mu \approx 2$$ and $$\sigma \approx 0.6$$, which is the orange curve. The mirror image at $$-2$$ does exactly as well, so which mode you land on depends on where the optimizer starts.

The KL values agree with the picture. The blue fit has forward KL of about $$0.555$$ and reverse KL of about $$1.27$$. The orange fit has reverse KL of about $$0.692$$. That's basically $$\log 2$$, since on its mode $$p \approx q/2$$ and so $$q \log(q/p) \approx q \log 2$$. Its forward KL is around $$10.4$$, because it gives almost no probability to half of the data.

## Variational posteriors come out too narrow

So which fit is the right one? Neither, really. Forward KL wants a $$q$$ that never misses anything $$p$$ could produce, which is what you'd want out of a density model. Reverse KL wants a $$q$$ that never produces anything $$p$$ wouldn't, which is closer to what you'd want from a sampler.

One consequence is that reverse KL tends to underestimate uncertainty, even with only one mode. Take a correlated Gaussian posterior with precision matrix $$\Lambda$$ and fit a mean-field $$q$$ to it, meaning $$q$$ is fully factorized across the coordinates. The means come out exactly right. Each variance comes out as $$1/\Lambda_{ii}$$, which is the conditional variance of that coordinate given all the others. That is never bigger than the true marginal variance $$(\Lambda^{-1})_{ii}$$, and usually it's smaller.
