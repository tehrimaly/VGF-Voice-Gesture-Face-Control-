import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time

# Initialize mediapipe
mp_face = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

screen_w, screen_h = pyautogui.size()

# Blink detection thresholds
EAR_THRESHOLD = 0.22      # Adjust if needed
MOUTH_THRESHOLD = 0.6

smoothening = 5
prev_x, prev_y = 0, 0

def euclidean(a, b):
    return np.linalg.norm(np.array(a) - np.array(b))

def eye_aspect_ratio(landmarks, eye_points):
    top = euclidean(landmarks[eye_points[1]], landmarks[eye_points[2]])
    bottom = euclidean(landmarks[eye_points[3]], landmarks[eye_points[4]])
    width = euclidean(landmarks[eye_points[0]], landmarks[eye_points[5]])
    return (top + bottom) / (2.0 * width)

def mouth_open_ratio(landmarks, top, bottom):
    return euclidean(landmarks[top], landmarks[bottom])

def normalize(val, a, b, c, d):
    return c + (val - a) * (d - c) / (b - a)

def main():
    cap = cv2.VideoCapture(0)
    face_mesh = mp_face.FaceMesh(refine_landmarks=True)

    last_click = time.time()

    print("Face control active. Press ESC to exit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        result = face_mesh.process(rgb)
        h, w, _ = frame.shape

        if result.multi_face_landmarks:
            face = result.multi_face_landmarks[0]

            # Get all landmarks as (x, y)
            lm = []
            for id_, lmks in enumerate(face.landmark):
                lm.append([lmks.x, lmks.y])

            # Nose tip -> cursor control
            nose = lm[1]      # landmark index 1 is nose tip
            nose_x = int(nose[0] * w)
            nose_y = int(nose[1] * h)

            # Map to screen
            screen_x = normalize(nose_x, 100, w-100, 0, screen_w)
            screen_y = normalize(nose_y, 100, h-100, 0, screen_h)

            # Smooth cursor
            global prev_x, prev_y
            curr_x = prev_x + (screen_x - prev_x) / smoothening
            curr_y = prev_y + (screen_y - prev_y) / smoothening
            pyautogui.moveTo(curr_x, curr_y)
            prev_x, prev_y = curr_x, curr_y

            # Blink Detection
            # Left eye indices
            left_eye = [33, 159, 145, 153, 154, 133]
            right_eye = [362, 386, 374, 380, 381, 263]

            left_ear = eye_aspect_ratio(lm, left_eye)
            right_ear = eye_aspect_ratio(lm, right_eye)

            # Mouth open detection
            mouth_ratio = mouth_open_ratio(lm, 13, 14)

            now = time.time()

            # Left click (left blink)
            if left_ear < EAR_THRESHOLD and now - last_click > 0.4:
                pyautogui.click()
                last_click = now
                cv2.putText(frame, "Left Click", (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Right click
            elif right_ear < EAR_THRESHOLD and now - last_click > 0.4:
                pyautogui.rightClick()
                last_click = now
                cv2.putText(frame, "Right Click", (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            # Double blink → double click
            elif left_ear < EAR_THRESHOLD and right_ear < EAR_THRESHOLD and now - last_click > 0.5:
                pyautogui.doubleClick()
                last_click = now
                cv2.putText(frame, "Double Click", (10, 90),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # Mouth open → Screenshot
            if mouth_ratio > MOUTH_THRESHOLD and now - last_click > 1:
                pyautogui.screenshot("face_screenshot.png")
                last_click = now
                cv2.putText(frame, "Screenshot!", (10, 140),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        cv2.imshow("Face Control", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
