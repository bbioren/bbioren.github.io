"""How a weight-stationary systolic array multiplies matrices.

Render (720p30):
    manim -qm systolic-array.py SystolicArray
"""

from manim import *

config.background_color = "#fdfdfb"

INK = "#1d2a44"
PEN = "#2456a6"
ORANGE = "#dd6b20"
SOFT_BLUE = "#bee3f8"
SOFT_ORANGE = "#feebc8"
GRAY = "#a0aec0"
GRID = "#dbe5f2"
MARGIN = "#e9a5a5"

Text.set_default(color=INK, font="Helvetica")
MathTex.set_default(color=INK)

# Y = X W with two input rows and a 4x4 weight matrix.
X = [[1, 2, 1, 3], [2, 1, 3, 1]]
W = [[1, 0, 2, 1], [2, 1, 0, 1], [0, 3, 1, 2], [1, 1, 0, 2]]
M, N = len(X), 4

CELL = 1.1
GRID_CENTER = np.array([-0.4, 0.55, 0])
GRID_LEFT = GRID_CENTER[0] - 2 * CELL
GRID_TOP = GRID_CENTER[1] + 2 * CELL
GRID_BOTTOM = GRID_CENTER[1] - 2 * CELL

TOKEN_FILL = [SOFT_ORANGE, SOFT_BLUE]
TOKEN_EDGE = [ORANGE, PEN]


def cell_center(k, c):
    return np.array([GRID_LEFT + (c + 0.5) * CELL, GRID_TOP - (k + 0.5) * CELL, 0])


def act_pos(m, k, t):
    """Where activation x[m][k] sits at cycle t (column c = t - m - k)."""
    c = t - m - k
    y = cell_center(k, 0)[1] - 0.03
    if c < 0:
        return np.array([GRID_LEFT - 0.4 - 0.62 * (-c - 1), y, 0])
    return np.array([GRID_LEFT + (c + 0.5) * CELL - 0.26, y, 0])


def psum_value(m, n, r):
    return sum(X[m][j] * W[j][n] for j in range(r + 1))


def psum_pos(m, n, r):
    if r <= 3:
        return cell_center(r, n) + np.array([0.28, -0.42, 0])
    return np.array([cell_center(0, n)[0], GRID_BOTTOM - 0.5 - 0.55 * m, 0])


class SystolicArray(Scene):
    def graph_paper(self):
        lines = VGroup()
        x = -7.5
        while x <= 7.5:
            lines.add(Line([x, -4.5, 0], [x, 4.5, 0], stroke_width=1, color=GRID))
            x += 0.5
        y = -4.5
        while y <= 4.5:
            lines.add(Line([-7.5, y, 0], [7.5, y, 0], stroke_width=1, color=GRID))
            y += 0.5
        lines.add(Line([-6.6, -4.5, 0], [-6.6, 4.5, 0], stroke_width=1.5, color=MARGIN))
        self.add(lines)

    def token(self, m, k):
        circ = Circle(radius=0.19, color=TOKEN_EDGE[m], stroke_width=2.5)
        circ.set_fill(TOKEN_FILL[m], opacity=1)
        lab = Text(str(X[m][k]), font_size=24)
        return VGroup(circ, lab)

    def psum_label(self, m, n, r):
        return Text(str(psum_value(m, n, r)), font_size=26, weight=BOLD, color=TOKEN_EDGE[m])

    def construct(self):
        self.graph_paper()

        # ---- title -------------------------------------------------------
        title = Text("How a systolic array multiplies matrices", font_size=40)
        sub = Text("the core of ML accelerators", font_size=28, color=PEN)
        head = VGroup(title, sub).arrange(DOWN, buff=0.3)
        self.play(FadeIn(head, shift=UP * 0.2), run_time=1.2)
        self.wait(1)
        self.play(FadeOut(head), run_time=0.8)

        # ---- right panel -------------------------------------------------
        px = 4.75
        eq = MathTex(r"Y = X\,W", font_size=44).move_to([px, 3.1, 0])
        dims = Text("X: 2 rows of 4    W: 4 x 4", font_size=24, color=PEN)
        dims.next_to(eq, DOWN, buff=0.2)
        self.play(Write(eq), FadeIn(dims), run_time=1.2)

        steps_txt = [
            "1. Weights load into\n    cells and stay put",
            "2. Inputs enter from the\n    left, skewed 1 cycle/row",
            "3. Each cell multiplies,\n    adds, passes sum down",
            "4. Finished sums exit\n    the bottom: rows of Y",
        ]
        steps = VGroup(
            *[Text(s, font_size=24, line_spacing=0.9, color=GRAY) for s in steps_txt]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        steps.move_to([px, -0.55, 0])

        # ---- grid of MAC cells ------------------------------------------
        cells = VGroup()
        for k in range(4):
            for c in range(4):
                sq = Square(CELL, color=INK, stroke_width=2)
                sq.set_fill(SOFT_BLUE, opacity=0.25)
                sq.move_to(cell_center(k, c))
                cells.add(sq)
        cell_cap = Text("4 x 4 multiply-accumulate cells", font_size=24, color=PEN)
        cell_cap.next_to(cells, UP, buff=0.12)
        self.play(Create(cells), FadeIn(cell_cap), run_time=1.5)
        self.wait(0.5)

        # step 1: weights
        wlabels = VGroup()
        for k in range(4):
            for c in range(4):
                w = Text(f"w {W[k][c]}", font_size=22, color=INK)
                w.move_to(cell_center(k, c) + np.array([-0.24, 0.37, 0]))
                wlabels.add(w)
        steps[0].set_color(ORANGE)
        self.play(FadeIn(steps[0]), LaggedStartMap(FadeIn, wlabels, lag_ratio=0.05), run_time=1.8)
        self.wait(0.8)

        # step 2: skewed inputs
        tokens = {}
        t0 = -1
        for m in range(M):
            for k in range(4):
                tok = self.token(m, k).move_to(act_pos(m, k, t0))
                tokens[(m, k)] = tok
        row_labels = VGroup(
            MathTex("x_0", font_size=36, color=ORANGE),
            MathTex("x_1", font_size=36, color=PEN),
        )
        legend = VGroup(
            Text("input row", font_size=24, color=INK), row_labels[0], row_labels[1]
        ).arrange(RIGHT, buff=0.2)
        legend.move_to([GRID_LEFT - 2.0, GRID_TOP + 0.35, 0])
        steps[1].set_color(ORANGE)
        self.play(
            steps[0].animate.set_color(INK),
            FadeIn(steps[1]),
            FadeOut(cell_cap),
            LaggedStart(*[FadeIn(tokens[(m, k)], shift=RIGHT * 0.3)
                          for k in range(4) for m in range(M)], lag_ratio=0.08),
            FadeIn(legend),
            run_time=2,
        )
        self.wait(1)

        # output row labels
        out_labels = VGroup(
            MathTex("y_0", font_size=36, color=ORANGE).move_to([GRID_LEFT - 0.45, GRID_BOTTOM - 0.5, 0]),
            MathTex("y_1", font_size=36, color=PEN).move_to([GRID_LEFT - 0.45, GRID_BOTTOM - 1.05, 0]),
        )

        # cycle counter
        cyc_word = Text("cycle", font_size=30, color=INK)
        cyc_num = Text("0", font_size=30, color=ORANGE, weight=BOLD)
        cyc_group = VGroup(cyc_word, cyc_num).arrange(RIGHT, buff=0.2)
        cyc_group.move_to([GRID_CENTER[0], GRID_BOTTOM - 1.75 + 0.0, 0])
        cyc_group.move_to([px, -3.3, 0])

        psums = {}
        t_last = (M - 1) + 3 + 4
        for t in range(0, t_last + 1):
            # phase A1: tokens step right (partial sums sit still in the bottom band)
            move = []
            for (m, k), tok in list(tokens.items()):
                c = t - m - k
                if c == 4:
                    move.append(FadeOut(tok, target_position=act_pos(m, k, t) + RIGHT * 0.2))
                    del tokens[(m, k)]
                elif c < 4:
                    move.append(tok.animate.move_to(act_pos(m, k, t)))
            if t == 0:
                move.append(FadeIn(cyc_group))
            else:
                cyc_num.become(
                    Text(str(t), font_size=30, color=ORANGE, weight=BOLD).move_to(cyc_num)
                )
            if t == 2:
                move += [steps[1].animate.set_color(INK), FadeIn(steps[2])]
                steps[2].set_color(ORANGE)
            if t == 4:
                move += [steps[2].animate.set_color(INK), FadeIn(steps[3]), FadeIn(out_labels)]
                steps[3].set_color(ORANGE)
            slow = 0.8 if t < 3 else 0.5
            self.play(*move, run_time=slow)

            # phase A2: partial sums step down (tokens sit still on the left)
            down = []
            for (m, n), lab in psums.items():
                r = t - m - n
                if 1 <= r <= 4:
                    down.append(lab.animate.move_to(psum_pos(m, n, r)))
            if down:
                self.play(*down, run_time=slow)

            # phase B: active cells multiply and add
            compute = []
            active = []
            for m in range(M):
                for n in range(N):
                    r = t - m - n
                    if 0 <= r <= 3:
                        active.append(cells[r * 4 + n])
                        new = self.psum_label(m, n, r).move_to(psum_pos(m, n, r))
                        if (m, n) in psums:
                            compute.append(Transform(psums[(m, n)], new))
                        else:
                            psums[(m, n)] = new
                            compute.append(FadeIn(new, scale=0.6))
            if compute:
                flash = [c.animate.set_fill(SOFT_ORANGE, opacity=0.9) for c in active]
                self.play(*compute, *flash, run_time=0.7 if t < 3 else 0.5)
                self.play(*[c.animate.set_fill(SOFT_BLUE, opacity=0.25) for c in active],
                          run_time=0.25)
            self.wait(0.6 if t < 3 else 0.15)

        self.play(steps[3].animate.set_color(INK), run_time=0.5)

        # check against Y = X W
        ycheck = MathTex(
            r"y_n = \sum_{k} x_k\, w_{kn}", font_size=36
        ).move_to([px, -3.3, 0])
        box = SurroundingRectangle(
            VGroup(*[psums[(m, n)] for m in range(M) for n in range(N)]),
            color=ORANGE, buff=0.12, corner_radius=0.08,
        )
        self.play(Create(box), FadeOut(cyc_group), FadeIn(ycheck), run_time=1.2)
        self.wait(2)

        # ---- zoom out to an accelerator ---------------------------------
        keep = cells
        others = VGroup(
            wlabels, out_labels, legend, box, eq, dims, steps, ycheck,
            *psums.values(), *tokens.values(),
        )
        self.play(FadeOut(others), run_time=1)

        def block(label, w, h, fill, pos):
            r = RoundedRectangle(width=w, height=h, corner_radius=0.15, color=INK, stroke_width=2.5)
            r.set_fill(fill, opacity=0.6).move_to(pos)
            t = VGroup(*[Text(l, font_size=24, color=INK) for l in label.split("\n")])
            t.arrange(DOWN, buff=0.14)
            if t.width > w - 0.3:
                t.scale_to_fit_width(w - 0.3)
            t.move_to(r)
            return VGroup(r, t)

        y0 = 0.9
        sram = block("on-chip\nSRAM buffer", 2.0, 3.2, SOFT_ORANGE, [-5.4, y0, 0])
        arr_box = RoundedRectangle(width=2.6, height=3.2, corner_radius=0.15, color=INK, stroke_width=2.5)
        arr_box.set_fill(SOFT_BLUE, opacity=0.25).move_to([-1.8, y0, 0])
        arr_lab = Text("systolic array", font_size=24, color=PEN).next_to(arr_box, DOWN, buff=0.15)
        acc = block("accumulation\nbuffer", 2.2, 1.4, SOFT_ORANGE, [1.55, y0, 0])
        vec = block("vector unit", 2.0, 1.4, SOFT_BLUE, [5.2, y0, 0])

        self.play(
            cells.animate.scale(0.5).move_to(arr_box.get_center() + UP * 0.1),
            run_time=1.5,
        )
        self.play(FadeIn(arr_box), FadeIn(arr_lab), run_time=0.8)

        def arrow(a, b, **kw):
            return Arrow(a, b, buff=0.08, color=INK, stroke_width=3,
                         max_tip_length_to_length_ratio=0.25, **kw)

        a1 = arrow(sram.get_right() + UP * 0.6, arr_box.get_left() + UP * 0.6)
        a1b = arrow(sram.get_right() + DOWN * 0.6, arr_box.get_left() + DOWN * 0.6)
        l1 = Text("weights", font_size=24, color=GRAY).next_to(a1, UP, buff=0.08)
        l1b = Text("inputs", font_size=24, color=GRAY).next_to(a1b, UP, buff=0.08)
        a2 = arrow(arr_box.get_right(), acc.get_left())
        a3 = arrow(acc.get_right(), vec.get_left())

        self.play(FadeIn(sram), Create(a1), Create(a1b), FadeIn(l1), FadeIn(l1b), run_time=1.3)
        self.wait(0.4)
        self.play(Create(a2), FadeIn(acc), run_time=1.2)
        acc_note = Text("partial sums add up\nacross tiles here", font_size=24,
                        line_spacing=0.9, color=PEN).next_to(acc, UP, buff=0.3)
        self.play(FadeIn(acc_note), run_time=0.8)
        self.wait(0.6)
        self.play(Create(a3), FadeIn(vec), run_time=1.2)
        vec_note = Text("elementwise ops:\nadd, ReLU, scale", font_size=24,
                        line_spacing=0.9, color=PEN).next_to(vec, UP, buff=0.3)
        self.play(FadeIn(vec_note), run_time=0.8)

        # results go back to SRAM
        bot = y0 - 2.5
        back = VMobject(color=ORANGE, stroke_width=3).set_points_as_corners([
            vec.get_bottom() + DOWN * 0.05,
            [vec.get_center()[0], bot, 0],
            [sram.get_center()[0], bot, 0],
        ])
        back_tip = Arrow([sram.get_center()[0], bot, 0], sram.get_bottom() + DOWN * 0.05,
                         buff=0, color=ORANGE, stroke_width=3,
                         max_tip_length_to_length_ratio=0.5)
        back_lab = Text("results written back for the next layer", font_size=24, color=ORANGE)
        back_lab.next_to([0, bot, 0], DOWN, buff=0.12)
        self.play(Create(back), run_time=1.2)
        self.play(Create(back_tip), FadeIn(back_lab), run_time=0.8)
        self.wait(0.8)

        trn = VGroup(
            Text("AWS Trainium's NeuronCore: a systolic-array tensor engine,", font_size=26),
            Text("plus vector and scalar engines", font_size=26),
        ).arrange(DOWN, buff=0.16).move_to([0, -3.2, 0])
        self.play(FadeIn(trn, shift=UP * 0.2), run_time=1.2)
        self.wait(3)
