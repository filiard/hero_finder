from PIL import Image
import numpy as np
import glob
import pytesseract

models = []


def extract_miniatures(im):
    im = Image.open(r"test3.jpg")
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
            extracted_miniatures.append(np.asarray(im_crop))
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
    return extracted_miniatures


def import_models():
    for filename in glob.glob('mini_models/*.jpg'):
        img = Image.open(filename)
        # img = img.resize((40, 40),Image.BICUBIC).convert('LA')
        img = img.resize((40, 40), Image.BICUBIC)
        models.append(np.asarray(img))
    return models


def mse(imageA, imageB):
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err


def get_concat_h(im1, im2):
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst


def find_best_match(extracted):
    differences = []
    for model in models:
        diff = mse(model, extracted)
        differences.append(diff)

    best_match = np.argmin(differences)
    return best_match

def read_heroes_text():
    left_position = 562
    top_position = 320
    end_left = left_position + 800
    end_top = top_position + 25
    image = Image.open(r"test3.jpg").convert('LA').crop((left_position, top_position, end_left, end_top))
    text = pytesseract.image_to_string(image)
    print(text)
