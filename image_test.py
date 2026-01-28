# from input.image_loader import *


# img_path = r"C:\Users\dai\Pictures\wallpapers\2950-3840x2160-desktop-4k-resident-evil-village-background-photo.jpg"
# image = load_image(img_path)
# print(image.show())

import torch 
print(torch.cuda.is_available())
print(torch.cuda.get_device_name())