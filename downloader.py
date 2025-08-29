import requests
from bs4 import BeautifulSoup
import os

def list_files(url):
    """Fetch directory listing from a host's shared folder."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        files = []
        for link in soup.find_all("a"):
            href = link.get("href")
            if href not in ("../", "/"):
                files.append(href)
        return files
    except Exception as e:
        return [f"Error: {e}"]

def download_file(url, filename, save_dir):
    """Download a file from the host and save locally."""
    try:
        response = requests.get(url + filename, stream=True)
        response.raise_for_status()

        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, filename)

        with open(save_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

        return f"Downloaded: {save_path}"
    except Exception as e:
        return f"Error downloading {filename}: {e}"
