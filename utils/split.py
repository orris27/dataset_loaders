'''
    Given directory named xx, which has a structure of 'xx/cls1/*.jpg, xx/cls2/*.jpg, ..., xx/cls_n/*.jpg',
    Saparate the directory into 'xx/train/cls1/*.jpg, xx/train/cls2/*.jpg, ..., xx/test/cls1/*.jpg, xx/test/cls2/*.jpg'

    Usage:
        python split.py --data_dir /home/orris/datasets/imagenet/imagenet_images/ --test_size 0.25

'''
import os
import shutil
import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--data_dir', type=str, required=True)
parser.add_argument('--test_size', type=float, default=0.25)
args = parser.parse_args()

test_size = args.test_size
data_dir = args.data_dir

os.makedirs(os.path.join(data_dir, 'train'), exist_ok=True)
os.makedirs(os.path.join(data_dir, 'val'), exist_ok=True)

for classname in os.listdir(data_dir):
    if classname in ['train', 'val']:
        continue
    filenames = os.listdir(os.path.join(data_dir, classname))
    if len(filenames) == 0:
        continue
    random.shuffle(filenames)
    split_idx = int(len(filenames) * test_size)
    train_files = filenames[split_idx:] 
    test_files = filenames[:split_idx]
    os.makedirs(os.path.join(data_dir, 'train', classname), exist_ok=True)
    os.makedirs(os.path.join(data_dir, 'val', classname), exist_ok=True)
    for filename in train_files:
        shutil.move(os.path.join(data_dir, classname, filename), os.path.join(data_dir, 'train', classname))
    for filename in test_files:
        shutil.move(os.path.join(data_dir, classname, filename), os.path.join(data_dir, 'val', classname))
    os.rmdir(os.path.join(data_dir, classname))
