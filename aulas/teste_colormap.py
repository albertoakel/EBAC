import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from matplotlib.colors import LinearSegmentedColormap

# Criando um colormap personalizado (Teal → Branco → Orange)
#003D59 • #414A4F • #FB9334 • #FE6625 • #44857D • #167070
teal_orange = LinearSegmentedColormap.from_list("TealOrange", ["#008080", "#FFFFFF", "#FF7700"])
teal_orange = LinearSegmentedColormap.from_list("TealOrange", ['#003D59', '#414A4F','#FB9334','#FE6625','#44857D','#167070'])

# Criando o heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(df, cmap=teal_orange, annot=True, linewidths=0.5)

plt.title("Heatmap com Teal & Orange (Custom)")
plt.show()