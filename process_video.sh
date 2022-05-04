#!/usr/bin/env bash

# Typical functional call
# process_video.sh /path/to/video.mp4 /desired/output/directory
# 

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

IN=$1
echo "Input Video Path: $1"
arrIN0=(${IN//\// })
echo "Vid name: ${arrIN0[-1]}"
arrIN=(${arrIN0[-1]//./ })
vid_name=${arrIN[0]}   

mkdir $2/output
python demo.py --vid_file $1 --output_folder $2/output/
echo "Processing $vid_name, extension '${arrIN[1]}'."

mkdir $2/processed_output
mkdir $2/processed_output/$vid_name/
python process_output.py \
    --input_folder $2/output/$vid_name/vibe_output.pkl \
    --output_folder $2/processed_output/$vid_name/ \
    --output_joint_format euler
echo "Completed under $2/output/$vid_name/"
