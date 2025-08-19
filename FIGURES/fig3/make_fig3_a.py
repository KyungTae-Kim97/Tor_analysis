import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import umap
import os

# 1. CSV file
filename = "./fig3/125-0-clustering.csv"

# 2. CSV file reading
data = pd.read_csv(filename, delimiter=",")  # or sep="\t"

# 3. select numeric values features (exclude the last column)
X = data.select_dtypes(include=[np.number]).iloc[:, :-1].values
y = data.iloc[:, -1].values

# 4. reduction UMAP
reducer = umap.UMAP(n_neighbors=15, min_dist=0.1, random_state=42)
X_umap = reducer.fit_transform(X)

# 5. create the name of the figure with directory
output_dir = "./fig_repository"
os.makedirs(output_dir, exist_ok=True)  # 디렉토리가 없으면 생성

image_name = os.path.splitext("fig3_a")[0] + ".png"
image_path = os.path.join(output_dir, image_name)

# 6. create a DataFrame for easy mapping
plot_df = pd.DataFrame({
    'UMAP1': X_umap[:, 0],
    'UMAP2': X_umap[:, 1],
    'Label': y
})

# Define mapping dictionary
label_mapping = {
    '0-CSM': 'USA1',
    '0-HOME': 'USA2',
    '0-DK': 'South Korea'
}

# Map new labels
plot_df['NewLabel'] = plot_df['Label'].map(label_mapping)

# Plot
plt.figure(figsize=(10, 6))
sns.scatterplot(data=plot_df, x='UMAP1', y='UMAP2', hue='NewLabel', palette='tab10', s=10)

plt.title("UMAP with 140 Features")
plt.xlabel("UMAP-1")
plt.ylabel("UMAP-2")
plt.legend(title="")

# Save the figure to the correct path
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.close()

print(f"the figure saved at: {image_path}")


