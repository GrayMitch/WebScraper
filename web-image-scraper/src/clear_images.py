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

def main():
    # Use the same base directory as in your main.py
    base_directory = "forklift_dataset"
    clear_image_directory(base_directory)

if __name__ == "__main__":
    main()