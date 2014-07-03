#!/usr/bin/env python

import web  # web.py
import smbus
import os

urls = (
    '/', 'index',
    '/images/(.*)', 'images' #this is where the image folder is located....
)


app = web.application(urls, globals())

class index:
    def GET(self):
        os.system("./plot-data.sh")
        return "<html><body style='background-color:black'><img src='images/graph.png' /></body></html>"

class images:
    def GET(self, name):
        web.header("Content-Type", "images/png") # Set the Header
        return open("graph.png","rb").read() # Notice 'rb' for reading images

if __name__ == "__main__":
    app.run()
