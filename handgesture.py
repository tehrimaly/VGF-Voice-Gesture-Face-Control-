import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time

# Initialize Mediapipe and PyAutoGUI
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1)
screen_width, screen_height = pyautogui.size()

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Smooth motion settings
prev_x, prev_y = 0, 0
smoothening = 3  # smaller = faster response

# Click cooldown (very short for speed)
last_click_time = 0
click_cooldown = 0.3  # seconds

def distance(a, b):
    return np.linalg.norm(np.array(a) - np.array(b))

while True:
    success, frame = cap.read()
    if not success:
        print("Camera not found.")
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)
    frame_height, frame_width, _ = frame.shape

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            index_finger = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            middle_finger = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            thumb = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

            x = int(index_finger.x * frame_width)
            y = int(index_finger.y * frame_height)

            # Map camera coordinates to screen
            screen_x = np.interp(x, (100, frame_width - 100), (0, screen_width))
            screen_y = np.interp(y, (100, frame_height - 100), (0, screen_height))

            curr_x = prev_x + (screen_x - prev_x) / smoothening
            curr_y = prev_y + (screen_y - prev_y) / smoothening
            pyautogui.moveTo(curr_x, curr_y)
            prev_x, prev_y = curr_x, curr_y

            # Finger distances
            index_middle = distance([index_finger.x, index_finger.y], [middle_finger.x, middle_finger.y])
            thumb_index = distance([thumb.x, thumb.y], [index_finger.x, index_finger.y])
            thumb_middle = distance([thumb.x, thumb.y], [middle_finger.x, middle_finger.y])

            now = time.time()

            # --- Gestures ---
            # Left Click (Index + Middle close)
            if index_middle < 0.05 and (now - last_click_time > click_cooldown):
                pyautogui.click()
                last_click_time = now
                cv2.putText(frame, "Left Click", (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Right Click (Thumb + Index close)
            elif thumb_index < 0.05 and (now - last_click_time > click_cooldown):
                pyautogui.rightClick()
                last_click_time = now
                cv2.putText(frame, "Right Click", (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            # Double Click (Thumb + Middle close)
            elif thumb_middle < 0.05 and (now - last_click_time > click_cooldown):
                pyautogui.doubleClick()
                last_click_time = now
                cv2.putText(frame, "Double Click", (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # Screenshot (All three close together)
            elif (thumb_index < 0.05 and thumb_middle < 0.05 and index_middle < 0.05 and
                  (now - last_click_time > 1)):
                pyautogui.screenshot("gesture_screenshot.png")
                last_click_time = now
                cv2.putText(frame, "Screenshot!", (10, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    cv2.imshow("Hand Gesture Control", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
