"""Geometry, proportions, colors, and motion parameters for the eOnOs character."""

import numpy as np

CONFIG = dict(
    # Background
    bg_color='#1a1a2e',

    # Lambda legs
    leg_apex=np.array([0.0, 0.0, 0.0]),
    leg_left_foot=np.array([-1.1, -1.9, 0.0]),
    leg_right_foot=np.array([1.1, -1.9, 0.0]),
    leg_stroke_width=8,

    # Spine (thin connector from apex to head area)
    spine_top=np.array([0.0, 0.9, 0.0]),
    spine_stroke_width=2.5,
    spine_opacity=0.3,

    # Eyes (O shapes)
    eye_left_center=np.array([-0.5, 1.65, 0.0]),
    eye_right_center=np.array([0.5, 1.65, 0.0]),
    eye_radius=0.36,
    eye_stroke_width=3.5,
    pupil_radius=0.10,
    pupil_max_offset=0.16,

    # Nose (n shape)
    nose_center=np.array([0.0, 1.05, 0.0]),
    nose_width=0.28,
    nose_height=0.22,
    nose_stroke_width=3.5,

    # Left arm (e shape)
    arm_e_center=np.array([-0.95, 0.55, 0.0]),
    # Right arm (S shape)
    arm_s_center=np.array([0.95, 0.55, 0.0]),
    arm_scale=0.75,
    arm_stroke_width=5,

    # Colors
    body_color='#e8dfd0',
    eye_color='#f0ece4',
    pupil_color='#1a1a2e',
    nose_color='#d0c8bc',
    arm_e_color='#aec6d8',
    arm_s_color='#d8c6a8',

    # Shoulder connections
    shoulder_stroke_width=2,
    shoulder_opacity=0.25,

    # Motion parameters
    s_wave_speed=2.0,
    s_wave_amp=0.06,
    blink_dur=0.3,
    look_dur=0.4,
    walk_leg_angle=0.25,
    walk_step_dur=0.5,
)
