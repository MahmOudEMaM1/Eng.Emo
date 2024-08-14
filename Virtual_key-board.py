import cv2
import mediapipe as mp
import time

#model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Define the keyboard Components
keys = [
    # Row 1
    {'char': 'Q', 'pos': ((50, 100), (90, 140)), 'pressed': False, 'start_time': 0},
    {'char': 'W', 'pos': ((100, 100), (140, 140)), 'pressed': False, 'start_time': 0},
    {'char': 'E', 'pos': ((150, 100), (190, 140)), 'pressed': False, 'start_time': 0},
    {'char': 'R', 'pos': ((200, 100), (240, 140)), 'pressed': False, 'start_time': 0},
    {'char': 'T', 'pos': ((250, 100), (290, 140)), 'pressed': False, 'start_time': 0},
    {'char': 'Y', 'pos': ((300, 100), (340, 140)), 'pressed': False, 'start_time': 0},
    {'char': 'U', 'pos': ((350, 100), (390, 140)), 'pressed': False, 'start_time': 0},
    {'char': 'I', 'pos': ((400, 100), (440, 140)), 'pressed': False, 'start_time': 0},
    {'char': 'O', 'pos': ((450, 100), (490, 140)), 'pressed': False, 'start_time': 0},
    {'char': 'P', 'pos': ((500, 100), (540, 140)), 'pressed': False, 'start_time': 0},

    # Row 2
    {'char': 'A', 'pos': ((70, 150), (110, 190)), 'pressed': False, 'start_time': 0},
    {'char': 'S', 'pos': ((120, 150), (160, 190)), 'pressed': False, 'start_time': 0},
    {'char': 'D', 'pos': ((170, 150), (210, 190)), 'pressed': False, 'start_time': 0},
    {'char': 'F', 'pos': ((220, 150), (260, 190)), 'pressed': False, 'start_time': 0},
    {'char': 'G', 'pos': ((270, 150), (310, 190)), 'pressed': False, 'start_time': 0},
    {'char': 'H', 'pos': ((320, 150), (360, 190)), 'pressed': False, 'start_time': 0},
    {'char': 'J', 'pos': ((370, 150), (410, 190)), 'pressed': False, 'start_time': 0},
    {'char': 'K', 'pos': ((420, 150), (460, 190)), 'pressed': False, 'start_time': 0},
    {'char': 'L', 'pos': ((470, 150), (510, 190)), 'pressed': False, 'start_time': 0},

    # Row 3
    {'char': 'Z', 'pos': ((100, 200), (140, 240)), 'pressed': False, 'start_time': 0},
    {'char': 'X', 'pos': ((150, 200), (190, 240)), 'pressed': False, 'start_time': 0},
    {'char': 'C', 'pos': ((200, 200), (240, 240)), 'pressed': False, 'start_time': 0},
    {'char': 'V', 'pos': ((250, 200), (290, 240)), 'pressed': False, 'start_time': 0},
    {'char': 'B', 'pos': ((300, 200), (340, 240)), 'pressed': False, 'start_time': 0},
    {'char': 'N', 'pos': ((350, 200), (390, 240)), 'pressed': False, 'start_time': 0},
    {'char': 'M', 'pos': ((400, 200), (440, 240)), 'pressed': False, 'start_time': 0},

    # Space button
    {'char': ' ', 'pos': ((200, 250), (300, 290)), 'label': 'SPACE', 'pressed': False, 'start_time': 0},

    # Backspace button
    {'char': 'Backspace', 'pos': ((310, 250), (455, 290)), 'label': 'BACKSPACE', 'pressed': False, 'start_time': 0}
]

# Track the current state of pressed keys
key_pressed = {key['char']: False for key in keys}
key_press_delay = 0.2  # 200 milliseconds delay

# Function to check if the fingertip is on a key
def check_key_press(x, y, keys):
    for key in keys:
        (x1, y1), (x2, y2) = key['pos']
        if x1 <= x <= x2 and y1 <= y <= y2:
            return key
    return None

# Function to draw the keyboard on the image
def draw_keyboard(image, keys):
    for key in keys:
        (x1, y1), (x2, y2) = key['pos']
        color = (0, 255, 0) if key['pressed'] else (255, 255, 255)  # Green if pressed, else white
        cv2.rectangle(image, (x1, y1), (x2, y2), color, -1)  # Filled rectangle
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 0), 2)  # Black border

        # Draw the character label
        char_label = key.get('label', key['char'])
        cv2.putText(image, char_label, (x1 + 10, y2 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

# Function to draw all hand landmarks
def draw_hand_landmarks(image, hand_landmarks, mp_hands):
    for idx, landmark in enumerate(hand_landmarks.landmark):
        x = int(landmark.x * image.shape[1])
        y = int(landmark.y * image.shape[0])
        if idx == mp_hands.HandLandmark.INDEX_FINGER_TIP:
            cv2.circle(image, (x, y), 10, (0, 255, 0), -1)  # Larger green circle for fingertip
        else:
            cv2.circle(image, (x, y), 5, (255, 0, 0), -1)  # Smaller blue circles for other landmarks
    return hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

cap = cv2.VideoCapture(0)
typed_text = ""

while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    image = cv2.flip(image, 1)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            index_fingertip = draw_hand_landmarks(image, hand_landmarks, mp_hands)
            x, y = int(index_fingertip.x * image.shape[1]), int(index_fingertip.y * image.shape[0])

            key = check_key_press(x, y, keys)
            if key:
                current_time = time.time()
                # Start timer if fingertip is on the key
                if not key['pressed']:
                    key['start_time'] = current_time
                    key['pressed'] = True
                else:
                    # Check if the fingertip has been on the key for the delay duration
                    if current_time - key['start_time'] >= key_press_delay:
                        if not key_pressed[key['char']]:
                            if key['char'] == 'Backspace':
                                # Handle backspace: delete the last character in the typed text
                                typed_text = typed_text[:-1]
                            else:
                                typed_text += key['char']
                            key_pressed[key['char']] = True
            else:
                # Reset pressed status for all keys if no key is being pressed
                for key in keys:
                    key['pressed'] = False
                    key_pressed[key['char']] = False

    draw_keyboard(image, keys)

    # Draw the typed text box
    cv2.rectangle(image, (50, 50), (600, 90), (255, 255, 255), -1)
    cv2.putText(image, typed_text, (60, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    cv2.imshow('Virtual Keyboard', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
