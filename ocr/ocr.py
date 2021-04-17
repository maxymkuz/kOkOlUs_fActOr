import cv2
import os
from decord import VideoReader
from decord import cpu, gpu
<<<<<<< HEAD
import easyocr

reader = easyocr.Reader(['en'])
video = VideoReader("vim.mp4")
print(len(video))
current_frame = 0
fps = int(round(video.get_avg_fps()))
q = 0
text = open('text.txt', 'w')
time = open('time.txt', 'w')

for current_frame in range(0, len(video), 5 * fps):
    if current_frame % (len(video) // 100) < 5 * fps:
        print(str(q) + '%', current_frame)
        q += 1
    image = video[current_frame].asnumpy()
    name = 'tmp/' + str(current_frame) + '.jpg'
    cv2.imwrite(name, image)
    result = [[x[1], x[2]] for x in reader.readtext(f'{name}')]
    result = list(filter(lambda x: x[1] > 0.5, result))
    for i in result:
        for x in i[0].split():
            text.write(x + '\n')
            time.write(str(current_frame // fps) + '\n')
    os.remove(name)

text.close()
time.close()
=======
from kornia.losses import ssim_loss
import easyocr
import numpy as np
import torch

'''
class OCR_Saver:
    def __init__(self):
        self.reader = easyocr.Reader(['en'])

    def __call__(self, video_src):
        video = VideoReader(video_src)
        print(len(video))
        current_frame = 0
        fps = int(round(video.get_avg_fps()))
        q = 0
        text = []
        time = []
        prev_image = 0
        for current_frame in range(0, len(video), 5 * fps):
            if current_frame % (len(video) // 100) < 5 * fps:
                print(str(q) + '%', current_frame)
                q += 1
            image = video[current_frame].asnumpy()
            if current_frame > 0:
                print(ssim_loss(torch.tensor(np.transpose(image)[np.newaxis, :, :, :]).type(torch.FloatTensor), prev_image,
                           window_size=11))
                print(image.shape, prev_image.shape)
            name = 'tmp/' + str(current_frame) + '.jpg'
            cv2.imwrite(name, image)
            result = [[x[1], x[2]] for x in self.reader.readtext(f'{name}')]
            result = list(filter(lambda x: x[1] > 0.5, result))
            for i in result:
                for x in i[0].split():
                    text.append(x)
                    time.append(current_frame // fps)
            os.remove(name)
            prev_image = torch.tensor(np.transpose(image)[np.newaxis, :, :, :].copy()).type(torch.FloatTensor)
'''


class OCR_Saver:
    def __init__(self, languages=["en"]):
        self.reader = easyocr.Reader(languages)

    def __call__(self, video_src, miss_frames=True,to_print=False):
        video = cv2.VideoCapture(video_src)
        fps = round(video.get(cv2.CAP_PROP_FPS))
        q = 0
        text = []
        time = []
        prev_image = 0
        current_frame = 0
        length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        while True:
            success, image = video.read()
            if not success:
                break
            if current_frame % (5 * fps) != 0:
                current_frame += 1
                continue
            current_frame += 1
            if to_print and current_frame % (length // 100) < 5 * fps:
                print(str(q) + '%', current_frame)
                q += 1
            if miss_frames and current_frame > fps:
                if ssim_loss(torch.tensor(np.transpose(image)[np.newaxis, :, :, :]).type(torch.FloatTensor),
                             prev_image,
                             window_size=11) < 0.05:
                    print("Miss")
                    continue
            name = 'tmp/' + str(current_frame) + '.jpg'
            cv2.imwrite(name, image)
            result = [[x[1], x[2]] for x in self.reader.readtext(f'{name}', paragraph=False)]
            result = list(filter(lambda x: x[1] > 0.5, result))
            for i in result:
                for x in i[0].split():
                    text.append(x)
                    time.append(current_frame // fps)
            os.remove(name)
            prev_image = torch.tensor(np.transpose(image)[np.newaxis, :, :, :].copy()).type(torch.FloatTensor)
        return text, time


ocr = OCR_Saver()
ocr('/home/fedynyak/hack/lecture_test.mp4')
>>>>>>> 6750bcb975886809da830e0e58a13700eb53d549
