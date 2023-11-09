# import pandas as pd
#
# scene = pd.read_csv("scenes.csv")
# i1 = pd.read_csv("imageDf1.csv")
# i2 = pd.read_csv("imageDf2.csv")
# imageList = [i1, i2]
# t1 = pd.read_csv("text1.csv")
# t2 = pd.read_csv("text2.csv")
# textList = [t1, t2]
# audio = [["xx", "yy"], ["uu"]]
# print(scene.columns)
# print(i1.columns)
# print(t1.columns)
# sceneLists = scene["SceneNumber"].tolist()
# results = pd.Dataframe(columns=["SceneNumber", "StartTime (TimeStamp)", 'EndTime (Seconds)',
#                                 'image_name', 'settings1', 'settings2', 'settings3', 'objects',
#                                 'people count', 'activities_content',
#                                 'TextStartTime', 'TextEndTime', 'TextClass',
#                                 "audioClass"
#                                 ])
#
#
# for i, j in enumerate(sceneLists):
#     # scene
#     st = scene.loc[scene['SceneNumber'] == j, 'StartTime (TimeStamp)'].values[0]
#     et = scene.loc[scene['SceneNumber'] == j, 'EndTime (TimeStamp)'].values[0]
#     # image
#     temp = imageList[i]
#     for ind, row in temp.iterrows():
#
#
#
