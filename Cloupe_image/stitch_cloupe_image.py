import json
import struct
import logging
import gzip
import io
import os
import argparse
from PIL import Image

logging.basicConfig(level=logging.INFO, format="[%(asctime)s][%(levelname)s] %(message)s")

def decompress_chunk(chunk):
    if chunk[:2] == b"\x1f\x8b":
        try:
            with gzip.GzipFile(fileobj=io.BytesIO(chunk)) as gz:
                return gz.read()
        except OSError as e:
            logging.error(f"GZIP decompression failed: {e}")
            return chunk
    return chunk

def stitch_cloupe_image(cloupe_path):
    output_file = os.path.basename(cloupe_path).replace(".cloupe", "_stitched_image.tiff")

    try:
        with open(cloupe_path, "rb") as f:
            header_raw = f.read(4096)
            header = json.loads(header_raw.decode("utf-8", errors="replace").strip("\x00"))
            f.seek(header["indexBlock"]["Start"])
            block_raw = f.read(header["indexBlock"]["End"] - header["indexBlock"]["Start"])
            index_block = json.loads(decompress_chunk(block_raw).decode("utf-8", errors="replace").strip("\x00"))
        logging.info("Loaded header and index block.")
    except Exception as e:
        logging.error(f"Failed to read header or index: {e}")
        return

    tiles_list = index_block.get("SpatialImageTiles", [])
    if not tiles_list:
        logging.error("No SpatialImageTiles found in .cloupe file.")
        return

    tile_info = tiles_list[0]
    full_width, full_height = tile_info["Dims"]
    tile_size = tile_info["TileSize"]
    tiles_dict = tile_info["Tiles"]
    img_format = tile_info.get("Format", "png")

    logging.info(f"Stitching image of {full_width}x{full_height} from {len(tiles_dict)} tiles ({tile_size} px each).")

    stitched = Image.new("RGB", (full_width, full_height))
    processed = 0

    zoom_levels = [int(tile_path.split("/")[0]) for tile_path in tiles_dict.keys()]
    max_zoom_level = max(zoom_levels)
    logging.info(f"Using highest zoom level: {max_zoom_level}")

    for tile_path, meta in tiles_dict.items():
    
        if not tile_path.startswith(f"{max_zoom_level}/"):
            continue  
        
        try:
            row_col = os.path.basename(tile_path).replace(f".{img_format}", "").split("_")
            row, col = int(row_col[0]), int(row_col[1])  
    
            with open(cloupe_path, "rb") as f:
                f.seek(meta["Start"])
                tile_bytes = f.read(meta["End"] - meta["Start"])
    
            tile_data = decompress_chunk(tile_bytes)
            tile_img = Image.open(io.BytesIO(tile_data))  
            tile_width, tile_height = tile_img.size
    
            y, x = col * tile_size, row * tile_size  # x = col * size, y = row * size
            stitched.paste(tile_img, (x, y, x + tile_width, y + tile_height))
    
            processed += 1
            if processed % 100 == 0:
                logging.info(f"Stitched {processed}/{len(tiles_dict)} tiles.")

        except Exception as e:
            logging.warning(f"Failed to process tile {tile_path}: {e}")
            
stitched = stitched.transpose(Image.ROTATE_270)       # Rotate 90 degrees to the right
stitched = stitched.transpose(Image.FLIP_LEFT_RIGHT)  # Then flip horizontally

    try:
        stitched.save("stitched_highres.tiff", format="TIFF")
        logging.info("✅ High-res image saved as: stitched_highres.tiff")

        img_resized = stitched.copy()
        img_resized.thumbnail((5000, 5000))
        img_resized.save("stitched_downsampled.tiff", format="TIFF")
        logging.info("✅ Downsampled image saved as: stitched_downsampled.tiff")
    except Exception as e:
        logging.error(f"❌ Could not save image: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stitch a high-res image from a 10x Genomics .cloupe file")
    parser.add_argument("--input", required=True, help="Path to .cloupe file")

    args = parser.parse_args()
    stitch_cloupe_image(args.input)
