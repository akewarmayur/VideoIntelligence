from time import sleep
import os
import subprocess
import re
import glob
import shutil
import pandas as pd
import datetime


class ProcessFiles:
    def __init__(self):
        pass

    def atoi(self, text):
        return int(text) if text.isdigit() else text

    def natural_keys(self, text):
        return [self.atoi(c) for c in re.split(r'(\d+)', text)]

    def extract_frames(self, framesPath, input_video):
        dir = os.listdir(framesPath)
        if len(dir) == 0:
            print("Empty directory")
            fps = 1
            query = "ffmpeg -i " + input_video + " -pix_fmt rgb24 -vf fps=" + str(
                fps) + " " + framesPath + "img_%06d.png"
            response = subprocess.Popen(query, shell=True, stdout=subprocess.PIPE).stdout.read()
            _ = str(response).encode('utf-8')
        frames = []
        for file in glob.glob(framesPath + '/*'):
            frames.append(file)
        frames.sort(key=self.natural_keys)
        return frames

    def createFolders(self, video_id, scene_list):
        outputPath = os.getcwd() + "/output/" + str(video_id) + "/"
        if not os.path.exists(outputPath):
            os.makedirs(outputPath)
        framesPath = outputPath + "/FramesSavedHere/"

        if not os.path.exists(framesPath):
            os.makedirs(framesPath)
        scenesFramesPath = []
        for i in scene_list:
            sp = framesPath + str(i) + "/"
            scenesFramesPath.append(sp)
            if not os.path.exists(sp):
                os.makedirs(sp)
        return scenesFramesPath

    def convert_video_to_audio_ffmpeg(self, video_file, audio_path):
        """Converts video to audio directly using `ffmpeg` command
        with the help of subprocess module"""
        try:
            query = "ffmpeg -i " + video_file + " -ab 160k -ac 2 -ar 44100 -vn " + audio_path
            response = subprocess.Popen(query, shell=True, stdout=subprocess.PIPE).stdout.read()
            s = str(response).encode('utf-8')

        except Exception as e:
            print(e)
            return str(e)



    def imagesP(self, input_video, imagesPath):
        print("Extracting Images .....................")
        list_of_frames = self.extract_frames(imagesPath, input_video)
        return list_of_frames

    def formatTime(self, tt):
        return tt.split('.')[0]

    def convert(self, seconds):
        seconds = seconds % (24 * 3600)
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        return "%d:%02d:%02d" % (hour, minutes, seconds)

    def frame2Timestamp(self, frame):
        try:
            ss = self.convert(int(frame))
            date_time_obj = datetime.datetime.strptime(ss, '%H:%M:%S')
            return date_time_obj.time()
        except:
            ss = self.convert(int(frame))
            date_time_obj = datetime.datetime.strptime(ss, '%H:%M:%S')
            return date_time_obj.time()

