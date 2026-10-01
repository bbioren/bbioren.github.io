---
layout: post
title: three ways to shard
date: 2026-07-22
description: data, tensor, and pipeline parallelism on 4 devices, animated.
tags: visual-proofs video
categories: systems
kind: video
thumbnail: /assets/img/projects/three-ways-to-shard.png
related_posts: false
---

{% include video.liquid path="assets/video/three-ways-to-shard.mp4" class="img-fluid rounded" controls=true autoplay=false muted=true loop=true %}

<div class="caption">Splitting one network across 4 devices: by batch, by weights, or by layers.</div>

If a model is too slow or too big for one device, how do you spread it over four? There are three basic answers, and each one splits a different thing.

**Data parallel** splits the batch. Every device keeps a full copy of the model and runs forward and backward on its own slice of the data, giving a local gradient $$g_i$$. Before anyone updates, the devices run an all-reduce so each one ends up with the same average

$$g = \tfrac{1}{4}(g_0 + g_1 + g_2 + g_3).$$

Since everyone applies the same update, the copies never drift apart. The catch is that each device still has to fit the whole model.

**Tensor parallel** splits the weights inside a layer. For $$Y = XW$$, cut $$W$$ into column blocks $$W_0, \dots, W_3$$. Each device gets the same input $$X$$ and computes $$Y_i = XW_i$$, a slice of the output. Gathering the slices gives the full $$Y$$. This saves memory on big layers, but the devices talk inside every split layer, so it needs fast links.

**Pipeline parallel** splits the layers. Device 0 runs the first stage, then hands its activations to device 1, and so on. To keep devices busy, the batch is cut into $$M$$ micro-batches that flow through like an assembly line. Some slots are still empty while the pipeline fills and drains. With $$P$$ stages, the forward pass leaves an idle fraction of

$$\frac{P-1}{M+P-1},$$

which is $$3/7$$ for $$P = M = 4$$. More micro-batches shrink this bubble.

Real training runs often combine all three.

Source: [manim/three-ways-to-shard.py](https://github.com/bbioren/bbioren.github.io/blob/main/manim/three-ways-to-shard.py)
