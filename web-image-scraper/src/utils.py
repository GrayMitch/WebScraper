def create_directory(directory):
    import os
    if not os.path.exists(directory):
        os.makedirs(directory)

def is_valid_url(url):
    from urllib.parse import urlparse
    parsed = urlparse(url)
    return all([parsed.scheme, parsed.netloc])