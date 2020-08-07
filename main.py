from mss import mss
from PIL import Image
import functions

im = mss().shot()

extracted_miniatures = functions.extract_miniatures(im)

# import model miniatures #
models = functions.import_models()

hero1 = extracted_miniatures[44]


hero2 = models[functions.find_best_match(hero1)]        #hero2 = predicted hero


#dupa = functions.models[functions.find_best_match(hero1)]
#functions.get_concat_h(Image.fromarray(hero1), Image.fromarray(hero2)).show()

functions.read_heroes_text()







# Image.fromarray(models[0]).show()

# cent1 = models[0]
# cent11 = cent1.astype(np.int16)
# cent2 = miniatures[48]
# cent22 = cent2.astype(np.int16)

# res = np.abs(np.subtract(cent11, cent22))
# res2=np.sum(res)
# Image.fromarray(res).imshow()

# print("dupa2")
