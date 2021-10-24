# HandControl: Controlling computers with the swipe of a hand
This module along with BodyTracking.py are used to control computer functions without the use of a mouse.<br><br>
Functions included:
* Moving mouse
* Left and right-clicks
* Highlighting text
* Move files and windows
* Scrolling up and down
* Volume control

# USAGE
<strong>* * * Must have webcam in order for CV to register hand * * * </strong><br><br>
Computer screens vary and so some parameters may need to be adjusted to fit accordingly. Hand distance from the screen is also taken into consideration when considering click functions. The HandControl class can be initialized with just screen dimensions, however it is recommended that the camera dimensions are equivalent to the screen dimensions for optimal performance and hand tracking. Furthmore, the frame_pad is recommended to be no less than 1/5th (20%) the size of the screen <u>height</u> and no more than 1/3rd (33%) to allote both room for hand movement and stability of mouse.

<h2>Functions</h2>
<strong><u>LEFT-CLICK</u></strong><br>
In order to simulate a mouse left-click, simply pinch the index finger and thumb together and quickly release. A click-drag (for moving and highlighting text) is simulated the same way except the pinch is <u>held</u> at a starting point and let go to end drag.<br><br>

<Strong>RIGHT-CLICK</strong><br>
To simulate a right-click the user will push their middle finger downwards towards the wrist as the hand is upright. When the middle fingers returns to position the right-click will be executed. As with the left-click, the right-click function can be held down until the finger is returned to the original upright position.<br><br>

<strong>SCROLLING</strong><br>
To scroll the window up or down the index finger will be the only finger left up while the others are closed (a pointing gesture). The direction that the finger is pointing towards is the direction the page will scroll in. The starting position of the scroll is parallel to the ground (in this case the camera), and the more it is angled up or down, the more the scroll velocity will increase in that direction (pointing straight up is 100% velocity scrolling up while straight down is 100% downward).<br><br>
 
<strong>VOLUME ADJUSTMENT</strong><br>
Volume adjustment is triggered by raising the index and middle finger and closing all other fingers into the palm. While the hand is kept upright (palm forward), move fingers left to decrease volume and right to increase it.
  
<h2>Stopping Mouse Control</h2>
In order to stop the hand from controlling the mouse, the user may create a fist (all fingers into the palm) to cease control.  
