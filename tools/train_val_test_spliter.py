import random
import os
import pandas as pd
from tools.settings import *
'''
    This script will save 3 files: train.txt, val.txt, test.txt.
    each file has the following format:
    --------------------------------------------------------------
    PathFile <Tab> actionName
    ex:
        data/video/video_1	slap
        data/video/video_2	punch
        data/video/video_2	kick

	--------------------------------------------------------------
'''
punch_path = punch_path
kick_path = kick_path

def accumulate_videos(videos_path):
    videos = os.listdir(videos_path)
    videos_path_list = []
    for video in videos:
        videos_path_list.append(videos_path + video)
    return videos_path_list

def append_label(videos_path, action):
    data_with_label = []
    for video_path in videos_path:
        data_with_label.append([video_path, action])
    return data_with_label

def split_train_val_test_data(videos):
    random.shuffle(videos)
    number_of_total_data = len(videos)
    number_of_test_videos = int(number_of_total_data * test_dataset_ratio)
    number_of_val_videos = int(number_of_total_data * val_dataset_ratio)

    list_of_test_videos = videos[ : number_of_test_videos]
    list_of_val_videos = videos[number_of_test_videos : (number_of_test_videos+number_of_val_videos)]
    list_of_train_videos = videos[(number_of_test_videos+number_of_val_videos) : ]
    return list_of_train_videos, list_of_val_videos, list_of_test_videos

def split():
    print("Splitting the ginen dataset into Train Test={0} Validation={1}".format(test_dataset_ratio, val_dataset_ratio))
    #Preparing Dataset List
    #slap
    slap_videos = accumulate_videos(slap_path)
    slap_videos = append_label(slap_videos, "slap")
    train_slap_videos, val_slap_videos, test_slap_videos = split_train_val_test_data(slap_videos)
    #punch
    punch_videos = accumulate_videos(punch_path)
    punch_videos = append_label(punch_videos, "punch")
    train_punch_videos, val_punch_videos, test_punch_videos = split_train_val_test_data(punch_videos)
    #kick
    kick_videos = accumulate_videos(kick_path)
    kick_videos = append_label(kick_videos, "kick")
    train_kick_videos, val_kick_videos, test_kick_videos = split_train_val_test_data(kick_videos)

    #Preparing Dataset
    train_data_list = train_slap_videos + train_punch_videos + train_kick_videos
    random.shuffle(train_data_list)
    train = pd.DataFrame(train_data_list, columns = ['Video_url', 'action'])
    train.to_csv(os.path.join(dataset_path, 'train.csv'), index=False)

    val_data_list = val_slap_videos + val_punch_videos + val_kick_videos
    random.shuffle(val_data_list)
    val = pd.DataFrame(val_data_list, columns = ['Video_url', 'action'])
    val.to_csv(os.path.join(dataset_path, 'val.csv'), index=False)

    test_data_list = test_slap_videos + test_punch_videos + test_kick_videos
    random.shuffle(test_data_list)
    test = pd.DataFrame(test_data_list, columns = ['Video_url', 'action'])
    test.to_csv(os.path.join(dataset_path, 'test.csv'), index=False)
    print("Done")
