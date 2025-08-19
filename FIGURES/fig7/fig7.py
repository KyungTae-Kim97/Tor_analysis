import matplotlib.pyplot as plt
import os

# X-axis: Traffic percentages and corresponding time (in seconds)
percentages = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
time_labels = ["10% (12s)", "20% (24s)", "30% (36s)", "40% (48s)", "50% (60s)",
               "60% (72s)", "70% (84s)", "80% (96s)", "90% (108s)", "100% (120s)"]

# Accuracy values for each setting
usa1 = [42.5, 78.1, 85.1, 87.5, 88.8, 88.6, 89.0, 88.8, 88.6, 88.8]
usa2 = [41.3, 76.8, 84.1, 88.0, 88.1, 88.0, 88.1, 88.0, 87.8, 88.0]
korea = [32.5, 74.5, 80.6, 80.6, 82.6, 82.1, 81.5, 81.6, 81.6, 81.6]

# Create the plot
plt.figure(figsize=(12, 6))
plt.plot(percentages, usa1, marker='o', label='USA1')
plt.plot(percentages, usa2, marker='o', label='USA2')
plt.plot(percentages, korea, marker='o', label='South Korea')

# X-axis and labels
plt.xticks(percentages, time_labels, rotation=45)
plt.xlabel('Traffic Percentage (Elapsed Time)')
plt.ylabel('Accuracy (%)')
#plt.title('Accuracy vs Traffic Percentage (Elapsed Time) Across Locations')
plt.grid(True)
plt.legend()
plt.tight_layout()

# Save and show the figure
#plt.savefig('fig7_wtcm.png')

# Ensure the directory exists
output_dir = "./fig_repository"
os.makedirs(output_dir, exist_ok=True)

# Full path for saving the image
image_path = os.path.join(output_dir, "fig7_wtcm.png")

# Save the figure
plt.savefig(image_path, dpi=300, bbox_inches='tight')
print(f"Figure saved to: {image_path}")
#plt.show()