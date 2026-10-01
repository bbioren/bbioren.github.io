---
layout: post
title: flash attention
date: 2026-06-25
description: exact attention without ever storing the N by N score matrix
tags: visual-proofs video
categories: systems
kind: video
thumbnail: /assets/img/projects/flash-attention.png
related_posts: false
---

{% include video.liquid path="assets/video/flash-attention.mp4" class="img-fluid rounded" controls=true autoplay=false muted=true loop=true %}

<div class="caption">Standard attention vs. FlashAttention's tiled loop with an online softmax.</div>

Why is attention slow on long sequences? Mostly because of memory, not arithmetic. The standard recipe computes $$S = QK^\top/\sqrt{d}$$, which is an $$N \times N$$ matrix, writes it to the GPU's big but slow HBM, reads it back to take a row-wise softmax, writes the result $$P$$, and then reads $$P$$ again to compute $$O = PV$$. For long sequences that matrix is huge, and moving it around dominates the runtime.

FlashAttention never builds that matrix in HBM. It loads a block of query rows $$Q_i$$ into the small, fast on-chip SRAM and keeps it there. Then it streams the key and value blocks $$K_j, V_j$$ through one at a time. Each step makes a small tile $$S_j = Q_i K_j^\top/\sqrt{d}$$ that only lives on chip.

The catch is that softmax needs the max and the sum over a whole row, and we only see one block of the row at a time. The fix is to keep a running max $$m$$, a running sum $$\ell$$, and a running unnormalized output $$O$$, starting from $$m = -\infty$$, $$\ell = 0$$, $$O = 0$$. For each new block:

$$m_{\text{new}} = \max\big(m_{\text{old}}, \operatorname{rowmax}(S_j)\big)$$

$$\ell_{\text{new}} = e^{m_{\text{old}} - m_{\text{new}}}\,\ell_{\text{old}} + \operatorname{rowsum}\big(e^{S_j - m_{\text{new}}}\big)$$

$$O_{\text{new}} = e^{m_{\text{old}} - m_{\text{new}}}\,O_{\text{old}} + e^{S_j - m_{\text{new}}}\,V_j$$

When a bigger max shows up, the factor $$e^{m_{\text{old}} - m_{\text{new}}}$$ rescales everything already summed so it matches the new reference point. After the last block, dividing $$O$$ by $$\ell$$ gives exactly $$\operatorname{softmax}(QK^\top/\sqrt{d})\,V$$. Nothing is approximated. The extra memory is just $$m$$ and $$\ell$$ for each row, so $$O(N)$$ instead of $$O(N^2)$$, and since the big matrix never goes to HBM, there are far fewer slow reads and writes.

Source: [manim/flash-attention.py](https://github.com/bbioren/bbioren.github.io/blob/main/manim/flash-attention.py)
