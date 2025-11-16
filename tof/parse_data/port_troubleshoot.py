# Unused so far
# For troubleshooting when pyserial cannot connect to port
# Usually, permission errors can be solved by closing all Arduino applications / serial monitors and plotters

import serial
import serial.tools.list_ports
import psutil
import time

print("=== COM Port Diagnostic ===\n")

# Check if port exists
ports = serial.tools.list_ports.comports()
com9_exists = False
for port in ports:
    if port.device == 'COM9':
        com9_exists = True
        print(f"✓ COM9 detected: {port.description}")
        print(f"  Hardware ID: {port.hwid}")

if not com9_exists:
    print("✗ COM9 not found")
    exit()

print("\nAttempting to open COM9...")

# Try to open with exclusive access
try:
    ser = serial.Serial('COM9', 115200, timeout=1, exclusive=True)
    print("✓ SUCCESS! Port opened.")
    ser.close()
except serial.SerialException as e:
    print(f"✗ FAILED: {e}\n")
    
    # Check processes
    print("Checking for processes that might be using the port...")
    print("(This may take a moment)\n")
    
    suspicious_processes = []
    for proc in psutil.process_iter(['pid', 'name', 'open_files']):
        try:
            proc_name = proc.info['name'].lower()
            # Check for common serial-using programs
            if any(keyword in proc_name for keyword in ['arduino', 'java', 'putty', 'teraterm', 'python', 'serial']):
                suspicious_processes.append(f"{proc.info['name']} (PID: {proc.info['pid']})")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    if suspicious_processes:
        print("Potentially blocking processes:")
        for p in suspicious_processes:
            print(f"  - {p}")
        print("\nTry closing these programs and run this script again.")
    else:
        print("No obvious blocking processes found.")
        print("\nTry these steps:")
        print("1. Unplug Arduino USB cable")
        print("2. Wait 5 seconds")
        print("3. Plug it back in")
        print("4. Run this script again immediately")