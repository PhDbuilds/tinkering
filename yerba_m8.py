import onewire, ds18x20, time
from machine import Pin, I2C, PWM
from ssd1306 import SSD1306_I2C

# Set up the LED pins
red = Pin(18, Pin.OUT)
amber = Pin(19, Pin.OUT)
green = Pin(20, Pin.OUT)

# Set up I2C and the pins we're using for it
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)

# Set the data pin for the sensor
SensorPin = Pin(26, Pin.IN)

# Tell MicroPython we're using a DS18B20 sensor, and which pin it's on
sensor = ds18x20.DS18X20(onewire.OneWire(SensorPin))

# Look for DS18B20 sensors (each contains a unique rom code)
roms = sensor.scan()

# Set up the Buzzer pin as PWM
buzzer = PWM(Pin(13))

# Start PWM duty to 0% at program start
buzzer.duty_u16(0)
buzzer.freq(5000)  # Higher pitch

# Short delay to stop I2C falling over
time.sleep(1)

# Define the display and size (128x32)
display = SSD1306_I2C(128, 32, i2c)


def buzz():
    buzzer.duty_u16(10000)
    time.sleep(0.5)
    buzzer.duty_u16(0)


def leds():
    red.value(1)  # Red LED on
    amber.value(1)  # Amber LED on
    green.value(1)  # Green LED on
    time.sleep(0.5)
    red.value(0)  # Red LED off
    amber.value(0)  # Amber LED off
    green.value(0)  # Green LED off


def alarm():
    for i in range(3):
        buzz()
        leds()


def drinkup():
    # Create our library of tone variables for "Jingle Bells"
    C = 523
    D = 587
    E = 659
    G = 784

    # Create volume variable (Duty cycle)
    volume = 10000

    # Play the tune

    # "Jin..."
    buzzer.duty_u16(volume)  # Volume up
    buzzer.freq(E)  # Set frequency to the E note
    time.sleep(0.05)  # Delay
    buzzer.duty_u16(0)  # Volume off
    time.sleep(0.1)  # Delay

    # "...gle"
    buzzer.duty_u16(volume)
    buzzer.freq(E)
    time.sleep(0.05)
    buzzer.duty_u16(0)
    time.sleep(0.1)

    # "Bells"
    buzzer.duty_u16(volume)
    buzzer.freq(E)
    time.sleep(0.05)
    buzzer.duty_u16(0)
    time.sleep(0.1)  # longer delay

    # "Jin..."
    buzzer.duty_u16(volume)
    buzzer.freq(E)
    time.sleep(0.05)
    buzzer.duty_u16(0)
    time.sleep(0.1)

    # "...gle"
    buzzer.duty_u16(volume)
    buzzer.freq(E)
    time.sleep(0.05)
    buzzer.duty_u16(0)
    time.sleep(0.1)

    # "Bells"
    buzzer.duty_u16(volume)
    buzzer.freq(E)
    time.sleep(0.05)
    buzzer.duty_u16(0)
    time.sleep(0.25)  # longer delay

    # "Jin..."
    buzzer.duty_u16(volume)
    buzzer.freq(E)
    time.sleep(0.05)
    buzzer.duty_u16(0)
    time.sleep(0.1)

    # "...gle"
    buzzer.duty_u16(volume)
    buzzer.freq(G)
    time.sleep(0.05)
    buzzer.duty_u16(0)
    time.sleep(0.1)

    # "All"
    buzzer.duty_u16(volume)
    buzzer.freq(C)
    time.sleep(0.05)
    buzzer.duty_u16(0)
    time.sleep(0.1)

    # "The"
    buzzer.duty_u16(volume)
    buzzer.freq(D)
    time.sleep(0.05)
    buzzer.duty_u16(0)
    time.sleep(0.1)

    # "Way"
    buzzer.duty_u16(volume)
    buzzer.freq(E)
    time.sleep(0.05)
    buzzer.duty_u16(0)
    time.sleep(0.1)


# Duty to 0 to turn the buzzer off
buzzer.duty_u16(0)

while True:  # Run forever
    sensor.convert_temp()  # Convert the sensor units to centigrade

    time.sleep(
        2
    )  # Wait 2 seconds (you must wait at least 1 second before taking a reading)

    for rom in roms:  # For each sensor found (just 1 in our case)
        temp = sensor.read_temp(rom)  # Print the temperature reading with °C after it
        print(temp)
        if 60 <= temp <= 65:
            drinkup()
            display.fill(0)
            display.text("DRINK UP MATE", 0, 0)
            display.show()
            time.sleep(10)
        elif temp > 65:
            alarm()
            display.fill(0)
            display.text("TOO HOT", 0, 0)
            display.show()
            time.sleep(10)
        temp = str(temp) + " C"
        time.sleep(1)  # Wait 5 seconds before starting the loop again
        # Clear the display first
        display.fill(0)

        display.text("Temperature:", 0, 0)
        # Write a line of text to the display
        display.text(temp, 50, 12)

        # Update the display
        display.show()
