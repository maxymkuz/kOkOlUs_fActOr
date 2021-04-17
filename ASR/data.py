import os
import os
import pytube
import re
import string
import json
from urllib.parse import urlparse, parse_qs
import main


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


def get_video(url):
    youtube = pytube.YouTube(url)
    video = youtube.streams.first()
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    title = regex.sub('', video.title)
    ids = extract_video_id(url)
    video.download(f'tmp', filename=title)
    print(title)
    src = 'tmp/' + title + '.mp4'
    result_asr, timestamp_asr = main.get_asr_data(src)
    os.remove(src)
    return {
        'title': title,
        'path': url,
        'words_lst': result_asr,
        'timestamp_lst': timestamp_asr
    }, ids


if __name__ == "__main__":
    videos = [
    'https://www.youtube.com/watch?v=Z3Wvw6BivVI',
    'https://www.youtube.com/watch?v=Yocja_N5s1I&t=1s',
    'https://www.youtube.com/watch?v=TG55ErfdaeY',
    'https://www.youtube.com/watch?v=KTB_OFoAQcc',
    'https://www.youtube.com/watch?v=spUNpyF58BY',
    'https://www.youtube.com/watch?v=K3odScka55A',
    'https://www.youtube.com/watch?v=wEoyxE0GP2M&t=2s',
    'https://www.youtube.com/watch?v=LFKZLXVO-Dg',
    'https://www.youtube.com/watch?v=Uj3_KqkI9Zo',
    'https://www.youtube.com/watch?v=V0CdS128-q4',
    'https://www.youtube.com/watch?v=vplFSx4WVeg',
    'https://www.youtube.com/watch?v=eNkvmj_SWTk',
    'https://www.youtube.com/watch?v=T98PIp4omUA',
    'https://www.youtube.com/watch?v=ktWL3nN38ZA',
    'https://www.youtube.com/watch?v=RT-hUXUWQ2I',
    'https://www.youtube.com/watch?v=AI6Ccfno6Pk',
    'https://www.youtube.com/watch?v=aCPkszeKRa4',
]
    ans = {}
    for i in range(len(videos)):
        dct, idx = get_video(videos[i])
        ans[idx] = dct
        if not os.path.exists("jsons"):
            os.mkdir("jsons")
        with open(f'jsons/final.json', 'w') as f:
            json.dump(ans, f, indent=4)