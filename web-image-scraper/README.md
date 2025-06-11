# Web Image Scraper

This project is a web image scraper that allows users to search for images based on a specific keyword and saves them to a designated directory called `forklift_dataset`.

## Project Structure

```
web-image-scraper
├── src
│   ├── main.py          # Entry point of the application
│   ├── scraper.py       # Contains the ImageScraper class for scraping images
│   └── utils.py         # Utility functions for directory creation and URL validation
├── forklift_dataset      # Directory where downloaded images will be saved
├── requirements.txt      # Lists the dependencies required for the project
└── README.md             # Documentation for the project
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd web-image-scraper
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the scraper:
   ```
   python src/main.py
   ```

2. When prompted, enter a search keyword for the images you want to download.

3. The images will be saved in the `forklift_dataset` directory.

## Dependencies

This project requires the following Python packages:
- requests
- beautifulsoup4

Make sure to install these packages using the `requirements.txt` file provided.

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes.