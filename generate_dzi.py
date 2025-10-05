import os
import pyvips  # 正確名稱

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TILES_DIR = os.path.join(BASE_DIR, 'tiles_output')
TIF_PATH = r"C:/Users/s4111/PycharmProjects/NASA/LRO_WAC_Mosaic_Global_303ppd_v02.tif"

# 確保輸出資料夾存在
os.makedirs(TILES_DIR, exist_ok=True)

# 使用 pyvips 生成 DZI（Deep Zoom）
image = pyvips.Image.new_from_file(TIF_PATH, access='sequential')
dzi_filename = 'new_image.dzi'  # 輸出的 DZI 名稱
image.dzsave(os.path.join(TILES_DIR, dzi_filename), tile_size=128, overlap=1, suffix='.jpg')

print(f"Generated DZI: {dzi_filename} in {TILES_DIR}")
