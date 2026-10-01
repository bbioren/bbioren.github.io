---
layout: post
title: linearity of expectation needs nothing
date: 2026-08-05
description: why adding expectations never requires independence, and how indicator variables turn hard counting into bookkeeping
tags: visual-proofs probability combinatorics
categories: math
related_posts: false
---

Ask someone to compute the expected value of a sum and you can watch them start to worry about independence. Are the pieces independent? If not, isn't everything ruined? For expectations of sums, it never matters. Linearity of expectation has no independence hypothesis at all, and that is exactly why it's so useful: you can break a messy random quantity into simple pieces that depend on each other in tangled ways, and the tangle never shows up in the answer.

## The statement

For any random variables $$X$$ and $$Y$$ on the same probability space with finite expectations,

$$
\mathbb{E}[X + Y] = \mathbb{E}[X] + \mathbb{E}[Y],
$$

and more generally $$\mathbb{E}\big[\sum_{i=1}^n c_i X_i\big] = \sum_{i=1}^n c_i\, \mathbb{E}[X_i]$$ for constants $$c_i$$. Nothing is assumed about how the $$X_i$$ relate to each other. They can be independent, perfectly correlated, or one can be a deterministic function of another.

Here is the heuristic for why this should be true. An expectation is just a weighted sum over outcomes: on a finite sample space, $$\mathbb{E}[X] = \sum_\omega X(\omega)\, P(\omega)$$. Independence is a statement about how probabilities _multiply_ across events. But linearity only asks you to _add_ the values $$X(\omega) + Y(\omega)$$ outcome by outcome and then take a weighted sum. Addition doesn't care about dependence. A quick sanity check: take $$Y = -X$$, which is as dependent as it gets. Then $$\mathbb{E}[X + Y] = \mathbb{E}[0] = 0 = \mathbb{E}[X] - \mathbb{E}[X]$$, just as linearity says.

## Why it matters

The trick that makes linearity powerful is to write a count as a sum of **indicator variables**. If $$A$$ is an event, its indicator $$\mathbf{1}_A$$ is $$1$$ when $$A$$ happens and $$0$$ otherwise, so $$\mathbb{E}[\mathbf{1}_A] = P(A)$$. Then any count "how many of these events happen?" has expectation equal to the sum of the probabilities.

**The hat-check problem.** Here $$n$$ people check their hats, and the hats come back in a uniformly random order. How many people expect to get their own hat back? Let $$\mathbf{1}_i$$ indicate that person $$i$$ gets their own hat, and let $$X = \sum_{i=1}^n \mathbf{1}_i$$ be the number of fixed points of the random permutation. Person $$i$$ is equally likely to receive any of the $$n$$ hats, so $$P(\mathbf{1}_i = 1) = 1/n$$, and

$$
\mathbb{E}[X] = \sum_{i=1}^n \frac{1}{n} = 1.
$$

The answer is $$1$$ for every $$n$$: three people or three million. These indicators are very much _not_ independent. If persons $$1$$ through $$n-1$$ all get their own hats, person $$n$$ is guaranteed to get theirs. Even two of them are correlated: $$P(\mathbf{1}_1 = \mathbf{1}_2 = 1) = \frac{1}{n(n-1)}$$, which is not $$\frac{1}{n^2}$$. Computing the full distribution of $$X$$ takes inclusion–exclusion. Computing its mean takes one line.

**Distinct birthdays.** Now let $$k$$ people have independent birthdays, each uniform over $$n = 365$$ days. Let $$D$$ be the number of _distinct_ birthdays among them. Counting people is the wrong move here. Count days instead: let $$\mathbf{1}_d$$ indicate that at least one person has birthday $$d$$, so $$D = \sum_{d=1}^{n} \mathbf{1}_d$$. Day $$d$$ is missed by all $$k$$ people with probability $$(1 - 1/n)^k$$, so

$$
\mathbb{E}[D] = n\left(1 - \left(1 - \frac{1}{n}\right)^k\right).
$$

For $$k = 23$$ this is about $$22.32$$. So on average a room of 23 people loses about $$0.68$$ birthdays to collisions, which is the birthday paradox in a different light. Again the day indicators are dependent (they always sum to at most $$k$$, so learning that many days are taken makes the rest less likely), and again it doesn't matter.

## The proof is a grid

My favorite way to see linearity is to write down every outcome and every indicator in one table. Take the hat-check problem with $$n = 3$$. There are $$3! = 6$$ permutations, each with probability $$1/6$$. Make one row per outcome and one column per indicator, and fill in a $$1$$ wherever that person gets their own hat.

<div class="row justify-content-center mt-3">
  <div class="col-sm-10 mt-3 mt-md-0">
    {% include figure.liquid loading="eager" path="assets/img/blog/linearity-of-expectation-needs-nothing/hat-check-grid.svg" class="img-fluid rounded" zoomable=true %}
  </div>
</div>
<div class="caption">
  All six ways to hand back three hats, each with probability 1/6. A 1 in column i means person i got their own hat. Row sums give X, the number of fixed points. Column sums count how often each person gets lucky. Both ways of adding up the grid find the same six 1s.
</div>

Read the grid two ways. **Across a row**, you get $$X(\omega)$$, the number of fixed points of that outcome: $$3$$ for the identity, $$1$$ for each of the three swaps, and $$0$$ for the two 3-cycles. Averaging the orange column with weight $$1/6$$ gives

$$
\mathbb{E}[X] = \tfrac{1}{6}(3 + 1 + 1 + 1 + 0 + 0) = 1.
$$

**Down a column**, you get how many outcomes make indicator $$\mathbf{1}_i$$ equal to one. Each column has exactly two $$1$$s, so $$\mathbb{E}[\mathbf{1}_i] = 2/6 = 1/3$$ and

$$
\mathbb{E}[\mathbf{1}_1] + \mathbb{E}[\mathbf{1}_2] + \mathbb{E}[\mathbf{1}_3] = \tfrac{1}{6}(2 + 2 + 2) = 1.
$$

That is the whole proof. In symbols, it's swapping the order of a finite double sum:

$$
\mathbb{E}\Big[\sum_i \mathbf{1}_i\Big] = \sum_\omega P(\omega) \sum_i \mathbf{1}_i(\omega) = \sum_i \sum_\omega P(\omega)\, \mathbf{1}_i(\omega) = \sum_i \mathbb{E}[\mathbf{1}_i].
$$

Look at where the dependence lives in the picture. It's in the _pattern_ of the 1s. The identity row has three 1s in it, and no row has exactly two, because if two people get their own hats, the third must too. Dependence shapes how the 1s cluster within rows. But the total number of 1s doesn't change depending on whether you count them row by row or column by column. Linearity only ever looks at that total. The same argument works for any finite sample space and any entries, not just 0s and 1s. For general random variables, the sum over outcomes becomes an integral, and linearity of the integral does the same job.

## The part that gets missed

The freedom from independence belongs to expectations of _sums_, and it stops right there. Variance is not linear: $$\operatorname{Var}(X + Y) = \operatorname{Var}(X) + \operatorname{Var}(Y) + 2\operatorname{Cov}(X, Y)$$, so variances add only when the pieces are uncorrelated. In the hat-check problem the covariances really do matter. Using $$\mathbf{1}_i^2 = \mathbf{1}_i$$ and the pair probability above, $$\mathbb{E}[X^2] = 1 + n(n-1)\cdot\frac{1}{n(n-1)} = 2$$, so $$\operatorname{Var}(X) = 1$$ for $$n \ge 2$$. Treating the indicators as independent would give $$1 - 1/n$$ instead. Products are worse: $$\mathbb{E}[XY] = \mathbb{E}[X]\,\mathbb{E}[Y]$$ is _equivalent_ to $$X$$ and $$Y$$ being uncorrelated, and independence is the usual way to guarantee it. The other fine print is about infinite sums. $$\mathbb{E}\big[\sum_{i=1}^\infty X_i\big] = \sum_{i=1}^\infty \mathbb{E}[X_i]$$ holds when every $$X_i \ge 0$$ (monotone convergence) or when $$\sum_i \mathbb{E}\vert X_i \vert \lt \infty$$ (dominated convergence), but not in general. Here's a counterexample. Let $$P(N = m) = 2^{-m}$$ for $$m \ge 1$$, and set $$X_m = 2^m \mathbf{1}\{N = m\} - 2^{m+1} \mathbf{1}\{N = m+1\}$$. Each $$\mathbb{E}[X_m] = 1 - 1 = 0$$. But the sum telescopes to $$\sum_m X_m = 2\cdot\mathbf{1}\{N = 1\}$$, which has expectation $$1$$. Independence was never the hypothesis that mattered. Convergence is.
