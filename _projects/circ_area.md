---
layout: page
title: Area of a Circle
description: Visual intuition for the area of a circle!
img: assets/img/circAreaVisual.jpg
importance: 1
category: intuition
related_publications: false
---


<div class="col-sm mt-3 mt-md-0">
    {% include video.liquid path="assets/video/circAreaVideo.mp4" class="img-fluid rounded z-depth-1" controls=true autoplay=true %}
</div>

<div class="caption">
    Animation created using Manim. Hopefully this visual gives intuition on the reasoning behind a common formula.
</div>

Source code:
{% raw %}

```python
from manim import *
import math

class CircleAreaProof(Scene):
    def construct(self):
        circle = Circle(radius = 2, color = BLUE)
        self.play(Create(circle))

        num = 30 # desired number of sectors
        sectors = VGroup()
        for i in range(num):
            sector = Sector(
                radius=2,
                start_angle= i * (TAU / num),  # update starting angle based on current sector
                angle=TAU / num,
                color=RED,
                fill_opacity=0.1,
                stroke_width = 4,
                stroke_opacity = .75
            )
            sectors.add(sector)

            # show the radius on the first sector
            if i == 0:
                self.play(Create(sector))
                radius_lable = Text("r", font_size = 25)
                radius_lable.next_to(sector, UP, buff = -.1)
                self.play(Create(radius_lable))
                self.wait(1)
                self.play(FadeOut(radius_lable))


        self.play(Create(sectors[1:num]), run_time = 2)  # first sector already created
        self.wait(1)

        # transform circumfrence to top
        l = Line(np.array([-(TAU * 2) / 2, 0, 0]), np.array([(TAU * 2) / 2, 0, 0]), color = BLUE)
        self.play(ReplacementTransform(circle, l.next_to(sectors, UP, buff = 1)), run_time = 2)
        line_label = Text("circumfrence", font_size = 25)
        line_label.next_to(l, DOWN, buff = .25)
        self.play(Create(line_label))
        self.wait(1)

        # scale and line up sectors to screen
        width_sectors = 0
        for i in range(num):
            width_sectors += sectors[i].get_width() + .05

        scaler =  (config.frame_width - 2) / width_sectors
        self.play(
            sectors.animate.scale(scaler).arrange(RIGHT, buff =  0.05),
            run_time = 2
                  )
        
        # rotate sectors to position
        for i in range(num):
            if i % 2 == 0:
                self.play(sectors[i].animate.rotate((TAU / 4)  -  ((TAU / (2 * num)) * (1 + 2 * i))), run_time = 1 / (1.2 * i + 1))
            else:
                self.play(sectors[i].animate.rotate((TAU / 2) + (TAU / 4)  -  ((TAU / (2 * num)) * (1 + 2 * i))), run_time = 1 / (1.2 * i + 1))

        # make rectangle
        scaler = ((TAU * 2) / 2) / (sectors[0].get_width() * (num / 2))
        self.play(
            sectors.animate.scale(scaler).arrange(RIGHT, buff = (- (1/2) * sectors[0].width) - .1)
                  )
        
        # create radius line for height
        x = sectors[0].get_left()[0] - .5
        bottom = sectors[0].get_bottom()[1]
        top = sectors[0].get_top()[1]
        line = Line(np.array([x, bottom, 0]), np.array([x, top, 0]))
        self.play(Create(line))
        self.play(Write(MathTex(r"r").next_to(line, LEFT)))

        # create half the circumfrence
        half = Line(l.get_left(), l.get_center(), color = RED)
        half_label = MathTex(r"\pi r").next_to(half, UP)
        halfGroup = VGroup()
        halfGroup.add(half, half_label)
        self.play(Create(halfGroup), run_time = 1.5)

        # position half the circumfrence line
        self.play(halfGroup.animate.scale(sectors.get_width() / halfGroup.get_width()).next_to(sectors, UP, buff = 0.5))

        # display final formula
        self.play(Write(MathTex(r"Area = \pi r^2").next_to(sectors, DOWN, buff = 1)))
        self.wait(3)
```

{% endraw %}