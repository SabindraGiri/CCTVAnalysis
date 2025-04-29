from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import cv2
import torch
import numpy as np
from transformers import DetrImageProcessor, DetrForObjectDetection
from PIL import Image

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load the DETR model and processor once at startup
processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify({"message": "No file part in the request."}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"message": "No selected file."}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    print(f"[INFO] Received file: {filepath}")

    cap = cv2.VideoCapture(filepath)
    if not cap.isOpened():
        return jsonify({"message": "Failed to open video file."}), 500

    frame_count = 0
    detected_labels = {}
    prev_gray = None
    motion_magnitudes = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1

        if frame_count % 20 != 0:
            continue

        # Convert frame for analysis
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_frame)

        # Object Detection
        inputs = processor(images=pil_image, return_tensors="pt")
        outputs = model(**inputs)
        target_sizes = torch.tensor([pil_image.size[::-1]])
        results = processor.post_process_object_detection(outputs, threshold=0.9, target_sizes=target_sizes)[0]

        for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
            label_name = model.config.id2label[label.item()]
            detected_labels[label_name] = detected_labels.get(label_name, 0) + 1

        # Motion Detection using Optical Flow
        if prev_gray is not None:
            flow = cv2.calcOpticalFlowFarneback(prev_gray, gray,
                                                None, 0.5, 3, 15, 3, 5, 1.2, 0)
            magnitude, _ = cv2.cartToPolar(flow[..., 0], flow[..., 1])
            mean_magnitude = np.mean(magnitude)
            motion_magnitudes.append(mean_magnitude)

        prev_gray = gray

    cap.release()

    # Estimate motion state
    avg_motion = np.mean(motion_magnitudes) if motion_magnitudes else 0
    if avg_motion > 2.5:
        motion_label = "running"
    elif avg_motion > 0.8:
        motion_label = "walking"
    else:
        motion_label = "still"

    # Activity Recognition Logic
    loitering = False
    group_gathering = False
    analyzed_frames = max(1, frame_count // 20)  # Prevent divide-by-zero

    if 'person' in detected_labels:
        appearance_ratio = detected_labels['person'] / analyzed_frames
        if appearance_ratio > 0.6:
            loitering = True
        if detected_labels['person'] >= 9:
            group_gathering = True

    print(f"[INFO] Processed {frame_count} frames.")
    print(f"[INFO] Detections: {detected_labels}")
    print(f"[INFO] Motion avg: {avg_motion:.2f}, classified as: {motion_label}")

    return jsonify({
        "message": f"Video {file.filename} analyzed successfully.",
        "total_frames": frame_count,
        "detected_objects": detected_labels,
        "activity": {
            "loitering": loitering,
            "group_gathering": group_gathering,
            "motion": motion_label
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
