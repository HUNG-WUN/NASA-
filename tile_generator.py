# tile_generator.py
import os
import math
from PIL import Image
import argparse

def generate_tiles(image_path, output_dir, tile_size=256):
    os.makedirs(output_dir, exist_ok=True)
    img = Image.open(image_path)
    width, height = img.size

    # 計算最大層級（zoom levels）
    max_level = int(math.ceil(math.log2(max(width, height))))

    for level in range(max_level + 1):
        scale = 2 ** (max_level - level)
        level_width = math.ceil(width / scale)
        level_height = math.ceil(height / scale)

        # 縮放影像到該層級
        level_img = img.resize((level_width, level_height), Image.Resampling.LANCZOS)
        level_dir = os.path.join(output_dir, str(level))
        os.makedirs(level_dir, exist_ok=True)

        # 切成瓦片
        x_tiles = math.ceil(level_width / tile_size)
        y_tiles = math.ceil(level_height / tile_size)

        for x in range(x_tiles):
            for y in range(y_tiles):
                left = x * tile_size
                upper = y * tile_size
                right = min(left + tile_size, level_width)
                lower = min(upper + tile_size, level_height)

                tile = level_img.crop((left, upper, right, lower))
                tile.save(os.path.join(level_dir, f"{x}_{y}.jpg"), "JPEG")

    print(f"✅ Finished tiling {image_path}, saved to {output_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("image", help="Path to the large image")
    parser.add_argument("--out", default="tiles_output", help="Output directory")
    args = parser.parse_args()

    generate_tiles(args.image, args.out)
