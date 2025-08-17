import os
from PIL import Image

SUPPORTED_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.bmp', '.webp', '.tiff')

def resize_exact():
    source_folder = input("[/] Path to original images: ")
    output_folder = input("[/] Path to extract resized images: ")
    size_input = input("[x] Insert WIDTH and HEIGHT (128x128 for example): ").lower().strip()
    if not os.path.isdir(source_folder):
        print(f"[!] ERR: Folder '{source_folder}' not found")
        return
    
    try:
        width_str, height_str = size_input.split('x')
        target_width = int(width_str)
        target_height = int(height_str)
        if target_width <= 0 or target_height <= 0:
            raise ValueError
    except ValueError:
        print("[!] ERR: Incorrect resolution format, use it as WIDTHxHEIGHT (128x128 for example)")
        return
    print("-" * 30)
    
    resized_count = 0
    skipped_count = 0

    for root, _, files in os.walk(source_folder):
        for filename in files:
            if filename.lower().endswith(SUPPORTED_EXTENSIONS):
                try:
                    full_path = os.path.join(root, filename)
                    with Image.open(full_path) as img:
                        original_size = img.size
                        resized_img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
                        
                        relative_path = os.path.relpath(root, source_folder)
                        output_subdir = os.path.join(output_folder, relative_path)
                        os.makedirs(output_subdir, exist_ok=True)
                        
                        output_path = os.path.join(output_subdir, filename)
                        if not filename.lower().endswith('.png') and resized_img.mode == 'RGBA':
                           resized_img = resized_img.convert('RGB')
                        
                        resized_img.save(output_path)

                    print(f"[>]: {filename} ({original_size[0]}x{original_size[1]} --> {target_width}x{target_height})")
                    resized_count += 1

                except Exception as e:
                    print(f"[!] ERR: File resize error: '{filename}': {e}")
                    skipped_count += 1
    print("-" * 30)
    print("[O] Resizing complete!")
    print(f"[O] Processed {resized_count} files")
    print(f"[O] Skipped {skipped_count} files")
    print(f"[>] Saved in: {output_folder}")


if __name__ == "__main__":
    resize_exact()