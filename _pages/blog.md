---
layout: default
permalink: /blog/
title: sketchbook
---

<div class="page-head">
  <h1>Sketchbook</h1>
  <span class="hand">short posts, mostly one picture that explains one idea.</span>
</div>

{% assign by_year = site.posts | group_by_exp: "p", "p.date | date: '%Y'" %}
{% for y in by_year %}

<p class="year">{{ y.name }}</p>
<div class="sketch">
  {% for post in y.items %}
    {% include nb/post_card.liquid post=post %}
  {% endfor %}
</div>
{% endfor %}
