import random
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time
import pygame



# Initialize sound effects
pygame.mixer.init()
pygame.mixer.music.load("Resources/rps.mp3")
sound_effects = {
    "win": pygame.mixer.Sound("Resources/win.wav"),
    "lose": pygame.mixer.Sound("Resources/lose.wav"),
    "draw": pygame.mixer.Sound("Resources/draw.wav"),
}

def display_exit_button(imgBG):
    cv2.rectangle(imgBG, (10, 10), (60, 60), (0, 0, 255), 2, cv2.LINE_AA)
    cv2.putText(imgBG, "ESC", (13, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)

def check_for_exit(event, imgBG):
    if event == cv2.EVENT_LBUTTONDOWN:
        if 10 <= event.x <= 60 and 10 <= event.y <= 60:
            cv2.destroyAllWindows()
            cap.release()
            exit(0)

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

detector = HandDetector(maxHands=1)

timer = 0
stateResult = False
startGame = False
scores = [0, 0]  # [AI, Player]

cv2.namedWindow("Rock Paper Scissors")
cv2.setMouseCallback("Rock Paper Scissors", check_for_exit)
music_start_time = None

while True:
    imgBG = cv2.imread("Resources/BG.png")
    success, img = cap.read()

    imgScaled = cv2.resize(img, (0, 0), None, 0.875, 0.875)
    imgScaled = imgScaled[:, 80:480]

    # Find Hands
    hands, img = detector.findHands(imgScaled)  # with draw
    display_exit_button(imgBG)

    if startGame:

        if stateResult is False:
            timer = time.time() - initialTime
            cv2.putText(imgBG, str(int(timer)), (605, 435), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)

            if timer > 3:
                stateResult = True
                timer = 0

                if hands:
                    playerMove = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    if fingers == [0, 0, 0, 0, 0]:
                        playerMove = 1
                    if fingers == [1, 1, 1, 1, 1]:
                        playerMove = 2
                    if fingers == [0, 1, 1, 0, 0]:
                        playerMove = 3

                    randomNumber = random.randint(1, 3)
                    imgAI = cv2.imread(f'Resources/{randomNumber}.png', cv2.IMREAD_UNCHANGED)
                    imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

                    # Player Wins
                    if (playerMove == 1 and randomNumber == 3) or \
                            (playerMove == 2 and randomNumber == 1) or \
                            (playerMove == 3 and randomNumber == 2):
                        scores[1] += 1
                        sound_effects["win"].play()

                    # AI Wins
                    elif (playerMove == 3 and randomNumber == 1) or \
                            (playerMove == 1 and randomNumber == 2) or \
                            (playerMove == 2 and randomNumber == 3):
                        scores[0] += 1
                        sound_effects["lose"].play()

                    # Draw
                    else:
                        sound_effects["draw"].play()

    imgBG[234:654, 795:1195] = imgScaled

    if stateResult:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

    cv2.putText(imgBG, str(scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.putText(imgBG, str(scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)

    cv2.imshow("BG", imgBG)

    key = cv2.waitKey(1)
    if key == ord('s'):
        pygame.mixer.music.play(-1)
        music_start_time = time.time()
        startGame = True
        initialTime = time.time()
        stateResult = False
    elif key == 27:  # Esc key
        break
    else:
        if music_start_time and time.time() - music_start_time >= 3:  # Stop the music after 3 seconds
            pygame.mixer.music.stop()
            music_start_time = None


