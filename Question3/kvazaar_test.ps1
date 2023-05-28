$input_video = "road_movie_1920x1080_25-001.yuv"
$output_prefix = "output_"
$bitrates = @(1000000, 2000000, 4000000, 8000000)
$subme_options = @(0, 1, 2, 3, 4)

foreach ($bitrate in $bitrates) {
    foreach ($subme in $subme_options) {
        $output_video = "${output_prefix}bitrate_${bitrate}_subme_${subme}.hvc"
        $log_file = "log_bitrate_${bitrate}_subme_${subme}.txt"
        
        kvazaar -i $input_video --input-res 1920x1080 --input-fps 25 --me hexbs `
                --bitrate $bitrate --subme $subme -o $output_video 2>&1 | Tee-Object -FilePath $log_file
    }
}
