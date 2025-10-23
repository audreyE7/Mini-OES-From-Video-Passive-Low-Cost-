# python/bands_timeseries.py
import numpy as np, json, matplotlib.pyplot as plt

with open("calibration/pixel_to_nm.json") as f: cal = json.load(f)
a,b = cal["coef"][0], cal["coef"][1]        # nm ≈ a*px + b

specs = np.load("results/spec_cube.npy")    # from plasma video
pix = np.load("results/pixel_axis.npy")
nm_axis = a*pix + b

def band_intensity(center_nm, halfwidth_nm=2.0):
    mask = (nm_axis > center_nm-halfwidth_nm) & (nm_axis < center_nm+halfwidth_nm)
    return specs[:, mask].mean(axis=1)

# common lines (adjust to your gas):
Halpha = band_intensity(656.3, 2.0)
Hbeta  = band_intensity(486.1, 2.0)

t = np.arange(len(Halpha))  # frame index (scale by fps if you want seconds)
ratio = Halpha / (Hbeta + 1e-9)

plt.figure(); plt.plot(t, Halpha, label="Hα 656nm"); plt.plot(t, Hbeta, label="Hβ 486nm")
plt.legend(); plt.xlabel("Frame"); plt.ylabel("Band intensity (a.u.)")
plt.tight_layout(); plt.savefig("results/line_timeseries.png", dpi=180)

plt.figure(); plt.plot(t, ratio, color='purple'); plt.xlabel("Frame"); plt.ylabel("Hα/Hβ")
plt.title("Line ratio (proxy for excitation/temperature trend)")
plt.tight_layout(); plt.savefig("results/line_ratio.png", dpi=180)
print("Saved results/line_timeseries.png and results/line_ratio.png")
