import os
from ocr.ocr import OCR_Saver
import os
import pytube
import re
import string
def get_data(src, language=['en']):
    ocr = OCR_Saver(language)
    result_ocr, timestamp_ocr = ocr(src, to_print=True)
    return result_ocr, timestamp_ocr, [], []


def get_video(url):
    youtube = pytube.YouTube(url)
    video = youtube.streams.first()
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    title = regex.sub('',video.title.replace(' ', ''))
    video.download(f'tmp',filename=title)
    print(title)
    src = 'tmp/' + title + '.mp4'
    result_ocr, timestamp_ocr, result_asr, timestamp_asr = get_data(src)
    os.remove(src)
    return [{
        'title': title,
        'path': url,
        'words_lst': result_ocr,
        'timestamp_lst': timestamp_ocr
    }, {
        'title': title,
        'path': url,
        'words_lst': result_asr,
        'timestamp_lst': timestamp_asr
    }]


get_video('https://www.youtube.com/watch?v=Ilg3gGewQ5U')
