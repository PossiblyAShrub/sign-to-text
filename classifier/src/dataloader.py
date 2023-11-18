from typing import List, Tuple

import glob
import os

import torch
from torch.utils.data import Dataset
from PIL import Image

class AslDataset(Dataset):
    classes: List[str]
    data: List[Tuple[str, str]]

    def __init__(self, root: str):
        self.classes = [os.path.basename(p) for p in glob.iglob(f"{root}/*")]

        self.data = []
        for class_ in self.classes:
            items = glob.glob(f"{root}/{class_}/*.jpg")
            self.data += [(class_, item) for item in items]

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        label, path = self.data[idx]
        with Image.open(path) as im:
            pixels = torch.tensor(im.getdata())

        return {"label": label, "image": pixels}
