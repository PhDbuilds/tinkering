# Imports
from machine import Pin, I2C, PWM
from ssd1306 import SSD1306_I2C
import time

# Set up our button name and GPIO pin number
# Also set the pin as an input and use a pull down
button = Pin(13, Pin.IN, Pin.PULL_DOWN)

# Set up the Buzzer pin as PWM
buzzer = PWM(Pin(12))  # Set the buzzer to PWM mode


def buzzer_test():
    """Test the buzzer on startup"""
    buzzer.freq(1500)
    buzzer.duty_u16(10000)
    time.sleep(1)
    buzzer.duty_u16(0)


# Run buzzer test on startup
buzzer_test()

# Set up our beam pin
beam = Pin(27, Pin.IN, Pin.PULL_DOWN)

# Set up I2C and the pins we're using for it
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)

# Short delay to stop I2C falling over
time.sleep(1)

# Define the display and size (128x32)
display = SSD1306_I2C(128, 32, i2c)

# Clear the display first
display.fill(0)


def alarm(times):
    """Sound the alarm"""
    for i in range(times):
        for freq in range(500, 2000, 50):
            buzzer.freq(freq)
            buzzer.duty_u16(10000)
            time.sleep(0.01)
        for freq in range(2000, 500, -50):
            buzzer.freq(freq)
            buzzer.duty_u16(10000)
            time.sleep(0.01)
        buzzer.duty_u16(0)


jumps = 0


while True:  # Loop forever
    time.sleep(0.2)  # Short delay

    if button.value() == 1:  # If button 1 is pressed
        print("Button 1 pressed")
        jumps = 0

    if beam.value() == 0:  # If the beam is broken
        print("Beam Broken!")
        jumps += 1
        print(f"Jump count: {jumps}")
        alarm(3)
        time.sleep(5)

    # Clear display and redraw
    display.fill(0)
    # Write a line of text to the display
    display.text(" /\_/\\", 0, 0)
    display.text("( o.o )    jumps:", 0, 12)
    display.text(f" > ^ <      {jumps}", 0, 24)

    # Update the display
    display.show()
