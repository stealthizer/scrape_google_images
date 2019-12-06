# Scrape Google Images 

Python script derived from https://gist.github.com/genekogan/ebd77196e4bf0705db51f86431099e57 that scrapes google images a defined number of images that match the requested query, stored on the chosen folder

```
$ virtualenv --python=python3 venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
```

Usage:

```
(venv)$  python3 scrapeimages.py -s name_to_scrape -n number_of_images_to_retrieve -d /path_to_download 
```