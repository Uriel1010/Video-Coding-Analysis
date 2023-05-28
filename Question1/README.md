# Video Coding Project - Question 1

This repository contains code for analyzing video coding performance metrics from log files.

## Question 1

This section focuses on analyzing the log files and extracting relevant metrics for video coding experiments.

### Files

- `question1.py`: The Python script for parsing log files and generating bar charts.
- `output_diamond.h265`, `output_diamond.txt`: Output files generated during video coding using the diamond search algorithm.
- `output_fullsearch.txt`: Output file generated during video coding using the full search algorithm.
- `output_hexbs.h265`, `output_hexbs.txt`: Output files generated during video coding using the hexagonal search algorithm with block size variations.
- `output_tzs.h265`, `output_tzs.txt`: Output files generated during video coding using the TZS (Three-Step) algorithm.
- `road_movie_1920x1080_25-001.yuv`: Input video file used in the video coding experiments.
- `road_movie_1920x1080_25-001_fullsearch.hvc`: Output file generated during video coding using the full search algorithm.

### Usage

1. Place the log files and related files in the same directory as the `question1.py` script.
2. Run the `question1.py` script.
3. The script will parse the log files, extract metrics such as PSNR, FPS, and bandwidth, and generate bar charts for visualization.

### Dependencies

- Python 3.x
- `chardet` library
- `matplotlib` library

### Example

The script assumes the log files follow a specific format and extracts metrics based on predefined patterns. Make sure the log files are correctly formatted for accurate results.

## License

This project is licensed under the [MIT License](LICENSE).
