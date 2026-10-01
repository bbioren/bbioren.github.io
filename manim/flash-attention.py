"""FlashAttention: computing exact attention without materializing the N x N matrix.

Render (720p30):
    manim -qm flash-attention.py FlashAttention
"""

from manim import *

INK = "#FFFFFF"  # text and structure
PEN = "#58C4DD"  # Manim BLUE_C, main objects
ORANGE = "#F9D84A"  # Manim YELLOW, the highlight
# fills: the stroke color at 0.3 opacity over black, pre-blended so blocks stay
# opaque (moving copies can then slide behind the HBM box cleanly)
SOFT_BLUE = "#1a3b42"
SOFT_ORANGE = "#4b4116"
GRAY = "#a0a0a0"
HBM_FILL = "#161616"
SRAM_FILL = "#1f1b0a"

Text.set_default(color=INK, font="Helvetica")
MathTex.set_default(color=INK)
Tex.set_default(color=INK)


def cell_grid(rows, cols, size, fill, stroke=PEN, opacity=1):
    g = VGroup()
    for r in range(rows):
        for c in range(cols):
            sq = Square(size, stroke_width=1, stroke_color=stroke)
            sq.set_fill(fill, opacity=opacity)
            sq.move_to([c * size, -r * size, 0])
            g.add(sq)
    g.move_to(ORIGIN)
    return g


def block(w, h, fill, label=None, fs=26, stroke=PEN):
    r = Rectangle(width=w, height=h, stroke_color=stroke, stroke_width=2)
    r.set_fill(fill, opacity=1)
    if label is None:
        return VGroup(r)
    t = MathTex(label, font_size=fs).move_to(r)
    return VGroup(r, t)


def column(n_blocks, w, bh, fill, name, highlight=None):
    blocks = VGroup()
    for i in range(n_blocks):
        f = SOFT_ORANGE if highlight == i else fill
        s = ORANGE if highlight == i else PEN
        b = Rectangle(width=w, height=bh, stroke_color=s, stroke_width=2)
        b.set_fill(f, opacity=1)
        blocks.add(b)
    blocks.arrange(DOWN, buff=0)
    lab = MathTex(name, font_size=30).next_to(blocks, UP, buff=0.12)
    return blocks, lab


class FlashAttention(Scene):
    # Calm pacing: every animation is stretched 1.8x (at least 1.5 s) and every
    # pause is at least 1.5 s. Pass raw=True to keep an exact time.
    SLOW = 1.7

    def play(self, *anims, run_time=1.0, raw=False, **kw):
        if not raw:
            run_time = max(1.5, run_time * self.SLOW)
        super().play(*anims, run_time=run_time, **kw)

    def wait(self, duration=1.0, raw=False, **kw):
        if not raw:
            duration = max(1.5, duration * self.SLOW)
        super().wait(duration, **kw)

    def construct(self):

        # ---------- Title ----------
        title = Text("FlashAttention", font_size=56)
        sub = Text("exact attention without the N×N matrix", font_size=30, color=PEN)
        VGroup(title, sub).arrange(DOWN, buff=0.35)
        self.play(Write(title), FadeIn(sub, shift=UP * 0.2), run_time=1.5)
        self.wait(0.7)
        self.play(FadeOut(title), FadeOut(sub))

        # ---------- Part 1: standard attention ----------
        head = Text("Standard attention", font_size=34).to_edge(UP, buff=0.35)
        self.play(FadeIn(head))

        n, cs = 8, 0.34
        S = cell_grid(n, n, cs, SOFT_BLUE).move_to([-2.3, -0.75, 0])
        Q = block(0.5, n * cs, SOFT_BLUE, "Q").next_to(S, LEFT, buff=0.25)
        KT = block(n * cs, 0.5, SOFT_BLUE, "K^\\top").next_to(S, UP, buff=0.25)
        self.play(FadeIn(Q), FadeIn(KT), run_time=1)
        s_lab = MathTex(r"S = QK^\top/\sqrt{d}", font_size=32).next_to(S, DOWN, buff=0.25)
        nn = MathTex(r"N \times N", font_size=30, color=ORANGE).next_to(s_lab, DOWN, buff=0.12)
        self.play(LaggedStartMap(FadeIn, S, lag_ratio=0.01), Write(s_lab), run_time=1.5)
        self.play(FadeIn(nn))

        # HBM box on the right
        hbm = RoundedRectangle(width=4.6, height=4.9, corner_radius=0.15,
                               stroke_color=INK, stroke_width=2)
        hbm.set_fill(HBM_FILL, opacity=1).move_to([4.4, -0.6, 0])
        hbm_lab = Text("HBM (big, slow)", font_size=26).next_to(hbm, UP, buff=0.12)
        self.play(FadeIn(hbm), FadeIn(hbm_lab))

        S_h = S.copy()
        S_target = S.copy().scale(0.45).move_to(hbm.get_center() + LEFT * 1.15 + UP * 0.8)
        self.play(Transform(S_h, S_target), run_time=1.5)
        S_h_lab = MathTex("S", font_size=30).next_to(S_h, DOWN, buff=0.1)
        w1 = Text("write N×N", font_size=24, color=ORANGE).next_to(hbm, DOWN, buff=0.15)
        self.play(FadeIn(S_h_lab), FadeIn(w1))
        self.wait(0.5)

        # softmax: read S back, write P
        P_h = S_h.copy().set_fill(SOFT_ORANGE, opacity=1).set_stroke(ORANGE)
        P_target = P_h.copy().move_to(hbm.get_center() + RIGHT * 1.15 + UP * 0.8)
        arrow_sp = Arrow(S_h.get_right(), P_target.get_left(), buff=0.05,
                         color=INK, stroke_width=3, max_tip_length_to_length_ratio=0.3)
        sm = Text("softmax", font_size=24).next_to(VGroup(S_h, P_target), UP, buff=0.2)
        self.play(GrowArrow(arrow_sp), FadeIn(sm), Transform(P_h, P_target), run_time=1.5)
        P_h_lab = MathTex("P", font_size=30).next_to(P_h, DOWN, buff=0.1)
        w2 = Text("read N×N, write N×N", font_size=24, color=ORANGE).next_to(hbm, DOWN, buff=0.15)
        self.play(FadeIn(P_h_lab), Transform(w1, w2))
        self.wait(0.5)

        # O = P V
        pv = MathTex(r"O = P\,V", font_size=34).move_to(hbm.get_center() + DOWN * 1.35)
        w3 = Text("read N×N again", font_size=24, color=ORANGE).next_to(hbm, DOWN, buff=0.15)
        self.play(Write(pv), Transform(w1, w3), run_time=1.2)
        self.wait(0.5)
        cost = MathTex(r"\text{memory } O(N^2)", font_size=36, color=ORANGE)
        cost.next_to(nn, DOWN, buff=0.15)
        cost.move_to([S.get_center()[0], -3.55, 0])
        self.play(FadeOut(nn), Write(cost))
        self.wait(3, raw=True)

        self.play(*[FadeOut(m) for m in [head, S, Q, KT, s_lab, hbm, hbm_lab, S_h, S_h_lab,
                                         P_h, P_h_lab, arrow_sp, sm, pv, w1, cost]], run_time=1.2, raw=True)

        # ---------- Part 2: FlashAttention tiling ----------
        head2 = Text("FlashAttention: tile and stream", font_size=34).to_edge(UP, buff=0.35)
        self.play(FadeIn(head2))

        hbm2 = RoundedRectangle(width=5.0, height=5.6, corner_radius=0.15,
                                stroke_color=INK, stroke_width=2)
        hbm2.set_fill(HBM_FILL, opacity=1).move_to([-3.75, -0.75, 0])
        hbm2_lab = Text("HBM (big, slow)", font_size=26).next_to(hbm2, UP, buff=0.1)
        sram = RoundedRectangle(width=6.2, height=5.6, corner_radius=0.15,
                                stroke_color=ORANGE, stroke_width=3)
        sram.set_fill(SRAM_FILL, opacity=1).move_to([3.2, -0.75, 0])
        sram_lab = Text("SRAM (on-chip, small, fast)", font_size=26, color=ORANGE)
        sram_lab.next_to(sram, UP, buff=0.1)

        nb, bw, bh = 4, 0.6, 1.0
        Qc, Ql = column(nb, bw, bh, SOFT_BLUE, "Q", highlight=1)
        Kc, Kl = column(nb, bw, bh, SOFT_BLUE, "K")
        Vc, Vl = column(nb, bw, bh, SOFT_BLUE, "V")
        Oc, Ol = column(nb, bw, bh, "#000000", "O")
        cols = VGroup(VGroup(Qc, Ql), VGroup(Kc, Kl), VGroup(Vc, Vl), VGroup(Oc, Ol))
        cols.arrange(RIGHT, buff=0.45).move_to(hbm2.get_center() + DOWN * 0.15)

        self.play(FadeIn(hbm2), FadeIn(hbm2_lab), FadeIn(sram), FadeIn(sram_lab), run_time=1)
        self.play(FadeIn(cols), run_time=1)
        # moving copies pass behind the HBM box instead of over the O column
        hbm2.set_z_index(1)
        hbm2_lab.set_z_index(1)
        cols.set_z_index(2)

        # Q block moves on-chip and stays
        q_on = VGroup(Qc[1].copy(), MathTex("Q_i", font_size=28))
        q_dest = sram.get_left() + RIGHT * 0.85 + UP * 1.5
        q_on[1].move_to(q_dest)
        q_box = Qc[1].copy()
        self.play(q_box.animate.move_to(q_dest), run_time=1.2)
        q_lab = MathTex("Q_i", font_size=28).move_to(q_box).set_z_index(3)
        stays = Text("stays\non-chip", font_size=24, color=ORANGE, line_spacing=0.8).next_to(q_box, DOWN, buff=0.22)
        self.play(FadeIn(q_lab), FadeIn(stays))

        # running statistics panel
        stats = VGroup(
            MathTex(r"m_i \text{ (running max)}", font_size=28),
            MathTex(r"\ell_i \text{ (running sum)}", font_size=28),
            MathTex(r"O_i \text{ (running output)}", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        stats.move_to(sram.get_center() + DOWN * 1.65 + RIGHT * 0.2)
        stats_box = SurroundingRectangle(stats, color=PEN, buff=0.15, stroke_width=2)
        self.play(FadeIn(stats), Create(stats_box), run_time=1)

        k_dest = sram.get_center() + LEFT * 0.75 + UP * 1.5
        v_dest = sram.get_center() + LEFT * 0.0 + UP * 1.5
        tile_center = sram.get_center() + RIGHT * 1.75 + UP * 1.5
        counter = None
        for j in range(nb):
            kb = Kc[j].copy().set_stroke(ORANGE)
            vb = Vc[j].copy().set_stroke(ORANGE)
            kb.set_z_index(0)
            vb.set_z_index(0)
            rt = 1.5 if j else 2.0
            self.play(kb.animate.move_to(k_dest), vb.animate.move_to(v_dest),
                      Kc[j].animate.set_fill(SOFT_ORANGE), Vc[j].animate.set_fill(SOFT_ORANGE),
                      run_time=rt, raw=True)
            kl = MathTex(f"K_{j + 1}", font_size=26).move_to(kb)
            vl = MathTex(f"V_{j + 1}", font_size=26).move_to(vb)
            tile = cell_grid(3, 3, 0.33, SOFT_ORANGE, stroke=ORANGE).move_to(tile_center)
            tl = MathTex(r"S_{ij}", font_size=26).next_to(tile, DOWN, buff=0.1)
            new_counter = Text(f"block {j + 1} of {nb}", font_size=24, color=PEN)
            new_counter.next_to(stats_box, UP, buff=0.15).align_to(stats_box, RIGHT)
            anims = [FadeIn(kl), FadeIn(vl), FadeIn(tile), FadeIn(tl),
                     Indicate(stats, color=ORANGE, scale_factor=1.04)]
            if counter is None:
                anims.append(FadeIn(new_counter))
                counter = new_counter
            else:
                anims.append(Transform(counter, new_counter))
            self.play(*anims, run_time=1.5, raw=True)
            if j == 0:
                note = Text("tile lives\nonly here", font_size=24, color=ORANGE, line_spacing=0.8)
                note.next_to(tl, DOWN, buff=0.08)
                self.play(FadeIn(note), run_time=0.8)
                self.wait(0.6)
                self.play(FadeOut(note), run_time=0.5)
            self.play(*[FadeOut(m) for m in [kb, vb, kl, vl, tile, tl]],
                      Kc[j].animate.set_fill(SOFT_BLUE), Vc[j].animate.set_fill(SOFT_BLUE),
                      run_time=1.2, raw=True)

        # write O_i back once
        o_out = Rectangle(width=bw, height=bh, stroke_color=ORANGE, stroke_width=2)
        o_out.set_fill(SOFT_ORANGE, opacity=1).move_to(stats_box.get_left() + LEFT * 0.55)
        o_out.set_z_index(3)
        self.play(FadeIn(o_out), run_time=0.5)
        self.play(o_out.animate.move_to(Oc[1]), run_time=1.2)
        oil = MathTex(r"O_i/\ell_i", font_size=22).move_to(Oc[1]).set_z_index(4)
        wr = Text("written once", font_size=24, color=ORANGE).set_z_index(3)
        wr.move_to([hbm2.get_center()[0], Oc.get_bottom()[1] - 0.25, 0])
        self.play(FadeIn(oil), FadeIn(wr))
        self.wait(3, raw=True)

        self.play(*[FadeOut(m) for m in [head2, hbm2, hbm2_lab, sram, sram_lab, cols, q_box,
                                         q_lab, stays, stats, stats_box, counter, o_out, oil, wr]], run_time=1.2, raw=True)

        # ---------- Part 3: online softmax math ----------
        head3 = Text("Online softmax, one new block", font_size=34).to_edge(UP, buff=0.35)
        self.play(FadeIn(head3))

        init = MathTex(r"\text{start: } m = -\infty,\quad \ell = 0,\quad O = 0",
                       font_size=32, color=PEN)
        e1 = MathTex(r"S_j = Q_i K_j^\top/\sqrt{d}", font_size=36)
        e2 = MathTex(r"m_{\text{new}} = \max\big(m_{\text{old}},\ \mathrm{rowmax}(S_j)\big)",
                     font_size=36)
        e3 = MathTex(r"\ell_{\text{new}} = ", r"e^{m_{\text{old}} - m_{\text{new}}}",
                     r"\,\ell_{\text{old}} + \mathrm{rowsum}\big(e^{S_j - m_{\text{new}}}\big)",
                     font_size=36)
        e4 = MathTex(r"O_{\text{new}} = ", r"e^{m_{\text{old}} - m_{\text{new}}}",
                     r"\,O_{\text{old}} + e^{S_j - m_{\text{new}}}\,V_j", font_size=36)
        e5 = MathTex(r"\text{after the last block: } O_i = O / \ell", font_size=34, color=PEN)
        eqs = VGroup(init, e1, e2, e3, e4, e5).arrange(DOWN, buff=0.32)
        eqs.move_to(DOWN * 0.15)
        for e in [init, e1, e2, e3, e4, e5]:
            e.align_to(eqs, LEFT)
        eqs.move_to(DOWN * 0.15)

        self.play(FadeIn(init), run_time=0.8)
        self.play(Write(e1), run_time=2.5, raw=True)
        self.play(Write(e2), run_time=2.5, raw=True)
        self.play(Write(e3), run_time=3, raw=True)
        self.wait(1.5, raw=True)
        self.play(Write(e4), run_time=3, raw=True)
        self.wait(3, raw=True)
        self.play(e3[1].animate.set_color(ORANGE), e4[1].animate.set_color(ORANGE))
        boxes = VGroup(SurroundingRectangle(e3[1], color=ORANGE, buff=0.06),
                       SurroundingRectangle(e4[1], color=ORANGE, buff=0.06))
        why = Text("a new max shrinks the old terms to the new scale",
                   font_size=26, color=ORANGE).to_edge(DOWN, buff=0.3)
        self.play(Create(boxes), FadeIn(why), run_time=1)
        self.wait(3, raw=True)
        ex = MathTex(r"\text{e.g. } m: 3 \to 5 \;\Rightarrow\; \ell, O \text{ times } e^{3-5}",
                     font_size=30, color=ORANGE).to_edge(DOWN, buff=0.3)
        self.play(Transform(why, ex), run_time=2.5, raw=True)
        self.wait(3, raw=True)
        self.play(Write(e5), run_time=2.5, raw=True)
        self.wait(3, raw=True)
        self.play(*[FadeOut(m) for m in [head3, eqs, boxes, why]], run_time=1.2, raw=True)

        # ---------- Part 4: summary ----------
        head4 = Text("Same answer, less memory traffic", font_size=36).to_edge(UP, buff=0.5)
        r1 = MathTex(r"\text{Exact: } O = \mathrm{softmax}\!\big(QK^\top/\sqrt{d}\big)\,V",
                     r"\text{ (no approximation)}", font_size=34)
        r1[1].set_color(GRAY)
        r2 = MathTex(r"\text{Extra memory: }", r"O(N)", r"\text{ (}m,\ell\text{ per row) instead of }",
                     r"O(N^2)", font_size=34)
        r2[1].set_color(ORANGE)
        r3 = MathTex(r"\text{The } N\times N \text{ matrix never touches HBM}", font_size=34)
        r4 = MathTex(r"\Rightarrow \text{ far fewer HBM reads and writes}", font_size=34,
                     color=PEN)
        rows = VGroup(r1, r2, r3, r4).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        rows.move_to(DOWN * 0.1)
        card = SurroundingRectangle(rows, color=INK, buff=0.4, stroke_width=2,
                                    corner_radius=0.12)
        card.set_fill("#000000", opacity=0.85)
        self.play(FadeIn(head4))
        self.play(FadeIn(card))
        for r in [r1, r2, r3, r4]:
            self.play(FadeIn(r, shift=RIGHT * 0.2), run_time=1)
            self.wait(1.5, raw=True)
        self.wait(5, raw=True)
