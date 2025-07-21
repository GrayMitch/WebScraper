import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, urlparse
import os
import time
import base64
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException
from utils import is_valid_url

class ImageScraper:
    def __init__(self, search_key, save_dir):
        self.search_key = search_key
        self.save_dir = save_dir

    def search_images(self, search_key, max_results=10):
        """
        Retrieve image URLs directly from Google's image search results page.
        
        Args:
            search_key (str): The query to search for images.
            max_results (int): Maximum number of image URLs to return (default: 10).
        
        Returns:
            list: A list of image URLs (base64 or direct URLs).
        """
        if not search_key:
            print("No search key provided")
            return []

        image_urls = []
        driver = None
        try:
            # Set up Selenium with headless Chrome
            chrome_options = Options()
            chrome_options.add_argument("--headless")  # Uncomment for headless mode
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            
            try:
                driver = webdriver.Chrome(service=Service('/usr/bin/chromedriver'), options=chrome_options)
            except WebDriverException as e:
                print(f"Failed to initialize ChromeDriver: {e}")
                return []

            # URL-encode the search query
            query = quote(search_key)
            url = f"https://www.google.com/search?q={query}&tbm=isch"
            
            print(f"Loading Google image search: {url}")
            driver.get(url)
            
            # Handle potential consent screen
            try:
                consent_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Accept') or contains(@aria-label, 'agree') or contains(@aria-label, 'Consent')] | //div[contains(text(), 'Accept') or contains(text(), 'agree') or contains(text(), 'Consent')]"))
                )
                consent_button.click()
                print("Consent screen accepted")
                time.sleep(2)
            except TimeoutException:
                print("No consent screen found or failed to interact")
            except Exception as e:
                print(f"Error handling consent screen: {e}")

            # Check for CAPTCHA
            try:
                captcha = driver.find_element(By.ID, "recaptcha") or driver.find_element(By.XPATH, "//*[contains(text(), 'CAPTCHA') or contains(text(), 'unusual traffic')]")
                print("CAPTCHA detected. Please solve it manually in the browser and press Enter to continue...")
                input("Press Enter after solving CAPTCHA...")
            except:
                pass

            # Scroll to load more images
            last_height = driver.execute_script("return document.body.scrollHeight")
            while len(image_urls) < max_results:
                try:
                    # Wait for image thumbnails to load
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "img.YQ4gaf, img.rg_i"))
                    )
                    print("Thumbnails loaded successfully")
                    
                    # Get image elements
                    images = driver.find_elements(By.CSS_SELECTOR, "img.YQ4gaf, img.rg_i")
                    print(f"Found {len(images)} image elements")
                    
                    for img in images:
                        try:
                            src = img.get_attribute("src")
                            if src and (src.startswith("data:image") or is_valid_url(src)):
                                if src not in image_urls:
                                    image_urls.append(src)
                                    print(f"Collected image URL: {src[:50]}...")
                                    if len(image_urls) >= max_results:
                                        break
                        except Exception as e:
                            print(f"Error processing image: {e}")
                            continue
                    
                    if len(image_urls) >= max_results:
                        break
                    
                    # Scroll to load more images
                    driver.execute_script("window.scrollBy(0, 1000);")
                    time.sleep(2)
                    new_height = driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        print("No more images loaded after scrolling")
                        break
                    last_height = new_height
                    
                except TimeoutException:
                    print("Timeout waiting for thumbnails to load")
                    break

            if not image_urls:
                print("No images found. Saving page source for debugging...")
                with open("debug_page_source.html", "w", encoding="utf-8") as f:
                    f.write(driver.page_source)

        except Exception as e:
            print(f"Error during image search for '{search_key}': {e}")
            if driver:
                with open("debug_page_source.html", "w", encoding="utf-8") as f:
                    f.write(driver.page_source)
        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass
        
        print(f"Collected {len(image_urls)} unique image URLs for '{search_key}'")
        return image_urls

    def download_images(self, image_urls, save_dir="images"):
        """
        Download images from provided URLs (base64 or direct) and save them to the specified directory.
        
        Args:
            image_urls (list): List of image URLs to download (base64 or direct).
            save_dir (str): Directory to save the images (default: 'images').
        
        Returns:
            list: List of paths to the saved images.
        """
        if not image_urls:
            print(f"No image URLs provided for download")
            return []

        saved_paths = []
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        os.makedirs(save_dir, exist_ok=True)

        for i, url in enumerate(image_urls):
            try:
                if url.startswith("data:image"):
                    # Handle base64-encoded image
                    match = re.match(r"data:image/(.*?);base64,(.*)", url)
                    if not match:
                        print(f"Skipping invalid base64 URL: {url[:50]}...")
                        continue
                    img_type, img_data = match.groups()
                    if img_type not in ["jpeg", "jpg", "png", "webp"]:
                        print(f"Skipping unsupported image type: {img_type}")
                        continue
                    img_bytes = base64.b64decode(img_data)
                    ext = ".jpg" if img_type in ["jpeg", "jpg"] else f".{img_type}"
                    filename = f"image_{i+1}{ext}"
                else:
                    # Handle direct URL
                    parsed_url = urlparse(url)
                    filename = os.path.basename(parsed_url.path)
                    
                    if not filename or not any(filename.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.webp']):
                        filename = f"image_{i+1}"
                    
                    response = requests.get(url, headers=headers, stream=True, timeout=10)
                    response.raise_for_status()
                    
                    content_type = response.headers.get('content-type', '').lower()
                    if 'image' not in content_type:
                        print(f"Skipping {url}: Not an image (Content-Type: {content_type})")
                        continue
                    
                    ext = ""
                    if 'jpeg' in content_type:
                        ext = '.jpg'
                    elif 'png' in content_type:
                        ext = '.png'
                    elif 'gif' in content_type:
                        ext = '.gif'
                    elif 'webp' in content_type:
                        ext = '.webp'
                    else:
                        print(f"Skipping {url}: Unknown image content type ({content_type})")
                        continue
                    
                    filename = f"{os.path.splitext(filename)[0]}{ext}"
                    img_bytes = response.content

                # Ensure unique filename
                base, ext = os.path.splitext(filename)
                counter = 1
                final_filename = filename
                while os.path.exists(os.path.join(save_dir, final_filename)):
                    final_filename = f"{base}_{counter}{ext}"
                    counter += 1
                
                file_path = os.path.join(save_dir, final_filename)
                
                # Save image
                with open(file_path, 'wb') as f:
                    f.write(img_bytes)
                
                saved_paths.append(file_path)
                print(f"Downloaded: {file_path}")
                
                time.sleep(0.5)
                
            except requests.exceptions.RequestException as e:
                print(f"Failed to download {url[:50]}...: {e}")
                continue
            except PermissionError:
                print(f"Error: No permission to write to '{file_path}'") # type: ignore
                continue
            except Exception as e:
                print(f"Error saving {url[:50]}...: {e}")
                continue

        return saved_paths