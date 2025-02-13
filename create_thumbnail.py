import torch
import torchvision.models
import torchvision.transforms as transforms
from PIL import Image
import os
import random as r
from config import MODELPATH


class ThumbnailMaker:
    def __init__(self):
        self.topnImages = []
        self.model = self.prepare_model()
    
    def prepare_image(self, image):
        if image.mode != 'RGB':
            image = image.convert("RGB")
        Transform = transforms.Compose([  
                transforms.Resize(256),   
                transforms.ToTensor(),
                ])
        image = Transform(image)   
        image = image.unsqueeze(0)
        return image

    def prepare_model(self):
        model = torchvision.models.resnet50()
        model.avgpool = torch.nn.AdaptiveAvgPool2d(1)
        model.fc = torch.nn.Linear(in_features=2048, out_features=1)
        model.load_state_dict(torch.load(MODELPATH, map_location=torch.device('cpu'))) 
        return model.eval()

    def predict(self, image):
        image = self.prepare_image(image)
        with torch.no_grad():
            preds = self.model(image)
        score = preds.detach().numpy().item()
        return score

    def make_thumbnail(self):
        self.topnImages.sort(key=lambda x: self.predict(x), reverse=True)

        extras = []
        for filename in os.listdir("./assets"):
            if filename.endswith(".png"):
                extras.append(Image.open("./assets/stickers/" + filename))

        im1, im2, im3 = self.topnImages[:3]
        dst = Image.new('RGB', (im1.width + im2.width + im3.width, max(im1.height, im2.height, im3.height)), (255, 255, 255))
        dst.paste(im1, (0, 0))
        dst.paste(im2, (im1.width, 0))
        dst.paste(im3, (im1.width + im2.width, 0))

        for img in extras:
            w, h = int(img.width/2), int(img.height/2)
            dst.paste(img, (r.randrange(w, dst.width-w), r.randrange(h, dst.height-h)))
        
        return dst

    def compare_topn(self, clip):
        clipframes = []
        for i in range(int(clip.duration)):
            clipframes.append(Image.fromarray(clip.get_frame(i)))
        clipframes.sort(key=lambda x: self.predict(x), reverse=True)
        self.topnImages.append(clipframes[0])
