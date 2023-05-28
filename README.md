# Video Coding Project

This repository contains code and files related to video coding tasks.

## Question 1

The folder `Question1` contains the code and files for analyzing video encoding results.

- `question1.py`: Python script for parsing and analyzing video encoding results.
- `output_diamond.h265`, `output_diamond.txt`: Output files from encoding using the diamond search algorithm.
- `output_fullsearch.txt`: Output file from encoding using the full search algorithm.
- `output_hexbs.h265`, `output_hexbs.txt`: Output files from encoding using the hexagonal search algorithm with block size 16x16.
- `output_tzs.h265`, `output_tzs.txt`: Output files from encoding using the TZS (Three-Step) search algorithm.
- `road_movie_1920x1080_25-001.yuv`: Input video file used for encoding.
- `diagram_1.png`, `diagram_2.png`, `diagram_3.png`, `diagram_4.png`, `diagram_5.png`, `diagram_6.png`: Diagrams generated from the analysis.

## Question 2

The folder `Question2` contains the code and files for motion estimation and analysis.

- `question2.py`: Python script for performing motion estimation and analysis.
- `diagram_1.png`, `diagram_1D.png`, `diagram_2.png`, `diagram_2D.png`, `diagram_3.png`, `diagram_3D.png`, `diagram_4.png`, `diagram_4D.png`, `diagram_5.png`, `diagram_5D.png`, `diagram_6.png`, `diagram_6D.png`: Diagrams generated from the motion estimation and analysis.
- `frame_0.png`, `frame_1.png`: Frames extracted from the input video for analysis.
- `paris_cif.yuv`: Input video file used for analysis.

## Question 3

The folder `Question3` contains the code and files for analyzing bitrate, FPS, and PSNR values.

- `question3.py`: Python script for analyzing bitrate, FPS, and PSNR values.
- `bitrate_plot.png`, `fps_plot.png`, `psnr_plot.png`: Plots generated from the analysis.
- `kvazaar_test.ps1`, `kvazaar_test.ps1.bak`: PowerShell script files (if any) related to Kvazaar testing.
- `log_bitrate_*.txt`: Log files containing the output from Kvazaar encoding with different bitrates and subme values.
- `output_bitrate_*.hvc`: Output video files encoded using Kvazaar with different bitrates and subme values.
- `road_movie_1920x1080_25-001.yuv`: Input video file used for encoding and testing.

## License

This project is licensed under the [MIT License](LICENSE).
