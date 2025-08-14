# VMouse.py
# This is licensed under The 2LD OSL which can be found at https://github.com/2-LazyDevs/LICENSE/blob/main/LICENSE

import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time

print("VMouse - Virtual Mouse")
print("Version 0.5 - Alpha - Work in progress")
print("If you encounter any bugs or problems, report at https://github.com/2-LazyDevs/VMouse")
print("Licensed under The 2LD OSL - https://github.com/2-LazyDevs/LICENSE")
print("Made by AR-DEV-1 of 2LazyDevs")
print("Thanks to everyone who made this possible!")
print("")
print("")
print("")
print("")

# Config
SMOOTHING = 2 
PINCH_THRESHOLD = 0.05
DRAG_HOLD_TIME = 0.5
SWIPE_DISTANCE = 200
SWIPE_TIME = 0.4
ZOOM_MOVE_THRESHOLD = 15  # pixels movement to trigger zoom
pyautogui.FAILSAFE = False

FULLSCREEN_DISPLAY = input("Full screen mode? (y/n): ").strip().lower() == 'y'
# Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.6)
mp_draw = mp.solutions.drawing_utils

# Screen
screen_w, screen_h = pyautogui.size()
prev_x, prev_y = 0, 0

# State
pinch_start_time = None
dragging = False
scroll_mode = False
scroll_start_y = None
hand_positions = []
last_swipe_time = 0
zoom_mode = False
zoom_start_y = None
last_zoom_time = 0
CLICK_THRESHOLD = 0.04
CLICK_COOLDOWN = 0.3
last_click_time = 0

cap = cv2.VideoCapture(0)

def finger_distance(lm, f1, f2):
    return np.linalg.norm([lm[f1].x - lm[f2].x, lm[f1].y - lm[f2].y])

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks and results.multi_handedness:
        # Use best detected hand
        best_idx = max(range(len(results.multi_hand_landmarks)),
                       key=lambda i: results.multi_handedness[i].classification[0].score)

        hand_landmarks = results.multi_hand_landmarks[best_idx]
        handedness = results.multi_handedness[best_idx].classification[0].label
        lm = hand_landmarks.landmark

        index_finger = lm[mp_hands.HandLandmark.INDEX_FINGER_TIP]
        x = int(index_finger.x * screen_w)
        y = int(index_finger.y * screen_h)

        curr_x = prev_x + (x - prev_x) / SMOOTHING
        curr_y = prev_y + (y - prev_y) / SMOOTHING
        prev_x, prev_y = curr_x, curr_y


        click_dist = finger_distance(lm, mp_hands.HandLandmark.THUMB_TIP, mp_hands.HandLandmark.INDEX_FINGER_TIP)

        if click_dist < CLICK_THRESHOLD and time.time() - last_click_time > CLICK_COOLDOWN:
            pyautogui.click()
            last_click_time = time.time()
        pinch_dist = finger_distance(lm, mp_hands.HandLandmark.THUMB_TIP, mp_hands.HandLandmark.INDEX_FINGER_TIP)

        # Scroll mode
        if scroll_mode:
            if scroll_start_y is None:
                scroll_start_y = curr_y
            delta = scroll_start_y - curr_y
            if abs(delta) > 20:
                pyautogui.scroll(int(delta / 5))
                scroll_start_y = curr_y
        else:
            # Zoom mode (via 2 hands)
            if results.multi_hand_landmarks and len(results.multi_hand_landmarks) >= 2:
                # Get both hands
                hand1 = results.multi_hand_landmarks[0].landmark
                hand2 = results.multi_hand_landmarks[1].landmark

                # Use index finger tip distance between 2 hands
                index1 = hand1[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                index2 = hand2[mp_hands.HandLandmark.INDEX_FINGER_TIP]

                # Horizontal Distance
                hand_distance = np.linalg.norm([index1.x - index2.x, index1.y - index2.y])

                if hand_distance < 0.2: # Hands close together
                    if not zoom_mode:
                        zoom_mode = True
                        zoom_start_y = curr_y
                    else:
                        move_y = zoom_start_y - curr_y
                        if abs(move_y) > ZOOM_MOVE_THRESHOLD and time.time() - last_zoom_time > 0.2:
                            if move_y > 0:
                                pyautogui.hotkey('ctrl', '+')
                            else:
                                pyautogui.hotkey('ctrl', '-')
                            last_zoom_time = time.time()
                            zoom_start_y = curr_y
            else:
                zoom_mode = False
                zoom_start_y = None
                pyautogui.moveTo(curr_x, curr_y, duration=0)

        # Click / drag logic
        if pinch_dist < PINCH_THRESHOLD:
            if pinch_start_time is None:
                pinch_start_time = time.time()
            else:
                if time.time() - pinch_start_time > DRAG_HOLD_TIME:
                    if not dragging:
                        pyautogui.mouseDown()
                        dragging = True
        else:
            if pinch_start_time is not None:
                if dragging:
                    pyautogui.mouseUp()
                    dragging = False
                else:
                    if time.time() - pinch_start_time < DRAG_HOLD_TIME:
                        pyautogui.click()
                pinch_start_time = None

        # Other gestures
        pinch2 = finger_distance(lm, mp_hands.HandLandmark.INDEX_FINGER_TIP, mp_hands.HandLandmark.MIDDLE_FINGER_TIP)
        pinch3 = finger_distance(lm, mp_hands.HandLandmark.INDEX_FINGER_TIP, mp_hands.HandLandmark.RING_FINGER_TIP)

        if pinch2 < PINCH_THRESHOLD:
            pyautogui.rightClick()
            time.sleep(0.3)
        if pinch3 < PINCH_THRESHOLD:
            pyautogui.middleClick()
            time.sleep(0.3)

        # Swipe detection for back/forward
        hand_positions.append((time.time(), curr_x))
        hand_positions = [p for p in hand_positions if time.time() - p[0] < SWIPE_TIME]

        if len(hand_positions) > 1:
            dx = hand_positions[-1][1] - hand_positions[0][1]
            if abs(dx) > SWIPE_DISTANCE and time.time() - last_swipe_time > 0.5:
                if dx > 0:
                    pyautogui.hotkey('alt', 'right')
                else:
                    pyautogui.hotkey('alt', 'left')
                last_swipe_time = time.time()

        # Draw
        # mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        # cv2.putText(frame, f"Using: {handedness} hand", (10, 40),
                   #  cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        # if scroll_mode:
            # cv2.putText(frame, "SCROLL MODE", (10, 80),
                        # cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        # if zoom_mode:
            # cv2.putText(frame, "ZOOM MODE", (10, 120),
                        # cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

    else:
        zoom_mode = False
        zoom_start_y = None
    
    cv2.namedWindow("VMouse", cv2.WINDOW_NORMAL)
    width = screen_w if FULLSCREEN_DISPLAY else screen_w // 2
    cv2.resizeWindow("VMouse", width, screen_h)
    cv2.imshow("VMouse", frame)

    key = cv2.waitKey(1) & 0xFF
    if key in (27, ord('q')):
        break
    elif key == ord('s'):
        scroll_mode = not scroll_mode
        scroll_start_y = None

cap.release()
cv2.destroyAllWindows()
