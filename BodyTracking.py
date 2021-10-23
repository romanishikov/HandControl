import cv2
import mediapipe as mp


KEY_POINTS = {
              "wrist": 0,
              "thumb-cmc": 1, "thumb-mcp": 2, "thumb-ip": 3, "thumb": 4,
              "index-mcp": 5, "index-pip": 6, "index-dip": 7, "index": 8,
              "middle-mcp": 9, "middle-pip": 10, "middle-dip": 11, "middle": 12,
              "ring-mcp": 13, "ring-pip": 14, "ring-dip": 15, "ring": 16,
              "pinky-mcp": 17, "pinky-pip": 18, "pinky-dip": 19, "pinky": 20
              }


class HandDetector:
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5, fistTH=250, fingerUpTH=400):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.results = ""
        self.mpDraw = mp.solutions.drawing_utils

        self.fistThreshold = fistTH
        self.fingerUpThreshold = fingerUpTH

    def get_hands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if draw:
            if self.results.multi_hand_landmarks:
                for hand in self.results.multi_hand_landmarks:
                    self.mpDraw.draw_landmarks(img, hand, self.mpHands.HAND_CONNECTIONS,
                                               self.mpDraw.DrawingSpec((255, 0, 0)),
                                               self.mpDraw.DrawingSpec((255, 0, 255)))

        return img

    def get_hand_positions(self, img, handNo=0):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for hid, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy, cz = int(lm.x * w), int(lm.y * h), int(lm.z * c)
                lmList.append([hid, cx, cy, lm.z])

        return lmList

    def get_fingers_up(self, lmList):
        fingers_up = []
        FUT = self.fingerUpThreshold
        xWrist, yWrist = lmList[0][1], lmList[0][2]
        tip_list = [8, 12, 16, 20]
        for tip in tip_list:
            xVal, yVal, zVal = lmList[tip][1], lmList[tip][2], lmList[tip][3]
            if abs(yWrist - yVal) >= FUT or abs(xWrist-xVal) >= FUT:
                # print("Y: " + str(abs(yWrist - yVal)), "X: " + str(abs(xWrist - xVal)))
                fingers_up.append(tip)

        return fingers_up

    def check_if_fist(self, lmList):
        FT = self.fistThreshold
        xWrist, yWrist = lmList[0][1], lmList[0][2]
        xIndex, yIndex = lmList[8][1], lmList[8][2]
        xMiddle, yMiddle = lmList[12][1], lmList[12][2]
        xRing, yRing = lmList[16][1], lmList[16][2]
        xPinky, yPinky = lmList[20][1], lmList[20][2]
        
        yClosed = abs(yWrist-yIndex) < FT and abs(yWrist-yMiddle) < FT and abs(yWrist-yRing) < FT and abs(yWrist-yPinky) < FT
        xClosed = abs(xWrist-xIndex) < FT and abs(xWrist-xMiddle) < FT and abs(xWrist-xRing) < FT and abs(xWrist-xPinky) < FT

        if yClosed and xClosed:
            return True

        return False
