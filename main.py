import glob
import ctypes
import numpy as np
from mss import mss
from PIL import Image
import numpy

mss().shot()

im = Image.open(r"test2.jpg")
portrait_x, portrait_y = 40, 40
width, height = im.size
left_position = 554
top_position = 368
end_left = left_position + 40
end_top = top_position + 40
im2 = im.crop((left_position, top_position, end_left, end_top))
# im2.show()

# extract miniatures from screenshot#
extracted_miniatures = []
for y in range(6):
    for x in range(16):
        im_crop = im.crop((left_position, top_position, end_left, end_top))
        # change to numpy arrays #
        # extracted_miniatures.append(numpy.asarray(im_crop.convert('LA'))[:,:,0])
        extracted_miniatures.append(numpy.asarray(im_crop))
        # name = "mini"+str(y)+str(x)+".jpg"
        # im_crop.save(name)
        left_position += 50
        end_left += 50
    left_position = 554
    end_left = left_position + 40
    top_position += 50
    end_top += 50
# Image.fromarray(extracted_miniatures[0]).show()
print("dupa")

# import model miniatures #
basewidth = 40
bg_colour = (0, 0, 0)
models = []
for filename in glob.glob('mini2/*.jpg'):
    img = Image.open(filename)
    # img = img.resize((40, 40),Image.BICUBIC).convert('LA')
    img = img.resize((40, 40), Image.BICUBIC)
    models.append(numpy.asarray(img))#[:, :, :3]

# Image.fromarray(models[0]).show()

cent1 = models[0]
cent11 = cent1.astype(numpy.int16)
cent2 = extracted_miniatures[48]
cent22 = cent2.astype(numpy.int16)

res = numpy.abs(numpy.subtract(cent11, cent22))
res2=np.sum(res)
# Image.fromarray(res).imshow()

# print("dupa2")
