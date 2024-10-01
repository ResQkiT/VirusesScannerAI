import requests
from PIL import Image
import io

class Converter:
    api : str

    def __init__(self, api = "http://hulab.rxnfinder.org/smi2img/") -> None:
        self.api = api

    def convert(self, smile_str : str, width = 800, height = 800):
        smile_str = smile_str.strip()
        response = requests.get(f"{self.api}{smile_str}/?width={width}&height={height}")
        response.raise_for_status() 

        image_bytes = response.content
        image = Image.open(io.BytesIO(image_bytes))

        return image