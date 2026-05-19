import streamlit as st
import cv2
import numpy as np
import os
import subprocess
import sys

# ===================== PAGE CONFIG ===================== #
st.set_page_config(page_title="RIZZ-UP", layout="wide")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

FACE_DATA = "face_data.yml"

# ===================== FACE LOGIN ===================== #
def face_login():
    st.title("🔐 Face ID Authentication")

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    recognizer = cv2.face.LBPHFaceRecognizer_create()

    col1, col2 = st.columns(2)

    # ---------- REGISTER FACE ---------- #
    with col1:
        st.subheader("📸 Register Face")

        if st.button("Register My Face"):
            cap = cv2.VideoCapture(0)
            faces_data = []
            st.info("Look straight at the camera...")

            while len(faces_data) < 30:
                ret, frame = cap.read()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)

                for (x, y, w, h) in faces:
                    face = gray[y:y+h, x:x+w]
                    face = cv2.resize(face, (200, 200))
                    faces_data.append(face)
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)

                cv2.imshow("Registering Face", frame)
                if cv2.waitKey(1) & 0xFF == 27:
                    break

            cap.release()
            cv2.destroyAllWindows()

            labels = [0] * len(faces_data)
            recognizer.train(faces_data, np.array(labels))
            recognizer.save(FACE_DATA)

            st.success("✅ Face Registered Successfully!")

    # ---------- LOGIN ---------- #
    with col2:
        st.subheader("🔓 Login")

        if st.button("Login with Face ID"):
            if not os.path.exists(FACE_DATA):
                st.error("❌ No registered face found")
                return

            recognizer.read(FACE_DATA)
            cap = cv2.VideoCapture(0)
            st.info("Authenticating...")

            while True:
                ret, frame = cap.read()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)

                for (x, y, w, h) in faces:
                    face = gray[y:y+h, x:x+w]
                    face = cv2.resize(face, (200, 200))

                    label, confidence = recognizer.predict(face)

                    if confidence < 70:
                        cap.release()
                        cv2.destroyAllWindows()
                        st.success("✅ Login Successful!")
                        st.session_state.authenticated = True
                        st.rerun()

                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
                    cv2.putText(frame, "Scanning...", (x, y-10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)

                cv2.imshow("Face Login", frame)
                if cv2.waitKey(1) & 0xFF == 27:
                    break

            cap.release()
            cv2.destroyAllWindows()

# ===================== MAIN APP ===================== #
def main_app():
    st.markdown("<h1 style='text-align:center;'>RIZZ-UP</h1>", unsafe_allow_html=True)

    def run_script(script):
        subprocess.Popen([sys.executable, script])

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🤌 Hand Gesture"):
            run_script("handgesture.py")

    with col2:
        if st.button("🎤 Voice Control"):
            run_script("voice_control.py")

    with col3:
        if st.button("🙂 Face Control"):
            run_script("face_control.py")

# ===================== ROUTER ===================== #
if not st.session_state.authenticated:
    face_login()
else:
    main_app()


