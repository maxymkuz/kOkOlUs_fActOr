import os
from ocr.ocr import OCR_Saver
import os
import pytube


def get_data(src, language=['en']):
    ocr = OCR_Saver(language)
    result_ocr, timestamp_ocr = ocr(src,to_print=True)
    return result_ocr, timestamp_ocr, None, None


def get_video(url):
    youtube = pytube.YouTube(url)
    video = youtube.streams.first()
    print(video.title)
    video.download('tmp/')
    title = video.title
    src = 'tmp/' + title + '.mp4'
    result_ocr, timestamp_ocr, result_asr, timestamp_asr = get_data(src)
    os.remove(src)


get_video('https://www.youtube.com/watch?v=gK_7pr_t-Hk')
