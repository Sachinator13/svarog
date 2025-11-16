import serial
import time
import re
import statistics

arduino = serial.Serial(port='COM9', baudrate=115200, timeout=1)
time.sleep(2)

def collect_samples(num_samples=30, sensor_num=1):
    """Collect multiple samples from a sensor"""
    samples = []
    print(f"Collecting {num_samples} samples from Sensor {sensor_num}...")
    
    while len(samples) < num_samples:
        if arduino.in_waiting > 0:
            line = arduino.readline().decode('utf-8').rstrip()
            
            # Parse format: "Sensor1:8190 Sensor2:8190"
            match = re.search(r'Sensor1:(\d+)\s+Sensor2:(\d+)', line)
            if match:
                value = int(match.group(sensor_num))
                # Filter out out-of-range readings (8190 is often "out of range")
                if 0 < value < 8000:  
                    samples.append(value)
                    print(f"  Sample {len(samples)}/{num_samples}: {value}mm", end='\r')
                elif value >= 8190:
                    print(f"  Warning: Out of range reading ({value}mm)      ", end='\r')
    
    print()  # New line after collection
    return samples

def calibrate():
    """Interactive calibration procedure"""
    print("=== VL53L0X Calibration ===\n")
    print("Instructions:")
    print("1. Place white target at exact distance")
    print("2. Enter the actual distance when prompted")
    print("3. Sensor will collect 30 valid samples")
    print("4. Repeat for multiple distances")
    print("5. Note: 8190mm readings indicate 'out of range'\n")
    
    calibration_data = []
    
    while True:
        actual_dist = input("\nEnter actual distance in mm (or 'done' to finish): ")
        
        if actual_dist.lower() == 'done':
            break
        
        try:
            actual_dist = int(actual_dist)
        except ValueError:
            print("Please enter a number or 'done'")
            continue
        
        # Choose sensor
        sensor_choice = input("Calibrate Sensor 1 or 2? (1/2): ")
        sensor_num = 1 if sensor_choice == '1' else 2
        
        # Collect samples
        samples = collect_samples(num_samples=30, sensor_num=sensor_num)
        
        if len(samples) < 5:
            print("Not enough valid samples collected. Target might be out of range.")
            continue
        
        # Calculate statistics
        avg = statistics.mean(samples)
        std = statistics.stdev(samples) if len(samples) > 1 else 0
        min_val = min(samples)
        max_val = max(samples)
        
        print(f"\nResults for {actual_dist}mm:")
        print(f"  Average reading: {avg:.1f}mm")
        print(f"  Std deviation: {std:.1f}mm")
        print(f"  Range: {min_val}mm - {max_val}mm")
        print(f"  Error: {avg - actual_dist:.1f}mm ({((avg - actual_dist) / actual_dist * 100):.1f}%)")
        
        calibration_data.append({
            'sensor': sensor_num,
            'actual': actual_dist,
            'measured': avg,
            'std_dev': std,
            'min': min_val,
            'max': max_val,
            'error': avg - actual_dist
        })
    
    # Save results
    if calibration_data:
        with open('calibration_data.csv', 'w') as f:
            f.write("sensor,actual_mm,measured_mm,std_dev,min_mm,max_mm,error_mm,error_percent\n")
            for data in calibration_data:
                error_pct = (data['error'] / data['actual']) * 100
                f.write(f"{data['sensor']},{data['actual']},{data['measured']:.1f},{data['std_dev']:.1f},")
                f.write(f"{data['min']},{data['max']},{data['error']:.1f},{error_pct:.2f}\n")
        
        print("\n" + "="*60)
        print("Calibration data saved to calibration_data.csv")
        print("="*60)
        
        # Print summary table
        print("\nCalibration Summary:")
        print(f"{'Sensor':<8}{'Actual':<10}{'Measured':<12}{'Error':<10}{'Std Dev':<10}")
        print("-" * 60)
        for data in calibration_data:
            print(f"{data['sensor']:<8}{data['actual']:<10}{data['measured']:<12.1f}"
                  f"{data['error']:<10.1f}{data['std_dev']:<10.1f}")

try:
    calibrate()
except KeyboardInterrupt:
    print("\n\nCalibration cancelled")
finally:
    arduino.close()