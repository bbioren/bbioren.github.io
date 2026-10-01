---
layout: post
title: linearity of expectation needs nothing
date: 2026-08-05
description: you don't need independence to add expectations, and here's a table that shows why
tags: visual-proofs probability combinatorics
categories: math
related_posts: false
---

Whenever a problem asks for the expected value of a sum, there's a reflex to stop and check whether the pieces are independent. For expectations, you can skip that check. Linearity of expectation says

$$
\mathbb{E}[X + Y] = \mathbb{E}[X] + \mathbb{E}[Y]
$$

for any two random variables with finite means, and that's the whole hypothesis. $$X$$ and $$Y$$ can be independent, or strongly correlated, or $$Y$$ can just be some function of $$X$$. It doesn't matter.

I think this gets undersold in intro classes. It's usually stated once, next to the definition of expectation, and then everybody moves on to independence and variance, which are where the "real" content supposedly is. But linearity is the thing that solves problems.

## Hats

Here's the standard example. $$n$$ people check their hats at a party, and at the end of the night the hats get handed back in a completely random order. On average, how many people get their own hat back?

If you try to do this by finding the distribution of the number of matches, you end up doing inclusion–exclusion and it gets ugly fast. Instead, let $$\mathbf{1}_i$$ be $$1$$ if person $$i$$ gets their own hat and $$0$$ otherwise. The number of matches is $$X = \mathbf{1}_1 + \dots + \mathbf{1}_n$$. Person $$i$$ is equally likely to get any of the $$n$$ hats, so $$\mathbb{E}[\mathbf{1}_i] = 1/n$$, and

$$
\mathbb{E}[X] = n \cdot \frac{1}{n} = 1.
$$

So it's one, no matter how many people are at the party. That's kind of a strange answer, and the indicators here are definitely not independent (if everyone but one person has their own hat, the last person has to have theirs too). We just never needed them to be.

## Why it works

The proof is easiest to see if you write out every possible outcome. Take $$n = 3$$. There are $$6$$ ways to hand back three hats, each with probability $$1/6$$. Make a table with one row per outcome and one column per person, and put a $$1$$ wherever that person got their own hat.

<div class="row justify-content-center mt-3">
  <div class="col-sm-10 mt-3 mt-md-0">
    {% include figure.liquid loading="eager" path="assets/img/blog/linearity-of-expectation-needs-nothing/hat-check-grid.svg" class="img-fluid rounded" zoomable=true %}
  </div>
</div>
<div class="caption">
  Every way to return three hats. Adding across a row gives the number of matches for that outcome; adding down a column counts how often each person gets lucky.
</div>

Now there are two ways to add up all the $$1$$s in the table. If you go row by row, you get the number of matches in each outcome ($$3, 1, 1, 1, 0, 0$$), and averaging those gives $$\mathbb{E}[X] = 6/6 = 1$$. If you go column by column, each person gets their hat back in $$2$$ of the $$6$$ outcomes, so you get $$\mathbb{E}[\mathbf{1}_1] + \mathbb{E}[\mathbf{1}_2] + \mathbb{E}[\mathbf{1}_3] = 2/6 + 2/6 + 2/6 = 1$$.

Of course these agree, since it's the same six $$1$$s either way. That's really all linearity of expectation is: a double sum where you're allowed to swap the order.

$$
\sum_\omega P(\omega) \sum_i \mathbf{1}_i(\omega) = \sum_i \sum_\omega P(\omega)\, \mathbf{1}_i(\omega)
$$

You can actually see the dependence in the table if you look for it. No row has exactly two $$1$$s, because if two people have their own hats then so does the third. So the dependence changes how the $$1$$s are arranged across rows. But the total count doesn't care how they're arranged, and the total is the only thing the expectation sees.

## Where it stops working

The thing to be careful about is that this is only true for expectations of sums. Variance doesn't get the same deal:

$$
\operatorname{Var}(X + Y) = \operatorname{Var}(X) + \operatorname{Var}(Y) + 2\operatorname{Cov}(X, Y),
$$

so here the dependence does show up, in the covariance term. In the hat problem the variance of $$X$$ turns out to be exactly $$1$$, while pretending the indicators were independent would give you $$1 - 1/n$$. It's close, but it's wrong, and the difference is entirely those covariances.

I think the confusion comes from learning both facts in the same week. "Expectations add" and "variances add for independent variables" sound like two versions of the same rule, but only the second one actually has a condition.
