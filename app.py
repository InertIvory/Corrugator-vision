import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.set_page_config(page_title="Corrugator Vision", page_icon="⚙️", layout="wide")
st.title("⚙️ Corrugator Vision")
st.caption("Computer-vision workbench · Still-image inspection prototype")

with st.sidebar:
    st.header("Detection settings")
    mode = st.selectbox("Processing mode", ["Edge detection", "Threshold segmentation", "Contour inspection"])
    low = st.slider("Canny lower threshold", 0, 255, 60)
    high = st.slider("Canny upper threshold", 0, 255, 150)
    threshold = st.slider("Binary threshold", 0, 255, 120)
    min_area = st.number_input("Minimum contour area (px²)", min_value=0, max_value=2_000_000, value=250, step=50)
    st.info("Still-image prototype only. No machine, PLC, camera stream, or actuator connection.")

uploaded = st.file_uploader("Upload a machine image", type=["png", "jpg", "jpeg", "bmp"])
if uploaded:
    rgb = np.array(Image.open(uploaded).convert("RGB"))
else:
    rgb = np.full((420, 640, 3), 238, dtype=np.uint8)
    cv2.rectangle(rgb, (70, 70), (570, 350), (190, 195, 200), -1)
    cv2.rectangle(rgb, (100, 105), (540, 315), (70, 78, 86), 3)
    cv2.line(rgb, (120, 210), (520, 210), (30, 30, 30), 5)
    cv2.circle(rgb, (320, 210), 22, (20, 145, 210), -1)
    cv2.putText(rgb, "SYNTHETIC TEST IMAGE", (125, 390), cv2.FONT_HERSHEY_SIMPLEX, .8, (70, 70, 70), 2)
    st.caption("Synthetic sample displayed. Upload an image to inspect your own sample.")

gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
edges = cv2.Canny(gray, low, high)
_, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
contours, _ = cv2.findContours(binary.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
valid = [c for c in contours if cv2.contourArea(c) >= min_area]
annotated = rgb.copy()
for contour in valid:
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(annotated, (x, y), (x + w, y + h), (30, 180, 90), 2)
    cv2.putText(annotated, f"{int(cv2.contourArea(contour))} px2",
                (x, max(20, y - 7)), cv2.FONT_HERSHEY_SIMPLEX, .45, (20, 120, 60), 1)

left, right = st.columns(2)
left.subheader("Input image")
left.image(rgb, use_container_width=True)
right.subheader("Processed output")
output = edges if mode == "Edge detection" else binary if mode == "Threshold segmentation" else annotated
right.image(output, clamp=(output.ndim == 2), use_container_width=True)

st.subheader("Inspection summary")
a, b, c = st.columns(3)
a.metric("Image size", f"{rgb.shape[1]} × {rgb.shape[0]}")
b.metric("Contours detected", len(contours))
c.metric("Contours above minimum area", len(valid))
if valid:
    largest = max(valid, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest)
    st.write(f"Largest candidate: x={x}, y={y}, width={w}, height={h}; area={int(cv2.contourArea(largest))} px²")
else:
    st.write("No contours met the area threshold. Try a lower minimum area or adjust binary threshold.")

st.subheader("Next engineering steps")
st.markdown("""
- Gather labelled starter-point images and define a region of interest.
- Evaluate false positives and false negatives on held-out images.
- Add camera input on a suitable test computer after still-image validation.
- Consider PLC integration only after a machine risk assessment and independent approved safety controls.
""")
st.warning("Do not use this prototype to trigger machinery. It is an experimental still-image analysis tool, not a validated machine-vision safety system.")
