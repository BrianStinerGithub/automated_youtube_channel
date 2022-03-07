from cv2 import imshow
import torch
import torchvision.models
import torchvision.transforms as transforms
from PIL import Image


class ThumbnailMaker:
    def __init__(self):
        self.topnimages = []
        self.num_topn = 3
        self.model = self.prepare_model()
    
    def prepare_image(self, image):
        if image.mode != 'RGB':
            image = image.convert("RGB")
        Transform = transforms.Compose([
                transforms.Resize([224,224]),      
                transforms.ToTensor(),
                ])
        image = Transform(image)   
        image = image.unsqueeze(0)
        return image

    def predict(self, image):
        image = self.prepare_image(image)
        with torch.no_grad():
            preds = self.model(image)
        score = preds.detach().numpy().item()
        return score

    def prepare_model(self):
        model = torchvision.models.resnet50()
        model.avgpool = torch.nn.AdaptiveAvgPool2d(1) # for any size of the input
        model.fc = torch.nn.Linear(in_features=2048, out_features=1)
        model.load_state_dict(torch.load('model/model-resnet50.pth', map_location=torch.device('cpu'))) 
        return model.eval()
    
    def make_thumbnail(self, resample = Image.BICUBIC):
        top = self.topnimages
        min_height = min(im.height for im in top)
        im_list_resize = [im.resize((int(im.width * min_height / im.height), min_height),resample=resample) for im in top]
        total_width = sum(im.width for im in im_list_resize)
        dst = Image.new('RGB', (total_width, min_height))
        pos_x = 0
        for im in im_list_resize:
            dst.paste(im, (pos_x, 0))
            pos_x += im.width
        dst.save('thumbnail.jpg')

    def compare_topn(self, image):
        top = self.topnimages
        top.append(image)
        top.sort(key=lambda x: self.predict(x), reverse=True)
        if len(top) > self.num_topn:
            top.pop()
        self.topnimages = top
