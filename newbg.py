#! /bin/python
# author mcncm 2019

import os
import sys
import json
import requests
import shutil
import tkinter as tk

import filemapping

API_NAME = 'unsplash'
BG_CACHE_SIZE = 5
LOAD_BAR_LEN = 36

def issue_request(queries):
    api_url = 'https://api.unsplash.com/photos/random'
    r = requests.get(api_url, params=queries)
    return r.json()

def download_with_bar(url, path):
    """download a resource from `url` and write to `path`, with status bar"""
    r_img = requests.get(url, stream=True)
    try:
        r_len = int((r_img.headers.get('content-length')))
    except Exception as e:
        print('Download failed. Resource has no content-length header.')
        return
    if r_img.status_code == 200:
        with open(img_path, 'wb') as f:
            data_len = 0
            for data in r_img.iter_content(chunk_size=8192):
                data_len += len(data)
                f.write(data)
                frac_done = data_len / r_len
                loading_bar = '=' * round(LOAD_BAR_LEN * frac_done) +\
                              ' ' * round(LOAD_BAR_LEN * (1 - frac_done))
                print(f'Downloading from {API_NAME}: [{loading_bar}]',
                      file=sys.stderr, end=('\r' if data_len < r_len else '\n'))
        print()
    else:
        print(f'Got response {r.status_code} from {API_NAME}', file=sys.err)
    print(img_path)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('No wallpaper directory given')
    bg_dir = sys.argv[1]  # wallpapers

    tk_root = tk.Tk()
    width = tk_root.winfo_screenwidth()
    height = tk_root.winfo_screenheight()
    tk_root.destroy()

    secrets = filemapping.FileMapping('secrets.txt')

    queries = {
        'client_id': secrets['UNSPLASH_ACCESS_KEY'],
        'orientation': 'landscape',
    }

    # {
    #     'w': width,
    #     'h': height,
    #     'fit': 'crop',
    # }

    img_data = issue_request(queries)

    fn = '_'.join(img_data['alt_description'].split()) + '.jpg'
    api_dir = os.path.join(bg_dir, API_NAME)
    if not os.path.isdir(api_dir):
        os.makedirs(api_dir)
    if len(os.listdir(api_dir)) >= BG_CACHE_SIZE:
        # LRU eviction
        paths = map(lambda fn: os.path.join(api_dir, fn), os.listdir(api_dir))
        oldest_bg = min(paths, key=os.path.getctime)
        os.unlink(oldest_bg)

    img_path = os.path.join(api_dir, fn)
    download_with_bar(img_data['links']['download'], img_path)
