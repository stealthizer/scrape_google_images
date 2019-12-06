from bs4 import BeautifulSoup
import urllib3
import os
import argparse
import sys
import json


class ScrapeImages:

    def __init__(self, query, max_images, save_directory):
        self.header = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
        urllib3.disable_warnings()
        self.http = urllib3.PoolManager()
        self.query(query, max_images, save_directory)


    def get_soup(self, url):
        response = self.http.request(url=url, headers=self.header, method='GET')
        return BeautifulSoup(response.data, "html.parser")

    def get_image(self, image):
        return self.http.request(url=image, headers=self.header, method='GET')

    def normalize_query(self, query):
        query = query.split()
        return '+'.join(query)

    def query(self, query, max_images, save_directory):
        url = "https://www.google.co.in/search?q=" + self.normalize_query(query) + "&source=lnms&tbm=isch"
        soup = self.get_soup(url=url)
        images = []
        for a in soup.find_all("div", {"class": "rg_meta"}):
            link, file_type = json.loads(a.text)["ou"], json.loads(a.text)["ity"]
            images.append((link, file_type))
        for i, (image, file_type) in enumerate(images[0:max_images]):
            try:
                raw_img = self.get_image(image=image).data
                if len(file_type) == 0:
                    file_type = "jpg"
                f = open(os.path.join(save_directory, "img" + "_" + str(i) + "." + file_type), 'wb')
                print("writing " + save_directory + "/img" + "_" + str(i) + "." + file_type)
                f.write(raw_img)
                f.close()
            except Exception as e:
                print("could not load : " + image)
                print(e)


def main():
    parser = argparse.ArgumentParser(description='Scrape Google images')
    parser.add_argument('-s', '--search', type=str, help='search term', required=True)
    parser.add_argument('-n', '--num_images', type=int, help='num images to save', required=True)
    parser.add_argument('-d', '--directory', type=str, help='save directory', required=True)
    args = parser.parse_args()
    query = args.search
    max_images = args.num_images
    save_directory = args.directory

    ScrapeImages(query=query, max_images=max_images, save_directory=save_directory)

    sys.exit()


if __name__ == '__main__':
    main()
