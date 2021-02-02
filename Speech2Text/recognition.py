import os
import ffmpeg
from threading import Thread
import time
import shutil
import numpy as np
from vosk import Model, KaldiRecognizer, SetLogLevel
import wave
import json
from pathlib import Path

def get_length_audio(audio):
	length = ffmpeg.probe(audio)['format']['duration']
	return float(length)


def cutting_original_audio(audio, cut_dir, split_size=60*3):
	length = get_length_audio(audio)
	nums = round(length/split_size)

	new_audio_file = []
	for i in range(nums):
		new_audio_file.append(os.path.join(cut_dir, f'cut-{i}.wav'))
		os.system(f'ffmpeg -ss {i*split_size} -t {split_size} -i {audio} -ab 256k {new_audio_file[i]}')

	return new_audio_file

def read_wave(wf, rec):
	ans = ""
	while True:
	    data = wf.readframes(10000)
	    if len(data) == 0:
	        break
	    if rec.AcceptWaveform(data):
	        json_dump = json.loads(rec.Result())
	        tmp = json_dump['text']
	        tmp = tmp.capitalize()
	        ans += tmp
	        ans += '. '

	return ans

def save_file(result, file):
	with open(file,"w") as f:
	    f.write(result)


class SpeechToText(Thread):
    def __init__(self, number, audio_name, txt_dir):
        """Инициализация потока"""
        Thread.__init__(self)
        self.number = number
        self.audio_name = audio_name
        self.txt_dir = txt_dir

    def run(self):
        """Запуск потока"""
        print(f'start reading {self.audio_name}')
        start_time = time.time()

        wf = wave.open(self.audio_name, 'rb')
        rec = KaldiRecognizer(model, wf.getframerate())
        audio_rec = read_wave(wf, rec)

        txt_file = os.path.join(self.txt_dir, f'{self.number}.txt')
        result = '{}'.format(audio_rec)
        save_file(result, txt_file)

        os.remove(self.audio_name)
        print("--- {} seconds ---".format(time.time() - start_time))
        print(f"/nЗакончил считывание {self.audio_name}/n")


def main(audio_files, txt_dir):
    threads = []
    for num, audio_name in enumerate(audio_files):
        threads.append(SpeechToText(num, audio_name, txt_dir))
        threads[num].start()
    return threads


def run(audio_file, model_choice):

    if not os.path.exists(model_choice):
        print ("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
        exit (1)

    global model
    model = Model(model_choice)

    cut_dir = 'cut_dir'
    txt_dir = 'txt'

    if os.path.isdir(cut_dir):
        shutil.rmtree(cut_dir)
    if os.path.isdir(txt_dir):
        shutil.rmtree(txt_dir)
    os.mkdir(cut_dir)
    os.mkdir(txt_dir)



    print(audio_file)

    new_audio_files = cutting_original_audio(audio_file, cut_dir)

    threads = main(new_audio_files, txt_dir)
    for thr in threads:
    	thr.join()
