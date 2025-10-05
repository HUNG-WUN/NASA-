import os
import requests
import pyvips

def download_image(url, save_path="nasa_image.jpg"):
    print(f"Downloading from {url} ...")
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(save_path, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
        print(f"✅ Downloaded to {save_path}")
        return save_path
    else:
        raise Exception(f"Failed to download: {r.status_code}")

def convert_to_dzi(image_path, output_dir="static/tiles", output_name="output"):
    os.makedirs(output_dir, exist_ok=True)
    print(f"Converting {image_path} to DZI format ...")
    image = pyvips.Image.new_from_file(image_path, access="sequential")
    output_path = os.path.join(output_dir, output_name)
    image.dzsave(output_path)
    print(f"✅ DZI created: {output_path}.dzi")
    return f"{output_name}.dzi"

if __name__ == "__main__":
    # 範例：NASA 測試影像
    url = "https://images-assets.nasa.gov/image/PIA12235/PIA12235~orig.jpg"
    img_path = download_image(url, "nasa_image.jpg")
    convert_to_dzi(img_path)
