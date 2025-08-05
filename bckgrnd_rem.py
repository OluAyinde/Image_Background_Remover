import os
import csv
from PIL import Image
from transparent_background import Remover

# Define input and output directories and CSV file
input_folder = "/Users/Downloads/intype"  # Folder containing JPG images
output_folder = "/Users/Downloads/outtype"  # Folder to save PNG images
output_csv = "/Users/Downloads/outtype.csv"  # Output CSV file

# Create output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Initialize the InSPyReNet-based background remover
try:
    remover = Remover()  # Load default InSPyReNet model
    print("Background remover initialized successfully.")
except Exception as e:
    print(f"Error initializing transparent-background remover: {str(e)}")
    exit(1)

# List to store processed image details
processed_images = []

# Check if input folder exists
if not os.path.exists(input_folder):
    print(f"Input folder '{input_folder}' not found.")
    exit(1)

# Process each JPG file in the input folder
for filename in os.listdir(input_folder):
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        input_path = os.path.join(input_folder, filename)
        # Generate output filename by replacing .jpg/.jpeg with .png
        safe_name = os.path.splitext(filename)[0]
        output_filename = f"{safe_name}.png"
        output_path = os.path.join(output_folder, output_filename)

        try:
            # Open the image and ensure RGB format
            input_image = Image.open(input_path).convert("RGB")

            # Remove the background using transparent-background
            try:
                output_image = remover.process(input_image, type="rgba")
            except Exception as e:
                print(f"Background removal failed for {filename}: {str(e)}")
                continue

            # Save the image as PNG with transparent background
            output_image.save(output_path, "PNG")

            # Add to processed images list
            processed_images.append({
                "name": safe_name,
                "original_file": filename,
                "processed_file": output_filename,
                "output_path": output_path
            })

            print(f"Processed: {filename} -> {output_filename}")

        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")

# Write processed image details to output CSV
try:
    with open(output_csv, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["name", "original_file", "processed_file", "output_path"])
        writer.writeheader()
        for image in processed_images:
            writer.writerow(image)
    print(f"Output CSV file '{output_csv}' generated with {len(processed_images)} entries.")
except Exception as e:
    print(f"Error writing output CSV: {str(e)}")
    exit(1)