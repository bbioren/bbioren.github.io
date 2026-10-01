---
layout: post
title: markov, chebyshev, chernoff
date: 2026-09-26
description: three tail bounds, one trick, and how much each extra assumption buys you
tags: visual-proofs probability concentration
categories: math
thumbnail: /assets/img/blog/concentration-inequalities/tail-bounds-coin-flips.svg
related_posts: false
---

Flip 100 fair coins. How likely is it that you get 80 or more heads? You can just compute this one, since the number of heads is binomial, and the answer is about $$5.6 \times 10^{-10}$$. So it basically never happens.

Most of the time you can't compute the exact answer, though. You might only know the mean of some random quantity, or the mean and the variance, and you still want to say that it's unlikely to land far from the mean. That's what concentration inequalities do. They give an upper bound on a tail probability using only a little information about the distribution. The more you assume, the better the bound, and the coin example is a nice way to see how much better.

## Markov

The first one only needs the mean. If $$X \ge 0$$ and $$a \gt 0$$, then

$$
P(X \ge a) \le \frac{\mathbb{E}[X]}{a}.
$$

My favorite proof of this is a picture. Draw the function that is $$1$$ when $$x \ge a$$ and $$0$$ otherwise, and draw the line $$x/a$$ on top of it.

<div class="row justify-content-center mt-3">
  <div class="col-sm-10 mt-3 mt-md-0">
    {% include figure.liquid loading="eager" path="assets/img/blog/concentration-inequalities/step-under-line.svg" class="img-fluid rounded" zoomable=true %}
  </div>
</div>
<div class="caption">
  The step 1{x ≥ a} never goes above the line x/a, as long as x isn't negative.
</div>

For $$x$$ between $$0$$ and $$a$$ the step is $$0$$ and the line is positive. At $$x = a$$ they meet at $$1$$, and after that the line keeps going up while the step stays flat. So for every $$x \ge 0$$ we have that $$\mathbf{1}\{x \ge a\} \le x/a$$. Plug in $$X$$ and take the expectation of both sides. The expectation of an indicator is the probability of the event, so the left side is $$P(X \ge a)$$, and the right side is $$\mathbb{E}[X]/a$$, which is Markov's inequality.

The picture also shows why $$X$$ has to be nonnegative. For negative $$x$$ the line goes below zero and the inequality between the step and the line breaks.

For the coins, the number of heads has mean $$50$$, so Markov says $$P(X \ge 80) \le 50/80 = 0.625$$. That's true and not very useful. It's what you'd expect from a bound that only knows the mean.

## Chebyshev

Now say we also know the variance $$\sigma^2$$. The trick is to apply Markov to a different random variable. $$(X - \mu)^2$$ is nonnegative and its mean is $$\sigma^2$$, so

$$
P(\vert X - \mu \vert \ge t) = P\big((X - \mu)^2 \ge t^2\big) \le \frac{\sigma^2}{t^2}.
$$

For the coins, $$\sigma^2 = 100 \cdot \tfrac{1}{2} \cdot \tfrac{1}{2} = 25$$, and 80 heads is $$t = 30$$ above the mean. So Chebyshev gives $$25/900 \approx 0.028$$. That's about 20 times better than Markov, from knowing one more number.

## Chernoff

Why stop at squaring? Markov works on any nonnegative function of $$X$$, and the faster the function grows, the more it punishes large values. The fastest natural choice is an exponential. For any $$\lambda \gt 0$$,

$$
P(X \ge a) = P\big(e^{\lambda X} \ge e^{\lambda a}\big) \le e^{-\lambda a}\, \mathbb{E}\big[e^{\lambda X}\big],
$$

and then you pick the $$\lambda$$ that makes the right side smallest. This is where independence comes in. If $$X$$ is a sum of independent pieces, then $$\mathbb{E}[e^{\lambda X}]$$ factors into a product, one term per piece, which is what makes it possible to compute. Doing this carefully for a sum of $$n$$ independent variables that each lie in $$[0, 1]$$ gives Hoeffding's inequality,

$$
P(X - \mu \ge t) \le e^{-2t^2/n}.
$$

For the coins that's $$e^{-2 \cdot 900/100} = e^{-18} \approx 1.5 \times 10^{-8}$$. Compared to Chebyshev, that's six orders of magnitude better.

## Putting them side by side

Here are all three bounds next to the exact answer, for every threshold from 52 heads up to 90. The vertical axis is on a log scale, or else Chernoff and the exact answer would both look like zero past about 65 heads.

<div class="row justify-content-center mt-3">
  <div class="col-sm-10 mt-3 mt-md-0">
    {% include figure.liquid loading="eager" path="assets/img/blog/concentration-inequalities/tail-bounds-coin-flips.svg" class="img-fluid rounded" zoomable=true %}
  </div>
</div>
<div class="caption">
  The probability of at least k heads in 100 flips, and the three bounds on it. Each extra assumption bends the bound down a lot more.
</div>

Markov barely moves. Chebyshev falls off like $$1/t^2$$, which looks almost flat on a log scale. Chernoff falls off like $$e^{-t^2}$$, the same shape as the true tail, and it stays within a few orders of magnitude of the exact answer the whole way. That shape is really what "concentration" means. A sum of $$n$$ independent bounded things almost always lands within a few multiples of $$\sqrt{n}$$ of its mean, and the chance of landing farther out shrinks exponentially.

This is also why Hoeffding shows up all over machine learning. Say you want to know a classifier's accuracy to within one percentage point, with 95% confidence. Each test example is an independent 0/1 outcome, so applying Hoeffding to both tails gives $$P(\vert \hat{p} - p \vert \ge \epsilon) \le 2e^{-2n\epsilon^2}$$. Setting that equal to $$0.05$$ with $$\epsilon = 0.01$$ and solving, we have that

$$
n \ge \frac{\ln(2/0.05)}{2 \cdot 0.01^2} \approx 18{,}445
$$

test examples are enough, no matter what the classifier is or what the data looks like. Chebyshev would get you a guarantee too, but you'd need about 50,000 examples for the same one.
