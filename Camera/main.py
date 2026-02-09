import cv2
import numpy as np
import subprocess

cap = cv2.VideoCapture(0) 
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)



space_pressed = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape

    left_box = (15, 150, 150, 150)
    right_box = (w - 170, 150, 150, 150 )

    def detect_hand(box):
        x, y, bw, bh = box
        roi = frame[y:y+bh, x:x+bw]
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        lower = np.array([0, 30, 60])
        upper = np.array([20, 150, 255])
        mask = cv2.inRange(hsv, lower, upper)
        return cv2.countNonZero(mask) > 1500

    left_active = detect_hand(left_box)
    right_active = detect_hand(right_box)

    left_color = (0, 255, 0) if left_active else (0, 0, 255)
    right_color = (0, 255, 0) if right_active else (0, 0, 255)

    cv2.rectangle(frame, left_box[:2], (left_box[0]+left_box[2], left_box[1]+left_box[3]), left_color, 4)
    cv2.rectangle(frame, right_box[:2], (right_box[0]+right_box[2], right_box[1]+right_box[3]), right_color, 4)

    if left_active and right_active and not space_pressed:
        subprocess.run(["xdotool", "key", "space"])
        space_pressed = True
        cv2.putText(frame, "Jump", (w//2 - 60, 80), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4)
    elif not (left_active and right_active):
        space_pressed = False

    cv2.imshow("Camera", frame)

    if cv2.waitKey(1) & 0xFF in [ord('q'), ord('Q')]:
        break

cap.release()
cv2.destroyAllWindows()
