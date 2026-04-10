import sys
import json
import time
import select
from neopixel import Neopixel

# Config
NUM_LEDS = 284
PIN = 3
STATE_MACHINE = 0

strip = Neopixel(NUM_LEDS, STATE_MACHINE, PIN, mode="GRB")
strip.brightness(50)

DEVICE_NAME = "pico_neopixel"


def handle_command(cmd):
    action = cmd.get("action")
    

    if action == "check":
        return {"name": DEVICE_NAME, "num_leds": NUM_LEDS, "status": "ok"}

    elif action == "set_pixel":
        strip.set_pixel(cmd["id"], tuple(cmd["rgb"]), cmd.get("brightness"))
        strip.show()
        return {"status": "ok"}

    elif action == "set_line":
        strip.set_pixel_line(cmd["start"], cmd["end"], tuple(cmd["rgb"]), cmd.get("brightness"))
        strip.show()
        return {"status": "ok"}

    elif action == "gradient":
        strip.set_pixel_line_gradient(
            cmd["start"], cmd["end"],
            tuple(cmd["left_rgb"]), tuple(cmd["right_rgb"]),
            cmd.get("brightness")
        )
        strip.show()
        return {"status": "ok"}

    elif action == "fill":
        strip.fill(tuple(cmd["rgb"]), cmd.get("brightness"))
        strip.show()
        return {"status": "ok"}

    elif action == "clear":
        strip.clear()
        strip.show()
        return {"status": "ok"}

    elif action == "brightness":
        strip.brightness(cmd["value"])
        return {"status": "ok", "brightness": cmd["value"]}

    elif action == "traverse":
        strip.traverse(
            rgb=tuple(cmd.get("rgb", (255, 0, 0))),
            delay=cmd.get("delay", 0.05),
            clear_after=cmd.get("clear_after", True)
        )
        return {"status": "ok"}

    elif action == "traverse_rainbow":
        strip.traverse_rainbow(delay=cmd.get("delay", 0.05))
        return {"status": "ok"}

    elif action == "rotate_left":
        strip.rotate_left(cmd.get("count", 1))
        strip.show()
        return {"status": "ok"}

    elif action == "rotate_right":
        strip.rotate_right(cmd.get("count", 1))
        strip.show()
        return {"status": "ok"}
    
    
    elif action == "traverse_segment":
        coco_raw = cmd.get("coco", [])
        coco = [{'color': tuple(g['color']), 'count': g['count']} for g in coco_raw]
        strip.traverse_segment(
            pixel1=cmd.get("pixel1", 0),
            pixel2=cmd.get("pixel2", NUM_LEDS - 1),
            coco=coco,
            flash_max=cmd.get("flash_max", 5),
            on_max=cmd.get("on_max", 7),
            shift=cmd.get("shift", 1),
            delay=cmd.get("delay", 0.1),
        )
        return {"status": "ok"}
    
    elif action == "show":
        strip.show()
        return {"status": "ok"}

    else:
        return {"status": "error", "message": f"Unknown action: {action}"}


# Main loop — listen for JSON commands over serial
while True:
    try:
        line = sys.stdin.readline()
        if not line:
            continue

        line = line.strip()
        if not line:
            continue

        # Support legacy "check" plain text command
        if line == "check":
            print(json.dumps({"name": DEVICE_NAME, "num_leds": NUM_LEDS, "status": "ok"}))
            continue

        cmd = json.loads(line)
        result = handle_command(cmd)
        print(json.dumps(result))

    except ValueError:
        print(json.dumps({"status": "error", "message": "Invalid JSON"}))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))