import threading
import requests
import os
from threading import Semaphore

class ImageDownloader:
    def download_image(self, url, folder, filename):
        # Create the folder if it doesn't exist
        os.makedirs(folder, exist_ok=True)

        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Create the file path
            file_path = os.path.join(folder, filename)

            # Save the image to the file path
            with open(file_path, 'wb') as file:
                file.write(response.content)

            #print(f"Image downloaded successfully at {file_path}")
        else:
            return "Failed to download the image"