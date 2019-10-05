#! /bin/python
# author mcncm 2019

import os
import sys
import argparse
import json
import requests
import shutil
import tkinter as tk

import filemapping

API_NAME = 'unsplash'  # other possibilities: imgur, flickr,...
BG_CACHE_SIZE = 5
LOAD_BAR_LEN = 36

parser = argparse.ArgumentParser()
parser.add_argument('bg_dir', nargs=1)
parser.add_argument('-s', '--search', type=str, default=None)  # not quite there yet
parser.add_argument('-f', '--featured', action='store_true',
    help='only use featured images from web api')

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


def display_dimensions():
    tk_root = tk.Tk()
    width = tk_root.winfo_screenwidth()
    height = tk_root.winfo_screenheight()
    tk_root.destroy()

    return (width, height)


if __name__ == '__main__':
    args = parser.parse_args()
    try:
        bg_dir = args.bg_dir[0]
    except:
        print('No wallpaper directory given')

    width, height = display_dimensions()

    script_dir = os.path.dirname(sys.argv[0])
    secrets = filemapping.FileMapping(
                os.path.join(script_dir, 'secrets.txt'))

    queries = {
        'client_id': secrets['UNSPLASH_ACCESS_KEY'],
        'orientation': 'landscape',
    }

    # only return featured images
    if args.featured:
        queries['featured'] = True

    # include search terms
    if args.search:
        queries['query'] = args.search


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
