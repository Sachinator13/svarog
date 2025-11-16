import serial
import time

# Configure serial port
# Replace 'COM3' with your port (Windows: COM3, COM4, etc. | Mac/Linux: /dev/ttyUSB0, /dev/ttyACM0)
arduino = serial.Serial(port='COM9', baudrate=115200, timeout=1)

time.sleep(2)  # Wait for Arduino to reset after serial connection

print("Reading from Arduino...")

try:
    while True:
        if arduino.in_waiting > 0:
            # Read line from Arduino
            line = arduino.readline().decode('utf-8').rstrip()
            print(line)
            
except KeyboardInterrupt:
    print("\nExiting...")
    arduino.close()