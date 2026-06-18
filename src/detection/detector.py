"""
Module 1 — Industrial Hybrid Detection Engine
Layer 1 (Edge): Local YOLOv8 spatial tracking & Region of Interest math.
Layer 2 (Cloud): OpenRouter VLM verification for complex safety context.
"""

import cv2
import json
import os
import uuid
import base64
import numpy as np
from datetime import datetime, timezone
from pathlib import Path
from openai import OpenAI
from ultralytics import YOLO
from dotenv import load_dotenv

load_dotenv()

# ==========================================
# LAYER 1: EDGE COMPUTING (FAST & LOCAL)
# ==========================================
class EdgeProcessor:
    def __init__(self):
        print("Initializing Edge AI (Local YOLOv8)...")
        self.local_model = YOLO("yolov8n.pt")
        
        # Define the geometric coordinates of your Safe Walkway (0.0 to 1.0 percentages)
        self.walkway_polygon = np.array([
            [0.50, 1.00],  # Bottom-Left
            [0.45, 0.20],  # Top-Left
            [0.85, 0.20],  # Top-Right
            [1.00, 1.00]   # Bottom-Right
        ], dtype=np.float32)

    def is_person_safe(self, feet_x, feet_y, frame_width, frame_height):
        """Pure spatial math: Returns True if feet are inside the green polygon."""
        pixel_poly = (self.walkway_polygon * np.array([frame_width, frame_height])).astype(np.int32)
        result = cv2.pointPolygonTest(pixel_poly, (feet_x, feet_y), False)
        return result >= 0

    def get_feet_coordinates(self, box):
        """Calculates the bottom-center of a bounding box."""
        x1, y1, x2, y2 = map(int, box)
        feet_x = int((x1 + x2) / 2)
        feet_y = y2
        return feet_x, feet_y, x1, y1, x2, y2

# ==========================================
# LAYER 2: CLOUD ORCHESTRATION (SMART VLM)
# ==========================================
class CloudVLM:
    def __init__(self):
        print("Initializing Cloud AI Orchestration (OpenRouter)...")
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY")
        )
        # FIX B: Swapped to a much more reliable free Vision model
        self.model = "qwen/qwen2.5-vl-72b-instruct" 
        # Backup free model if Gemini is busy: "meta-llama/llama-3.2-11b-vision-instruct:free"

    def verify_safety_breach(self, cropped_image):
        """Compresses the image and asks the VLM for a final ruling."""
        
        # FIX A: Resize the crop to 256x256 max to prevent free-tier payload limits crashing the API
        small_crop = cv2.resize(cropped_image, (256, 256))
        
        # Lower the JPEG quality to 60 (down from 85) to shrink the base64 string further
        _, buffer = cv2.imencode('.jpg', small_crop, [cv2.IMWRITE_JPEG_QUALITY, 60])
        b64_image = base64.standard_b64encode(buffer).decode('utf-8')
        
        prompt = "Look at this factory worker. Are they wearing a high-visibility safety vest? Respond ONLY with valid JSON: {'wearing_vest': true/false, 'reason': 'short description'}"
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_image}"}}
                    ]
                }],
                max_tokens=100,
                temperature=0.0
            )
            
            message_content = response.choices[0].message.content
            if not message_content:
                return {"wearing_vest": False, "reason": "API returned empty response."}

            content = message_content.strip()
            if "```json" in content: 
                content = content.split("```json")[1].split("```")[0].strip()
                
            return json.loads(content)
            
        except Exception as e:
            print(f"  [API Warning]: VLM check failed: {e}")
            return {"wearing_vest": False, "reason": "Cloud API unreachable - logging as unsafe."}

# ==========================================
# UNIFIED PIPELINE INTEGRATION
# ==========================================
def run_hybrid_pipeline(video_path):
    clip_id = Path(video_path).stem
    edge = EdgeProcessor()
    cloud = CloudVLM()
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open {video_path}")
        return []

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    playback_delay = int(1000 / fps) 
    
    violations_log = []
    
    # FIX: Initialize cooldown using video timestamp, starting in the negative
    last_api_call_video_time = -10.0 
    frame_idx = 0

    print(f"\nEngine Started: Tracking '{clip_id}' at normal speed...")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        timestamp_sec = frame_idx / fps
        
        pixel_poly = (edge.walkway_polygon * np.array([width, height])).astype(np.int32)
        cv2.polylines(frame, [pixel_poly], isClosed=True, color=(255, 150, 0), thickness=2)
        
        results = edge.local_model.track(frame, persist=True, verbose=False, classes=[0])
        
        if results[0].boxes is not None:
            for box in results[0].boxes.xyxy.cpu().numpy():
                feet_x, feet_y, x1, y1, x2, y2 = edge.get_feet_coordinates(box)
                is_safe = edge.is_person_safe(feet_x, feet_y, width, height)
                
                color = (0, 255, 0) if is_safe else (0, 0, 255)
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.circle(frame, (feet_x, feet_y), 6, color, -1)
                
                # FIX: Check cooldown against the video timestamp, not real-world time
                if not is_safe and (timestamp_sec - last_api_call_video_time > 3.0):
                    print(f"  ⚠️ EDGE ALERT at {timestamp_sec:.1f}s: Worker out of bounds. Waking Cloud VLM...")
                    last_api_call_video_time = timestamp_sec # Reset the video cooldown timer
                    
                    worker_crop = frame[max(0, y1):min(height, y2), max(0, x1):min(width, x2)]
                    
                    if worker_crop.size > 0:
                        vlm_ruling = cloud.verify_safety_breach(worker_crop)
                        
                        if not vlm_ruling.get("wearing_vest", True):
                            reason = vlm_ruling.get('reason', 'No visual confirmation.')
                            print(f"  🚨 CRITICAL VIOLATION: {reason}")
                            
                            violations_log.append({
                                "event_id": str(uuid.uuid4()),
                                "clip_id": clip_id,
                                "timestamp": datetime.now(timezone.utc).isoformat(),
                                "timestamp_in_clip_sec": round(timestamp_sec, 2),
                                "violation_detected": True,
                                "class_id": 0,
                                "behavior_class": "Safe Walkway Violation",
                                "observed_behavior": f"Worker out of bounds. VLM: {reason}",
                                "confidence": "high",
                                "policy_section": "Section 3.3.2"
                            })
                        else:
                            print("  ✅ VLM verified worker is wearing a vest. False alarm dismissed.")

        # FIX: Dynamically shrink the window to 50% size for easy viewing on any screen
        display_width = int(width * 0.5)
        display_height = int(height * 0.5)
        cv2.imshow("Industrial Hybrid Engine", cv2.resize(frame, (display_width, display_height)))
        
        if cv2.waitKey(playback_delay) & 0xFF == ord('q'):
            break
            
        frame_idx += 1

    cap.release()
    cv2.destroyAllWindows()
    return violations_log

if __name__ == "__main__":
    os.makedirs("outputs", exist_ok=True)
    
    # Run the pipeline on the test video
    final_logs = run_hybrid_pipeline("data/train_clip.mp4")
    
    output_path = "outputs/raw_detections.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json