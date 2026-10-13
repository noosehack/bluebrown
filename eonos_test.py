"""Static character display and basic motion test for visual approval."""

from manim import *
from eonos_character import EonosCharacter
from eonos_config import CONFIG


class EonosStaticTest(Scene):
    def construct(self):
        self.camera.background_color = CONFIG['bg_color']

        eonos = EonosCharacter()

        # 1. Fade in the static character
        self.play(FadeIn(eonos, shift=UP * 0.3), run_time=1.5)
        self.wait(0.5)

        # 2. Blink
        self.play(eonos.blink())
        self.wait(0.4)

        # 3. Look around
        self.play(eonos.look_at([-5, 2, 0]))
        self.wait(0.3)
        self.play(eonos.look_at([5, -1, 0]))
        self.wait(0.3)
        self.play(eonos.look_forward())
        self.wait(0.3)

        # 4. S-arm undulation
        eonos.start_s_undulation()
        self.wait(3)

        # 5. Blink while undulating
        self.play(eonos.blink())
        self.wait(1)

        # 6. Fade out
        eonos.stop_s_undulation()
        self.play(FadeOut(eonos), run_time=1)
