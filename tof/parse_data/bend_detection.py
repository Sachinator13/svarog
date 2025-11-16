import serial
import re
import math

# Configure serial port
arduino = serial.Serial(port='COM9', baudrate=115200, timeout=1)

THRESHOLD = 130  # Threshold in mm (d in formula)
d = THRESHOLD
d_2 = THRESHOLD * math.tan(math.radians(12.5))  # d_2 in formula

print("Reading from sensor...")
print(f"Threshold (d): {THRESHOLD}mm")
print(f"d_2: {d_2:.2f}mm\n")

def bend_angle_approximation_1(x, d, d_2):
    """
    Calculate f(x) = arcsin(sin(12.5) * (d-x) / sqrt(d_2^2 + x^2 - 2*d_2*x*sin(12.5)))
    
    Args:
        x: sensor reading (distance)
        d: threshold value
        d_2: THRESHOLD * tan(12.5)
    
    Returns:
        f(x) value in degrees
    """
    try:
        sin_12_5 = math.sin(math.radians(12.5))
        
        numerator = sin_12_5 * (d - x)
        denominator = math.sqrt(d_2**2 + x**2 - 2*d_2*x*sin_12_5)
        
        # Calculate arcsin argument
        arcsin_arg = numerator / denominator
        
        # Check if argument is in valid range [-1, 1]
        if arcsin_arg < -1 or arcsin_arg > 1:
            return None
        
        # Calculate arcsin and convert to degrees
        result = math.asin(arcsin_arg)
        result_degrees = math.degrees(result)
        
        return result_degrees
    except Exception as e:
        return None
    

def bend_angle_approximation_2(x, d):
    """
    Calculate g(x) = arctan(tan(12.5) * (d-x) / d)
    
    Args:
        x: sensor reading (distance)
        d: threshold value
    
    Returns:
        g(x) value in degrees
    """
    try:
        tan_12_5 = math.tan(math.radians(12.5))
        
        # Calculate arctan argument
        arctan_arg = tan_12_5 * (d - x) / d
        
        # Calculate arctan and convert to degrees
        result = math.atan(arctan_arg)
        result_degrees = math.degrees(result)
        
        return result_degrees
    except Exception as e:
        return None

try:
    while True:
        if arduino.in_waiting > 0:
            line = arduino.readline().decode('utf-8').rstrip()
            
            # Parse format: "Sensor1:250"
            match = re.search(r'Sensor1:(\d+)', line)
            if match:
                distance = int(match.group(1))
                
                # Calculate f(x)
                f_value = bend_angle_approximation_1(distance, d, d_2)
                
                if distance > THRESHOLD:
                    status = "NOT BENDY"
                else:
                    status = "BENDY"
                
                if f_value is not None:
                    print(f"{distance}mm - {status} | BEND ANGLE = {f_value:.2f}°")
                else:
                    print(f"{distance}mm - {status} | BEND ANGLE = UNDEFINED")
                    
except KeyboardInterrupt:
    print("\nExiting...")
    arduino.close()
