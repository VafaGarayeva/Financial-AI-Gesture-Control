# ================= IMPORTS =================
import threading
import queue
import time
import cv2
import mediapipe as mp
import pandas as pd
import numpy as np
from playsound import playsound
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# ================= ALERT =================
def play_alert():

    try:
        playsound("alert.mp3")

    except:
        pass


# ================= DATA =================
df = pd.read_csv("creditcard.csv")

features = df[['Time', 'Amount']].copy()

scaler = StandardScaler()

features_scaled = scaler.fit_transform(features)

model = IsolationForest(
    contamination=0.03,
    random_state=42
)

model.fit(features_scaled)

# ================= QUEUE =================
transaction_queue = queue.Queue()

STREAM_DELAY = 2.2


def stream_data():

    while True:

        for row in df.itertuples(index=False):

            transaction_queue.put(row)

            time.sleep(STREAM_DELAY)


threading.Thread(
    target=stream_data,
    daemon=True
).start()

# ================= MEDIAPIPE =================
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# ================= CAMERA =================
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# ================= WINDOW =================
cv2.namedWindow(
    "FINAL FRAUD AI SYSTEM",
    cv2.WINDOW_NORMAL
)

cv2.resizeWindow(
    "FINAL FRAUD AI SYSTEM",
    1280,
    720
)

# ================= STATES =================
prev_time = time.time()

smooth_x = 0
prev_x = 0

alpha = 0.75

risk_history = []
transaction_feed = []

last_alert_time = 0
fraud_cooldown = 0

alert_flash_until = 0
alert_message_until = 0

last_swipe_time = 0

current_index = 0

# ================= TRANSACTION TIMER =================
last_transaction_update = 0

transaction_delay = 2.2

transaction = {
    "amount": 0,
    "score": 0,
    "country": "Unknown",
    "merchant": "Unknown"
}

# ================= EXTRA DATA =================
locations = [
    "Baku",
    "Moscow",
    "London",
    "Dubai",
    "Berlin",
    "Tokyo"
]

merchants = [
    "Amazon",
    "Steam",
    "Binance",
    "Apple",
    "PayPal",
    "Stripe"
]

# ================= EVENT ENGINE =================
def trigger_event(score):

    if score > 70:
        return "HIGH"

    elif score > 40:
        return "MEDIUM"

    else:
        return "LOW"


# ================= AI REASONS =================
def explain_fraud(score, amount):

    reasons = []

    if score > 60:
        reasons.append("Anomaly pattern detected")

    if amount > 1000:
        reasons.append("High transaction amount")

    if score > 40:
        reasons.append("Behavior deviation detected")

    if score > 85:
        reasons.append("Critical risk spike")

    if len(reasons) == 0:
        reasons.append("Normal transaction")

    return reasons


# ================= GLASS PANEL =================
def draw_glass_panel(frame):

    overlay = frame.copy()

    cv2.rectangle(
        overlay,
        (10, 10),
        (470, 430),
        (20, 20, 20),
        -1
    )

    frame = cv2.addWeighted(
        overlay,
        0.55,
        frame,
        0.45,
        0
    )

    return frame


# ================= RISK BAR =================
def draw_risk_bar(frame, score):

    cv2.rectangle(
        frame,
        (900, 80),
        (1240, 120),
        (40, 40, 40),
        -1
    )

    bar_width = int(score * 3.4)

    if score > 70:

        bar_color = (0, 0, 255)

    elif score > 40:

        bar_color = (0, 165, 255)

    else:

        bar_color = (0, 255, 0)

    cv2.rectangle(
        frame,
        (900, 80),
        (900 + bar_width, 120),
        bar_color,
        -1
    )

    cv2.putText(
        frame,
        f"RISK LEVEL: {int(score)}%",
        (900, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )


# ================= MAIN LOOP =================
while True:

    ret, frame = cap.read()

    if not ret:
        continue

    frame = cv2.flip(frame, 1)

    # ================= CYBER EFFECT =================
    overlay_dark = frame.copy()

    cv2.rectangle(
        overlay_dark,
        (0, 0),
        (frame.shape[1], frame.shape[0]),
        (0, 0, 0),
        -1
    )

    frame = cv2.addWeighted(
        overlay_dark,
        0.12,
        frame,
        0.88,
        0
    )

    # ================= FPS =================
    curr_time = time.time()

    fps = 1 / max(curr_time - prev_time, 0.001)

    prev_time = curr_time

    # ================= HAND DETECTION =================
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = hands.process(rgb)

    if result.multi_hand_landmarks:

        for hand in result.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                hand,
                mp_hands.HAND_CONNECTIONS
            )

            h, w, _ = frame.shape

            index_x = int(hand.landmark[8].x * w)

            thumb_x = int(hand.landmark[4].x * w)

            # ================= FIST DETECTION =================
            index_tip_y = hand.landmark[8].y
            index_pip_y = hand.landmark[6].y

            middle_tip_y = hand.landmark[12].y
            middle_pip_y = hand.landmark[10].y

            ring_tip_y = hand.landmark[16].y
            ring_pip_y = hand.landmark[14].y

            # ================= SMOOTH =================
            smooth_x = alpha * index_x + (1 - alpha) * smooth_x

            swipe = smooth_x - prev_x

            prev_x = smooth_x

            # ================= GESTURES =================
            finger_close = abs(index_x - thumb_x) < 45

            fist = (
                index_tip_y > index_pip_y and
                middle_tip_y > middle_pip_y and
                ring_tip_y > ring_pip_y
            )

            current_time = time.time()

            # ================= SWIPE RIGHT =================
            if (
                swipe > 140 and
                current_time - last_swipe_time > 1
            ):

                current_index += 1

                last_swipe_time = current_time

            # ================= SWIPE LEFT =================
            elif (
                swipe < -140 and
                current_time - last_swipe_time > 1
            ):

                current_index -= 1

                if current_index < 0:
                    current_index = 0

                last_swipe_time = current_time

            # ================= ALERT =================
            if (
                finger_close and
                fist and
                current_time - fraud_cooldown > 5
            ):

                if current_time - last_alert_time > 3:

                    threading.Thread(
                        target=play_alert,
                        daemon=True
                    ).start()

                    last_alert_time = current_time

                    fraud_cooldown = current_time

                    alert_flash_until = current_time + 1.5

                    alert_message_until = current_time + 3

                    transaction_feed.append(
                        "BLOCKED | FRAUD TRANSACTION"
                    )

                    if len(transaction_feed) > 8:
                        transaction_feed.pop(0)

    # ================= ALERT FLASH =================
    if time.time() < alert_flash_until:

        alert_overlay = frame.copy()

        cv2.rectangle(
            alert_overlay,
            (0, 0),
            (frame.shape[1], frame.shape[0]),
            (0, 0, 255),
            -1
        )

        frame = cv2.addWeighted(
            alert_overlay,
            0.08,
            frame,
            0.92,
            0
        )

    # ================= TRANSACTION STREAM =================
    current_stream_time = time.time()

    if (
        current_stream_time - last_transaction_update > transaction_delay
        and not transaction_queue.empty()
    ):

        last_transaction_update = current_stream_time

        row = transaction_queue.get()

        amount = row.Amount
        time_value = row.Time

        scaled = scaler.transform(
            np.array([[time_value, amount]])
        )

        anomaly = model.decision_function(scaled)[0]

        # ================= SMART AI SCORE =================
        normalized = np.interp(
            anomaly,
            [-0.20, 0.20],
            [100, 0]
        )

        score = normalized

        # RANDOM VARIATION
        score += np.random.randint(-18, 18)

        # HIGH AMOUNT BOOST
        if amount > 2000:
            score += 35

        elif amount > 1000:
            score += 20
        elif amount > 500:
            score += 10

        # LIMIT SCORE
        score = np.clip(score, 1, 99)

        # ================= SMOOTH TRANSITION =================
        if len(risk_history) > 0:

            score = (
                risk_history[-1] * 0.25 +
                score * 0.75
            )

        risk_history.append(score)

        if len(risk_history) > 20:
            risk_history.pop(0)

        location = locations[
            current_index % len(locations)
        ]

        merchant = merchants[
            current_index % len(merchants)
        ]

        transaction = {
            "amount": amount,
            "score": score,
            "country": location,
            "merchant": merchant
        }

        transaction_feed.append(
            f"{location} | ${amount:.0f} | {int(score)}%"
        )

        if len(transaction_feed) > 8:
            transaction_feed.pop(0)

    # ================= STATUS =================
    if transaction["score"] > 78:

        status = "HIGH RISK"
        color = (0, 0, 255)

    elif transaction["score"] > 48:

        status = "SUSPICIOUS"
        color = (0, 165, 255)

    else:

        status = "SAFE"
        color = (0, 255, 0)

    # ================= AI CONFIDENCE =================
    ai_confidence = np.clip(
        transaction["score"] + np.random.randint(5, 15),
        15,
        99
    )

    # ================= EVENT =================
    event_level = trigger_event(
        transaction["score"]
    )

    # ================= REASONS =================
    reasons = explain_fraud(
        transaction["score"],
        transaction["amount"]
    )

    # ================= SCANNING LINE =================
    scan_y = int((time.time() * 250) % frame.shape[0])

    cv2.line(
        frame,
        (0, scan_y),
        (frame.shape[1], scan_y),
        (0, 255, 255),
        1
    )

    # ================= PANELS =================
    frame = draw_glass_panel(frame)

    # ================= TITLE =================
    cv2.putText(
        frame,
        "AI POWERED FRAUD DETECTION",
        (30, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 255),
        2
    )

    # ================= TRANSACTION INFO =================
    cv2.putText(
        frame,
        f"AMOUNT: ${transaction['amount']:.2f}",
        (40, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"COUNTRY: {transaction['country']}",
        (40, 140),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"MERCHANT: {transaction['merchant']}",
        (40, 180),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"STATUS: {status}",
        (40, 230),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        color,
        2
    )

    cv2.putText(
        frame,
        f"AI CONFIDENCE: {ai_confidence:.1f}%",
        (40, 270),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 0, 255),
        2
    )

    cv2.putText(
        frame,
        f"EVENT: {event_level}",
        (40, 320),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 0),
        2
    )

    # ================= AI REASONS =================
    for i, reason in enumerate(reasons):

        cv2.putText(
            frame,
            f"- {reason}",
            (40, 370 + i * 25),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (220, 220, 220),
            1
        )

    # ================= ALERT MESSAGE =================
    if time.time() < alert_message_until:

        glow = frame.copy()

        cv2.rectangle(
            glow,
            (350, 250),
            (950, 420),
            (0, 0, 255),
            -1
        )

        frame = cv2.addWeighted(
            glow,
            0.12,
            frame,
            0.88,
            0
        )

        cv2.putText(
            frame,
            "FRAUD DETECTED",
            (430, 330),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.5,
            (255, 255, 255),
            4
        )

        cv2.putText(
            frame,
            "TRANSACTION BLOCKED",
            (450, 380),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (255, 255, 255),
            2
        )

    # ================= RISK BAR =================
    draw_risk_bar(
        frame,
        transaction["score"]
    )

    # ================= LIVE GRAPH =================
    cv2.rectangle(
        frame,
        (900, 180),
        (1240, 500),
        (30, 30, 30),
        -1
    )

    cv2.putText(
        frame,
        "LIVE AI RISK",
        (980, 160),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    if len(risk_history) > 1:

        for i in range(len(risk_history) - 1):

            line_score = risk_history[i]

            if line_score > 70:

                graph_color = (0, 0, 255)

            elif line_score > 40:

                graph_color = (0, 165, 255)

            else:

                graph_color = (0, 255, 0)

            x1 = 920 + i * 15
            y1 = 470 - int(risk_history[i] * 2.8)

            x2 = 920 + (i + 1) * 15
            y2 = 470 - int(risk_history[i + 1] * 2.8)

            cv2.line(
                frame,
                (x1, y1),
                (x2, y2),
                graph_color,
                2
            )

    # ================= LIVE FEED =================
    cv2.rectangle(
        frame,
        (900, 520),
        (1240, 680),
        (25, 25, 25),
        -1
    )

    cv2.putText(
        frame,
        "LIVE TRANSACTION FEED",
        (930, 545),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    for i, item in enumerate(transaction_feed[-5:]):

        feed_color = (180, 255, 180)

        if "BLOCKED" in item:
            feed_color = (0, 0, 255)

        cv2.putText(
            frame,
            item,
            (920, 580 + i * 22),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.52,
            feed_color,
            1
        )

    # ================= FPS =================
    cv2.putText(
        frame,
        f"FPS: {int(fps)}",
        (1150, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 0),
        2
    )

    # ================= FOOTER =================
    cv2.putText(
        frame,
        "AI FINTECH SECURITY ENGINE",
        (930, 705),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (150, 150, 150),
        1
    )

    # ================= SHOW =================
    cv2.imshow(
        "FINAL FRAUD AI SYSTEM",
        frame
    )

    # ================= EXIT =================
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ================= CLEANUP =================
cap.release()

hands.close()

cv2.destroyAllWindows()