from manim import *
import numpy as np


class FourierCirclesDrawing(Scene):
    """Spinning circles (epicycles) that trace out a path — the classic
    3Blue1Brown Fourier series visualization."""

    def construct(self):
        self.camera.background_color = "#1a1a2e"

        # Define a path to trace — a treble clef-inspired curve
        points = self.get_path_points()
        coeffs = self.get_fourier_coefficients(points, n_terms=40)

        # Sort by magnitude so largest circles come first
        coeffs.sort(key=lambda c: -abs(c[1]))

        # Draw the traced path first as a ghost
        ghost_path = VMobject(stroke_color=BLUE_B, stroke_opacity=0.15, stroke_width=1.5)
        ghost_dots = [self.coeff_to_point(coeffs, t / 300) for t in range(300)]
        ghost_path.set_points_smoothly(
            [np.array([p[0], p[1], 0]) for p in ghost_dots]
        )
        self.add(ghost_path)

        # Title
        title = Text("Fourier Series", font_size=36, color=WHITE, font="sans-serif")
        title.to_corner(UL, buff=0.4)
        subtitle = Text("Epicycles tracing a shape", font_size=20, color=GREY_B, font="sans-serif")
        subtitle.next_to(title, DOWN, aligned_edge=LEFT, buff=0.15)
        self.play(FadeIn(title, shift=DOWN * 0.2), FadeIn(subtitle, shift=DOWN * 0.2), run_time=1)

        # Animate the epicycles
        n_steps = 400
        traced = VMobject(stroke_color=TEAL_A, stroke_width=2.5)
        traced_points = []
        dot = Dot(radius=0.06, color=YELLOW)

        circles = VGroup()
        radii_lines = VGroup()
        n_circles = len(coeffs)

        for _ in range(n_circles):
            c = Circle(stroke_width=1, stroke_color=BLUE_D, stroke_opacity=0.35)
            circles.add(c)
            line = Line(ORIGIN, RIGHT, stroke_width=1.5, stroke_color=WHITE, stroke_opacity=0.5)
            radii_lines.add(line)

        self.add(circles, radii_lines, traced, dot)

        for step in range(n_steps):
            t = step / n_steps
            center = np.array([0.0, 0.0, 0.0])

            for i, (freq, amp, phase) in enumerate(coeffs):
                radius = abs(amp)
                angle = 2 * np.pi * freq * t + phase

                circles[i].become(
                    Circle(radius=radius, stroke_width=1, stroke_color=BLUE_D, stroke_opacity=0.3)
                    .move_to(center)
                )
                end = center + np.array([radius * np.cos(angle), radius * np.sin(angle), 0])
                radii_lines[i].become(
                    Line(center, end, stroke_width=1.5, stroke_color=WHITE, stroke_opacity=0.45)
                )
                center = end

            dot.move_to(center)
            traced_points.append(center.copy())

            if len(traced_points) > 1:
                traced.become(
                    VMobject(stroke_color=TEAL_A, stroke_width=2.5)
                    .set_points_smoothly(traced_points[-200:])
                )

            self.wait(1 / 60)

        self.play(FadeOut(circles), FadeOut(radii_lines), run_time=0.8)
        self.play(traced.animate.set_stroke(color=TEAL_B, width=3, opacity=1), run_time=1)
        self.wait(1)

    def get_path_points(self):
        """Generate a star-like path."""
        points = []
        n = 300
        for i in range(n):
            t = 2 * np.pi * i / n
            # 5-pointed star with smooth lobes
            r = 2.0 + 0.8 * np.cos(5 * t) + 0.3 * np.sin(3 * t)
            x = r * np.cos(t)
            y = r * np.sin(t)
            points.append(complex(x, y))
        return points

    def get_fourier_coefficients(self, points, n_terms=30):
        N = len(points)
        coeffs = []
        for n in range(-n_terms, n_terms + 1):
            c = sum(p * np.exp(-2j * np.pi * n * k / N) for k, p in enumerate(points)) / N
            coeffs.append((n, abs(c), np.angle(c)))
        return coeffs

    def coeff_to_point(self, coeffs, t):
        x, y = 0.0, 0.0
        for freq, amp, phase in coeffs:
            angle = 2 * np.pi * freq * t + phase
            x += amp * np.cos(angle)
            y += amp * np.sin(angle)
        return (x, y)


class TransformingShapes(Scene):
    """Smooth morphing between geometric shapes with a 3b1b aesthetic."""

    def construct(self):
        self.camera.background_color = "#1a1a2e"

        title = Text("Geometric Transformations", font_size=36, color=WHITE, font="sans-serif")
        title.to_corner(UL, buff=0.4)
        self.play(Write(title), run_time=1)

        circle = Circle(radius=2, color=TEAL_B, fill_opacity=0.2, stroke_width=3)
        square = Square(side_length=4, color=BLUE_B, fill_opacity=0.2, stroke_width=3)
        triangle = Triangle(color=GOLD_B, fill_opacity=0.2, stroke_width=3).scale(2.3)
        star = Star(n=5, outer_radius=2.5, inner_radius=1.0, color=MAROON_B, fill_opacity=0.2, stroke_width=3)

        label = Text("Circle", font_size=28, color=TEAL_B, font="sans-serif").to_edge(DOWN, buff=0.5)
        self.play(Create(circle), FadeIn(label), run_time=1.5)
        self.wait(0.5)

        new_label = Text("Square", font_size=28, color=BLUE_B, font="sans-serif").to_edge(DOWN, buff=0.5)
        self.play(Transform(circle, square), Transform(label, new_label), run_time=1.5)
        self.wait(0.5)

        new_label2 = Text("Triangle", font_size=28, color=GOLD_B, font="sans-serif").to_edge(DOWN, buff=0.5)
        self.play(Transform(circle, triangle), Transform(label, new_label2), run_time=1.5)
        self.wait(0.5)

        new_label3 = Text("Star", font_size=28, color=MAROON_B, font="sans-serif").to_edge(DOWN, buff=0.5)
        self.play(Transform(circle, star), Transform(label, new_label3), run_time=1.5)
        self.wait(0.5)

        # Explode into particles
        dots = VGroup(*[
            Dot(point=star.point_from_proportion(i / 50), radius=0.05, color=YELLOW)
            for i in range(50)
        ])
        self.play(FadeOut(circle), FadeOut(label), FadeOut(new_label3), FadeIn(dots), run_time=0.5)

        animations = []
        for d in dots:
            direction = d.get_center() / np.linalg.norm(d.get_center() + 1e-6)
            animations.append(d.animate.shift(direction * 4).set_opacity(0))
        self.play(*animations, run_time=2)
        self.wait(0.5)


class WaveSuperposition(Scene):
    """Sine wave addition — shows how complex waves build from simple ones."""

    def construct(self):
        self.camera.background_color = "#1a1a2e"

        title = Text("Wave Superposition", font_size=36, color=WHITE, font="sans-serif")
        title.to_corner(UL, buff=0.4)
        self.play(Write(title), run_time=1)

        axes = Axes(
            x_range=[0, 4 * PI, PI / 2],
            y_range=[-3, 3, 1],
            x_length=10,
            y_length=5,
            axis_config={"color": GREY_B, "stroke_width": 1},
        ).shift(DOWN * 0.3)

        wave1_func = lambda x: np.sin(x)
        wave2_func = lambda x: 0.5 * np.sin(2 * x)
        wave3_func = lambda x: 0.3 * np.sin(3 * x)
        combined_func = lambda x: wave1_func(x) + wave2_func(x) + wave3_func(x)

        wave1 = axes.plot(wave1_func, color=BLUE_B, stroke_width=2)
        wave2 = axes.plot(wave2_func, color=GREEN_B, stroke_width=2)
        wave3 = axes.plot(wave3_func, color=RED_B, stroke_width=2)
        combined = axes.plot(combined_func, color=YELLOW, stroke_width=3)

        l1 = Text("sin(x)", font_size=22, color=BLUE_B, font="sans-serif")
        l2 = Text("0.5 sin(2x)", font_size=22, color=GREEN_B, font="sans-serif")
        l3 = Text("0.3 sin(3x)", font_size=22, color=RED_B, font="sans-serif")
        lc = Text("Sum", font_size=22, color=YELLOW, font="sans-serif")

        legend = VGroup(l1, l2, l3, lc).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        legend.to_corner(UR, buff=0.5)

        self.play(Create(axes), run_time=1)

        self.play(Create(wave1), FadeIn(l1), run_time=1.5)
        self.wait(0.3)
        self.play(Create(wave2), FadeIn(l2), run_time=1.5)
        self.wait(0.3)
        self.play(Create(wave3), FadeIn(l3), run_time=1.5)
        self.wait(0.5)

        self.play(
            wave1.animate.set_stroke(opacity=0.25),
            wave2.animate.set_stroke(opacity=0.25),
            wave3.animate.set_stroke(opacity=0.25),
            run_time=0.5,
        )
        self.play(Create(combined), FadeIn(lc), run_time=2)
        self.wait(1.5)
