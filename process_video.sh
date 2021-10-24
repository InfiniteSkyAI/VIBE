#!/usr/bin/env bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

IN=$1
echo "Input Video Path: $1"
arrIN0=(${IN//\// })
echo "Vid name: ${arrIN0[-1]}"
arrIN=(${arrIN0[-1]//./ })
vid_name=${arrIN[0]}   

python demo.py --vid_file $1 --output_folder $SCRIPT_DIR/output/
echo "Processing $vid_name, extension '${arrIN[1]}'."

mkdir $SCRIPT_DIR/processed_output/$vid_name/
python process_output.py --input_folder $SCRIPT_DIR/output/$vid_name/vibe_output.pkl --output $SCRIPT_DIR/processed_output/$vid_name/
echo "Completed under $SCRIPT_DIR/output/$vid_name/"
