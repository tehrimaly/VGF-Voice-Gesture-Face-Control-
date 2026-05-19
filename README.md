# Multimodal Human-Computer Interface: Voice, Gesture, and Face Control

## Project Overview

This repository contains an advanced, multimodal Human-Computer Interface (HCI) designed to enable completely hands-free laptop and system control. By combining computer vision, facial tracking, and natural language processing, the software allows users to navigate their operating system, manipulate the cursor, execute shortcuts, and input commands using a combination of facial movements, hand gestures, and voice inputs.

This project bridges the gap between traditional peripherals and natural user interactions, offering an accessible solution for users with physical impairments or environments requiring touchless operations.

---

## Technical Architecture & Multimodal Pipeline

The system runs concurrently across three primary tracking and processing pipelines, synchronizing inputs to execute low-latency system-level commands:

### 1. Facial Tracking & Cursor Control

* **Technology:** OpenCV and MediaPipe Face Mesh.
* **Mechanism:** Tracks localized facial landmarks (such as nose-tip coordinates or eye gaze) to translate micro-movements into smooth, proportional mouse cursor tracking on the screen.
* **Facial Actions:** Maps specific facial expressions (e.g., blinking, raising eyebrows, or jaw opening) to mouse clicks and scrolling actions.

### 2. Hand Gesture Classification

* **Technology:** OpenCV and MediaPipe Hands.
* **Mechanism:** Extracts 21 distinct 3D hand landmarks from the webcam feed. Spatial distance formulas calculate the relative positions of fingertips to classify gestures.
* **Peripheral Mapping:** Translates predefined static and dynamic gestures into immediate keyboard shortcuts, window switching, or media controls.

### 3. Voice Command Processing

* **Technology:** Python SpeechRecognition and local/cloud NLP parsers.
* **Mechanism:** Monitors a microphone input stream, converts spoken audio into text, and processes the string through a command routing engine.
* **System Operations:** Executes high-level macro commands such as opening applications, typing text dictated by the user, or shutting down the interface.

---

## Core System Functionality

| Input Modality | Action / Gesture Detected | Executed System Command |
| --- | --- | --- |
| **Facial Mesh** | Head Movement (Nose Vector) | Directional Mouse Cursor Movement |
| **Facial Mesh** | Prolonged Left/Right Eye Blink | Left Click / Right Click |
| **Hand Tracking** | Extended Index Finger Only | Cursor Activation / Direct Tracking |
| **Hand Tracking** | Closed Fist (All Fingers Folded) | Global System Screenshot |
| **Voice Command** | "Open Browser" | Launches Default Web Browser |
| **Voice Command** | "Type [User Text]" | Emulates Keyboard Keystrokes for Dictation |

---

## Technical Stack

* **Programming Language:** Python
* **Computer Vision Frameworks:** OpenCV, MediaPipe (Face Mesh & Hands modules)
* **Speech Processing:** SpeechRecognition, PyAudio
* **Automation & OS Integration:** PyAutoGUI, Operating System API Bindings (OS/Sys modules)
* **Mathematical Operations:** NumPy (for coordinate smoothing and vector calculations)

---

## Installation & Setup

### Prerequisites

* Python 3.8 or higher
* Integrated or external USB Webcam
* Working Hardware Microphone

### Step-by-Step Installation

1. Clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/multimodal-interface.git
cd multimodal-interface

```

2. Install the necessary Python dependencies:

```bash
pip install -r requirements.txt

```

3. Initialize the multimodal application:

```bash
python main.py

```

---

## Calibration and Optimization

* **Lighting Conditions:** Ensure the environment is evenly lit to allow MediaPipe to accurately map facial and hand landmarks without losing frame tracking.
* **Voice Thresholds:** The application utilizes an automatic ambient noise adjustment phase upon startup to tune the microphone sensitivity to your environment.
