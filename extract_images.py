import base64
import os
import re

# Read the HTML file
with open('archive/phase1/output.html', 'r') as f:
    html_content = f.read()

# Define the output directory
output_dir = 'react-app/public/images'

# Create a directory to save the images if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Find all base64 encoded images
img_tags = re.findall(r'<img src="data:image/png;base64,([^"]+)" alt="([^"]+)">', html_content)

for i, (img_data, alt_text) in enumerate(img_tags):
    # Decode the base64 string
    img_bytes = base64.b64decode(img_data)
    
    # Create a filename
    filename = f'{output_dir}/{alt_text.replace(" ", "_")}.png'
    
    # Save the image
    with open(filename, 'wb') as f:
        f.write(img_bytes)
    
    print(f"Saved {filename}")

print("Image extraction complete.")
