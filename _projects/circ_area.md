---
layout: page
title: Area of a Circle
description: Visual intuition for the area of a circle!
img: assets/img/circAreaVisual.jpg
importance: 1
category: intuition
related_publications: false
---

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include video.html path="assets/video/circAreaVideo.mp4" class="img-fluid rounded z-depth-1" controls=true autoplay=true %}
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include video.html path="assets/video/circAreaVideo.mp4" class="img-fluid rounded z-depth-1" controls=true autoplay=true %}
    </div>
</div>

<div class="caption">
    Animation created using Manim. Hopefully this visual gives intuition on why the area of a circle is computed how it is.
</div>

The code in Python can be found below:
{% raw %}

```python
from manim import *
import math

class CircleAreaProof(Scene):
    def construct(self):
        circle = Circle(radius = 2, color = BLUE)
        self.play(Create(circle))
        #self.wait(2)
        #self.play(circle.animate.scale(.75), run_time = 5)
        #self.wait(0.5)

        num = 30 #number of sectors
        sectors = VGroup()
        for i in range(num):
            sector = Sector(
                radius=2,            # Radius of the sector
                start_angle= i * (TAU / num),       # Start angle (in radians)
                angle=TAU / num,       # Angle of the sector (in radians, e.g., 60 degrees)
                color=RED,        # Color of the sector
                fill_opacity=0.1,     # Fill opacity (0 is transparent, 1 is fully opaque)
                stroke_width = 4,
                stroke_opacity = .75
            )
            sectors.add(sector)

            if i == 0:
                self.play(Create(sector))
                radius_lable = Text("r", font_size = 25)
                radius_lable.next_to(sector, UP, buff = -.1)
                self.play(Create(radius_lable))
                self.wait(1)
                self.play(FadeOut(radius_lable))


        self.play(Create(sectors), run_time = 2)
        self.wait(1)

        l = Line(np.array([-(TAU * 2) / 2, 0, 0]), np.array([(TAU * 2) / 2, 0, 0]), color = BLUE)
        self.play(ReplacementTransform(circle, l.next_to(sectors, UP, buff = 1)), run_time = 2)
        line_label = Text("circumfrence", font_size = 25)
        line_label.next_to(l, DOWN, buff = .25)
        self.play(Create(line_label))
        self.wait(1)

        width_sectors = 0
        for i in range(num):
            width_sectors += sectors[i].get_width() + .05
            # print(sectors[i].get_width())

        # print(width_sectors)
        # print(config.frame_width)

        scaler =  (config.frame_width - 2) / width_sectors
        self.play(
            sectors.animate.scale(scaler).arrange(RIGHT, buff =  0.05),
            run_time = 2
                  )
        
        #print(sectors.get_width())
        

        # scale_factor = config.frame_width / sectors.get_width()
        # self.play(sectors.animate.scale(scale_factor))

        
        for i in range(num):
            if i % 2 == 0:
                self.play(sectors[i].animate.rotate((TAU / 4)  -  ((TAU / (2 * num)) * (1 + 2 * i))), run_time = 1 / (1.2 * i + 1))
            else:
                self.play(sectors[i].animate.rotate((TAU / 2) + (TAU / 4)  -  ((TAU / (2 * num)) * (1 + 2 * i))), run_time = 1 / (1.2 * i + 1))

        #scaler = (config.frame_width - 5) / (sectors[0].get_width() * (num / 2))
        scaler = ((TAU * 2) / 2) / (sectors[0].get_width() * (num / 2))

        self.play(
            sectors.animate.scale(scaler).arrange(RIGHT, buff = (- (1/2) * sectors[0].width) - .1)
                  )
        
        x = sectors[0].get_left()[0] - .5
        bottom = sectors[0].get_bottom()[1]
        top = sectors[0].get_top()[1]

        line = Line(np.array([x, bottom, 0]), np.array([x, top, 0]))
        self.play(Create(line))
        self.play(Write(MathTex(r"r").next_to(line, LEFT)))

        half = Line(l.get_left(), l.get_center(), color = RED)
        half_label = MathTex(r"\pi r").next_to(half, UP)

        halfGroup = VGroup()
        halfGroup.add(half, half_label)
        self.play(Create(halfGroup), run_time = 1.5)

        self.play(halfGroup.animate.scale(sectors.get_width() / halfGroup.get_width()).next_to(sectors, UP, buff = 0.5))

        self.play(Write(MathTex(r"Area = \pi r^2").next_to(sectors, DOWN, buff = 1)))


        self.wait(3)
```

{% endraw %}