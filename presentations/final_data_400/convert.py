import os
from pdf2image import convert_from_path

def convert_pdf_to_slides(pdf_path, output_folder):
    # Check if the output folder exists, if not, create it
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created directory: {output_folder}")

    print(f"Loading {pdf_path}... this might take a few seconds.")
    
    # Convert PDF pages to images
    # dpi=300 ensures the images are high quality so text stays crisp on screen
    pages = convert_from_path(pdf_path, dpi=300)
    
    print(f"Found {len(pages)} pages. Saving images...")

    # Loop through the pages and save them
    for i, page in enumerate(pages):
        # We add 1 so it starts at slide1.png instead of slide0.png
        slide_number = i + 1
        filename = f"slide{slide_number}.png"
        save_path = os.path.join(output_folder, filename)
        
        # Save the image as a PNG
        page.save(save_path, 'PNG')
        print(f"Saved: {save_path}")

    print("All slides extracted successfully!")

# --- Configuration ---
# Replace these strings with your actual file paths
PDF_FILE_PATH = r"CUTSLIDES.pdf" 
OUTPUT_DIRECTORY_PATH = r"C:\Users\popop\Desktop\final_data_400"

# Run the function
if __name__ == "__main__":
    convert_pdf_to_slides(PDF_FILE_PATH, OUTPUT_DIRECTORY_PATH)