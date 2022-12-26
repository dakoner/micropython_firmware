import time
import esp32

from machine import Pin
from machine import Timer

led = Pin(2, Pin.OUT)
led.off()

r = esp32.RMT(0, pin=led, clock_div=8) # 80MHz/8 = 10MHz so one time unit = 100ns

def handle_interrupt(pin):
    global r
    r.write_pulses((32767, 10), 1)  # Send HIGH for 32767 * 100ns = 300ms

# Camera trigger
pir = Pin(14, Pin.IN)
pir.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)

while True:
    time.sleep(1)
