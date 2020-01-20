## Download ImageNet
```bash
git clone https://github.com/orris27/ImageNet-Datasets-Downloader.git
```

Start downloading...
```bash
python downloader.py \
    -data_root /home/orris/datasets/imagenet \
    -number_of_classes 3 \
    -images_per_class 500
```
Or,
```bash
python ./downloader.py \
    -data_root /home/orris/datasets/imagenet \
    -use_class_list True \
    -class_list n09858165 n01539573 n03405111 \
    -images_per_class 500
```

