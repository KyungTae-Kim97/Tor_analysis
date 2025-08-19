import matplotlib.pyplot as plt
import numpy as np
import os

# raw data (non-cumulative) 
usa1 = [551, 2031, 331, 63, 8, 5, 6, 1, 0, 4]
usa2 = [215, 2121, 530, 95, 18, 12, 4, 0, 2, 3]
south_korea = [2, 1632, 978, 211, 136, 18, 11, 7, 1, 4]

# calculating cumulative 
usa1_cum = np.cumsum(usa1)
usa2_cum = np.cumsum(usa2)
south_korea_cum = np.cumsum(south_korea)

# X-axis label 
time_labels = ["10% (12s)", "20% (24s)", "30% (36s)", "40% (48s)", "50% (60s)",
               "60% (72s)", "70% (84s)", "80% (96s)", "90% (108s)", "100% (120s)"]

x = np.arange(len(time_labels))

# draw a graph 
plt.figure(figsize=(10, 6))
plt.plot(x, usa1_cum, marker='o', label='USA1')
plt.plot(x, usa2_cum, marker='s', label='USA2')
plt.plot(x, south_korea_cum, marker='^', label='South Korea')

plt.xticks(x, time_labels, rotation=45)
plt.xlabel("Time Interval")
plt.ylabel("Cumulative Page Loads")
#plt.title("Cumulative Page Loads Over Time by Location")
plt.legend()
plt.grid(True)
plt.tight_layout()

# Save file
#plt.savefig("fig6_cumulative.png", dpi=300)

# Ensure the directory exists
output_dir = "./fig_repository"
os.makedirs(output_dir, exist_ok=True)

# Full path for saving the image
image_path = os.path.join(output_dir, "fig6_cumulative.png")

# Save the figure
plt.savefig(image_path, dpi=300, bbox_inches='tight')
print(f"Figure saved to: {image_path}")


#plt.show()