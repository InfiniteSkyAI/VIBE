
IN=$1
arrIN=(${IN//./ })
vid_name=${arrIN[0]}   
echo "Processing $vid_name, extension '${arrIN[1]}'."

python demo.py --vid_file $1 --output_folder output/

python process_output.py --input_folder output/$vid_name/vibe_output.pkl --output processed_output/

