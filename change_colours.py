from PIL import Image
import numpy as np

GRUVBOX_BASE_COLOURS: list[tuple[int]] = [
    (40, 40, 40), (204, 36, 29), (152, 151, 26), (215, 153, 33),
    (69, 133, 136), (177, 98, 134), (104, 157, 106), (213, 93, 14)
]

# Generate a list of colours that are faded versions of the base colours
def generate_fades(colours: list[tuple[int]], num_shades: int = 5) -> list[tuple[int]]:
    extended: list = []
    for colour in colours:
        for factor in np.linspace(0.5, 1.5, num_shades):
            shade = tuple(min(max(int(c * factor), 0), 255) for c in colour)
            extended.append(shade)
    return list(set(extended))

# Colours manipulation functions
def blend_colours(original: tuple, target: list[tuple], blend_ratio: float) -> tuple[int]:
    return tuple(int(o * (1 - blend_ratio) + t * blend_ratio) for o, t in zip(original, target))

def closest_colour(rgb: tuple[int], palette: list[tuple[int]]) -> tuple[int]:
    return min(palette, key = lambda colour: sum((s - c) ** 2 for s, c in zip(rgb, colour)))

def load_image(image_name: str) -> np.ndarray:
    return np.array(Image.open(image_name))

# Call it with extended palette to ensure smoother generation
def change_pixels(image_as_array: np.ndarray, palette: list[tuple[int]], blend_ratio: float) -> np.ndarray:
    return np.array([
        [blend_colours(pixel, closest_colour(pixel, palette), blend_ratio) for pixel in row]
        for row in image_as_array
    ])

def generate_image(image_name: str, output_name: str, blend: float) -> None:
    extended_palette: list[tuple[int]] = generate_fades(GRUVBOX_BASE_COLOURS)
    
    image: np.ndarray = load_image(image_name)
    
    new_image = Image.fromarray(np.uint8(change_pixels(image, extended_palette, blend)))
    new_image.save(output_name)