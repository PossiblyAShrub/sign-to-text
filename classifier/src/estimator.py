import pickle
from PIL import Image

import torch
import torch.nn.functional as F

from dataloader import preprocess_image

class Model:
    def __init__(self, path: str):
        with open(path, "rb") as f:
            image_net, model, classes = pickle.load(f)

        image_net.eval()
        model.eval()

        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        image_net.to(self.device)
        model.to(self.device)

        self.image_net = image_net
        self.classes = classes
        self.model = model

    def check(self, image: Image) -> str:
        pixels = preprocess_image(image).to(torch.float).unsqueeze(0).to(self.device)

        emb = self.model(self.image_net(pixels))
        est = F.softmax(emb, dim=-1).argmax().to("cpu")

        return self.classes[est]
