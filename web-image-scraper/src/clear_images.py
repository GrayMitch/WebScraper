import os
import glob

def clear_image_directory(directory):
    """
    Remove all image files from the specified directory.
    
    Args:
        directory (str): Path to the directory containing images to be deleted.
    
    Returns:
        int: Number of image files deleted.
    """
    # Define common image file extensions
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.webp', '*.gif']
    
    # Ensure the directory exists
    if not os.path.exists(directory):
        print(f"Directory '{directory}' does not exist.")
        return 0
    
    deleted_count = 0
    
    # Iterate through all image extensions
    for ext in image_extensions:
        # Find all files with the current extension
        image_files = glob.glob(os.path.join(directory, ext))
        
        for file_path in image_files:
            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
                deleted_count += 1
            except PermissionError:
                print(f"Error: No permission to delete '{file_path}'")
            except Exception as e:
                print(f"Error deleting '{file_path}': {e}")
    
    print(f"Total images deleted: {deleted_count}")
    return deleted_count

def remove_empty_directories(directory):
    """
    Remove empty directories in the specified directory.
    
    Args:
        directory (str): Path to the directory to clean up.
    """
    for root, dirs, files in os.walk(directory, topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            try:
                os.rmdir(dir_path)
                print(f"Removed empty directory: {dir_path}")
            except OSError as e:
                print(f"Error removing directory '{dir_path}': {e}")
    # Try to remove the root directory itself if it's empty
    try:
        os.rmdir(directory)
        print(f"Removed empty root directory: {directory}")
    except OSError as e:
        print(f"Error removing root directory '{directory}': {e}")

def main():
    # Use the same base directory as in your main.py
    base_directory = "forklift_dataset"
    clear_image_directory(base_directory)
    remove_empty_directories(base_directory)

if __name__ == "__main__":
    main()