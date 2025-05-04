import pyautogui

pyautogui.PAUSE = 1
pyautogui.FAILSAFE = False

for _ in range(3):
    pyautogui.moveTo(100, 100, duration=0.1)
    pyautogui.moveTo(400, 100, duration=0.1)
    pyautogui.moveTo(400, 400, duration=0.1)
    pyautogui.moveTo(100, 400, duration=0.1)
