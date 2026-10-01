---
layout: post
title: which way does kl point?
date: 2026-07-08
description: forward kl covers every mode, reverse kl picks one, and the two most common objectives in machine learning point in opposite directions
tags: visual-proofs information-theory machine-learning
categories: math
related_posts: false
---

KL divergence is usually introduced as "a distance between distributions," and the very next sentence says it isn't one, because it isn't symmetric. Then the course moves on. But the asymmetry is the whole story: swapping the arguments changes what a fitted model looks like, and the two most common objectives in machine learning sit on opposite sides of that swap.

## The statement

For distributions $$p$$ and $$q$$ on the same space,

$$
\mathrm{KL}(p \Vert q) = \mathbb{E}_{x \sim p}\left[\log \frac{p(x)}{q(x)}\right] \ge 0,
$$

with equality iff $$p = q$$. This is Gibbs' inequality, and it takes one line of Jensen (log is concave):

$$
-\mathrm{KL}(p \Vert q) = \mathbb{E}_{p}\left[\log \frac{q}{p}\right] \le \log \mathbb{E}_{p}\left[\frac{q}{p}\right] = \log \int_{p \gt 0} q \, dx \le \log 1 = 0.
$$

The heuristic to keep in mind is that the expectation is taken under the _first_ argument. You only pay where the first distribution puts mass. Wherever $$p(x) = 0$$, the integrand is weighted by zero and $$q$$ can do whatever it likes there. Swap the arguments and you swap whose support counts.

## Why it matters

Take data $$x_1, \dots, x_n$$ drawn from $$p_{\text{data}}$$ and a model $$q_\theta$$. The average log-likelihood is a Monte Carlo estimate of an expectation under the data:

$$
\begin{aligned}
\frac{1}{n}\sum_{i=1}^n \log q_\theta(x_i) \;\approx\; \mathbb{E}_{p_{\text{data}}}[\log q_\theta(x)]
&= \mathbb{E}_{p_{\text{data}}}[\log p_{\text{data}}(x)] - \mathbb{E}_{p_{\text{data}}}\left[\log \frac{p_{\text{data}}(x)}{q_\theta(x)}\right] \\
&= -H(p_{\text{data}}) - \mathrm{KL}(p_{\text{data}} \Vert q_\theta).
\end{aligned}
$$

The entropy doesn't depend on $$\theta$$, so maximum likelihood (equivalently, minimizing cross-entropy) is minimizing $$\mathrm{KL}(p_{\text{data}} \Vert q_\theta)$$. That's the **forward** KL, with the data first.

Now variational inference. We want the posterior $$p(z \mid x)$$, can't compute it, and pick an approximation $$q(z)$$ from a tractable family. Expanding $$\log p(x,z) = \log p(z \mid x) + \log p(x)$$ inside an expectation over $$q$$ gives

$$
\log p(x) = \underbrace{\mathbb{E}_{q}\left[\log \frac{p(x,z)}{q(z)}\right]}_{\text{ELBO}} + \mathrm{KL}\big(q(z) \Vert p(z \mid x)\big).
$$

The left side is fixed, so maximizing the ELBO is minimizing $$\mathrm{KL}(q \Vert p)$$, the **reverse** KL with the approximation first. It has to be this way round: the expectation must be under $$q$$, because $$q$$ is the only thing we can sample from. So the most common way to fit a model and the most common way to approximate a posterior minimize the same quantity with the arguments switched.

## The picture

Here is what the switch does. The target is a bimodal mixture

$$
p = \tfrac12 \mathcal{N}(-2, 0.6^2) + \tfrac12 \mathcal{N}(2, 0.6^2),
$$

and we fit a single Gaussian $$q = \mathcal{N}(\mu, \sigma^2)$$ to it, once in each direction.

<div class="row justify-content-center mt-3">
  <div class="col-sm-10 mt-3 mt-md-0">
    {% include figure.liquid loading="eager" path="assets/img/blog/which-way-kl/forward-vs-reverse-kl-fits.svg" class="img-fluid rounded" zoomable=true %}
  </div>
</div>
<div class="caption">
  The bimodal target (black, shaded) with the best single Gaussian under each direction of KL. Forward KL (blue) covers both modes and puts mass in the empty valley; reverse KL (orange, dashed) sits on one mode and ignores the other. All curves are exact densities.
</div>

**Forward, $$\mathrm{KL}(p \Vert q)$$.** The integrand is $$p \log(p/q)$$. Look at either black bump: if $$q$$ were tiny there, $$\log(p/q)$$ would be huge, and it gets weighted by $$p$$, which is not tiny. So $$q$$ can't afford to be near zero anywhere $$p$$ has mass. This is the zero-avoiding (or mass-covering) behavior. Putting mass in the valley at $$x = 0$$ costs nothing, because there the integrand is weighted by $$p \approx 0$$. So the blue curve spreads out to cover both modes and spills into the gap.

For a Gaussian $$q$$ the optimum can be written down exactly. Up to a constant,

$$
\mathrm{KL}(p \Vert q) = \log \sigma + \frac{\mathbb{E}_p[(x - \mu)^2]}{2\sigma^2},
$$

which is minimized at $$\mu = \mathbb{E}_p[x]$$ and $$\sigma^2 = \mathrm{Var}_p(x)$$. That's just moment matching. Here $$\mathbb{E}_p[x] = 0$$ and $$\mathrm{Var}_p(x) = 0.6^2 + 2^2 = 4.36$$ (within-component variance plus the spread of the means), so the blue curve is $$\mathcal{N}(0, 4.36)$$ with $$\sigma \approx 2.088$$. More generally, when $$q$$ ranges over an exponential family, the forward-KL fit matches the expected sufficient statistics.

**Reverse, $$\mathrm{KL}(q \Vert p)$$.** Now the integrand is $$q \log(q/p)$$, weighted by $$q$$. The danger has moved: wherever $$q \gt 0$$ but $$p \approx 0$$, you pay $$\log(q/p) \to \infty$$. The valley is now the expensive place to be, and the blue curve would be heavily penalized for its mass there. Missing a mode costs nothing, because there the integrand is weighted by $$q \approx 0$$. This is the zero-forcing (or mode-seeking) behavior: $$q$$ goes to zero wherever $$p$$ does, and the cheapest way to do that with one bump is to hide inside a single mode. Minimizing numerically gives $$\mu \approx 2$$, $$\sigma \approx 0.6$$, which is the orange curve. By symmetry $$\mathcal{N}(-2, 0.6^2)$$ is an equally good optimum, so reverse KL isn't even convex here and the mode you get depends on initialization.

The numbers back up the picture. The blue fit has $$\mathrm{KL}(p \Vert q) \approx 0.555$$ but $$\mathrm{KL}(q \Vert p) \approx 1.27$$. The orange fit has $$\mathrm{KL}(q \Vert p) \approx 0.692$$, almost exactly $$\log 2$$, since on its mode $$p \approx q/2$$. But its forward KL is about $$10.4$$, because it assigns almost no probability to half the data.

## The part that gets missed

Neither fit is the "right" answer. Each one answers a different question. Forward KL asks for a $$q$$ that never misses anything $$p$$ can produce, which is what you want from a density model of data. Reverse KL asks for a $$q$$ that never produces anything $$p$$ wouldn't, which is what you want from a sampler you plan to trust. Choosing a direction is a modeling decision, not a technicality. And it has a predictable cost that the usual presentation of variational inference glosses over: reverse KL **underestimates uncertainty**. That isn't specific to multimodal targets. Even for a correlated Gaussian posterior with precision matrix $$\Lambda$$, the mean-field reverse-KL fit gets the means exactly right but sets each variance to $$1/\Lambda_{ii}$$, the conditional variance, which is never larger (and usually strictly smaller) than the true marginal variance $$(\Lambda^{-1})_{ii}$$. So VI posteriors come out overconfident by construction. When a variational posterior looks reassuringly tight, the first thing to remember is which way the KL pointed.
