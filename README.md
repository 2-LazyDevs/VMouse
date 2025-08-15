# VMouse
VMouse is a virtual mouse written in Python which utilizes OpenCV (Open ComputerVision), Mediapipe & pyautogui to move your mouse cursor with your hand. Basically, it tracks your hand's movement via your camera & where ever you move your hand, the cursor will follow. 

# Controls:
The controls are:

**Mouse Movement:**
- Move pointer → Move your index finger around in front of the camera.
  
**Clicking & Dragging (Single Hand):**
- Left Click → Briefly pinch thumb + index finger (less than `0.5s`).
- Drag & Drop → Pinch thumb + index finger and hold for more than `0.5s`, then release to drop.

**Other Clicks:**
- Right Click → Pinch index + middle fingers.
- Middle Click → Pinch index + ring fingers.

**Scrolling:**
- Press `S` to toggle scroll mode.
- While in scroll mode → Move hand up/down to scroll.

**Zooming (Two Hands Required):**
- Put both hands in frame, bring them close together (index fingertips within ~20% of screen width).
- Move hands up to zoom in `(Ctrl + +)`.
- Move hands down to zoom out `(Ctrl + -)`.

**Swiping (Back / Forward):**
- Swipe right → Browser forward (Alt + →).
- Swipe left → Browser back (Alt + ←).

**Keyboard Shortcuts while running the program:**
- `S` → Toggle scroll mode.
- `Q` or `Esc` → Quit.

`Notice: This file is only compatible with Python 3.12 for now as Mediapipe currently doesn't support 3.13, so if you get a Python error saying no compatible version found, it's most likely that you are running 3.13`

# How to use:

To use VMouse, download the latest release from the releases page. Extract the file from the zip. Navigate to the folder where you have extracted the files via CMD/SHELL, then run:
```pip install -r requirements.txt``` to install the required packages. Then run the file via: ```py VMouse.py``` or ```py Path/To/VMouse/VMouse.py```

# FAQ

`What is VMouse?`

`Ans: VMouse is a virtual mouse written in Python which utilizes OpenCV (Open ComputerVision), Mediapipe & pyautohui to move your mouse cursor with your hand. Basically, it tracks your hand's movement via your camera & where ever you move your hand, the cursor will follow. `

`Q2. Can I modify this?`

`Ans: Yes, you can modify this & add as many features as you want. Though, if you publish it online, it must be distributed with The 2LD OSL.`

`Q3. How do I use it?`

`Ans: To use VMouse, you can have a look at the How to use section.`

`Q4. What are the controls?`

`Ans: You should have a look at the controls section.`

`Q5. Which Python version does VMouse use?`

`Ans: VMouse uses Python 3.12`

`Q6. Do I need any special equipment to run this program?`

`Ans: No! All you need to do is install Python 3.12, hae a camera & install the required libraries.`

`Q7. Can I use two hands for normal control?`

`Ans: Yes, but zoom will trigger if both hands are close together and moved vertically. Keep them apart if you don’t want zoom.`

`Q8. Does it work in all apps?`

`Ans: It simulates real mouse and keyboard events, so it works in most desktop apps, browsers, and games that accept standard input.`

`Q9. My zoom keeps triggering when I don’t want it. What can I do?`

`Ans: Zoom mode only activates when two hands are close together. If you’re seeing accidental zoom, keep your second hand out of the camera view.`

`Q10. How do I quit the program?`

`Ans: Press Q or Esc in the program window.`

`Q11. Does it require an internet connection?`

`Ans: Yes, it does but to only install the required libraries. Otherwise, it runs entirely offline.`

