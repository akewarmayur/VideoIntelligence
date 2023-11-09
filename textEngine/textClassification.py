from transformers import pipeline
from textEngine.textPrompts import prompts
import pandas as pd

class ZeroShot:

    def model(self):
        zero_shot_classifier = pipeline("zero-shot-classification", device="cuda")
        return zero_shot_classifier

    def get_prediction(self, model, sentence, classes):
        # classi, classes, '', feture
        try:
            result = model(sequences=sentence, candidate_labels=classes, multi_label=False)
            predicted_classes = result['labels'][:1]
            predicted_score = result['scores'][:1]
            return predicted_classes[0], predicted_score[0]
        except Exception as e:
            print("Exception in getting prediction:", str(e))
            return "neutral", 0

    def moderationProcess(self, sentence, threshold):
        zero_shot_classifier = self.model()
        try:
            aa = self.get_prediction(zero_shot_classifier, sentence, prompts)
            confidence = aa[1] * 100
            print(aa[0], confidence)
            if confidence >= threshold:
                prediction = aa[0]
            else:
                prediction = "neutral"
        except Exception as e:
            print(e)
            prediction = "neutral"

        return prediction

    def get_scene_text_attributes(self, df, threshold):
        res = pd.DataFrame(columns=["Text", "StartTime", "EndTime", "Class"])
        for ind, row in df.iterrows():
            prediction = self.moderationProcess(row["Text"], threshold)
            le = len(res)
            res.loc[le] = [row["Text"], row["StartTime"], row["EndTime"], prediction]
        return res


