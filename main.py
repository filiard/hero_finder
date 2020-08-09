import functions
from PIL import Image

source_image = r'monitor-1.jpg'

heroes_to_find = functions.read_heroes_text(source_image)

hero_models = functions.import_models()

pics_in_screenshot = functions.extract_miniatures(source_image)
found_positions = []
found_coords = []

for hero in heroes_to_find:
    found_positions.append(functions.find_hero_position(hero))

for position in found_positions:
    found_coords.append(functions.find_coords(position))

global last_img

for coord in found_coords:
    last_img = functions.draw_box(coord)

last_img.show()
print("KONIEC")
