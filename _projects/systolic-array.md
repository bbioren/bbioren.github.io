---
layout: page
title: Systolic Array
description: how ML accelerators multiply matrices, one cycle at a time
img: assets/img/projects/systolic-array.png
importance: 3
category: include
math: true
---

{% include video.liquid path="assets/video/systolic-array.mp4" class="img-fluid rounded" controls=true autoplay=false muted=true loop=true %}

<div class="caption">A 4 x 4 weight-stationary systolic array computing two rows of Y = XW.</div>

Most of the work in a neural network is matrix multiplication, so accelerators like TPUs and the tensor engine in AWS Trainium's NeuronCores are built around a grid of tiny multiply-accumulate cells called a systolic array.

How does a grid of cells multiply matrices? In the weight-stationary version shown here, cell $$(k, n)$$ is loaded with the weight $$w_{kn}$$ once and keeps it. An input row $$x$$ comes in from the left, with $$x_k$$ entering row $$k$$. Each cycle, every cell takes the activation coming from its left neighbor and the partial sum coming from above, computes

$$
s_{\text{out}} = s_{\text{in}} + x_k \, w_{kn},
$$

passes $$x_k$$ to the right and $$s_{\text{out}}$$ down. By the time a partial sum falls out the bottom of column $$n$$ it has picked up one product from every row, so it equals $$y_n = \sum_k x_k w_{kn}$$.

Why the skew? Row $$k$$ gets its input one cycle after row $$k-1$$, which is exactly how long the partial sum takes to travel down one cell. Without the delay, a sum would reach row $$k$$ before the matching $$x_k$$ arrived.

The nice part is that nothing goes back to memory in between. Every value is used by a neighbor on the next cycle, and once the pipe fills, a new input row can enter every cycle while earlier ones are still finishing.

A real chip wraps this in more hardware. An on-chip SRAM buffer feeds weights and inputs, an accumulation buffer adds up partial results when a big matrix is split into tiles, and a vector unit does elementwise work like adding a bias or applying ReLU before results go back for the next layer. Trainium's NeuronCore follows this shape, with a systolic-array tensor engine alongside vector and scalar engines.

Source: [manim/systolic-array.py](https://github.com/bbioren/bbioren.github.io/blob/main/manim/systolic-array.py)
