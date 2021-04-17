#!/home/vova/miniconda3/envs/asr/bin/python

from vosk import Model, KaldiRecognizer, SetLogLevel
import sys
import os
import wave
import json
import glob
import subprocess
import concurrent.futures


def transcribe_vosk_filename(filepath, model):
    model = Model(model)

    wf = wave.open(filepath, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())

    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print ("Audio file must be WAV format mono PCM.")
        exit (1)


    rec.AcceptWaveform(wf.readframes(10**8))
    result = json.loads(rec.FinalResult())

    stamps = [x["start"] for x in result["result"]]
    words = [x["word"] for x in result["result"]]

    return words, stamps


def mp4_to_wav(path, outpath, sample_rate=16000):
    subprocess.call(["ffmpeg", "-i", str(path), "-vn", "-y", "-acodec", "pcm_s16le", "-ar", str(sample_rate), "-ac", "1", str(outpath)])


def get_asr_data(path, thr=12, lang="en"):
    model = f"models/{lang}"
    wav_path = "tmp.wav"

    mp4_to_wav(path, wav_path)
    
    f = wave.open(wav_path)
    l = f.getnframes() / f.getframerate()
    ans = ""
    seq = l // thr + 1

    if not os.path.exists("tmp"):
        os.mkdir("tmp")
    with concurrent.futures.ThreadPoolExecutor(max_workers=24) as executor:
        futures = []
        stamps = []
        text = []
        for i in range(thr):
            subprocess.call(["sox", wav_path, f"tmp/try_{i}.wav", "trim", str(seq * i), str(seq)])
            futures.append(executor.submit(transcribe_vosk_filename, f"tmp/try_{i}.wav", model))
        concurrent.futures.wait(futures)
        for i in range(thr):
            tx, sps = futures[i].result()
            text.extend(tx)
            stamps.extend([x + seq * i for x in sps])

    stamps = [round(x, 2) for x in stamps]

    return text, stamps
