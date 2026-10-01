"""Consistent hashing: why a hash ring moves ~1/N of the keys when servers change,
while hash(key) mod N moves most of them.

Render (720p30):
    manim -qm consistent-hashing.py ConsistentHashing
"""

import numpy as np
from manim import *

config.background_color = "#fdfdfb"

INK = "#1d2a44"
BLUE = "#2456a6"
ORANGE = "#dd6b20"
SOFT_BLUE = "#bee3f8"
SOFT_ORANGE = "#feebc8"
GRAY = "#a0aec0"
GRID = "#dbe5f2"
MARGIN = "#e9a5a5"

Text.set_default(color=INK, font="Helvetica")
MathTex.set_default(color=INK)

# Part 1: made-up hash values for 12 keys
HASHES = [17, 42, 8, 33, 61, 25, 90, 14, 76, 53, 39, 68]

# Part 2: positions on the ring, in degrees clockwise from the top
RING_KEYS = [10, 55, 80, 100, 140, 175, 215, 235, 245, 270, 320, 345]
RING_SERVERS = {"A": 30, "B": 120, "C": 200, "D": 290}
NEW_SERVER = ("E", 255)
REMOVED = "B"


def owner(theta, servers):
    """Next server clockwise from theta (inclusive)."""
    after = [(p, s) for s, p in servers.items() if p >= theta]
    if after:
        return min(after)[1]
    return min((p, s) for s, p in servers.items())[1]


class ConsistentHashing(Scene):
    def ring_point(self, theta, r=None):
        r = self.R if r is None else r
        t = np.deg2rad(theta)
        return self.C + r * np.array([np.sin(t), np.cos(t), 0])

    def cw_arc(self, t1, t2, r=None, **kw):
        r = self.R if r is None else r
        span = (t2 - t1) % 360
        return Arc(
            radius=r,
            start_angle=np.deg2rad(90 - t1),
            angle=-np.deg2rad(span),
            arc_center=self.C,
            **kw,
        )

    def construct(self):
        self.background()

        title = Text("Consistent hashing", font_size=48).to_edge(UP, buff=0.5)
        sub = Text("spreading keys across servers", font_size=30, color=BLUE)
        sub.next_to(title, DOWN, buff=0.3)
        self.play(Write(title), FadeIn(sub, shift=0.2 * UP), run_time=1.5)
        self.wait(1)
        self.play(FadeOut(title), FadeOut(sub))

        self.part_mod()
        self.part_ring()
        self.part_vnodes()
        self.part_summary()

    # ------------------------------------------------------------------
    def background(self):
        lines = VGroup()
        for x in np.arange(-7.5, 7.51, 0.5):
            lines.add(Line([x, -4.2, 0], [x, 4.2, 0], stroke_color=GRID, stroke_width=1))
        for y in np.arange(-4.0, 4.01, 0.5):
            lines.add(Line([-7.5, y, 0], [7.5, y, 0], stroke_color=GRID, stroke_width=1))
        margin = Line([-6.4, -4.2, 0], [-6.4, 4.2, 0], stroke_color=MARGIN, stroke_width=2)
        self.add(lines, margin)

    # ------------------------------------------------------------------
    def part_mod(self):
        head = Text("Naive: server = hash(key) mod N", font_size=34).to_edge(UP, buff=0.4)
        self.play(FadeIn(head))

        def col_x(i, n):
            return (i - (n - 1) / 2) * 2.3 + 0.3

        def server_box(i, n):
            box = RoundedRectangle(width=1.7, height=0.6, corner_radius=0.1,
                                   stroke_color=BLUE, fill_color=SOFT_BLUE, fill_opacity=1)
            lab = Text(f"server {i}", font_size=24)
            g = VGroup(box, lab)
            g.move_to([col_x(i, n), 1.9, 0])
            return g

        def slot(col, row, n):
            return np.array([col_x(col, n), 1.05 - 0.62 * row, 0])

        servers = VGroup(*[server_box(i, 4) for i in range(4)])
        n_label = MathTex("N = 4", font_size=36).to_corner(DL, buff=0.6).shift(RIGHT * 0.6)
        self.play(FadeIn(servers), Write(n_label))

        keys = []
        rows = [0] * 4
        for h in HASHES:
            box = RoundedRectangle(width=1.0, height=0.48, corner_radius=0.08,
                                   stroke_color=INK, stroke_width=1.5,
                                   fill_color=WHITE, fill_opacity=1)
            lab = Text(str(h), font_size=24)
            k = VGroup(box, lab)
            s = h % 4
            k.move_to(slot(s, rows[s], 4))
            rows[s] += 1
            keys.append(k)
        cap = Text("12 keys, labeled by their hash", font_size=26, color=BLUE)
        cap.to_edge(DOWN, buff=0.5).shift(RIGHT * 1.2)
        self.play(LaggedStart(*[FadeIn(k, shift=0.2 * DOWN) for k in keys], lag_ratio=0.08),
                  FadeIn(cap), run_time=2)
        self.wait(1)

        # add a fifth server
        new_servers = VGroup(*[server_box(i, 5) for i in range(5)])
        n5 = MathTex("N = 5", font_size=36).move_to(n_label)
        cap2 = Text("add server 4: every key recomputes hash mod 5", font_size=26, color=BLUE)
        cap2.move_to(cap)
        self.play(
            *[Transform(servers[i], new_servers[i]) for i in range(4)],
            FadeIn(new_servers[4], shift=0.3 * LEFT),
            Transform(n_label, n5), Transform(cap, cap2),
            *[k.animate.move_to(k.get_center() + (col_x(h % 4, 5) - col_x(h % 4, 4)) * RIGHT)
              for k, h in zip(keys, HASHES)],
            run_time=1.5,
        )
        self.wait(0.5)

        rows = [0] * 5
        anims = []
        moved = 0
        for k, h in zip(keys, HASHES):
            s = h % 5
            target = slot(s, rows[s], 5)
            rows[s] += 1
            if h % 4 != h % 5:
                moved += 1
                tk = k.copy().move_to(target)
                tk[0].set_fill(SOFT_ORANGE, 1).set_stroke(ORANGE, width=3)
                anims.append(Transform(k, tk, path_arc=-0.6))
            else:
                anims.append(k.animate.move_to(target))
        self.play(*anims, run_time=2)
        result = Text(f"{moved} of 12 keys moved", font_size=30, color=ORANGE, weight=BOLD)
        result.move_to(cap)
        self.play(Transform(cap, result))
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in [head, servers, new_servers[4], n_label, cap, *keys]])
        self.mod_moved = moved

    # ------------------------------------------------------------------
    def part_ring(self):
        self.C = np.array([-2.6, -0.35, 0])
        self.R = 2.3
        head = Text("The hash ring", font_size=36).to_edge(UP, buff=0.4)
        ring = Circle(radius=self.R, stroke_color=INK, stroke_width=3).move_to(self.C)
        self.play(FadeIn(head), Create(ring), run_time=1.5)

        cap = Text("hash servers and keys to spots on a circle", font_size=26, color=BLUE)
        cap.to_edge(DOWN, buff=0.35)

        servers = dict(RING_SERVERS)
        marks = {}
        for s, p in servers.items():
            marks[s] = self.server_mark(s, p)
        dots = [Dot(self.ring_point(t), radius=0.09, color=INK) for t in RING_KEYS]
        self.play(FadeIn(cap), LaggedStart(*[FadeIn(m) for m in marks.values()], lag_ratio=0.2),
                  run_time=1.5)
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.06), run_time=1.5)

        # clockwise rule on one key
        demo_t = 140
        demo = dots[RING_KEYS.index(demo_t)]
        tgt = owner(demo_t, servers)
        arc = self.cw_arc(demo_t, servers[tgt] - 6, r=self.R + 0.22,
                          stroke_color=ORANGE, stroke_width=5)
        arc.add_tip(tip_length=0.18, tip_width=0.18)
        arc.get_tip().set_color(ORANGE)
        cap2 = Text("each key walks clockwise to the next server", font_size=26, color=BLUE)
        cap2.move_to(cap)
        self.play(Transform(cap, cap2), demo.animate.set_color(ORANGE).scale(1.4))
        self.play(Create(arc), run_time=1.5)
        self.wait(0.5)
        self.play(FadeOut(arc), demo.animate.set_color(INK).scale(1 / 1.4))

        # load bars on the right
        bars = self.Bars(self, ["A", "B", "C", "D", "E"], origin=np.array([2.2, -2.3, 0]))
        counts = self.count(servers)
        self.play(FadeIn(bars.frame), *bars.set(counts, show=["A", "B", "C", "D"]), run_time=1.5)
        self.wait(0.5)

        # add server E
        e, ep = NEW_SERVER
        old = {t: owner(t, servers) for t in RING_KEYS}
        servers[e] = ep
        marks[e] = self.server_mark(e, ep)
        new = {t: owner(t, servers) for t in RING_KEYS}
        movers = [d for d, t in zip(dots, RING_KEYS) if old[t] != new[t]]
        prev = max(p for p in servers.values() if p < ep)
        zone = self.cw_arc(prev, ep, stroke_color=ORANGE, stroke_width=9)
        cap3 = Text("add server E", font_size=26, color=BLUE).move_to(cap)
        self.play(Transform(cap, cap3), FadeIn(marks[e], scale=1.5))
        self.play(Create(zone), *[d.animate.set_color(ORANGE).scale(1.4) for d in movers])
        counts = self.count(servers)
        cap4 = Text(f"only keys in one arc move: {len(movers)} of 12, from D to E",
                    font_size=26, color=ORANGE).move_to(cap)
        self.play(Transform(cap, cap4), *bars.set(counts, show=list("ABCDE")), run_time=1.5)
        self.ring_moved = len(movers)
        self.wait(1.5)
        self.play(FadeOut(zone), *[d.animate.set_color(INK).scale(1 / 1.4) for d in movers])

        # remove server B
        r = REMOVED
        old = {t: owner(t, servers) for t in RING_KEYS}
        rp = servers.pop(r)
        new = {t: owner(t, servers) for t in RING_KEYS}
        movers = [d for d, t in zip(dots, RING_KEYS) if old[t] != new[t]]
        heir = new[[t for t in RING_KEYS if old[t] == r][0]]
        prev = max(p for p in servers.values() if p < rp)
        zone = self.cw_arc(prev, rp, stroke_color=ORANGE, stroke_width=9)
        cap5 = Text(f"remove server {r}", font_size=26, color=BLUE).move_to(cap)
        self.play(Transform(cap, cap5), Create(zone),
                  *[d.animate.set_color(ORANGE).scale(1.4) for d in movers])
        self.play(FadeOut(marks.pop(r), scale=0.3))
        counts = self.count(servers)
        counts[r] = 0
        cap6 = Text(f"its {len(movers)} keys go to the next server, {heir}; nothing else moves",
                    font_size=26, color=ORANGE).move_to(cap)
        self.play(Transform(cap, cap6), *bars.set(counts, show=list("ABCDE")), run_time=1.5)
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in [head, ring, zone, cap, bars.group(), *dots,
                                         *marks.values()]])

    def count(self, servers):
        c = {s: 0 for s in "ABCDE"}
        for t in RING_KEYS:
            c[owner(t, servers)] += 1
        return c

    def server_mark(self, name, theta, color=BLUE, fill=SOFT_BLUE, size=0.34):
        sq = Square(side_length=size, stroke_color=color, stroke_width=3,
                    fill_color=fill, fill_opacity=1)
        sq.move_to(self.ring_point(theta)).rotate(-np.deg2rad(theta))
        lab = Text(name, font_size=28, color=color, weight=BOLD)
        lab.move_to(self.ring_point(theta, self.R + 0.5))
        return VGroup(sq, lab)

    class Bars:
        """Vertical bar chart: one bar per server."""

        def __init__(self, scene, names, origin, unit=0.42, gap=0.85, title="keys per server"):
            self.names = names
            self.origin = origin
            self.unit = unit
            self.gap = gap
            width = gap * len(names)
            base = Line(origin + 0.2 * LEFT, origin + width * RIGHT, stroke_color=INK, stroke_width=2)
            t = Text(title, font_size=26).next_to(base, UP, buff=3.3)
            self.labels = VGroup(*[
                Text(n, font_size=26, weight=BOLD, color=BLUE).move_to(self.x(i) + 0.32 * DOWN)
                for i, n in enumerate(names)])
            self.frame = VGroup(base, t)
            self.bars = {}
            self.nums = {}
            for i, n in enumerate(names):
                b = Rectangle(width=0.5, height=0.01, stroke_color=BLUE, stroke_width=2,
                              fill_color=SOFT_BLUE, fill_opacity=1)
                b.move_to(self.x(i), aligned_edge=DOWN)
                self.bars[n] = b
                num = Text("0", font_size=24).next_to(b, UP, buff=0.1)
                self.nums[n] = num
            self.shown = set()

        def x(self, i):
            return self.origin + (i + 0.5) * self.gap * RIGHT - 0.1 * RIGHT

        def group(self):
            return VGroup(self.frame, *[self.labels[i] for i, n in enumerate(self.names) if n in self.shown],
                          *[self.bars[n] for n in self.shown], *[self.nums[n] for n in self.shown])

        def set(self, counts, show, fmt="{}", scale=None):
            anims = []
            for i, n in enumerate(self.names):
                if n not in show:
                    continue
                v = counts.get(n, 0)
                h = max(v * (scale or self.unit), 0.01)
                nb = Rectangle(width=0.5, height=h, stroke_color=BLUE, stroke_width=2,
                               fill_color=SOFT_BLUE, fill_opacity=1)
                nb.move_to(self.x(i), aligned_edge=DOWN)
                nn = Text(fmt.format(v), font_size=24).next_to(nb, UP, buff=0.1)
                if n in self.shown:
                    anims += [Transform(self.bars[n], nb), Transform(self.nums[n], nn)]
                else:
                    self.bars[n].become(nb)
                    self.nums[n].become(nn)
                    anims += [GrowFromEdge(self.bars[n], DOWN), FadeIn(self.nums[n]),
                              FadeIn(self.labels[i])]
                    self.shown.add(n)
            return anims

    # ------------------------------------------------------------------
    def part_vnodes(self):
        head = Text("Virtual nodes", font_size=36).to_edge(UP, buff=0.4)
        ring = Circle(radius=self.R, stroke_color=INK, stroke_width=3).move_to(self.C)
        cap = Text("one spot per server: uneven arcs, uneven load", font_size=26, color=BLUE)
        cap.to_edge(DOWN, buff=0.35)
        styles = {"A": (BLUE, SOFT_BLUE), "B": (ORANGE, SOFT_ORANGE), "C": (INK, "#e2e8f0")}

        single = {"A": [40], "B": [95], "C": [230]}
        many = {"A": [5, 95, 182, 268], "B": [38, 118, 214, 305], "C": [62, 155, 243, 330]}

        def marks_for(layout):
            g = VGroup()
            for s, ps in layout.items():
                c, f = styles[s]
                for p in ps:
                    g.add(self.server_mark(s, p, color=c, fill=f, size=0.3))
            return g

        def shares(layout):
            pts = sorted((p, s) for s, ps in layout.items() for p in ps)
            out = {s: 0 for s in layout}
            for i, (p, s) in enumerate(pts):
                out[s] += (p - pts[i - 1][0]) % 360
            return {s: round(100 * v / 360) for s, v in out.items()}

        bars = self.Bars(self, ["A", "B", "C"], origin=np.array([2.6, -2.3, 0]),
                         gap=1.1, title="share of the ring")
        m1 = marks_for(single)
        self.play(FadeIn(head), Create(ring), FadeIn(cap), run_time=1.2)
        self.play(FadeIn(m1), FadeIn(bars.frame),
                  *bars.set(shares(single), show=list("ABC"), fmt="{}%", scale=0.055),
                  run_time=1.5)
        self.wait(1)

        m2 = marks_for(many)
        cap2 = Text("give each server several spots: the arcs average out",
                    font_size=26, color=BLUE).move_to(cap)
        self.play(Transform(cap, cap2), FadeOut(m1), FadeIn(m2),
                  *bars.set(shares(many), show=list("ABC"), fmt="{}%", scale=0.055),
                  run_time=2)
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in [head, ring, cap, m2, bars.group()]])

    # ------------------------------------------------------------------
    def part_summary(self):
        head = Text("Keys moved when one server is added", font_size=34).to_edge(UP, buff=0.6)

        def panel(name, formula, note, color, fill):
            box = RoundedRectangle(width=5.4, height=3.6, corner_radius=0.2,
                                   stroke_color=color, stroke_width=3,
                                   fill_color=fill, fill_opacity=0.6)
            t = Text(name, font_size=32, weight=BOLD, color=color)
            f = MathTex(formula, font_size=56)
            n = Text(note, font_size=26)
            VGroup(t, f, n).arrange(DOWN, buff=0.45).move_to(box)
            return VGroup(box, t, f, n)

        left = panel("hash(key) mod N", r"\approx \tfrac{N}{N+1}",
                     f"most keys (here {self.mod_moved} of 12)", ORANGE, SOFT_ORANGE)
        right = panel("hash ring", r"\approx \tfrac{1}{N}",
                      f"one arc (here {self.ring_moved} of 12)", BLUE, SOFT_BLUE)
        VGroup(left, right).arrange(RIGHT, buff=0.7).shift(0.4 * DOWN + 0.2 * RIGHT)
        self.play(FadeIn(head))
        self.play(FadeIn(left, shift=0.2 * UP), run_time=1.2)
        self.play(FadeIn(right, shift=0.2 * UP), run_time=1.2)
        self.wait(3)
