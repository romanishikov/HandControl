import cv2
import time
import mouse
import platform
import BodyTracking as BT


class MouseControl:
    def __init__(self, screen_width, screen_height, cam_width=640, cam_height=480, frame_pad=100):
        # Specify the dimension of the camera and computer screen. Recommended to be the same as one another.
        # NOTE: CAM DIMENSIONS SHOULD NOT BE MORE THAN MONITOR DIMENSIONS
        self.wCam = cam_width
        self.hCam = cam_height
        self.wScreen = screen_width
        self.hScreen = screen_height
        # Add padding to the camera feed to allow room for hand to fully cross screen. Subtract from each side of cam.
        self.framePad = frame_pad
        # Get the center of the camera feed
        self.xCenter = self.wCam / 2
        self.yCenter = self.hCam / 2
        # Get the proportions for:
        # a) Distance between camera center and the frame edge on the X and Y axis
        # b) Monitor size with respect to cam dimensions
        self.xFrameRatio = self.xCenter / self.framePad
        self.yFrameRatio = self.yCenter / self.framePad
        self.xProportion = self.wScreen / self.wCam
        self.yProportion = self.hScreen / self.hCam
        # Assuming the hand is read bottom to top (Y axis), set the distance required to register a click (left/right)
        # - Left-click measures distance between tip of index to tip of thumb
        # - Right-click measures distance between tip of middle finger and wrist
        # * * * Divider values can be adjusted to what works best on the monitor * * *
        self.LClickDistance = self.hCam / 18
        self.RClickDistance = self.hCam / 5
        # Specify the distance required to register a fist and if a finger(s) is held up/extended.
        # - Fist is measured by calculating distance of each finger to the wrist;
        #   if all fingers are less than threshold than it is considered a fist.
        # - Fingers measures the same way with all fingers, except if fingers exceed threshold
        #   then we count them as being "up" or extended.
        # * * * Divider values can be adjusted to what works best on the monitor * * *
        self.fistThreshold = int(self.hCam / 4.5)
        self.fingerThreshold = int(self.hCam / 2.7)

    def run(self, camera_index=0):
        cap = cv2.VideoCapture(camera_index)
        cap.set(3, self.wCam)
        cap.set(4, self.hCam)

        hd = BT.HandDetector(maxHands=1, detectionCon=0.9, fistTH=self.fistThreshold, fingerUpTH=self.fingerThreshold)

        while True:
            success, img = cap.read()

            img = hd.get_hands(img, draw=True)
            lmList = hd.get_hand_positions(img, handNo=0)
            if len(lmList) != 0:
                fingers_up = hd.get_fingers_up(lmList)  # Get the fingers that are straightened out
                is_fist = hd.check_if_fist(lmList)  # Making a fist deactivates mouse control
                if not is_fist:
                    xWrist, yWrist = lmList[0][1], lmList[0][2]  # Used in conjunction with middle to right-click
                    xThumb, yThumb = lmList[4][1], lmList[4][2]  # Used in conjunction with index to left-click
                    xIndex, yIndex = lmList[8][1], lmList[8][2]  # Used with thumb for left-click measurements
                    xMiddle, yMiddle = lmList[12][1], lmList[12][2]  # Used for right-click measurements
                    xIndexMCP, yIndexMCP = lmList[5][1], lmList[5][2]  # Used for scrolling measurements
                    xRingMCP, yRingMCP = lmList[13][1], lmList[13][2]  # Point that the mouse will reference

                    # Formulas for adjusting the position of the mouse based on cam and frame dimensions
                    xAdjust = (self.xCenter - xRingMCP) / self.xFrameRatio
                    yAdjust = (self.yCenter - yRingMCP) / self.yFrameRatio
                    # The X axis measures right-to-left so we adjust it here
                    xMouse = self.wScreen - ((xRingMCP-xAdjust) * self.xProportion)
                    yMouse = (yRingMCP-yAdjust) * self.yProportion

                    if [8] == fingers_up:  # Using only index finger, point up or down to scroll in that direction
                        self.__scroll_page(yIndex, yIndexMCP)
                    else:
                        self.__check_click("right", abs(xWrist - xMiddle), abs(yWrist - yMiddle))
                        self.__check_click("left", abs(xThumb - xIndex), abs(yThumb - yIndex))

                    mouse.move(xMouse, yMouse)

            cv2.imshow("Live", img)
            cv2.waitKey(1)

    def __check_click(self, click_type, xDistance, yDistance):
        click_ratio = self.RClickDistance if click_type == "right" else self.LClickDistance
        if yDistance <= click_ratio >= xDistance:
            if not mouse.is_pressed(click_type):
                mouse.press(click_type)
        elif mouse.is_pressed(click_type):
            mouse.release(click_type)
            time.sleep(0.2)  # This is optional, however having a pause upon release lets the action reset properly

    @staticmethod
    def __scroll_page(index_pos, index_mcp_pos):
        diff = abs(index_pos - index_mcp_pos) if abs(index_pos - index_mcp_pos) <= 200 else 200
        scroll_rate = 0.005 * diff
        if index_pos > index_mcp_pos:
            mouse.wheel(-scroll_rate)
        elif index_pos < index_mcp_pos:
            mouse.wheel(scroll_rate)

