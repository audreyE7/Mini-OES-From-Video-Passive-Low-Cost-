# python/extract_spectrum.py
import cv2, numpy as np, matplotlib.pyplot as plt, json, sys

vid = sys.argv[1] if len(sys.argv)>1 else "videos/plasma_spectrum.mp4"
# ROI: y0,y1 define the horizontal stripe; x0,x1 the width you want
ROI = {"x0":100, "x1":1180, "y0":260, "y1":320}  # tweak once

cap = cv2.VideoCapture(vid)
n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)); fps = cap.get(cv2.CAP_PROP_FPS)

specs = []
ret, frame = cap.read()
if not ret: raise SystemExit("No frames")
h,w = frame.shape[:2]
x0,x1,y0,y1 = ROI["x0"],ROI["x1"],ROI["y0"],ROI["y1"]

cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
while True:
    ret, frame = cap.read()
    if not ret: break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    stripe = gray[y0:y1, x0:x1]             # crop spectral stripe
    s1d = stripe.mean(axis=0)               # average vertically → 1D
    s1d = s1d - np.percentile(s1d, 1)       # simple dark/baseline correction
    s1d[s1d<0] = 0
    specs.append(s1d)

cap.release()
specs = np.array(specs)                     # shape: [frames, pixels]
np.save("results/spec_cube.npy", specs)
np.save("results/pixel_axis.npy", np.arange(x0,x1))
print("Saved results/spec_cube.npy and results/pixel_axis.npy")
