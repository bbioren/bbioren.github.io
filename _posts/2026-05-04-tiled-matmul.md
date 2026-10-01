---
layout: post
title: tiled matrix multiply
date: 2026-05-04
description: why loading tiles into on-chip memory makes matmul fast
tags: visual-proofs video
categories: systems
kind: video
thumbnail: /assets/img/projects/tiled-matmul.png
related_posts: false
---

{% include video.liquid path="assets/video/tiled-matmul.mp4" class="img-fluid rounded" controls=true autoplay=false muted=true loop=true %}

<div class="caption">Naive vs. tiled matrix multiply, counted in reads from slow memory.</div>

Why is a tiled matrix multiply so much faster than the three nested loops from a textbook? The arithmetic is the same. What changes is how often you go back to slow memory.

Take $$C = A B$$ with $$n \times n$$ matrices. One output is a dot product, $$C_{ij} = \sum_k A_{ik} B_{kj}$$, so the naive version reads a full row of $$A$$ and a full column of $$B$$: $$2n$$ reads for one number. Do that for all $$n^2$$ outputs and you get $$2n^3$$ reads. Most of them are repeats. Row $$i$$ of $$A$$ gets fetched again for every output in row $$i$$ of $$C$$.

Processors have a small, fast memory close to the arithmetic units (shared memory on a GPU, on-chip SRAM in general). Tiling uses it. Split everything into $$T \times T$$ blocks. To compute one $$T \times T$$ block of $$C$$, load a tile of $$A$$ and a tile of $$B$$ into fast memory, multiply them, add the result into the $$C$$ block, then move to the next pair of tiles along $$k$$. There are $$n/T$$ such pairs, each costing $$2T^2$$ reads, so one block of $$C$$ costs $$2nT$$ reads. Spread over its $$T^2$$ outputs that is

$$\frac{2nT}{T^2} = \frac{2n}{T}$$

reads per output, down from $$2n$$. In the video, $$n = 8$$ and $$T = 4$$, so 16 reads per output drops to 4.

The reason is reuse. Once $$A_{ik}$$ is on chip, it gets used for all $$T$$ outputs in its row of the $$C$$ block instead of just one. The multiply-adds per value loaded (the arithmetic intensity) go up by a factor of $$T$$. Bigger tiles help more, but both tiles plus the partial $$C$$ block have to fit in that small fast memory, which is what limits $$T$$ in practice.

Source: [manim/tiled-matmul.py](https://github.com/bbioren/bbioren.github.io/blob/main/manim/tiled-matmul.py)
