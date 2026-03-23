from machine import Pin, PWM
import sys
import json

# ─── PIN LAYOUT ───────────────────────────────────────────
# Each light needs 3 PWM pins (R, G, B)
# 8 lights × 3 pins = 24 pins total

LIGHTS = {
    0: (PWM(Pin(0)),  PWM(Pin(1)),  PWM(Pin(2))),
    1: (PWM(Pin(3)),  PWM(Pin(4)),  PWM(Pin(5))),
    2: (PWM(Pin(6)),  PWM(Pin(7)),  PWM(Pin(8))),
    3: (PWM(Pin(9)),  PWM(Pin(10)), PWM(Pin(11))),
    4: (PWM(Pin(12)), PWM(Pin(13)), PWM(Pin(14))),
    5: (PWM(Pin(15)), PWM(Pin(16)), PWM(Pin(17))),
    6: (PWM(Pin(18)), PWM(Pin(19)), PWM(Pin(20))),
    7: (PWM(Pin(21)), PWM(Pin(22)), PWM(Pin(26))),
}

# ─── SET ALL PWM FREQUENCIES ──────────────────────────────
for r, g, b in LIGHTS.values():
    r.freq(1000)
    g.freq(1000)
    b.freq(1000)

# ─── HELPER FUNCTIONS ─────────────────────────────────────
def set_rgb(light_id, r, g, b):
    """Set a light to an RGB color."""
    if light_id not in LIGHTS:
        return "ERROR invalid light id"
    red, green, blue = LIGHTS[light_id]
    red.duty_u16(int(r * 257))    # 0-255 → 0-65535
    green.duty_u16(int(g * 257))
    blue.duty_u16(int(b * 257))
    return "OK"

def get_rgb(light_id):
    """Get current RGB state of a light."""
    if light_id not in LIGHTS:
        return None
    red, green, blue = LIGHTS[light_id]
    r = red.duty_u16() // 257
    g = green.duty_u16() // 257
    b = blue.duty_u16() // 257
    return [r, g, b]

def all_off():
    """Turn all lights off."""
    for i in LIGHTS:
        set_rgb(i, 0, 0, 0)
        
def all_on(r=255, g=255, b=255):
    """Turn all lights on. Defaults to white."""
    for i in LIGHTS:
        set_rgb(i, r, g, b)

# ─── STARTUP ──────────────────────────────────────────────
all_off()  # start with all lights off

# ─── MAIN LOOP ────────────────────────────────────────────
while True:
    try:
        line = sys.stdin.readline().strip()

        if not line:
            continue

        # ── IDENTIFY ──────────────────────────────────────
        # USBSearch sends "check" to find the device
        if line == "check":
            response = json.dumps({"name": "PicoLED", "lights": len(LIGHTS)})
            print(response)

        # ── SET one light ─────────────────────────────────
        # SET 0 255 0 128  → light 0, purple
        elif line.startswith("SET"):
            parts = line.split()
            light_id = int(parts[1])
            r = int(parts[2])
            g = int(parts[3])
            b = int(parts[4])
            result = set_rgb(light_id, r, g, b)
            print(result)

        # ── GET one light ─────────────────────────────────
        # GET 0  → returns current RGB of light 0
        elif line.startswith("GET"):
            parts = line.split()
            light_id = int(parts[1])
            state = get_rgb(light_id)
            if state:
                print(json.dumps(state))
            else:
                print("ERROR invalid light id")

        # ── ALL OFF ───────────────────────────────────────
        elif line == "OFF":
            all_off()
            print("OK")

        # ── UNKNOWN COMMAND ───────────────────────────────
        else:
            print("ERROR unknown command")

    except Exception as e:
        print(f"ERROR {e}")




