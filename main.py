import sys
import utime
import esp32

from machine import Pin, PWM
from machine import Timer

class Program():
    def __init__(self):
        self.pwm = None

        # Camera trigger
        self.trigger = Pin(12, Pin.OUT)
        self.trigger.off()

        # Camera strobe
        self.strobe = Pin(14, Pin.IN, Pin.PULL_UP)
        self.strobe.irq(trigger=Pin.IRQ_FALLING, handler=self.handle_interrupt)


    def handle_interrupt(self, pin):
        print('int!')
        #self.rmt.write_pulses((32767, 10), 1)  # Send HIGH for 32767 * 100ns = 3ms



    def loop(self):
        while True:
            try:
                line = input("scopie:> ")
                if line.startswith('L'):
                    if self.pwm:
                        self.pwm.deinit()
                        self.pwm = None
                    led = Pin(2, Pin.OUT)

                    s = line.split(' ')
                    b = bool(int(s[1]))
                    if b:
                        print("led on")
                        led.on()
                    else:
                        print("led off")
                        led.off()
                elif line.startswith('Q'):
                    if self.pwm:
                        self.pwm.deinit()
                        self.pwm = None
                    rmt = esp32.RMT(0, pin=Pin(2), clock_div=255) # 1 time unit = 3 us
                    s = line.split(' ')
                    rmt.write_pulses((32767, 32767, 32767, 32767), 1)
                    rmt.wait_done()
                    rmt.deinit()
                elif line.startswith('P'):
                    s = line.split(' ')
                    freq = int(s[1])
                    duty = int(s[2])
                    self.pwm = PWM(self.led, freq=freq, duty=duty)
                    print(self.pwm)
                elif line.startswith('S'):
                    if self.rmt:
                        self.rmt.deinit()
                    if self.pwm:
                        self.pwm.deinit()
                    s = line.split(' ')
                    led = Pin(2, Pin.OUT)
                    led.off()
                    delay = int(s[1])
                    print("light up and sleep for", delay)
                    led.on()
                    utime.sleep_us(delay)
                    led.off()
                elif line.startswith('C'):
                    s = line.split(' ')
                    self.trigger.off()
                    utime.sleep_ms(10)
                    delay = int(s[1])
                    print("trigger camera for", delay)
                    self.trigger.on()
                    utime.sleep_us(delay)
                    self.trigger.off()
                else:
                    print("Unknown: ", line)
            except Exception as e:
                print(str(e))

p = Program()
p.loop()