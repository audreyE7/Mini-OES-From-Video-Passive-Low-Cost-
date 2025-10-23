# python/calibrate_wavelengths.py
import numpy as np, matplotlib.pyplot as plt, json

specs = np.load("results/spec_cube.npy")    # from calibration video
pix = np.load("results/pixel_axis.npy")

mean_spec = specs.mean(axis=0)
plt.plot(pix, mean_spec); plt.title("Click x-pixel of known peaks; close when done")
pts = plt.ginput(n=-1, timeout=0)           # click peaks, any number
plt.close()

clicked = [p[0] for p in pts]
# Example: CFL mercury lines (nm). Replace with what you used:
known_nm = [436.0, 546.1, 577.0]            # 3 lines is great; 2 is ok

if len(clicked) != len(known_nm):
    raise SystemExit("Provide same count of clicks as known wavelengths")

# Fit pixel→nm (linear; use polyfit deg=2 if needed)
coef = np.polyfit(clicked, known_nm, deg=1)
cal = {"coef": coef.tolist(), "clicked_px": clicked, "known_nm": known_nm}
with open("calibration/pixel_to_nm.json","w") as f: json.dump(cal, f, indent=2)
print("Saved calibration/pixel_to_nm.json", cal)
