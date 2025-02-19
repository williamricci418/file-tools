import os
import subprocess

def convert_svg_to_png(l_directory, l_export_dpi, l_export_width, l_export_height, l_source_format, l_target_format):
    """
    Converts all .svg files in the specified directory and its subdirectories to .png format.

    Parameters:
    l_directory (str): Path to the directory containing .svg files.
    l_export_dpi (int): DPI for the output image.
    l_export_width (int): Width for the output image in pixels.
    l_export_height (int): Height for the output image in pixels.
    l_source_format (str): Source format (e.g., 'svg').
    l_target_format (str): Target format (e.g., 'png').
    """
    if not os.path.exists(l_directory):
        print(f"The directory '{l_directory}' does not exist.")
        return

    # Set file counter
    file_count_success = 0
    file_count_fail = 0
    file_count_total = 0

    # Walk through the directory and its subdirectories
    for root, _, files in os.walk(l_directory):
        for filename in files:
            if filename.lower().endswith('.svg'):
                svg_path = os.path.join(root, filename)
                
                # Split the filename to insert the amended text
                name_part, extension = os.path.splitext(filename)
                
                filename_amended = str(l_export_width) + 'x' + str(l_export_height)
                
                png_filename = f"{name_part}_{filename_amended}.{l_target_format}"

                # Create the complete PNG path
                png_path = os.path.join(root, png_filename)
                
                ##print(f"Source: {svg_path}")
                ##print(f"Target: {png_path}")
                
                # Check if the .png file already exists - delete if true
                if os.path.exists(png_path):
                    print(f"Deleting existing file '{png_path}'")
                    os.remove(png_path)
                try:
                    # Use Inkscape for conversion
                    subprocess.run([
                        'inkscape', svg_path,
                        f'--export-dpi={l_export_dpi}',
                        f'--export-width={l_export_width}',
                        f'--export-height={l_export_height}',
                        f'--export-type={l_target_format}',
                        '--export-filename', png_path
                    ], check=True)
                    file_count_success += 1
                    print(f"Converted '{svg_path}' to '{png_path}'")
                except subprocess.CalledProcessError as e:
                    file_count_fail += 1
                    print(f"Failed to convert '{svg_path}': {e}")
                except FileNotFoundError:
                    print("Inkscape not found. Please ensure it is installed and added to your PATH.")
    
    file_count_total = file_count_success + file_count_fail
    
    print(f"Conversion complete. Total files processed: {file_count_total}. Total files converted successfully: {file_count_success}. Total files failed to convert: {file_count_fail}.")
    
if __name__ == "__main__":
    directory_path = ('D:\Workspace\Icons')
    export_dpi = 300
    export_height = 64
    export_width = 64
    source_extension = 'svg'
    target_extension = 'png'

    convert_svg_to_png(l_directory=directory_path, l_export_dpi=export_dpi, l_export_width=export_width, l_export_height=export_height, l_source_format=source_extension, l_target_format=target_extension)
