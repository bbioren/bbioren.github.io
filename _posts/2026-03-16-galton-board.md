---
layout: post
title: galton board
date: 2026-03-16
description: a live galton board that grows a bell curve
tags: visual-proofs interactive
categories: math
kind: interactive
thumbnail: /assets/img/projects/galton-board.svg
related_posts: false
---

<div class="viz" id="galton-board"></div>
<script src="{{ '/assets/notebook/viz/galton-board.js' | relative_url | bust_file_cache }}" defer></script>

Each ball falls through $$n$$ rows of pegs. At every peg it goes right with probability $$p$$ and left with probability $$1-p$$, independently of everything else. The bin it lands in is just the number of times it went right. Call that $$X$$.

What is the chance a ball ends up in bin $$k$$? It has to pick exactly $$k$$ rights out of $$n$$ bounces. Any one such path has probability $$p^k(1-p)^{n-k}$$, and there are $$\binom{n}{k}$$ of them, so

$$
P(X = k) = \binom{n}{k} p^k (1-p)^{n-k}.
$$

That is the binomial distribution, and the orange ticks show it times the number of balls so far. The bars should settle onto them as the count grows.

Why does it look like a bell? Write $$X = B_1 + \cdots + B_n$$, where each $$B_i$$ is 1 for a right bounce and 0 for a left one. Each $$B_i$$ has mean $$p$$ and variance $$p(1-p)$$, so

$$
E[X] = np, \qquad \operatorname{Var}(X) = np(1-p).
$$

The central limit theorem says a sum of many independent, identically distributed pieces with finite variance is approximately normal, whatever the pieces look like. A single bounce is about as un-bell-shaped as it gets, two spikes at 0 and 1, but add sixteen of them and the result is already close to $$N(np, np(1-p))$$. That is the dashed curve.

Try pushing $$p$$ toward 0.1 with only a few rows. The binomial gets lopsided and the normal curve spills past bin 0, so the approximation is worse. Add rows and it improves again. The usual rule of thumb is that it works well once $$np$$ and $$n(1-p)$$ are both bigger than about 5.

Source: [assets/notebook/viz/galton-board.js](https://github.com/bbioren/bbioren.github.io/blob/main/assets/notebook/viz/galton-board.js)
