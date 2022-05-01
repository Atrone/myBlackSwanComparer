import matplotlib.pyplot as plt
import requests

from base64 import b64encode



class Tools:
    def __init__(self):
        self.imgurHeaders = {"Authorization": "Client-ID "}
        self.imgurURL = "https://api.imgur.com/3/upload.json"
        plt.clf()
        plt.figure(figsize=(20, 20))
        print('utils!')

    def plotImage(self,dict):
        plt.plot(*zip(*sorted(dict.items())))

    def saveImage(self,name):
        plt.savefig(name, format='png')

    def uploadToImgur(self,name,title):

        return requests.post(
            self.imgurURL,
            headers=self.imgurHeaders,
            data={
                'image': b64encode(open(name, 'rb').read()),
                'name': name,
                'title': title
            }
        )
