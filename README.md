# bluebrown

Programmatic math animations in the style of 3Blue1Brown, built with [Manim](https://www.manim.community/).

## Setup

```bash
pip install manim
```

## Render

```bash
# Preview quality (480p)
manim render -ql scenes/demo.py FourierCirclesDrawing

# Medium quality (720p)
manim render -qm scenes/demo.py FourierCirclesDrawing

# Production quality (1080p)
manim render -qh scenes/demo.py FourierCirclesDrawing
```

## Scenes

- **FourierCirclesDrawing** — Epicycles tracing a shape via Fourier decomposition
- **TransformingShapes** — Smooth morphing between geometric primitives
- **WaveSuperposition** — Sine wave addition building complex waveforms
