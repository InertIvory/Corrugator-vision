# Corrugator Vision

A Streamlit + OpenCV prototype for image-based inspection and early-stage starter-point detection experiments.

## Features
- Upload an image or use a synthetic test image
- Canny edge detection
- Binary threshold segmentation
- Contour inspection with bounding boxes and area labels
- Adjustable thresholds and minimum contour area

## Run locally
Python 3.10–3.12 recommended.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Community Cloud
1. Push this folder to a GitHub repository.
2. Sign in at https://share.streamlit.io.
3. Choose **Create app**, then select the repository, branch, and `app.py`.
4. Deploy.

## Safety
Still-image demo only. It does not connect to a production camera, PLC, actuator, or machine. Never use its output to control equipment. Validate performance and use approved machine-safety controls before any real-world integration.
