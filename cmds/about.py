from .base import Module
from glob import glob
import json

class About(Module):
    DESCRIPTION = "This command shows information about GIFBot."
    string = None

    def response(self, query, message):
        link = "https://github.com/"
        return f"Hello! My name is GIFBot, and I am a GroupMe bot hired to provide wonderful GIFs to our members. I am maintained by Robert Freeman and built from the code for MemeOverflow (created by Ausaf Ahmed)! You can find my code at: {link}"