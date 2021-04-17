import os
from ocr.ocr import OCR_Saver
import os
import pytube
import re
import string
import json
from urllib.parse import urlparse, parse_qs


def extract_video_id(url):
    # Examples:
    # - http://youtu.be/SA2iWivDJiE
    # - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    # - http://www.youtube.com/embed/SA2iWivDJiE
    # - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    query = urlparse(url)
    if query.hostname == 'youtu.be': return query.path[1:]
    if query.hostname in {'www.youtube.com', 'youtube.com'}:
        if query.path == '/watch': return parse_qs(query.query)['v'][0]
        if query.path[:7] == '/watch/': return query.path.split('/')[1]
        if query.path[:7] == '/embed/': return query.path.split('/')[2]
        if query.path[:3] == '/v/': return query.path.split('/')[2]
        # below is optional for playlists
        if query.path[:9] == '/playlist': return parse_qs(query.query)['list'][0]
   # returns None for invalid YouTube url


def get_data(src, language=['en']):
    ocr = OCR_Saver(language)
    result_ocr, timestamp_ocr = ocr(src, to_print=True)
    return result_ocr, timestamp_ocr


def get_video(url, save_folder='jsons/'):
    youtube = pytube.YouTube(url)
    video = youtube.streams.first()
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    title = regex.sub('', video.title)
    ids = extract_video_id(url)
    video.download(f'tmp', filename=title)
    print(title)
    src = 'tmp/' + title + '.mp4'
    result_ocr, timestamp_ocr = get_data(src)
    os.remove(src)
    return {
        'id': ids,
        'title': title,
        'path': url,
        'words_lst': result_ocr,
        'timestamp_lst': timestamp_ocr
    }


videos = [
    'https://www.youtube.com/watch?v=Z3Wvw6BivVI',
]
for i in range(len(videos)):
    dct = get_video(videos[i])
    with open(f'jsons/{i}.json', 'w') as f:
        json.dump(dct, f)
