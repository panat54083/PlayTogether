from PIL import Image
import os

# print(os.getcwd())
img_path = '{}/picture/exclamation point2.PNG'.format(os.getcwd())
im1 = Image.open(img_path)
rgb_im = im1.convert('RGB')
rgb_im.save('{}/picture/exclamation point2.jpg'.format(os.getcwd()))
os.remove(img_path)
