import os
import chardet
import matplotlib.pyplot as plt


def parse_file(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        encoding = chardet.detect(raw_data)['encoding']
    with open(file_path, 'r', encoding=encoding) as f:
        lines = f.readlines()

    psnr = None
    fps = None
    bandwidth = None

    for line in reversed(lines):
        if 'AVG PSNR' in line:
            psnr = float(line.split('AVG PSNR Y ')[1].split()[0])
        elif 'FPS' in line:
            fps = float(line.split('FPS: ')[1])
        elif 'Bitrate' in line:
            bandwidth = float(line.split('Bitrate: ')[1].split()[0]) * 1000

        if psnr is not None and fps is not None and bandwidth is not None:
            break

    return {'psnr': psnr, 'fps': fps, 'bandwidth': bandwidth}

if __name__ == '__main__':
    txt_files = [f for f in os.listdir('..') if f.endswith('.txt')]

    psnr_values = []
    fps_values = []
    bandwidth_values = []
    file_names = []

    for txt_file in txt_files:
        result = parse_file(txt_file)
        psnr_values.append(result['psnr'])
        fps_values.append(result['fps'])
        bandwidth_values.append(result['bandwidth'])
        file_names.append(os.path.splitext(txt_file)[0].split('_')[-1].split('.')[0])

    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    fig, axs = plt.subplots(3, 1, figsize=(8, 12))

    axs[0].bar(file_names, psnr_values, color=colors[0])
    axs[0].set_xlabel('File')
    axs[0].set_ylabel('PSNR')

    axs[1].bar(file_names, fps_values, color=colors[1])
    axs[1].set_xlabel('File')
    axs[1].set_ylabel('FPS')

    axs[2].bar(file_names, bandwidth_values, color=colors[2])
    axs[2].set_xlabel('File')
    axs[2].set_ylabel('Bandwidth')

    plt.tight_layout()
    plt.show()

