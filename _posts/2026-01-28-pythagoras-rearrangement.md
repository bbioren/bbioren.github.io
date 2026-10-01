---
layout: post
title: pythagoras by rearrangement
date: 2026-01-28
description: slide four triangles around a square and watch a² + b² = c² fall out
tags: visual-proofs interactive
categories: math
kind: interactive
thumbnail: /assets/img/projects/pythagoras-rearrangement.svg
related_posts: false
---

<div class="viz" id="pythagoras-rearrangement"></div>
<script src="{{ '/assets/notebook/viz/pythagoras-rearrangement.js' | relative_url | bust_file_cache }}" defer></script>

Take a right triangle with legs $$a$$ and $$b$$ and hypotenuse $$c$$. Make four copies and put them inside a square of side $$a + b$$.

In the first arrangement, each triangle sits in a corner with its right angle tucked into that corner. The hypotenuses face inward and enclose a tilted square. Its sides are all $$c$$, and its corners are right angles because the two acute angles of the triangle add up to $$90^\circ$$. So the orange hole has area $$c^2$$.

Now slide the triangles. Pair them up into two $$a \times b$$ rectangles and push those into opposite corners. The orange hole is now two squares, one of side $$a$$ and one of side $$b$$, with total area $$a^2 + b^2$$.

Why do those two areas have to match? Nothing else changed. The big square is the same in both pictures, and the four triangles are the same four triangles, so they cover the same amount of it. Whatever is left over has to be the same too:

$$
c^2 = (a+b)^2 - 4 \cdot \tfrac{1}{2}ab = a^2 + b^2.
$$

The second slider changes the shape of the triangle while keeping $$a + b$$ fixed at 10. The numbers below the picture are computed from $$a$$ and $$b$$ only, and $$c^2$$ always comes out equal to $$a^2 + b^2$$. Try a very lopsided triangle. The small square shrinks, the large one grows, the tilted square gets bigger, and the totals still agree.

Notice that no triangle has to rotate. One stays put and the other three just slide.

Source: [assets/notebook/viz/pythagoras-rearrangement.js](https://github.com/bbioren/bbioren.github.io/blob/main/assets/notebook/viz/pythagoras-rearrangement.js)
