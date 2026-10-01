"""Three basic ways to split a neural network across 4 devices.

Render (720p30):
    manim -qm three-ways-to-shard.py ThreeWaysToShard
"""

from manim import *

config.background_color = "#fdfdfb"

INK = "#1d2a44"
BLUE_PEN = "#2456a6"
ORANGE = "#dd6b20"
SOFT_BLUE = "#bee3f8"
SOFT_ORANGE = "#feebc8"
GRAY = "#a0aec0"
GRID = "#dbe5f2"
MARGIN = "#e9a5a5"
FONT = "Helvetica"

Text.set_default(color=INK, font=FONT)
MathTex.set_default(color=INK)

DEV_X = [-4.8, -1.6, 1.6, 4.8]
BOX_Y = -0.5


def T(s, size=28, **kw):
    if "\n" in s:
        return VGroup(*[Text(l, font_size=size, **kw) for l in s.split("\n")]).arrange(DOWN, buff=0.1)
    return Text(s, font_size=size, **kw)


class ThreeWaysToShard(Scene):
    # ---------- helpers ----------
    def paper(self):
        lines = VGroup()
        x = -7.5
        while x <= 7.5:
            lines.add(Line([x, -4.2, 0], [x, 4.2, 0], stroke_width=1, color=GRID))
            x += 0.5
        y = -4.0
        while y <= 4.0:
            lines.add(Line([-7.3, y, 0], [7.3, y, 0], stroke_width=1, color=GRID))
            y += 0.5
        margin = Line([-6.6, -4.2, 0], [-6.6, 4.2, 0], stroke_width=2, color=MARGIN)
        self.add(lines, margin)

    def devices(self, height=2.6):
        boxes = VGroup()
        labels = VGroup()
        for i, x in enumerate(DEV_X):
            b = RoundedRectangle(
                corner_radius=0.15, width=2.6, height=height,
                stroke_color=INK, stroke_width=2,
            ).move_to([x, BOX_Y, 0])
            boxes.add(b)
            labels.add(T(f"Device {i}", 24).next_to(b, DOWN, buff=0.15))
        return boxes, labels

    def header(self, s):
        return T(s, 36, weight=BOLD).to_edge(UP, buff=0.35)

    def caption(self, s):
        return T(s, 26).move_to([0, -3.35, 0])

    def clear(self):
        self.play(*[FadeOut(m) for m in self.mobjects if m not in self.bg], run_time=1)

    # ---------- scene ----------
    def construct(self):
        self.paper()
        self.bg = list(self.mobjects)

        title = T("Three ways to split a network", 44, weight=BOLD)
        sub = T("across 4 devices", 32, color=BLUE_PEN).next_to(title, DOWN, buff=0.3)
        self.play(Write(title), FadeIn(sub, shift=UP * 0.2), run_time=1.5)
        self.wait(1)
        self.play(FadeOut(title), FadeOut(sub))

        self.data_parallel()
        self.clear()
        self.tensor_parallel()
        self.clear()
        self.pipeline_parallel()
        self.clear()
        self.summary()

    # ---------- 1. data parallel ----------
    def data_parallel(self):
        head = self.header("1. Data parallel")
        boxes, labels = self.devices()
        self.play(FadeIn(head), Create(boxes), FadeIn(labels), run_time=1.5)

        # full model copy in every device
        models = VGroup()
        for b in boxes:
            bars = VGroup(*[
                RoundedRectangle(corner_radius=0.05, width=1.7, height=0.22,
                                 stroke_color=BLUE_PEN, fill_color=SOFT_BLUE,
                                 fill_opacity=1, stroke_width=2)
                for _ in range(3)
            ]).arrange(DOWN, buff=0.1).move_to(b.get_center() + DOWN * 0.25)
            models.add(bars)
        cap = self.caption("Every device holds a full copy of the model")
        self.play(LaggedStart(*[FadeIn(m) for m in models], lag_ratio=0.2), FadeIn(cap), run_time=1.5)
        self.wait(0.5)

        # batch of 8 examples, 2 per device
        batch = VGroup(*[
            Square(0.4, stroke_color=ORANGE, fill_color=SOFT_ORANGE, fill_opacity=1, stroke_width=2)
            for _ in range(8)
        ]).arrange(RIGHT, buff=0.12).move_to([0, 2.2, 0])
        blabel = T("batch", 26).next_to(batch, LEFT, buff=0.3)
        self.play(FadeIn(batch), FadeIn(blabel))
        self.wait(0.3)
        new_cap = self.caption("Each device gets a different slice of the batch")
        anims = []
        for i, b in enumerate(boxes):
            pair = VGroup(batch[2 * i], batch[2 * i + 1])
            target = b.get_center() + UP * 0.8
            anims.append(pair.animate.arrange(RIGHT, buff=0.12).move_to(target))
        self.play(*anims, FadeOut(blabel), Transform(cap, new_cap), run_time=1.5)
        self.wait(0.5)

        # local gradients
        grads = VGroup(*[
            MathTex(f"g_{i}", font_size=40, color=ORANGE).move_to(b.get_center() + DOWN * 1.0)
            for i, b in enumerate(boxes)
        ])
        self.play(FadeIn(grads, shift=UP * 0.2),
                  Transform(cap, self.caption("Forward and backward: each computes its own gradient")),
                  run_time=1.2)
        self.wait(0.7)

        # all-reduce
        total = MathTex(r"g = \tfrac{1}{4}(g_0 + g_1 + g_2 + g_3)", font_size=40, color=ORANGE).move_to([0, 2.2, 0])
        self.play(Transform(cap, self.caption("All-reduce: combine the gradients...")))
        self.play(*[g.copy().animate.move_to(total.get_center()).set_opacity(0) for g in grads],
                  FadeIn(total), run_time=1.5)
        finals = VGroup(*[MathTex("g", font_size=40, color=ORANGE).move_to(g) for g in grads])
        sent = VGroup(*[MathTex("g", font_size=40, color=ORANGE).move_to(total) for _ in grads])
        self.play(Transform(cap, self.caption("...and send the average back to every device")))
        self.play(*[ReplacementTransform(s, f) for s, f in zip(sent, finals)],
                  *[FadeOut(g) for g in grads], run_time=1.5)
        self.play(*[Indicate(f, color=ORANGE) for f in finals],
                  Transform(cap, self.caption("Same gradient everywhere, so the copies stay identical")))
        self.wait(1)

    # ---------- 2. tensor parallel ----------
    def tensor_parallel(self):
        head = self.header("2. Tensor parallel")
        self.play(FadeIn(head))

        fills = [SOFT_BLUE, SOFT_ORANGE, SOFT_BLUE, SOFT_ORANGE]
        cols = VGroup(*[
            Rectangle(width=0.55, height=1.4, stroke_color=BLUE_PEN, stroke_width=2,
                      fill_color=fills[i], fill_opacity=1)
            for i in range(4)
        ]).arrange(RIGHT, buff=0).move_to([0.6, 1.9, 0])
        wlab = MathTex("W", font_size=44).next_to(cols, LEFT, buff=0.3)
        eq = MathTex("Y = X", font_size=44).next_to(wlab, LEFT, buff=0.2)
        clabs = VGroup(*[MathTex(f"W_{i}", font_size=30).next_to(c, UP, buff=0.1) for i, c in enumerate(cols)])
        cap = self.caption("One layer's weight matrix, split by columns")
        self.play(FadeIn(eq), FadeIn(wlab), FadeIn(cols), FadeIn(clabs), FadeIn(cap), run_time=1.5)
        self.wait(0.7)

        boxes, labels = self.devices()
        self.play(Create(boxes), FadeIn(labels), FadeOut(eq), FadeOut(wlab), run_time=1.2)
        anims = []
        for i, b in enumerate(boxes):
            c_target = b.get_center() + LEFT * 0.75 + DOWN * 0.15
            anims.append(cols[i].animate.move_to(c_target))
            anims.append(clabs[i].animate.move_to(c_target + UP * 0.95))
        self.play(*anims, Transform(cap, self.caption("Each device stores one slice, and all get the same input X")),
                  run_time=1.5)
        self.wait(0.5)

        # compute slices
        arrows, ys, ylabs = VGroup(), VGroup(), VGroup()
        for i, b in enumerate(boxes):
            c = cols[i]
            y = Rectangle(width=0.55, height=1.4, stroke_color=ORANGE, stroke_width=2,
                          fill_color=SOFT_ORANGE, fill_opacity=1).move_to(b.get_center() + RIGHT * 0.75 + DOWN * 0.15)
            a = Arrow(c.get_right(), y.get_left(), buff=0.1, stroke_width=3, color=INK,
                      max_tip_length_to_length_ratio=0.3)
            xl = MathTex(f"XW_{i}", font_size=26).next_to(a, UP, buff=0.05)
            yl = MathTex(f"Y_{i}", font_size=30, color=ORANGE).next_to(y, UP, buff=0.1)
            arrows.add(VGroup(a, xl)); ys.add(y); ylabs.add(yl)
        self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.15),
                  LaggedStart(*[FadeIn(y) for y in ys], lag_ratio=0.15),
                  FadeIn(ylabs),
                  Transform(cap, self.caption("Each computes its slice of the output: Y_i = X W_i")),
                  run_time=1.8)
        self.wait(0.8)

        # gather
        ycopy = VGroup(*[VGroup(y, l).copy() for y, l in zip(ys, ylabs)])
        targets = VGroup(*[
            Rectangle(width=0.55, height=1.4, stroke_color=ORANGE, stroke_width=2,
                      fill_color=SOFT_ORANGE, fill_opacity=1)
            for _ in range(4)
        ]).arrange(RIGHT, buff=0).move_to([0.6, 1.9, 0])
        tl = VGroup(*[MathTex(f"Y_{i}", font_size=30, color=ORANGE).next_to(t, UP, buff=0.1) for i, t in enumerate(targets)])
        yfull = MathTex("Y", font_size=44).next_to(targets, LEFT, buff=0.3)
        self.play(*[ReplacementTransform(ycopy[i], VGroup(targets[i], tl[i])) for i in range(4)],
                  FadeIn(yfull),
                  Transform(cap, self.caption("All-gather: the slices are joined into the full output")),
                  run_time=1.8)
        self.wait(0.6)
        self.play(Transform(cap, self.caption("This happens inside every split layer, so it talks a lot")))
        self.wait(1.2)

    # ---------- 3. pipeline parallel ----------
    def pipeline_parallel(self):
        head = self.header("3. Pipeline parallel")
        self.play(FadeIn(head))

        boxes, labels = self.devices(height=1.6)
        boxes.shift(UP * 0.9); labels.shift(UP * 0.9)
        stages = VGroup()
        for i, b in enumerate(boxes):
            r = RoundedRectangle(corner_radius=0.08, width=2.0, height=0.7, stroke_color=BLUE_PEN,
                                 fill_color=SOFT_BLUE, fill_opacity=1, stroke_width=2).move_to(b)
            l = T(f"layers {2*i+1}-{2*i+2}", 24).move_to(r)
            stages.add(VGroup(r, l))
        cap = self.caption("8 layers, cut into 4 stages: 2 layers per device")
        self.play(Create(boxes), FadeIn(labels), LaggedStart(*[FadeIn(s, shift=DOWN * 0.3) for s in stages], lag_ratio=0.2),
                  FadeIn(cap), run_time=1.8)
        arrows = VGroup(*[
            Arrow(boxes[i].get_right(), boxes[i + 1].get_left(), buff=0.05, stroke_width=4, color=ORANGE,
                  max_tip_length_to_length_ratio=0.4)
            for i in range(3)
        ])
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.3),
                  Transform(cap, self.caption("Activations are passed from one stage to the next")), run_time=1.5)
        self.wait(0.8)
        self.play(FadeOut(VGroup(boxes, labels, stages, arrows)),
                  Transform(cap, self.caption("Split the batch into 4 micro-batches and stream them through")))

        # schedule grid: rows = devices, cols = time steps (forward pass)
        P, M = 4, 4
        Tn = P + M - 1
        cw, ch = 1.25, 0.6
        x0 = -3.3
        y0 = 1.6
        cells = {}
        grid = VGroup()
        for d in range(P):
            for t in range(Tn):
                c = Rectangle(width=cw, height=ch, stroke_color=GRAY, stroke_width=1.5)
                c.move_to([x0 + t * cw, y0 - d * ch, 0])
                cells[(d, t)] = c
                grid.add(c)
        rlabs = VGroup(*[T(f"Device {d}", 24).next_to(cells[(d, 0)], LEFT, buff=0.25) for d in range(P)])
        tarrow = Arrow(cells[(P - 1, 0)].get_corner(DL) + DOWN * 0.3, cells[(P - 1, Tn - 1)].get_corner(DR) + DOWN * 0.3,
                       buff=0, stroke_width=3, color=INK, max_tip_length_to_length_ratio=0.03)
        tlab = T("time", 24).next_to(tarrow, DOWN, buff=0.1)
        self.play(Create(grid), FadeIn(rlabs), GrowArrow(tarrow), FadeIn(tlab), run_time=1.5)

        fills = [SOFT_BLUE, SOFT_ORANGE, SOFT_BLUE, SOFT_ORANGE]
        for t in range(Tn):
            step = []
            for d in range(P):
                m = t - d
                if 0 <= m < M:
                    c = cells[(d, t)]
                    blk = Rectangle(width=cw, height=ch, stroke_color=BLUE_PEN, stroke_width=1.5,
                                    fill_color=fills[m], fill_opacity=1).move_to(c)
                    lab = T(f"mb {m+1}", 24).move_to(c)
                    step.append(FadeIn(VGroup(blk, lab)))
            self.play(*step, run_time=0.45)
        self.wait(0.4)

        idle = VGroup()
        for d in range(P):
            for t in range(Tn):
                m = t - d
                if not (0 <= m < M):
                    idle.add(Rectangle(width=cw, height=ch, stroke_width=0, fill_color=GRAY,
                                       fill_opacity=0.45).move_to(cells[(d, t)]))
        self.play(FadeIn(idle),
                  Transform(cap, self.caption("Gray slots are idle: the pipeline bubble (12 of 28 here)")),
                  run_time=1.2)
        self.wait(0.6)
        frac = MathTex(r"\text{idle fraction} = \frac{P-1}{M+P-1} = \frac{3}{7}", font_size=36).move_to([0, -1.9, 0])
        pm = T("P = 4 stages, M = 4 micro-batches (forward pass shown)", 24, color=GRAY).next_to(frac, DOWN, buff=0.2)
        self.play(Write(frac), FadeIn(pm), run_time=1.2)
        self.play(Transform(cap, self.caption("More micro-batches (bigger M) make the bubble smaller")))
        self.wait(1.5)

    # ---------- summary ----------
    def summary(self):
        head = T("Same 4 devices, three ways to split", 36, weight=BOLD).to_edge(UP, buff=0.35)
        data = [
            ("Data parallel", "the batch", "full model", "gradients\n(all-reduce)"),
            ("Tensor parallel", "weights within\na layer", "a slice of each layer", "layer outputs\n(gather, every layer)"),
            ("Pipeline parallel", "the layers", "a few whole layers", "activations\nbetween stages"),
        ]
        cards = VGroup()
        for name, splits, holds, comm in data:
            box = RoundedRectangle(corner_radius=0.15, width=4.0, height=5.1, stroke_color=INK, stroke_width=2)
            t = T(name, 30, weight=BOLD, color=BLUE_PEN)
            k1 = T("splits", 22, color=GRAY)
            v1 = T(splits, 28)
            k2 = T("each device holds", 22, color=GRAY)
            v2 = T(holds, 26)
            k3 = T("communicates", 22, color=GRAY)
            v3 = T(comm, 28, color=ORANGE)
            col = VGroup(t, k1, v1, k2, v2, k3, v3)
            t.move_to(box.get_top() + DOWN * 0.5)
            k1.move_to(box.get_top() + DOWN * 1.15)
            v1.next_to(k1, DOWN, buff=0.12)
            k2.move_to(box.get_top() + DOWN * 2.55)
            v2.next_to(k2, DOWN, buff=0.12)
            k3.move_to(box.get_top() + DOWN * 3.75)
            v3.next_to(k3, DOWN, buff=0.12)
            cards.add(VGroup(box, col))
        cards.arrange(RIGHT, buff=0.3).move_to([0, -0.6, 0])
        self.play(FadeIn(head), run_time=1)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cards], lag_ratio=0.3), run_time=2.2)
        self.wait(4)
