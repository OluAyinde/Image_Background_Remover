This repo was created to remove the background of multiple images. It is built on the foundation of `InSPYReNet` by [plemeri](https://github.com/plemeri/InSPyReNet). 

`Requirements:`

The following libraries need to be installed: `transparent-background`, `pillow`, `requests`, `torch`, `torchvision`, `numpy<2.0`.

`Running the scripts:`

Before running the script in your CLI, edit the following lines:

For `bkgrnd_rem.py`:
- `Line 9`: output_folder - this is the path to the folder to save the processed images.
- `Line 10`: input_csv - the path to the input `csv` file with name and image_url .
- `Line 11`: output_csv - the path to the output `csv` file with the name, original url, processed image name, and output path of the processed image.

For `bckgrnd_rem.py`:
- `Line 7`: input_folder - the path to the folder containing the images to be processed.
- `Line 8`: output_folder - the path to the folder to save the processed images.
- `Line 9`: output_csv - the path to the output `csv` file with the name, original url, processed image name, and output path of the processed image.
