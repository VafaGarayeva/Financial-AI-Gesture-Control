import streamlit as st
import cv2
import mediapipe as mp
import pandas as pd
import numpy as np

# Səhifə dizaynı
st.set_page_config(page_title="Vafa's AI Project", layout="wide")
st.title("🛡️ Financial Fraud Detector (AI + Gesture Control)")
st.sidebar.info("Vəfa Qarayeva tərəfindən hazırlandı.")

# Data simulyasiyası
data = {
    'Məbləğ': [150, 5200, 80, 4800, 210],
    'Saat': [14, 3, 11, 1, 16],
    'Tip': ['Local', 'International', 'Local', 'International', 'Local']
}
df = pd.DataFrame(data)

# AI Məntiqi (Sizin 1-ci gün hazırladığınız modelin bənzəri)
def check_fraud(row):
    if row['Məbləğ'] > 4000 and row['Saat'] < 6:
        return "🚨 FRAUD!"
    return "✅ CLEAN"

# Kamera və MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7)

st.subheader("📸 Canlı Kamera Analizi")
img_file = st.camera_input("Barmağınızı seçmək istədiyiniz sətrin üzərində tutun")

if img_file:
    # Şəkli emal etmək
    file_bytes = np.asarray(bytearray(img_file.read()), dtype=np.uint8)
    frame = cv2.imdecode(file_bytes, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        # Barmaq ucunu tapırıq
        point8 = results.multi_hand_landmarks[0].landmark[8]
        selected_idx = int(point8.y * len(df))
        selected_idx = max(0, min(selected_idx, len(df)-1))
        
        row = df.iloc[selected_idx]
        status = check_fraud(row)
        
        st.write(f"### 🎯 Seçilən Əməliyyat: Sətir {selected_idx + 1}")
        st.table(df.style.apply(lambda x: ['background-color: #ff4b4b' if x.name == selected_idx else '' for i in x], axis=1))
        
        if "FRAUD" in status:
            st.error(f"Sistem fırıldaqçılıq aşkar etdi: {row['Məbləğ']} AZN")
        else:
            st.success(f"Bu əməliyyat təhlükəsizdir.")
    else:
        st.warning("Barmaq aşkar edilmədi. Zəhmət olmasa əlinizi kameraya göstərin.")
