import sys
import utime
import esp32

from machine import Pin, PWM
from machine import Timer

TRIGGER_PIN=12
STROBE_PIN=14
LED_PIN=2

class Program():
    def __init__(self):
        self.pwm = None

        # Camera trigger
        self.trigger = Pin(TRIGGER_PIN, Pin.OUT)
        self.trigger.off()

        # Camera strobe
        self.strobe = Pin(STROBE_PIN, Pin.IN, Pin.PULL_DOWN)
        self.strobe.irq(trigger=Pin.IRQ_RISING, handler=self.handle_interrupt)


        self.led = Pin(LED_PIN)

    def handle_interrupt(self, pin):
        print('strobe')
        self.led.on()
        utime.sleep_us(100)
        self.led.off()

        #self.rmt.write_pulses((10, 10), 1)  # Send HIGH for 32767 * 100ns = 3ms

    def loop(self):
        while True:
            try:
                sys.stdout.write('scopie:> ')
                line = input()
                if line.startswith('L'):
                    self.led.init(mode=Pin.OUT)
                    s = line.split(' ')
                    b = bool(int(s[1]))
                    if b:
                        print("led on")
                        self.led.on()
                    else:
                        print("led off")
                        self.led.off()
                elif line.startswith('Q'):
                    rmt = esp32.RMT(0, pin=Pin(LED_PIN), clock_div=255) # 1 time unit = 3 us
                    rmt.write_pulses((32767, 32767, 32767, 32767), 1)
                    rmt.wait_done()
                    rmt.deinit()
                elif line.startswith('P'):
                    s = line.split(' ')
                    freq = int(s[1])
                    duty = int(s[2])
                    pwm = PWM(self.led, freq=freq, duty=duty)
                    print(pwm)
                elif line.startswith('S'):
                    self.led.init(mode=Pin.OUT)
                    s = line.split(' ')
                    self.led.off()
                    delay = int(s[1])
                    print("light up and sleep for", delay)
                    self.led.on()
                    utime.sleep_us(delay)
                    self.led.off()
                elif line.startswith('C'):
                    s = line.split(' ')
                    self.trigger.off()
                    utime.sleep_ms(10)
                    delay = int(s[1])
                    print("trigger camera for", delay)
                    self.trigger.on()
                    #utime.sleep_us(delay)
                    utime.sleep_ms(delay)
                    self.trigger.off()
                elif line.startswith('N'):
                    s = line.split(' ')
                    b = bool(int(s[1]))
                    if b:
                        print("trigger on")
                        self.trigger.on()
                    else:
                        print("trigger off")
                        self.trigger.off()
                else:
                    print("Unknown: ", line)
            except Exception as e:
                print(str(e))

p = Program()
p.loop()
