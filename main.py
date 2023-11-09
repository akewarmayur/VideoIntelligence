from sceneDetection.sceneDetection import SceneDetection
from audioEngine.audioPrediction import AudioPrediction
from processing.processingFiles import ProcessFiles
import pandas as pd
import torch
import clip
from imageEngine.processImages import ImageProcessing
from textEngine.video2asr import ASR
from textEngine.textClassification import ZeroShot
import argparse


class VideoAnalysis:

    def __int__(self):
        pass

    def get_model(self):
        model, preprocess = clip.load("ViT-B/32", device="cuda" if torch.cuda.is_available() else "cpu")
        return model, preprocess

    def detect_scenes(self, video_path):
        obj = SceneDetection()
        input_video = video_path
        scenesDF = obj.detect_scenes(input_video, 4, "True")
        return scenesDF

    def detect_audio(self, scene_path):
        obj = AudioPrediction()
        aa, map_list = obj.classify_audio("Scenes/1.mp4")
        audio_specifications = aa
        audio_maps = set(map_list)
        # print("All Audio Specifications", aa)
        # print("Audio Maps", map_list)
        return audio_specifications, audio_maps

    def startAudioEngine(self, scenesDF):
        audioRes = pd.DataFrame(columns=["SceneNumber", "audio_specifications", "audio_maps"])
        scenes_path = scenesDF["Path"].tolist()
        for ee, sc in enumerate(scenes_path):
            audio_specifications, audio_maps = self.detect_audio(sc)
            le = len(audioRes)
            audioRes.loc[le] = [ee + 1, ",".join(audio_specifications), ",".join(audio_maps)]
        return audioRes

    def extract_images(self, scene_path, where2save):
        obj = ProcessFiles()
        list_of_images = obj.extract_frames(where2save, scene_path)
        return list_of_images

    def startImageEngine(self, videoId, scenesDF, threshold, model, preprocess):
        imageResults = pd.DataFrame(columns=["SceneNumber", "image_name", "settings1", "settings2", "settings3",
                                             "objects",
                                             "people count",
                                             "activities_content"])
        objIP = ImageProcessing()
        allSceneFrames = []
        list_of_scenes = scenesDF["SceneNumber"].tolist()
        scenes_path = scenesDF["Path"].tolist()
        obj = ProcessFiles()
        scenesFramesPath = obj.createFolders(videoId, list_of_scenes)
        for j, sc in enumerate(scenes_path):
            list_of_frames = self.extract_images(sc, scenesFramesPath[j])
            allSceneFrames.append(list_of_frames)
        for ii, list_of_images in enumerate(allSceneFrames):
            df = objIP.start_process(list_of_images, threshold, model, preprocess)
            for ind, row in df.iterrows():
                le = len(imageResults)
                imageResults.loc[le] = [ii + 1, row["image_name"], row["settings1"], row["settings2"],
                                        row["settings3"],
                                        row["objects"],
                                        row["people count"],
                                        row["activities_content"]]
        return imageResults

    def startTextEngine(self, scenesDF, threshold):
        textResults = pd.DataFrame(columns=["SceneNumber", "StartTime", "EndTime", "Class"])
        obj = ASR()
        objT = ZeroShot()
        scenes_path = scenesDF["Path"].tolist()
        for ee, sc in enumerate(scenes_path):
            df = obj.video2srt(sc)
            tr = objT.get_scene_text_attributes(df, threshold)
            for ind, row in tr.iterrows():
                le = len(textResults)
                textResults.loc[le] = [ee + 1, row["StartTime"], row["EndTime"], row["Class"]]
        return textResults

    def sav_csv(self, what2save, videoId, name):
        what2save.to_csv("output/" + videoId + "/" + str(name) + ".csv")

    def startProcess(self, videoId, video_path, imageThreshold, textThreshold):
        model, preprocess = self.get_model()
        scenesDF = self.detect_scenes(video_path)
        scenesDF = pd.read_csv("Scenes/scenes.csv")
        # Image Engine
        imageResults = self.startImageEngine(videoId, scenesDF, imageThreshold, model, preprocess)
        self.sav_csv(imageResults, videoId, "imageResults")
        # Text Engine
        textResults = self.startTextEngine(scenesDF, textThreshold)
        self.sav_csv(textResults, videoId, "textResults")
        # # Audio Engine
        audioResults = self.startAudioEngine(scenesDF)
        self.sav_csv(audioResults, videoId, "aduioResults")


        self.sav_csv(scenesDF, videoId, "scenes")


if __name__ == '__main__':
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('--video_path', action='store', type=str, required=True)
    my_parser.add_argument('--videoId', action='store', type=str, required=True)
    my_parser.add_argument('--imageThreshold', action='store', type=int, required=True)
    my_parser.add_argument('--textThreshold', action='store', type=int, required=True)
    args = my_parser.parse_args()
    video_path = args.video_path
    videoId = args.videoId
    imageThreshold = args.imageThreshold
    textThreshold = args.textThreshold
    obj = VideoAnalysis()
    obj.startProcess(videoId, video_path, imageThreshold, textThreshold)
