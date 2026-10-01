---
layout: page
title: Consistent Hashing
description: Why a hash ring moves far fewer keys than hash mod N when servers come and go.
img: assets/img/projects/consistent-hashing.png
importance: 3
category: include
math: true
---

{% include video.liquid path="assets/video/consistent-hashing.mp4" class="img-fluid rounded" controls=true autoplay=false muted=true loop=true %}

<div class="caption">Adding a server to hash mod N reshuffles most keys. On a hash ring, only one arc changes hands.</div>

Say you have a pile of keys and $$N$$ servers, and you want each key to live on exactly one server. The obvious rule is $$\text{server} = h(k) \bmod N$$. It spreads keys out fine, but it falls apart the moment $$N$$ changes. Going from 4 servers to 5, a key stays put only if $$h \bmod 4 = h \bmod 5$$, which for a well mixed hash happens with probability $$1/5$$. So about $$N/(N+1)$$ of all keys move, and in the video 10 of the 12 do. For a cache that means almost every lookup misses right after you scale up.

Consistent hashing fixes this by hashing the servers too. Put every server and every key at a spot on a circle, and send each key clockwise to the first server it hits. Now each server owns the arc between its counterclockwise neighbor and itself.

Adding a server E splits one arc. The keys that land between E and its counterclockwise neighbor switch to E, and nothing else changes. With servers spread evenly that is about $$1/N$$ of the keys. Removing a server is the mirror image: its arc merges into the next server clockwise, so only its own keys move.

The catch is that a handful of random spots on a circle can leave very uneven arcs, so one server might own half the ring. The usual fix is virtual nodes. Each physical server gets hashed to many spots instead of one, and its share is the sum of many small arcs, which averages out close to $$1/N$$. Real systems use far more than the four per server shown here.

Source: [manim/consistent-hashing.py](https://github.com/bbioren/bbioren.github.io/blob/main/manim/consistent-hashing.py)
