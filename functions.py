from PIL import Image, ImageDraw, ImageGrab
import numpy as np
import glob
import pytesseract

dict = {'ABADDON': 0, 'ALCHEMIST': 1, 'ANCIENT APPARITION': 2, 'ANTI-MAGE': 3, 'ARC WARDEN': 4, 'AXE': 5, 'BANE': 6, 'BATRIDER': 7, 'BEASTMASTER': 8,
        'BLOODSEEKER': 9, 'BOUNTY HUNTER': 10, 'BREWMASTER': 11, 'BRISTLEBACK': 12, 'BROODMOTHER': 13, 'CENTAUR WARRUNNER': 14, 'CHAOS KNIGHT': 15, 'CHEN': 16,
        'CLINKZ': 17, 'CLOCKWERK': 18, 'CRYSTAL MAIDEN': 19, 'DARK SEER': 20, 'DARK WILLOW': 21, 'DAZZLE': 22, 'DEATH PROPHET': 23, 'DISRUPTOR': 24, 'DOOM': 25,
        'DRAGON KNIGHT': 26, 'DROW RANGER': 27, 'EARTH SPIRIT': 28, 'EARTHSHAKER': 29, 'ELDER TITAN': 30, 'EMBER SPIRIT': 31, 'ENCHANTRESS': 32, 'ENIGMA': 33,
        'FACELESS VOID': 34, 'GRIMSTROKE': 35, 'GYROCOPTER': 36, 'HUSKAR': 37, 'INVOKER': 38, 'IO': 39, 'JAKIRO': 40, 'JUGGERNAUT': 41,
        'KEEPER OF THE LIGHT': 42, 'KUNKKA': 43, 'LEGION COMMANDER': 44, 'LESHRAC': 45, 'LICH': 46, 'LIFESTEALER': 47, 'LINA': 48, 'LION': 49, 'LONE DRUID': 50,
        'LUNA': 51, 'LYCAN': 52, 'MAGNUS': 53, 'MARS': 54, 'MEDUSA': 55, 'MEEPO': 56, 'MIRANA': 57, 'MONKEY KING': 58, 'MORPHLING': 59, 'NAGA SIREN': 60,
        'NATURES PROPHET': 61, 'NECROPHOS': 62, 'NIGHT STALKER': 63, 'NYX ASSASSIN': 64, 'OGRE MAGI': 65, 'OMNIKNIGHT': 66, 'ORACLE': 67,
        'OUTWORLD DEVOURER': 68, 'PANGOLIER': 69, 'PHANTOM ASSASSIN': 70, 'PHANTOM LANCER': 71, 'PHOENIX': 72, 'PUCK': 73, 'PUDGE': 74, 'PUGNA': 75,
        'QUEEN OF PAIN': 76, 'RAZOR': 77, 'RIKI': 78, 'RUBICK': 79, 'SAND KING': 80, 'SHADOW DEMON': 81, 'SHADOW FIEND': 82, 'SHADOW SHAMAN': 83,
        'SILENCER': 84, 'SKYWRATH MAGE': 85, 'SLARDAR': 86, 'SLARK': 87, 'SNAPFIRE': 88, 'SNIPER': 89, 'SPECTRE': 10, 'SPIRIT BREAKER': 91, 'STORM SPIRIT': 92,
        'SVEN': 93, 'TECHIES': 94, 'TEMPLAR ASSASSIN': 95, 'TERRORBLADE': 96, 'TIDEHUNTER': 97, 'TIMBERSAW': 98, 'TINKER': 99, 'TINY': 100,
        'TREANT PROTECTOR': 101, 'TROLL WARLORD': 102, 'TUSK': 103, 'UNDERLORD': 104, 'UNDYING': 105, 'URSA': 106, 'VENGEFUL SPIRIT': 107, 'VENOMANCER': 108,
        'VIPER': 109, 'VISAGE': 110, 'VOID SPIRIT': 111, 'WARLOCK': 112, 'WEAVER': 113, 'WINDRANGER': 114, 'WINTER WYVERN': 115, 'WITCH DOCTOR': 116,
        'WRAITH KING': 117, 'ZEUS': 118}

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
hero_models = []
left_position = 554
top_position = 368
end_left = left_position + 40
end_top = top_position + 40


def extract_miniatures(im, left_position=left_position, top_position=top_position, end_left=end_left, end_top=end_top):
    im = Image.open(im)

    extracted_miniatures = []
    for y in range(6):
        for x in range(16):
            im_crop = im.crop((left_position, top_position, end_left, end_top))

            extracted_miniatures.append(np.asarray(im_crop))

            left_position += 50
            end_left += 50
        left_position = 554
        end_left = left_position + 40
        top_position += 50
        end_top += 50

    return extracted_miniatures


snapshot = ImageGrab.grab()
snapshot.save('monitor-1.jpg')
initial_image = r'monitor-1.jpg'

pics_in_screenshot = extract_miniatures(initial_image)
global source_image
source_image = initial_image


def import_models():
    for filename in glob.glob('mini_models/*.jpg'):
        img = Image.open(filename)
        img = img.resize((40, 40), Image.BICUBIC)
        hero_models.append(np.asarray(img))
    return hero_models


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
    for model in hero_models:
        diff = mse(model, extracted)
        differences.append(diff)

    best_match = np.argmin(differences)
    return best_match


def read_heroes_text(source_image):
    image = Image.open(source_image).convert('LA').crop((562, 320, 562 + 800, 320 + 25))
    heroes = pytesseract.image_to_string(image)[27:].split("/")
    heroes_stripped = []
    for hero in heroes:
        heroes_stripped.append(hero.strip())
    return heroes_stripped


def find_hero_position(hero):
    if dict.get(hero) >= 0:
        model_picture = hero_models[dict.get(hero)]
        differences = []
        for pic in pics_in_screenshot:
            diff = mse(model_picture, pic)
            differences.append(diff)
        return np.argmin(differences)
    else:
        return 0


def find_coords(position, initial_left=left_position, initial_top=top_position, initial_end_left=end_left, initial_end_top=end_top):
    y_grid = position // 16
    x_grid = position % 16
    left_up = initial_left + (x_grid * 50), initial_top + (y_grid * 50)
    right_up = initial_left + (x_grid * 50) + 40, initial_top + (y_grid * 50)
    left_bot = initial_left + (x_grid * 50), initial_top + (y_grid * 50) + 40
    right_bot = initial_left + (x_grid * 50) + 40, initial_top + (y_grid * 50) + 40
    return (left_up, right_up, right_bot, left_bot, left_up)


def draw_box(coord, source_image=source_image):
    image = Image.open(source_image)
    d = ImageDraw.Draw(image)
    line_color = (255, 0, 255)
    d.line(coord, fill=line_color, width=2)
    source_image = image
    image.save("monitor-1.jpg")
    return source_image
