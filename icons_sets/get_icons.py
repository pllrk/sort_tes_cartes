import requests
from bs4 import BeautifulSoup
import os
from PIL import Image
from io import BytesIO
import re
import subprocess
import tempfile
import json

# Set up headers to mimic a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# URL of the page to scrape
url = 'https://edhrec.com/sets'

# Directory to save images
output_dir = 'edhrec_set_png'
svg_dir = 'edhrec_set_svgs'  # Directory for raw SVGs if conversion fails
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
if not os.path.exists(svg_dir):
    os.makedirs(svg_dir)

def sanitize_filename(name):
    """Sanitize set name to be used as a filename."""
    return re.sub(r'[^\w\s-]', '', name).strip().replace(' ', '_')

def download_and_convert_image(img_url, set_name):
    """Download image (SVG or other format) and save as JPG with sanitized set name."""
    try:
        # Verify URL is valid
        if not img_url or img_url == '':
            print(f'Skipping {set_name}: Empty or invalid image URL')
            return
        
        # Download the image
        response = requests.get(img_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Check content type
        content_type = response.headers.get('content-type', '')
        print(f'Content type for {set_name} ({img_url}): {content_type}')
        
        # Sanitize set name for filename
        sanitized_name = sanitize_filename(set_name)
        output_path = os.path.join(output_dir, f'{sanitized_name}.png')
        svg_path = os.path.join(svg_dir, f'{sanitized_name}.svg')
        
        # Save raw SVG for debugging
        with open(svg_path, 'wb') as f:
            f.write(response.content)
        print(f'Saved raw SVG for {set_name} as {svg_path}')
        
        # Check if the image is an SVG
        if img_url.endswith('.svg') or 'image/svg' in content_type:
            try:
                # Use ImageMagick to convert SVG to PNG
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_png:
                    subprocess.run(['convert', svg_path, temp_png.name], check=True, capture_output=True)
                    img = Image.open(temp_png.name)
                    # Convert to RGB if necessary
                    if img.mode in ('RGBA', 'P'):
                        img = img.convert('RGB')
                    # Save as JPG
                    img.save(output_path, 'JPEG', quality=95)
                    print(f'Saved image for {set_name} as {output_path}')
                    os.remove(temp_png.name)  # Clean up temporary file
            except subprocess.CalledProcessError as convert_error:
                print(f'ImageMagick conversion failed for {set_name} ({img_url}): {convert_error.stderr.decode()}')
                print(f'Raw SVG saved at {svg_path} for manual inspection')
                return
            except Exception as e:
                print(f'Image processing failed for {set_name} ({img_url}): {e}')
                print(f'Raw SVG saved at {svg_path} for manual inspection')
                return
        else:
            # Handle non-SVG images
            try:
                img = Image.open(BytesIO(response.content))
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                img.save(output_path, 'JPEG', quality=95)
                print(f'Saved image for {set_name} as {output_path}')
                os.remove(svg_path)  # Remove SVG if not needed
            except Exception as img_error:
                print(f'Image processing failed for {set_name} ({img_url}): {img_error}')
                print(f'Raw file saved at {svg_path} for manual inspection')
                return
        
    except requests.RequestException as req_error:
        print(f'Network error for {set_name} ({img_url}): {req_error}')
    except Exception as e:
        print(f'Unexpected error for {set_name} ({img_url}): {e}')

def scrape_edhrec_sets():
    """Scrape set names and images from the EDHREC sets page."""
    try:
        # Check if ImageMagick is installed
        result = subprocess.run(['convert', '--version'], capture_output=True, text=True)
        if result.returncode != 0:
            print("Error: ImageMagick is not installed or not found in PATH.")
            print("Install ImageMagick: https://imagemagick.org/script/download.php")
            return
        print("ImageMagick detected, proceeding with scraping.")
        
        # Fetch the webpage
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find set items based on provided structure
        set_items = soup.find_all('div', class_='SubNav_item__bXE1v')
        
        if not set_items:
            print("No set items found. The HTML structure may have changed.")
            return
        
        print(f'Found {len(set_items)} sets to process.')
        for item in set_items:
            # Extract set name
            name_tag = item.find('span', class_='SubNav_textLeft__8fqWq')
            set_name = name_tag.get_text(strip=True) if name_tag else 'Unknown_Set'
            
            # Extract image URL
            img_tag = item.find('img', class_='set-icon')
            img_url = img_tag['src'] if img_tag and 'src' in img_tag.attrs else None
            
            print(f'Processing {set_name} with image URL: {img_url}')
            if img_url:
                # Handle relative URLs
                if img_url.startswith('/'):
                    img_url = 'https://edhrec.com' + img_url
                download_and_convert_image(img_url, set_name)
            else:
                print(f'Skipping {set_name}: No image URL found')
                
    except requests.RequestException as e:
        print(f'Error fetching webpage: {e}')
    except Exception as e:
        print(f'Unexpected error: {e}')

if __name__ == '__main__':
    scrape_edhrec_sets()