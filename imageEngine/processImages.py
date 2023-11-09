from helperFunctions.imageHelper import ImageHelper
import imageEngine.imagePrompts as prompts
import imageEngine.listofObjects as objects
import pandas as pd
import re


class ImageProcessing:

    def __int__(self):
        pass

    def process_predictions(self, list_of_images, prompts, threshold, model, preprocess):
        objHelp = ImageHelper()
        results = {}
        batch_predictions = objHelp.get_clip_prediction_in_batch(list_of_images, list(prompts.keys()), 3, model,
                                                                 preprocess)
        for key, Highest3Predictions in batch_predictions.items():
            try:
                c1 = Highest3Predictions[0][0]
                s1 = 100 * Highest3Predictions[0][1]
                if s1 >= threshold:
                    results[key] = prompts[c1]
                else:
                    results[key] = "others"
            except Exception as e:
                print(e)
        return results

    def objects_analysis(self, list_of_images, threshold, model, preprocess):
        objHelp = ImageHelper()
        results = {}
        batch_predictions = objHelp.get_clip_prediction_in_batch(list_of_images, objects.objects, 3, model,
                                                                 preprocess)
        for key, Highest3Predictions in batch_predictions.items():
            try:
                c1 = Highest3Predictions[0][0]
                s1 = 100 * Highest3Predictions[0][1]
                if s1 >= threshold:
                    results[key] = c1
                else:
                    results[key] = "others"
            except Exception as e:
                print(e)
        return results

    def process_predictionsDF(self, aa, prompts, threshold, model, preprocess):
        objHelp = ImageHelper()
        results = {}
        # aa = {11: ['a', 'b', 'c'], 22: ['r'], 33: ['x'], 44: ['pp', 'qq']}
        for k, v in aa.items():
            batch_predictions = objHelp.get_clip_prediction_in_batch(v, list(prompts.keys()), 3, model,
                                                                     preprocess)
            ss = []
            for key, Highest3Predictions in batch_predictions.items():
                try:
                    c1 = Highest3Predictions[0][0]
                    s1 = 100 * Highest3Predictions[0][1]
                    if s1 >= threshold:
                        ss.append(prompts[c1])
                    else:
                        ss.append("others")
                except Exception as e:
                    print(e)
            results[k] = ",".join(ss)
        return results

    def process_predictionsObjects(self, aa, model, preprocess, pr):
        objHelp = ImageHelper()
        ObjectResults = {}
        ObjectCountResults = {}
        # aa = {11: ['a', 'b', 'c'], 22: ['r'], 33: ['x'], 44: ['pp', 'qq']}
        prompts = ["a photo of " + str(i) for i in pr]
        for k, v in aa.items():
            batch_predictions = objHelp.get_clip_prediction_in_batch(v, prompts, 3, model,
                                                                     preprocess)
            ss = []
            for key, Highest3Predictions in batch_predictions.items():
                try:
                    c1 = Highest3Predictions[0][0]
                    msc1 = Highest3Predictions[0][0]
                    s1 = 100 * Highest3Predictions[0][1]
                    if s1 >= 70:
                        ss.append(c1)
                    else:
                        ss.append("others")
                except Exception as e:
                    print(e)
            my_list = [x for x in ss if x != "others"]
            zz = (list(set(my_list)))
            if len(zz) != 0:
                ObjectResults[k] = ",".join(zz)
                ObjectCountResults[k] = len(zz)
            else:
                ObjectResults[k] = "others"
                ObjectCountResults[k] = 0
        return ObjectResults, ObjectCountResults

    def settings(self, list_of_images, threshold, model, preprocess):
        # settings 1 [bar, bedroom]
        s1Prompts = prompts.settings1
        # settings 2 [lighting]
        s2Prompts = prompts.settings2
        # settings 3 [angle]
        s3Prompts = prompts.settings3

        s1Results = self.process_predictions(list_of_images, s1Prompts, threshold, model, preprocess)
        s2Results = self.process_predictions(list_of_images, s2Prompts, threshold, model, preprocess)
        s3Results = self.process_predictions(list_of_images, s3Prompts, threshold, model, preprocess)
        return s1Results, s2Results, s3Results

    def activities_content(self, list_of_images, threshold, model, preprocess):
        results = self.process_predictions(list_of_images, prompts.activities_content, threshold, model,
                                           preprocess)
        return results

    def people_count(self, list_of_images, threshold, model, preprocess):
        results = self.process_predictions(list_of_images, prompts.people_count, threshold, model,
                                           preprocess)
        return results

    def atoi(self, text):
        return int(text) if text.isdigit() else text

    def natural_keys(self, text):
        return [self.atoi(c) for c in re.split(r'(\d+)', text)]

    def start_process(self, list_of_images, threshold, model, preprocess):
        res = pd.DataFrame(columns=["image_name", "settings1", "settings2", "settings3",
                                    "objects",
                                    "people count",
                                    "activities_content"])
        print(list_of_images)
        s1Results, s2Results, s3Results = self.settings(list_of_images, threshold, model, preprocess)
        activities_content_results = self.activities_content(list_of_images, threshold, model, preprocess)
        people_count_results = self.people_count(list_of_images, threshold, model, preprocess)
        object_results = self.objects_analysis(list_of_images, threshold, model, preprocess)
        for k, v in s1Results.items():
            try:
                le = len(res)
                res.loc[le] = [k, v, s2Results[k], s3Results[k],
                               object_results[k],
                               people_count_results[k],
                               activities_content_results[k]]


            except:
                pass

        return res
