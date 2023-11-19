from typing import List, Tuple

import glob
import os

import torch
from torch.utils.data import Dataset
from torchvision import transforms
from PIL import Image

preprocess_image = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
])


class AslDataset(Dataset):
    classes: List[str]
    data: List[Tuple[int, str]]

    def __init__(self, root: str):
        self.classes = [os.path.basename(p) for p in glob.iglob(f"{root}/*")]

        self.data = []
        for i, class_ in enumerate(self.classes):
            items = glob.glob(f"{root}/{class_}/*.jpg")
            self.data += [(i, item) for item in items]

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        label, path = self.data[idx]
        with Image.open(path) as im:
            pixels = preprocess_image(im)

        return {"label": label, "image": pixels}


class AslTestDataset(Dataset):
    data: List[Tuple[int, str]]

    def __init__(self, root: str, classes: List[str]):
        self.data = []
        for path in glob.iglob(f"{root}/*.jpg"):
            name = os.path.basename(path)
            name = name.replace("_test.jpg", "")
            class_ = classes.index(name)
            class_ = torch.tensor(class_)

            self.data.append((class_, path))

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        label, path = self.data[idx]
        with Image.open(path) as im:
            pixels = preprocess_image(im)

        return {"label": label, "image": pixels}
