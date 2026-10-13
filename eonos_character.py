"""Reusable eOnOs animated character built from letter-shaped geometry."""

from manim import *
import numpy as np
from eonos_config import CONFIG

# ---------------------------------------------------------------------------
# Raw letter shapes — centered at origin, unit scale
# ---------------------------------------------------------------------------

# Lowercase 'e': crossbar left→right, then counterclockwise arc, opening at lower-right
_E_RAW = np.array([
    [-0.45,  0.00, 0],  # crossbar left
    [-0.15,  0.00, 0],
    [ 0.15,  0.00, 0],
    [ 0.45,  0.00, 0],  # crossbar right
    [ 0.48,  0.28, 0],  # arc: curving up
    [ 0.30,  0.50, 0],
    [ 0.00,  0.55, 0],  # top
    [-0.30,  0.50, 0],
    [-0.48,  0.28, 0],  # left, above crossbar
    [-0.48, -0.28, 0],  # left, below crossbar
    [-0.30, -0.50, 0],
    [ 0.00, -0.55, 0],  # bottom
    [ 0.30, -0.45, 0],
    [ 0.42, -0.22, 0],  # tail end (opening)
])

# Uppercase 'S': top-right to bottom-left with two opposing curves
_S_RAW = np.array([
    [ 0.35,  0.55, 0],
    [ 0.10,  0.65, 0],
    [-0.25,  0.58, 0],
    [-0.40,  0.32, 0],
    [-0.18,  0.08, 0],
    [ 0.00,  0.00, 0],  # center crossing
    [ 0.18, -0.08, 0],
    [ 0.40, -0.32, 0],
    [ 0.25, -0.58, 0],
    [-0.10, -0.65, 0],
    [-0.35, -0.55, 0],
])


class EonosCharacter(VGroup):
    """A programmable character whose parts are the letters e, O, n, O, S
    standing on Lambda legs."""

    def __init__(self, config=None, **kwargs):
        super().__init__(**kwargs)
        self.cfg = {**CONFIG, **(config or {})}
        self._s_time = 0.0
        self._build()

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def _build(self):
        c = self.cfg

        # Lambda legs
        self.left_leg = Line(
            c['leg_apex'], c['leg_left_foot'],
            stroke_width=c['leg_stroke_width'], color=c['body_color'],
        )
        self.right_leg = Line(
            c['leg_apex'], c['leg_right_foot'],
            stroke_width=c['leg_stroke_width'], color=c['body_color'],
        )

        # Spine
        self.spine = Line(
            c['leg_apex'], c['spine_top'],
            stroke_width=c['spine_stroke_width'],
            color=c['body_color'], stroke_opacity=c['spine_opacity'],
        )

        # Shoulder connections (thin lines from spine to arm edges)
        arm_y = c['arm_e_center'][1]
        e_edge_x = c['arm_e_center'][0] + 0.48 * c['arm_scale']
        s_edge_x = c['arm_s_center'][0] - 0.40 * c['arm_scale']
        self.left_shoulder = Line(
            [0, arm_y, 0], [e_edge_x, arm_y, 0],
            stroke_width=c['shoulder_stroke_width'],
            stroke_opacity=c['shoulder_opacity'], color=c['body_color'],
        )
        self.right_shoulder = Line(
            [0, arm_y, 0], [s_edge_x, arm_y, 0],
            stroke_width=c['shoulder_stroke_width'],
            stroke_opacity=c['shoulder_opacity'], color=c['body_color'],
        )

        # Arms
        self._build_arm_e()
        self._build_arm_s()

        # Nose (n shape)
        self._build_nose()

        # Eyes (O O) with pupils
        self._build_eyes()

        # Add in render order: back → front
        self.add(
            self.left_leg, self.right_leg,
            self.spine,
            self.left_shoulder, self.right_shoulder,
            self.arm_e, self.arm_s,
            self.nose,
            self.eye_group,
        )

    def _build_arm_e(self):
        c = self.cfg
        pts = _E_RAW * c['arm_scale'] + c['arm_e_center']
        self.arm_e = VMobject(
            stroke_color=c['arm_e_color'],
            stroke_width=c['arm_stroke_width'],
            fill_opacity=0,
        )
        self.arm_e.set_points_smoothly(list(pts))
        self._e_base_pts = [p.copy() for p in pts]

    def _build_arm_s(self):
        c = self.cfg
        pts = _S_RAW * c['arm_scale'] + c['arm_s_center']
        self.arm_s = VMobject(
            stroke_color=c['arm_s_color'],
            stroke_width=c['arm_stroke_width'],
            fill_opacity=0,
        )
        self.arm_s.set_points_smoothly(list(pts))
        self._s_base_pts = [p.copy() for p in pts]

    def _build_nose(self):
        c = self.cfg
        w, h = c['nose_width'], c['nose_height']
        ctr = c['nose_center']
        pts = [
            ctr + np.array([-w / 2, -h / 2, 0]),
            ctr + np.array([-w / 2,  h / 4, 0]),
            ctr + np.array([-w / 4,  h / 2, 0]),
            ctr + np.array([0,       h / 2 + 0.02, 0]),
            ctr + np.array([ w / 4,  h / 2, 0]),
            ctr + np.array([ w / 2,  h / 4, 0]),
            ctr + np.array([ w / 2, -h / 2, 0]),
        ]
        self.nose = VMobject(
            stroke_color=c['nose_color'],
            stroke_width=c['nose_stroke_width'],
            fill_opacity=0,
        )
        self.nose.set_points_smoothly(pts)

    def _build_eyes(self):
        c = self.cfg
        self.left_eye = Circle(
            radius=c['eye_radius'], color=c['eye_color'],
            stroke_width=c['eye_stroke_width'],
        ).move_to(c['eye_left_center'])
        self.right_eye = Circle(
            radius=c['eye_radius'], color=c['eye_color'],
            stroke_width=c['eye_stroke_width'],
        ).move_to(c['eye_right_center'])
        self.left_pupil = Dot(
            radius=c['pupil_radius'], color=c['pupil_color'], fill_opacity=1,
        ).move_to(c['eye_left_center'])
        self.right_pupil = Dot(
            radius=c['pupil_radius'], color=c['pupil_color'], fill_opacity=1,
        ).move_to(c['eye_right_center'])
        self.eye_group = VGroup(
            self.left_eye, self.right_eye,
            self.left_pupil, self.right_pupil,
        )

    # ------------------------------------------------------------------
    # Animations
    # ------------------------------------------------------------------

    def blink(self, duration=None):
        """Close and open the eyes."""
        d = duration or self.cfg['blink_dur']
        center = (self.left_eye.get_center() + self.right_eye.get_center()) / 2
        self.eye_group.save_state()
        closed = self.eye_group.copy().stretch(0.08, 1, about_point=center)
        return Succession(
            Transform(self.eye_group, closed,
                      run_time=d * 0.4, rate_func=rush_into),
            Restore(self.eye_group,
                    run_time=d * 0.6, rate_func=rush_from),
        )

    def look_at(self, target, duration=None):
        """Move pupils toward a world-space point."""
        d = duration or self.cfg['look_dur']
        t = np.array(target)
        if t.shape == (2,):
            t = np.array([t[0], t[1], 0.0])
        max_off = self.cfg['pupil_max_offset']
        threshold = 3.0

        anims = []
        for eye, pupil in [(self.left_eye, self.left_pupil),
                           (self.right_eye, self.right_pupil)]:
            ec = eye.get_center()
            direction = t - ec
            direction[2] = 0
            dist = np.linalg.norm(direction)
            if dist > 1e-6:
                strength = min(dist / threshold, 1.0)
                offset = direction / dist * strength * max_off
            else:
                offset = np.zeros(3)
            anims.append(pupil.animate(run_time=d).move_to(ec + offset))
        return AnimationGroup(*anims)

    def look_forward(self, duration=None):
        """Return pupils to eye centers."""
        d = duration or self.cfg['look_dur']
        return AnimationGroup(
            self.left_pupil.animate(run_time=d).move_to(
                self.left_eye.get_center()),
            self.right_pupil.animate(run_time=d).move_to(
                self.right_eye.get_center()),
        )

    # --- S-arm continuous undulation ---

    def start_s_undulation(self):
        """Begin the serpentine motion on the S-shaped arm."""
        self._s_time = 0.0
        base = self._s_base_pts
        c = self.cfg

        def _updater(mob, dt):
            self._s_time += dt
            t = self._s_time * c['s_wave_speed']
            n = len(base)
            new_pts = []
            for i, p in enumerate(base):
                progress = i / (n - 1)
                envelope = np.sin(np.pi * progress)
                x_off = c['s_wave_amp'] * envelope * np.sin(t + progress * 6)
                new_pts.append(p + np.array([x_off, 0, 0]))
            fresh = VMobject(
                stroke_color=c['arm_s_color'],
                stroke_width=c['arm_stroke_width'],
                fill_opacity=0,
            )
            fresh.set_points_smoothly(new_pts)
            mob.become(fresh)

        self.arm_s.add_updater(_updater)

    def stop_s_undulation(self):
        self.arm_s.clear_updaters()
