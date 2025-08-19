import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# data
data = {
    'Feature Vector': ['125', '125', '125', '140', '140', '140', 'CUMUL', 'CUMUL', 'CUMUL'],
    'Location': ['USA1', 'USA2', 'South Korea', 'USA1', 'USA2', 'South Korea', 'USA1', 'USA2', 'South Korea'],
    'Day 1': [95.1, 95.5, 95.8, 94.1, 94.7, 93.6, 90.0, 94.9, 91.3],
    'Day 2': [85.5, 82.0, 78.3, 86.3, 70.2, 80.0, 89.0, 81.2, 81.3],
    'Day 6': [77.5, 80.4, 80.3, 84.9, 78.3, 79.2, 81.8, 80.0, 75.6],
}
df = pd.DataFrame(data)

# Melt
df_melt = df.melt(id_vars=['Feature Vector', 'Location'], value_vars=['Day 1', 'Day 2', 'Day 6'],
                  var_name='Test Day', value_name='Accuracy')

# Group
summary_cross = df_melt.groupby(['Location', 'Feature Vector']).agg(
    Mean_Accuracy=('Accuracy', 'mean'),
    Std_Dev=('Accuracy', 'std')
).reset_index()

# Plot
plt.figure(figsize=(8, 6))
sns.barplot(data=summary_cross, x='Location', y='Mean_Accuracy', hue='Feature Vector', palette='Set2')

#plt.title('Mean Accuracy by Location and Feature Vector')
plt.ylabel('Mean Accuracy (%)')
plt.ylim(70, 100)
plt.xlabel('Location')
plt.xticks(ticks=[0, 1, 2], labels=['USA1', 'USA2', 'South Korea'], rotation=0)
plt.legend(title='Feature Vector')
plt.grid(axis='y')

plt.tight_layout()

# save PNG 
#plt.savefig('fig5_mean_by_location_feature.png', dpi=300)

# Ensure the directory exists
output_dir = "./fig_repository"
os.makedirs(output_dir, exist_ok=True)

# Full path for saving the image
image_path = os.path.join(output_dir, "fig5_mean_by_location_feature.png")

# Save the figure
plt.savefig(image_path, dpi=300, bbox_inches='tight')
print(f"Figure saved to: {image_path}")


# Show
#plt.show()