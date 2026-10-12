# Live Image Detection

**A YOLOv8 object-detection web app — upload an image or point your webcam at the world and see detections drawn in real time, in the browser.**

A Flask application that wraps an Ultralytics YOLOv8 model (exported to ONNX) behind a simple two-tab UI: **image upload** returns an annotated image plus the structured list of detections, and **live camera** streams the webcam with bounding boxes rendered on every frame.

<p align="center"><em>⬇️ Add a screenshot or short GIF of the detection UI here.</em></p>

---

## Features

- **Image upload detection** — upload a photo, get it back annotated with bounding boxes, and receive each detection's label, confidence score, and coordinates as JSON.
- **Live webcam stream** — a real-time MJPEG feed (`/video_feed`) that runs inference on each frame and overlays detections.
- **ONNX inference** — runs the model exported to ONNX for portable, framework-independent inference.
- **Training pipeline included** — the scripts used to train the model (on the COCO128 dataset) and export it are in the repo, so the full workflow from training to serving is reproducible.

## How it works

```text
   Browser                    Flask (app.py)                 YOLOv8 (best.onnx)
 ┌─────────┐   POST /detect   ┌──────────────┐   predict()   ┌────────────────┐
 │ Upload  │ ───────────────▶ │  /detect     │ ────────────▶ │  Ultralytics   │
 │  image  │ ◀─────────────── │  annotate +  │ ◀──────────── │  inference     │
 └─────────┘  annotated img   │  JSON boxes  │   detections  └────────────────┘
                              │              │
 ┌─────────┐  GET /video_feed │  /video_feed │   per-frame
 │ Webcam  │ ◀═══════════════ │  MJPEG       │ ◀── inference (OpenCV capture)
 └─────────┘   live stream    └──────────────┘
```

## Tech stack

| Area | Tools |
| --- | --- |
| Model | Ultralytics YOLOv8 (`best.onnx`, trained on COCO128) |
| Inference | ONNX via Ultralytics, OpenCV |
| Web server | Flask |
| Image handling | OpenCV, Pillow, NumPy |
| Frontend | HTML + vanilla JS (upload / live-camera tabs) |

## Project structure

```text
app.py              # Flask app: / , /detect (upload) , /video_feed (webcam stream)
inference_onnx.py   # Standalone ONNX inference on a single image
main.py             # Training + export pipeline (YOLOv8 on COCO128)
best.onnx           # Exported trained model served by the app
templates/          # index.html UI
static/             # CSS / JS assets
```

## Getting started

**Prerequisites:** Python 3.10+.

```bash
git clone https://github.com/cypriotCodder/Live-Image-Detection.git
cd Live-Image-Detection

# Install dependencies
pip install flask ultralytics opencv-python pillow numpy

# Run the app
python app.py
```

Then open **http://localhost:5000**. Use the **Image Upload** tab to detect objects in a photo, or the **Live Camera** tab to stream from your webcam (the server reads camera device `0`).

> **Note:** the live-camera feed uses the webcam attached to the machine running the server, so it's intended for local use.

## Retraining the model

`main.py` trains YOLOv8 on the COCO128 dataset and exports the result; `inference_onnx.py` runs the exported ONNX model against a single image. Swap in your own dataset to retrain for a different set of classes.

## Possible improvements

- Pin dependencies in a `requirements.txt` (and optionally a `Dockerfile`) for reproducible setup.
- Add `uploads/` to `.gitignore` so run-time uploads aren't committed.
- Serve behind a production WSGI server (gunicorn/uvicorn) instead of Flask's debug server.

## License

Released under the [MIT License](LICENSE).
