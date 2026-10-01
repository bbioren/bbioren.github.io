"""Why tiling makes matrix multiplication fast.

Render (720p30):
    manim -qm tiled-matmul.py TiledMatmul
"""

from manim import *

config.background_color = "#fdfdfb"

INK = "#1d2a44"
BLUE_PEN = "#2456a6"
ORANGE = "#dd6b20"
SOFT_BLUE = "#bee3f8"
SOFT_ORANGE = "#feebc8"
GRAY = "#a0aec0"
PAPER = "#fdfdfb"
GRID = "#dbe5f2"
MARGIN = "#e9a5a5"

Text.set_default(color=INK, font="Helvetica")
MathTex.set_default(color=INK)

N = 8  # matrix size
T = 4  # tile size
CELL = 0.32
NOTE_POS = np.array([-3.6, -3.4, 0])


def graph_paper():
    lines = VGroup()
    x = -7.5
    while x <= 7.5:
        lines.add(Line([x, -4.5, 0], [x, 4.5, 0], stroke_width=1, color=GRID))
        x += 0.5
    y = -4.5
    while y <= 4.5:
        lines.add(Line([-7.5, y, 0], [7.5, y, 0], stroke_width=1, color=GRID))
        y += 0.5
    margin = Line([-6.6, -4.5, 0], [-6.6, 4.5, 0], stroke_width=2, color=MARGIN)
    return VGroup(lines, margin)


def make_grid(center, n=N, cell=CELL):
    g = VGroup()
    for r in range(n):
        for c in range(n):
            sq = Square(side_length=cell, stroke_color=INK, stroke_width=1.2)
            sq.set_fill(PAPER, opacity=1)
            sq.move_to(
                center + np.array([(c - (n - 1) / 2) * cell, ((n - 1) / 2 - r) * cell, 0])
            )
            g.add(sq)
    return g


def cell(g, r, c, n=N):
    return g[r * n + c]


def block(g, r0, c0, size=T, n=N):
    return VGroup(*[cell(g, r, c, n) for r in range(r0, r0 + size) for c in range(c0, c0 + size)])


def tile_lines(g, n=N, cell_size=CELL):
    """Thick lines on the tile boundaries of a grid."""
    left = g.get_left()[0]
    right = g.get_right()[0]
    top = g.get_top()[1]
    bottom = g.get_bottom()[1]
    lines = VGroup()
    for k in range(0, n + 1, T):
        x = left + k * cell_size
        y = top - k * cell_size
        lines.add(Line([x, top, 0], [x, bottom, 0], stroke_width=4, color=BLUE_PEN))
        lines.add(Line([left, y, 0], [right, y, 0], stroke_width=4, color=BLUE_PEN))
    return lines


class TiledMatmul(Scene):
    def construct(self):
        self.add(graph_paper())

        title = Text("Why tiling makes matrix multiply fast", font_size=40)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=1.5)
        self.wait(1)
        self.play(FadeOut(title))

        # ---------- the three matrices ----------
        c_center = np.array([4.3, -1.3, 0])
        a_center = c_center + np.array([-3.0, 0, 0])
        b_center = c_center + np.array([0, 2.95, 0])
        A = make_grid(a_center)
        B = make_grid(b_center)
        C = make_grid(c_center)
        a_lab = MathTex("A", font_size=40).next_to(A, UP, buff=0.15)
        b_lab = MathTex("B", font_size=40).next_to(B, LEFT, buff=0.2)
        c_lab = MathTex("C", font_size=40).next_to(C, RIGHT, buff=0.2)
        eq = MathTex(r"C = A \cdot B", font_size=36).move_to([1.3, 2.5, 0])
        n_lab = MathTex(r"n = 8", font_size=32).next_to(eq, DOWN, buff=0.3)

        self.play(
            LaggedStart(Create(A), Create(B), Create(C), lag_ratio=0.3),
            FadeIn(a_lab), FadeIn(b_lab), FadeIn(c_lab),
            run_time=2,
        )
        self.play(Write(eq), Write(n_lab), run_time=1)

        # ---------- memory boxes ----------
        slow_box = RoundedRectangle(
            width=5.0, height=1.5, corner_radius=0.15,
            stroke_color=INK, stroke_width=2,
        ).set_fill(GRAY, opacity=0.18).move_to([-3.6, 2.15, 0])
        slow_lab = Text("slow memory (off-chip)", font_size=28).move_to(slow_box.get_center() + UP * 0.25)
        slow_sub = Text("big, but every read is expensive", font_size=24, color=BLUE_PEN)
        slow_sub.next_to(slow_lab, DOWN, buff=0.15)

        counter_lab = Text("reads from slow memory:", font_size=28).move_to([-4.0, -2.7, 0])
        counter = Integer(0, font_size=40, color=ORANGE).next_to(counter_lab, RIGHT, buff=0.25)

        self.play(Create(slow_box), FadeIn(slow_lab), FadeIn(slow_sub), run_time=1.2)
        self.play(FadeIn(counter_lab), FadeIn(counter))
        self.wait(0.5)

        # ---------- naive ----------
        naive_head = Text("Naive: one output at a time", font_size=30, color=BLUE_PEN)
        naive_head.move_to([-3.6, 0.6, 0])
        self.play(FadeIn(naive_head))

        def reset_fill(cells):
            return [m.animate.set_fill(PAPER, opacity=1) for m in cells]

        # first output: sweep slowly over k
        i, j = 1, 2
        self.play(cell(C, i, j).animate.set_fill(ORANGE, opacity=0.8), run_time=0.6)
        for k in range(N):
            self.play(
                cell(A, i, k).animate.set_fill(SOFT_BLUE, opacity=1),
                cell(B, k, j).animate.set_fill(SOFT_BLUE, opacity=1),
                ChangeDecimalToValue(counter, 2 * (k + 1)),
                run_time=0.28,
            )
        note = MathTex(r"n + n = 2n = 16 \text{ reads for one output}", font_size=32)
        note.move_to([-3.6, -0.2, 0])
        self.play(Write(note), run_time=1.2)
        self.wait(0.8)

        # two more outputs, quickly
        done = [cell(C, i, j)]
        for (i2, j2), total in [((1, 3), 32), ((2, 3), 48)]:
            old = [cell(A, i, k) for k in range(N)] + [cell(B, k, j) for k in range(N)]
            self.play(
                *reset_fill(old),
                done[-1].animate.set_fill(SOFT_ORANGE, opacity=1),
                run_time=0.4,
            )
            i, j = i2, j2
            self.play(
                cell(C, i, j).animate.set_fill(ORANGE, opacity=0.8),
                *[cell(A, i, k).animate.set_fill(SOFT_BLUE, opacity=1) for k in range(N)],
                *[cell(B, k, j).animate.set_fill(SOFT_BLUE, opacity=1) for k in range(N)],
                ChangeDecimalToValue(counter, total),
                run_time=0.9,
            )
            done.append(cell(C, i, j))
        self.wait(0.4)

        note2 = MathTex(
            r"\text{all } n^2 \text{ outputs: } 2n \cdot n^2 = 1024 \text{ reads}",
            font_size=32,
        ).next_to(note, DOWN, buff=0.3)
        note3 = Text("The same row of A is read again\nfor every output in that row.",
                     font_size=24, color=ORANGE)
        note3.next_to(note2, DOWN, buff=0.3)
        self.play(Write(note2), run_time=1.2)
        self.play(FadeIn(note3))
        self.wait(1.5)

        old = [cell(A, i, k) for k in range(N)] + [cell(B, k, j) for k in range(N)]
        self.play(
            *reset_fill(old + done),
            FadeOut(note), FadeOut(note2), FadeOut(note3), FadeOut(naive_head),
            ChangeDecimalToValue(counter, 0),
            run_time=1,
        )

        # ---------- tiled ----------
        sram_box = RoundedRectangle(
            width=5.0, height=2.5, corner_radius=0.15,
            stroke_color=ORANGE, stroke_width=3,
        ).set_fill(SOFT_ORANGE, opacity=0.35)
        sram_box.stretch_to_fit_height(2.6).move_to([-3.6, -0.85, 0])
        sram_lab = Text("SRAM / on-chip", font_size=28, color=ORANGE)
        sram_sub = Text("(small, fast)", font_size=24, color=INK)
        VGroup(sram_lab, sram_sub).arrange(RIGHT, buff=0.25).move_to(sram_box.get_top() + DOWN * 0.35)
        load_arrow = Arrow(
            slow_box.get_bottom(), sram_box.get_top(), buff=0.05,
            color=INK, stroke_width=4, max_tip_length_to_length_ratio=0.35,
        )
        tiles_A = tile_lines(A)
        tiles_B = tile_lines(B)
        tiles_C = tile_lines(C)
        t_lab = MathTex(r"T = 4", font_size=32).next_to(n_lab, DOWN, buff=0.2)

        self.play(
            Create(sram_box), FadeIn(sram_lab), FadeIn(sram_sub), GrowArrow(load_arrow),
            run_time=1.2,
        )
        self.play(Create(tiles_A), Create(tiles_B), Create(tiles_C), Write(t_lab), run_time=1.5)
        self.add_foreground_mobjects(tiles_A, tiles_B, tiles_C)

        c_tile = block(C, 0, 0)
        self.play(c_tile.animate.set_fill(SOFT_ORANGE, opacity=1), run_time=0.8)

        small = 0.25
        a_slot = np.array([-4.8, -1.05, 0])
        b_slot = np.array([-2.4, -1.05, 0])
        a_tag = Text("tile of A", font_size=24).next_to(a_slot, DOWN, buff=0.58)
        b_tag = Text("tile of B", font_size=24).next_to(b_slot, DOWN, buff=0.58)

        loaded = VGroup()
        for step in range(N // T):
            k0 = step * T
            a_blk = block(A, 0, k0)
            b_blk = block(B, k0, 0)
            prev = [m for m in loaded]
            anims = [a_blk.animate.set_fill(SOFT_BLUE, opacity=1),
                     b_blk.animate.set_fill(SOFT_BLUE, opacity=1)]
            if step > 0:
                anims += reset_fill(list(block(A, 0, 0)) + list(block(B, 0, 0)))
                anims.append(FadeOut(loaded))
            self.play(*anims, run_time=0.8)

            a_copy = a_blk.copy()
            b_copy = b_blk.copy()
            self.play(
                a_copy.animate.scale(small / CELL).move_to(a_slot),
                b_copy.animate.scale(small / CELL).move_to(b_slot),
                ChangeDecimalToValue(counter, (step + 1) * 2 * T * T),
                *([FadeIn(a_tag), FadeIn(b_tag)] if step == 0 else []),
                run_time=1.5,
            )
            loaded = VGroup(a_copy, b_copy)

            if step == 0:
                load_note = MathTex(r"2T^2 = 32 \text{ reads}", font_size=30)
                load_note.move_to(NOTE_POS)
                self.play(FadeIn(load_note))
                self.wait(0.5)

                # reuse: one value of A feeds a whole row of the C tile
                a_val = a_copy[0]
                row_c = VGroup(*[cell(C, 0, c) for c in range(T)])
                reuse = Text("each loaded value is used T = 4 times", font_size=24, color=ORANGE)
                reuse.move_to(NOTE_POS)
                self.play(
                    a_val.animate.set_fill(ORANGE, opacity=1),
                    cell(A, 0, 0).animate.set_fill(ORANGE, opacity=1),
                    run_time=0.6,
                )
                lines = VGroup(*[
                    Line(cell(A, 0, 0).get_center(), m.get_center(), color=ORANGE, stroke_width=2.5)
                    for m in row_c
                ])
                self.play(
                    LaggedStart(*[Create(l) for l in lines], lag_ratio=0.3),
                    LaggedStart(*[m.animate.set_fill(ORANGE, opacity=0.8) for m in row_c], lag_ratio=0.3),
                    FadeOut(load_note), FadeIn(reuse),
                    run_time=1.6,
                )
                self.wait(1)
                self.play(
                    FadeOut(lines), FadeOut(reuse),
                    a_val.animate.set_fill(SOFT_BLUE, opacity=1),
                    cell(A, 0, 0).animate.set_fill(SOFT_BLUE, opacity=1),
                    *[m.animate.set_fill(SOFT_ORANGE, opacity=1) for m in row_c],
                    run_time=0.8,
                )
                acc = MathTex(r"C_{\text{tile}} \mathrel{+}= A_{\text{tile}} \cdot B_{\text{tile}}",
                              font_size=30)
                acc.move_to(NOTE_POS)
                self.play(Write(acc), c_tile.animate.set_fill(ORANGE, opacity=0.45), run_time=1.2)
                self.wait(0.6)
            else:
                k_note = Text("next k tile, keep accumulating", font_size=24, color=BLUE_PEN)
                k_note.move_to(NOTE_POS)
                self.play(FadeOut(acc), FadeIn(k_note), c_tile.animate.set_fill(ORANGE, opacity=0.85), run_time=1)
                self.wait(1)

        # tally for the tile
        tally = MathTex(
            r"16 \text{ outputs},\ 64 \text{ reads} \Rightarrow 4 \text{ per output}",
            font_size=30,
        ).move_to(NOTE_POS)
        self.play(FadeOut(k_note), run_time=0.5)
        self.play(Write(tally), run_time=1.2)
        self.wait(1.5)

        # ---------- summary ----------
        self.play(
            *[FadeOut(m) for m in [sram_box, sram_lab, sram_sub, load_arrow, loaded, a_tag, b_tag,
                                   tally, slow_box, slow_lab, slow_sub,
                                   counter, counter_lab]],
            *reset_fill(list(block(A, 0, T)) + list(block(B, T, 0))),
            run_time=1,
        )
        s_head = Text("Reads from slow memory per output", font_size=28, color=BLUE_PEN)
        s1 = MathTex(r"\text{naive: }\ 2n", font_size=40)
        s2 = MathTex(r"\text{tiled: }\ \frac{2n}{T}", font_size=40, color=ORANGE)
        s3 = Text("Each load now does T times more work.", font_size=24)
        s4 = Text("Bigger tiles help, up to what fits on chip.", font_size=24, color=BLUE_PEN)
        summary = VGroup(s_head, s1, s2, s3, s4).arrange(DOWN, buff=0.4).move_to([-3.5, 0.2, 0])
        s1.align_to(s_head, LEFT).shift(RIGHT * 0.6)
        s2.align_to(s1, LEFT)
        self.play(FadeIn(s_head))
        self.play(Write(s1), run_time=1)
        self.play(Write(s2), run_time=1)
        self.play(FadeIn(s3))
        self.play(FadeIn(s4))
        self.wait(3)
