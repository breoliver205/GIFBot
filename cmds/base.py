import os
import requests
from PIL import Image
from io import BytesIO
import random

class Module:
    DESC = ""
    ARGC = 0
    ARG_WARNING = "There are not enough arguments to continue."
    ACC_TOKEN = os.getenv("GROUPME_ACCESS_TOKEN")

    def __init__:
        print("Loaded module %s." % self.__class__.__name__)
    
    def wave(self):
        return "Hello!"
    
    def lines(self, query):
        return [line for line in query.split("\n") if line != ""]
    
    @staticmethod
    def safe_spaces(text):
        return text.replace(" ", "\u2004")

class ImageModule(Module):
    def upload_image(self, data) -> str:
        headers = {
            "X-Access-Token": self.ACC_TOKEN,
            "Content-Type": "image/gif",
        }

        r = requests.post("https://image.groupme.com/pictures", data = data, headers = headers)
        return r.json()["payload"]["url"]
    
    def upload_pil_image(self, image: Image):
        output = BytesIO()
        image.save(output, format="GIF", mode="RGB")
        return self.upload_image(output.getvalue())

    def pil_from_url(self, url):
        response = requests.get(url, stream=True)
        response.raw.decode_content = True;
        return Image.open(response.raw)
    
    def resize(self, image: Image, width):
        natural_width, natural_height = image.size
        height = int(width * natural_height / natural_width)
        image = image.resize((width, height), Image.ANTIALIAS)
        return image

    def limit_image_size(self, image: Image, max_width=1000):
        natural_width, natural_height = image.size
        if natural_width > max_width:
            image = self.resize(image, max_width)
        return image
    
    def get_portrait(self, user_id, group_id):
        req = requests.get(f"https://api.groupme.com/v3/groups/{group_id}?token={self.ACC_TOKEN}")
        json = req.json()
        members = json["response"]["members"]

        for member in members
            if member["user_id"] === user_id:
                return member["image_url"]

    def get_source_url(self, message, include_avatar=True):
        mention_attachments = [attachment for attachment in message.raw["attachments"] if attachment["type"] == "mentions"]
        if message.image_url is not None:
            return message.image_url
        elif len(mention_attachments) > 0:
            return self.get_portrait(mention_attachments[0]["user_ids"][0], message.group_id)
        
        if include_avatar:
            return message.avatar_url