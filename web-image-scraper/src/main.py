import os
from scraper import ImageScraper
from utils import create_directory

def main():
    search_keys = ["forklift"]
    base_directory = "forklift_dataset"
    downloaded_urls = set()  # Track downloaded image URLs

    # Create the base directory
    create_directory(base_directory)

    for key in search_keys:
        scraper = ImageScraper(search_key=key, save_dir=base_directory)
        print(f"Searching for images with key: {key}")
        image_urls = scraper.search_images(key)
        print(f"Found {len(image_urls)} image URLs for {key}")
        # Filter out URLs that have already been downloaded
        unique_urls = [url for url in image_urls if url not in downloaded_urls]
        print(f"Downloading {len(unique_urls)} unique images for {key}")
        saved_paths = scraper.download_images(unique_urls, base_directory)
        print(f"Saved {len(saved_paths)} images for {key}")
        downloaded_urls.update(unique_urls)  # Add new URLs to the set

if __name__ == "__main__":
    main()