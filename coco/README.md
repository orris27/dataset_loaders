## How to use
Reference: [this](https://github.com/yunjey/pytorch-tutorial/tree/master/tutorials/03-advanced/image_captioning)
```
# Install pycoco
git clone https://github.com/pdollar/coco.git
cd coco/PythonAPI/
make
python setup.py build
python setup.py install

# Prepare data
chmod +x download.sh
./download.sh

# Buil vocabulary & resize the image to fit ResNet
python build_vocab.py # build Vocabulary object which contains idx2word and word2idx
python resize.py # resize the images to 224x224 for ResNet
```


## Demo
See [demo.ipynb](./demo.ipynb)
