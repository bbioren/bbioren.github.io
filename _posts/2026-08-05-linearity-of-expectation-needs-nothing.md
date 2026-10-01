---
layout: post
title: linearity of expectation needs nothing
date: 2026-08-05
description: adding expectations doesn't need independence, shown with a table of returned hats
tags: visual-proofs probability combinatorics
categories: math
related_posts: false
thumbnail: /assets/img/blog/linearity-of-expectation-needs-nothing/hat-check-grid.svg
---

At a party, $$n$$ people check their hats, and at the end of the night the hats are handed back in a completely random order. On average, how many people get their own hat back?

You could try to find the whole distribution of the number of matches. That takes inclusion-exclusion and gets messy pretty quickly. We don't need it, though. Let $$\mathbf{1}_i$$ be $$1$$ if person $$i$$ gets their own hat and $$0$$ otherwise. Then the number of matches is just

$$
X = \mathbf{1}_1 + \dots + \mathbf{1}_n.
$$

What's the expectation of one of these indicators? Well, person $$i$$ is equally likely to end up with any of the $$n$$ hats, so they get their own hat with probability $$1/n$$. That means $$\mathbb{E}[\mathbf{1}_i] = 1/n$$. Adding up $$n$$ of these, we have that

$$
\mathbb{E}[X] = n \cdot \frac{1}{n} = 1.
$$

So the answer is one, no matter how many people are at the party. That's kind of a strange answer.

The step that makes this work is linearity of expectation:

$$
\mathbb{E}[X + Y] = \mathbb{E}[X] + \mathbb{E}[Y].
$$

This holds for any two random variables with finite means, and that's the whole hypothesis. $$X$$ and $$Y$$ can be independent, or strongly correlated, or $$Y$$ can just be some function of $$X$$, and the formula still holds. The indicators in the hat problem are definitely not independent. For example, if everyone except one person has their own hat, then the last person has to have theirs too (it's the only hat left). But if you look back at the computation above, we never used independence anywhere.

## Seeing it in a table of outcomes

So why doesn't the dependence matter? It's easiest to see by just writing out every outcome. For $$n = 3$$ there are $$6$$ ways to hand back the three hats, each with probability $$1/6$$. The table below has one row for each outcome and one column for each person, with a $$1$$ wherever that person got their own hat.

<div class="row justify-content-center mt-3">
  <div class="col-sm-10 mt-3 mt-md-0">
    {% include figure.liquid loading="eager" path="assets/img/blog/linearity-of-expectation-needs-nothing/hat-check-grid.svg" class="img-fluid rounded" zoomable=true %}
  </div>
</div>
<div class="caption">
  Every way to return three hats. A row adds up to the number of matches in that outcome, and a column adds up to the number of outcomes where that person gets their own hat.
</div>

Now we can add up the $$1$$s in the table in two different ways.

Going row by row gives the number of matches in each outcome. These are $$3, 1, 1, 1, 0, 0$$, and averaging them gives

$$
\mathbb{E}[X] = \frac{3 + 1 + 1 + 1 + 0 + 0}{6} = \frac{6}{6} = 1.
$$

Going column by column, each person gets their own hat back in $$2$$ of the $$6$$ outcomes. So we have that

$$
\mathbb{E}[\mathbf{1}_1] + \mathbb{E}[\mathbf{1}_2] + \mathbb{E}[\mathbf{1}_3] = \frac{2}{6} + \frac{2}{6} + \frac{2}{6} = 1.
$$

Of course the two agree, since they're counting the same six $$1$$s. And that's really all linearity of expectation is. In general it's just swapping the order of a double sum:

$$
\sum_\omega P(\omega) \sum_i \mathbf{1}_i(\omega) = \sum_i \sum_\omega P(\omega)\, \mathbf{1}_i(\omega).
$$

The left side adds up each row and then averages over the rows. The right side averages each column and then adds up the columns.

What about the dependence between the indicators? It's in the table too. No row has exactly two $$1$$s, because if two people have their own hats then the third person has to as well. So the dependence does change how the $$1$$s are spread out across the rows. But the expectation only cares about how many $$1$$s there are in total, and moving them around between rows doesn't change that.

## Variance is different

This only works for expectations of sums. I bring it up because it's easy to mix up with the fact that variances add for independent variables. "Expectations add" and "variances add" sound like two versions of the same rule, but only the variance version comes with a condition. In general the variance of a sum has an extra term,

$$
\operatorname{Var}(X + Y) = \operatorname{Var}(X) + \operatorname{Var}(Y) + 2\operatorname{Cov}(X, Y),
$$

and the dependence shows up there, in the covariance. In the hat problem the variance of $$X$$ turns out to be exactly $$1$$. If you pretended the indicators were independent, you'd get $$1 - 1/n$$ instead. The whole gap between those two numbers comes from the covariances.
