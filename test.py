import ArducamSDK
import numpy as np
import cv2

# Open the first Arducam camera
handle = ArducamSDK.OpenCamera(0)
if handle == 0:
    print("Failed to open Arducam camera.")
    exit()

# Start streaming
ArducamSDK.StartCamera(handle)

print("Camera started successfully. Press 'q' to quit.")

while True:
    ret, data = ArducamSDK.CaptureImage(handle)
    if not ret:
        print("Failed to capture image")
        continue

    # Convert raw bytes to a numpy array
    frame = np.frombuffer(data, dtype=np.uint8)
    frame = frame.reshape(800, 1280)  # for OV9281

    cv2.imshow("Arducam OV9281", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
ArducamSDK.StopCamera(handle)
ArducamSDK.CloseCamera(handle)
cv2.destroyAllWindows()
