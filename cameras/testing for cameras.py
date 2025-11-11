import cv2

for i in range(5):
    cam = cv2.VideoCapture(i)
    if cam.isOpened():
        print(f"Camera index {i} is available.")
        cam.release()
    else:
        print(f"Camera index {i} not available.")