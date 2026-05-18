# LEDcontrol_pico_micropython

MicroPython firmware for a Raspberry Pi Pico that drives a WS2812B LED strip and accepts JSON commands over USB serial.

## Hardware

- **MCU:** Raspberry Pi Pico (MicroPython)
- **LED strip:** WS2812B, 284 LEDs, GRB order, no white channel
- **Data pin:** GPIO **3** (the conventional GPIO 0 on this particular Pico is fried, hence the move to GPIO 3)
- **Power:** The strip needs 5 V at higher current than the Pico can supply, so it is driven from a **separate 5 V power supply**. Tie all grounds together.
- **Logic level shifter:** Required. The Pico's GPIO is 3.3 V; WS2812B data must be in the 5 V range, so the GPIO output is shifted from 3.3 V → 5 V before reaching the strip.

## Files

| File | Purpose |
| --- | --- |
| `main.py` | Runs on boot. Reads JSON commands from USB serial and dispatches them to the LED strip. |
| `neopixel.py` | Custom Neopixel driver (PIO-based). Adds animation helpers — most importantly `traverse_segment()`. |
| `test.py` | Standalone script for testing animations directly on the Pico without going through the serial API. |

## How it works

1. `main.py` boots, creates a `Neopixel(NUM_LEDS=284, PIN=3, mode="GRB")` strip at brightness 50, and enters a loop reading lines from `sys.stdin`.
2. Each line is parsed as JSON `{"action": "...", ...}` and dispatched. The Pico replies with a JSON status line.
3. The host-side API (running on the PC/server) opens the Pico's USB serial port and writes these JSON commands — this is how the rest of the NMR-Display project talks to the strip.

The custom `Neopixel` library exposes several helpers, but the main one used in production is `traverse_segment()`, which paints a sequence of colored groups on a sub-segment of the strip and scrolls them as an animation.

## Supported serial actions

Each command is a single JSON line. Responses are also single JSON lines.

| Action | Required fields | Notes |
| --- | --- | --- |
| `check` | — | Returns `{name, num_leds, status}`. The plain text `check` also works. |
| `set_pixel` | `id`, `rgb` | Optional `brightness`. |
| `set_line` | `start`, `end`, `rgb` | Inclusive range. Optional `brightness`. |
| `gradient` | `start`, `end`, `left_rgb`, `right_rgb` | Linear gradient between two colors. |
| `fill` | `rgb` | Fills the whole strip. |
| `clear` | — | Turns all LEDs off. |
| `brightness` | `value` | 1–255. |
| `traverse` | — | Optional `rgb`, `delay`, `clear_after`. Single-pixel walk. |
| `traverse_rainbow` | — | Optional `delay`. |
| `rotate_left` / `rotate_right` | — | Optional `count`. |
| `traverse_segment` | `coco` | Optional `pixel1`, `pixel2`, `flash_max`, `on_max`, `shift`, `delay`. `coco` is a list of `{color: [r,g,b], count: N}` groups. |
| `show` | — | Pushes the current buffer to the strip. |

Long-running animations (`traverse_segment`) are interruptible: they check for a new incoming serial command on each step and return early if one arrives.

## Testing on the Pico directly

Edit `test.py` to call whatever animation you want and run it on the Pico (e.g. via Thonny). This bypasses the serial protocol so you can iterate on the LED behavior without the host app.

## Configuration

If your wiring changes, update the constants at the top of [`main.py`](main.py):

```python
NUM_LEDS = 284
PIN = 3
STATE_MACHINE = 0
```
