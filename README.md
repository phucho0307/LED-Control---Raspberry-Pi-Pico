Notice: The LED strip we are using is WS2812B (without a white channel), which needs 5V power, so the Pico cannot power the whole long strip. Thus, it uses a separate 5V power source. Because of this, the data signal that transmits through each LED must be in the same voltage range. That's why it needs a logic level shifter to convert the GPIO pin output from 3.3V to 5V. Also, I'm using GPIO pin 03 on this Pico because this Pico's GPIO 0 (conventional) is fried.

1. There is a custom library named Neopixel. It has several functions, but you should mostly use traverse_segment().
2. The API calls one of the functions in main.py through USB serial.
3. To test functions directly from the Pico to the LED strip, use test.py.
