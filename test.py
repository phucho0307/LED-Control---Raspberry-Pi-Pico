from neopixel import Neopixel
import utime

numpix = 284
np = Neopixel(numpix, 0, 3, "GRB")
# Give the strip a moment to initialize before sending data
utime.sleep_ms(500)

np.brightness(255)  # Full brightness to rule out color confusion

color = (0, 255, 0)  # Pure red

# Main loop
coco = [
    {"color": [255, 255, 255], "count": 12},
    {"color": [136, 140, 141], "count": 1}
]
#while(True):
#np.fill([255,255,255])
#np.show()
np.traverse_segment(11, 157,[
    {"color": [44, 17, 79], "count": 40},    # Mylar (0–58)
    {"color": [255, 255, 255], "count": 1},   # gap (59)
], 20, 30, 1, 1)

   
   
   