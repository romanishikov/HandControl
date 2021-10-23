import pyautogui

from HandControl import MouseControl


if __name__ == "__main__":
    # Get the size of the current monitor
    width, height = pyautogui.size()  # E.g. 1920 X 1080
    hc = MouseControl(width, height)  # Basic example
    # hc = HandControl(width, height, cam_width=width, cam_height=height, frame_pad=300)  # Example with specs
    hc.run(1)  # Run using camera index 1import pyautogui
