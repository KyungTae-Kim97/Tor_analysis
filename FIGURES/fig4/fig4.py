import matplotlib.pyplot as plt
import os

# ----------------------------
# USA1 data
# ----------------------------
dates_usa1 = ["0614", "0615", "0620", "0710", "0714", "0721", "0728", "0804"]
usa1_125 = [95.1, 85.5, 77.5, 81.1, 80.2, 85.9, 78.2, 80.2]
usa1_140 = [94.1, 86.3, 84.9, 82.7, 85.3, 86.6, 78.3, 81.1]
usa1_cumul = [90.0, 89.0, 81.8, 84.6, 82.2, 90.5, 82.8, 82.5]

# ----------------------------
# USA2 data
# ----------------------------
dates_usa2 = ["0614", "0615", "0620", "0710", "0714", "0721", "0728", "0804"]
usa2_125 = [95.5, 82.0, 80.4, 79.6, 78.2, 76.7, 70.2, 50.8]
usa2_140 = [94.7, 70.2, 78.3, 62.4, 60.5, 65.3, 56.4, 41.8]
usa2_cumul = [94.9, 81.2, 80.0, 80.1, 79.6, 78.0, 70.2, 60.1]

# ----------------------------
# Korea data
# ----------------------------
dates_korea = ["0702", "0703", "0708", "0710", "0714", "0721", "0728", "0804"]
korea_125 = [95.8, 78.3, 80.3, 76.4, 81.4, 81.6, 70.8, 70.5]
korea_140 = [93.6, 80.0, 79.2, 79.3, 82.6, 82.2, 70.3, 68.3]
korea_cumul = [91.3, 81.3, 75.6, 81.5, 83.9, 82.9, 71.8, 71.2]

# ----------------------------
# Plotting (default sans-serif style)
# ----------------------------
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 11
})

fig, axes = plt.subplots(1, 3, figsize=(15, 4), sharey=True)

def plot_location(ax, dates, f125, f140, fcumul, title):
    ax.plot(dates, f125, marker='o', label="125")
    ax.plot(dates, f140, marker='s', label="140")
    ax.plot(dates, fcumul, marker='^', label="CUMUL")
    ax.set_title(title)
    ax.set_xlabel("Test Date")
    ax.set_ylim(40, 100)
    ax.grid(True, linestyle='--', alpha=0.5)

plot_location(axes[0], dates_usa1, usa1_125, usa1_140, usa1_cumul, "USA1")
plot_location(axes[1], dates_usa2, usa2_125, usa2_140, usa2_cumul, "USA2")
plot_location(axes[2], dates_korea, korea_125, korea_140, korea_cumul, "South Korea")

axes[0].set_ylabel("Accuracy (%)")
axes[2].legend(loc="lower right", fontsize=9)

plt.tight_layout()
# Ensure the directory exists
output_dir = "./fig_repository"
os.makedirs(output_dir, exist_ok=True)

# Full path for saving the image
image_path = os.path.join(output_dir, "fig4_three_locations.png")

# Save the figure
plt.savefig(image_path, dpi=400, bbox_inches='tight')
print(f"Figure saved to: {image_path}")
#plt.show()