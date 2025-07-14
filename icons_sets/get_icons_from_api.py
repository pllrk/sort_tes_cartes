import requests
from bs4 import BeautifulSoup
import os
from PIL import Image
from io import BytesIO
import re
import subprocess
import tempfile
import json


# Directory to save images
output_dir = 'edhrec_set_png'
svg_dir = 'edhrec_set_svgs'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
if not os.path.exists(svg_dir):
    os.makedirs(svg_dir)

def get_the_image(image_set, nom_set_code):
	output_path = os.path.join(output_dir, f'{nom_set_code}.png')
	svg_path = os.path.join(svg_dir, f'{nom_set_code}.svg')
	with open(svg_path, 'wb') as f:
		f.write(image_set.content)
	#print(nom_set_code)
	try:
		with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_png:
			subprocess.run(['convert', svg_path, temp_png.name], check=True, capture_output=True)
			img = Image.open(temp_png.name)
    		# Convert to RGB if necessary
			if img.mode in ('RGBA', 'P'):
				img = img.convert('RGB')
    		# Save as JPG
			img.save(output_path, 'PNG', quality=95)
			#print(f'Saved image for {nom_set_code} as {output_path}')
			os.remove(temp_png.name)  # Clean up temporary file
	except Exception as e:
			print(f'Image processing failed for {nom_set_code}')
			#print(f'Raw SVG saved at {svg_path} for manual inspection')
			return		

lien_list_global = "https://api.scryfall.com/sets/"
res=requests.get(lien_list_global)
list_global=json.loads(res.text)
#print(list_global)
i = 0
for caca in list_global['data']:
	i = i + 1
	nom_set_code = caca["code"]
	lien_set_url = caca['icon_svg_uri']
	image_set = requests.get(lien_set_url, timeout=10)
	if image_set.status_code == 200:
		#print(i)
		get_the_image(image_set, nom_set_code)
		#print(nom_set_code)
print('done')





#
#
#download_and_convert_image(img_url, set_name):
#"""Download image (SVG or other format) and save as JPG with sanitized set name."""
#try:
#    # Download the image
#    response = requests.get(img_url, timeout=10)
#    response.raise_for_status()
#    
#    # Check content type
#    content_type = response.headers.get('content-type', '')
#    print(f'Content type for {set_name} ({img_url}): {content_type}')
#  
#    # Check if the image is an SVG
#    if img_url.endswith('.svg') or 'image/svg' in content_type:
#        try:
#            # Use ImageMagick to convert SVG to PNG
#            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_png:
#                subprocess.run(['convert', svg_path, temp_png.name], check=True, capture_output=True)
#                img = Image.open(temp_png.name)
#                # Convert to RGB if necessary
#                if img.mode in ('RGBA', 'P'):
#                    img = img.convert('RGB')
#                # Save as JPG
#                img.save(output_path, 'JPEG', quality=95)
#                print(f'Saved image for {set_name} as {output_path}')
#                os.remove(temp_png.name)  # Clean up temporary file
#        except subprocess.CalledProcessError as convert_error:
#            print(f'ImageMagick conversion failed for {set_name} ({img_url}): {convert_error.stderr.decode()}')
#            print(f'Raw SVG saved at {svg_path} for manual inspection')
#            return
#        except Exception as e:
#            print(f'Image processing failed for {set_name} ({img_url}): {e}')
#            print(f'Raw SVG saved at {svg_path} for manual inspection')
#            return
#  
#    
#except requests.RequestException as req_error:
#    print(f'Network error for {set_name} ({img_url}): {req_error}')
#except Exception as e:
#    print(f'Unexpected error for {set_name} ({img_url}): {e}')
#