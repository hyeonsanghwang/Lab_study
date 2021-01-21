import cv2
import numpy as np

import torch
import torchvision.datasets as dsets
import torchvision.transforms as transforms


def download_mnist_dataset(path='../mnist_data'):
    dsets.MNIST(root=path, train=True, transform=transforms.ToTensor(), download=True)
    dsets.MNIST(root=path, train=False, transform=transforms.ToTensor(), download=True)


def save_mnist_test_images(mnist_path='../mnist_data', save_path='../mnist_data/test_images/'):
    batch_size = 1
    test_dataset = dsets.MNIST(root=mnist_path, train=False, transform=transforms.ToTensor(), download=False)
    test_loader = torch.utils.data.DataLoader(dataset=test_dataset, batch_size=batch_size, shuffle=False)

    for i, (images, labels) in enumerate(test_loader):
        image = (images.numpy()[0][0]*255).astype(np.uint8)
        cv2.imwrite(save_path+'image%04d.png' % i, image)


if __name__ == '__main__':
    download_mnist_dataset()
    save_mnist_test_images()
