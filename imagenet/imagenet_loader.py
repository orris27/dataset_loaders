import os

import torch
import torchvision.transforms as transforms
import torchvision.datasets as datasets


def get_imagenet(imagenet_dir, batch_size):

    # Data loading code
    traindir = os.path.join(imagenet_dir, 'train')
    valdir = os.path.join(imagenet_dir, 'val')
    normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                     std=[0.229, 0.224, 0.225])

    train_dataset = datasets.ImageFolder(
        traindir,
        transforms.Compose([
            transforms.RandomResizedCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            normalize,
        ]))


    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=4, pin_memory=True)

    val_loader = torch.utils.data.DataLoader(
        datasets.ImageFolder(valdir, transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            normalize,
        ])),
        batch_size=batch_size, shuffle=False, num_workers=4, pin_memory=True)

    return train_loader, val_loader



if __name__ == '__main__':
    train_loader, val_loader = get_imagenet('/home/orris/datasets/imagenet/imagenet_images', batch_size=16)

    for i, (input, target) in enumerate(train_loader):
        print(input.shape)
        break
