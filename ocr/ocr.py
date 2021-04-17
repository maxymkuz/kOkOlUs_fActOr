import cv2
import os
from decord import VideoReader
from decord import cpu, gpu
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
