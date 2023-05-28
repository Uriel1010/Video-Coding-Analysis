import glob

txt_files = glob.glob("*.txt")
for file in txt_files:
    print(file)

import os
import re
import pandas as pd
import matplotlib.pyplot as plt

log_files = [f"log_bitrate_{b}_subme_{s}.txt" for b in [1000000, 2000000, 4000000, 8000000] for s in range(5)]

data = []

for log_file in log_files:
    with open(log_file, "r", encoding='utf-16') as f:

        content = f.read()
        bitrate = int(re.search(r'(?<=bitrate_)\d+', log_file).group())
        subme = int(re.search(r'(?<=subme_)\d+', log_file).group())
        fps = float(re.search(r'(?<=FPS: )\d+\.\d+', content).group())
        avg_psnr_y = float(re.search(r'(?<=AVG PSNR Y )\d+\.\d+', content).group())
        actual_bitrate = float(re.search(r'(?<=Bitrate: )\d+\.\d+', content).group())

        data.append((bitrate, subme, fps, avg_psnr_y, actual_bitrate))

# Create DataFrame
df = pd.DataFrame(data, columns=["Bitrate", "Subme", "FPS", "Avg_PSNR_Y", "Actual_Bitrate"])
print(df)
# Plot FPS
fig, ax = plt.subplots()
df.pivot_table(values="FPS", index="Bitrate", columns="Subme").plot(ax=ax, marker='o', linestyle='-')
plt.title("FPS vs Subme for different bitrates")
plt.xlabel("Bitrate")
plt.ylabel("FPS")
plt.legend(title="Subme")
plt.grid()
plt.savefig('fps_plot.png')  # save the plot to a PNG file

plt.show()

# Plot Avg_PSNR_Y
fig, ax = plt.subplots()
df.pivot_table(values="Avg_PSNR_Y", index="Bitrate", columns="Subme").plot(ax=ax, marker='o', linestyle='-')
plt.title("Avg PSNR Y vs Subme for different bitrates")
plt.xlabel("Bitrate")
plt.ylabel("Avg PSNR Y")
plt.legend(title="Subme")
plt.grid()
plt.savefig('psnr_plot.png')  # save the plot to a PNG file

plt.show()

# Plot Actual_Bitrate
fig, ax = plt.subplots()
df.pivot_table(values="Actual_Bitrate", index="Bitrate", columns="Subme").plot(ax=ax, marker='o', linestyle='-')
plt.title("Actual Bitrate vs Subme for different bitrates")
plt.xlabel("Bitrate")
plt.ylabel("Actual Bitrate (Mbps)")
plt.legend(title="Subme")
plt.grid()
plt.savefig('bitrate_plot.png')  # save the plot to a PNG file

plt.show()
