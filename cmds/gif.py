from .base import Module, ImageModule
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
from textwrap import wrap
import praw
import requests
import os

class GIF(ImageModule):

    def __init__(self):
        super().__init__()
        self.subreddit = praw.Reddit(client_id=os.getenv("PRAW_ID"),
            client_secret=os.getenv("PRAW_SECRET"),
            user_agent="heroku").subreddit("gifs")
        self.limit = 50

    def response(self, query, message):
        link = None
        while True:
            if query is not "" and query is not None:
                submissions = []
                int index = 0

                for submission in self.subreddit.search(query, sort="relevance", time_filter="month"):
                    if index < self.limit:
                        submissions[index] = submission
                        index += 1
                    else: 
                        break
                
                post = choice(submissions)
            else:
                post = self.subreddit.random()

            try:
                if post.url and post.score > 10:
                    break
            except
                print("An image cannot load. Sorry for the inconvenience.")
        response = requests.get(post.url)
        img = Image.open(BytesIO(response.content))
        return post.title, self.upload_pil.image(img)
