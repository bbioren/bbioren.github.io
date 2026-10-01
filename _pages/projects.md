---
layout: default
title: projects
permalink: /projects/
---

<div class="page-head">
  <h1>Projects</h1>
  <span class="hand">things I built outside of research. click a photo.</span>
</div>

{% assign tilts = "-1.5deg,1deg,-0.5deg,1.5deg,-1deg,0.5deg" | split: "," %}

<div class="projects">
  {% assign sorted = site.projects | sort: "importance" %}
  {% for project in sorted %}
    {% if project.redirect %}{% assign href = project.redirect %}{% else %}{% assign href = project.url | relative_url %}{% endif %}
    {% assign i = forloop.index0 | modulo: 6 %}
    <a class="project" href="{{ href }}" style="--tilt: {{ tilts[i] }}">
      <span class="pic">
        <span class="tape" aria-hidden="true"></span>
        {% if project.img %}
          {% assign base = project.img | remove: '.png' | remove: '.jpg' | remove: '.jpeg' %}
          <picture>
            {% unless project.img contains '.svg' %}
              <source srcset="{{ base | append: '-800.webp' | relative_url }}" type="image/webp">
            {% endunless %}
            <img src="{{ project.img | relative_url }}" alt="" loading="lazy">
          </picture>
        {% endif %}
      </span>
      <span class="t">{{ project.title }}</span>
      <span class="d">{{ project.description }}</span>
      {% if project.redirect %}<span class="where">{{ project.redirect | remove: 'https://' | remove: 'http://' | split: '/' | first }}</span>{% endif %}
    </a>
  {% endfor %}
</div>
