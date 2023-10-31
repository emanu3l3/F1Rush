import requests

class WikiImgs:
    def __init__(self, urls, pithumbsize):
        self.urls = urls
        self.pithumbsize = pithumbsize
        self.images = []
        self.clear_urls()
        
    def clear_urls(self):
        for url in range(len(self.urls)):   
            # get only the page name from the urls 
            self.urls[url] = self.urls[url].split("/")[-1]
        
    def get_images(self):
        # use the Wikipedia API to get images from a page
        for url in range(len(self.urls)):
            response_img = requests.get(
                f"https://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&titles={self.urls[url]}&pithumbsize={self.pithumbsize}&redirects"
                ).json()
            try:
                response_img_pages = response_img["query"]["pages"]
                response_img_pages_id = list(response_img_pages)[0]
                self.images.append(response_img_pages[response_img_pages_id]["thumbnail"]["source"])
            except:
                self.images.append("./static/images/default.png")
        
        return self.images
    
    
        
