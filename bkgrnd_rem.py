import os
import csv
import requests
from PIL import Image
from io import BytesIO
from transparent_background import Remover

#Define output directory and CSV files
output_folder = "/Users/Downloads/outtype"  #Folder to save PNG images
input_csv = "/Users/Downloads/intype"  #Input CSV with name and image_url
output_csv = "/Users/Downloads/outtype.csv"  #Output CSV file

#Create output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

#Initialize the InSPyReNet-based background remover
try:
    remover = Remover()  #Load default InSPyReNet model
except Exception as e:
    print(f"Error initializing transparent-background remover: {str(e)}")
    exit(1)

#List to store processed image details
processed_images = []

#Read input CSV file
try:
    with open(input_csv, mode="r", newline="") as file:
        reader = csv.DictReader(file)
        #Check for required columns
        if "name" not in reader.fieldnames or "image_url" not in reader.fieldnames:
            raise ValueError("Input CSV must contain 'name' and 'image_url' columns")

        #Process each row in the CSV
        for row in reader:
            name = row["name"].strip()
            url = row["image_url"].strip()

            #Validate URL
            if not url.lower().endswith((".jpg", ".jpeg")):
                print(f"Skipping non-JPG URL for {name}: {url}")
                continue

            #Ensure name is valid for filename
            safe_name = "".join(c for c in name if c.isalnum() or c in (".", "_", "-")).rstrip()
            if not safe_name:
                safe_name = f"image_{len(processed_images) + 1}"
            output_filename = f"{safe_name}.png"
            output_path = os.path.join(output_folder, output_filename)

            try:
                #Download the image
                response = requests.get(url, timeout=10)
                response.raise_for_status()  #Raise error for bad status codes

                #Open the image from the response content
                input_image = Image.open(BytesIO(response.content)).convert("RGB")

                #Remove the background using transparent-background
                output_image = remover.process(input_image, type="rgba")

                #Save the image as PNG with transparent background
                output_image.save(output_path, "PNG")

                #Add to processed images list
                processed_images.append({
                    "name": name,
                    "original_url": url,
                    "processed_file": output_filename,
                    "output_path": output_path
                })

                print(f"Processed: {name} ({url}) -> {output_filename}")

            except requests.RequestException as e:
                print(f"Error downloading {url} for {name}: {str(e)}")
            except Exception as e:
                print(f"Error processing {url} for {name}: {str(e)}")

except FileNotFoundError:
    print(f"Input CSV file '{input_csv}' not found.")
    exit(1)
except Exception as e:
    print(f"Error reading input CSV: {str(e)}")
    exit(1)

#Write processed image details to output CSV
with open(output_csv, mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["name", "original_url", "processed_file", "output_path"])
    writer.writeheader()
    for image in processed_images:
        writer.writerow(image)

print(f"Output CSV file '{output_csv}' generated with {len(processed_images)} entries.")