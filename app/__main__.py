# Copyright 2024 tarxzf

import hashlib
import os
import random

from math import ceil
from pathlib import Path
from PIL import Image, ImageDraw

from data.config import GAP_OUT, BLOCK_SIZE, BLOCK_QUANTITY, BACKGROUND_COLOR, AVATAR_PATH


def generate_avatar(
        image: Image,
        gap: int,
        block_size: int,
        blocks: int,
        scheme: list[list[int]],
        color: tuple[int, int, int]
) -> Image.Image:
    draw = ImageDraw.Draw(image)

    for y in range(blocks):
        for x in range(blocks):
            pos_x = gap + x * block_size
            pos_y = gap + y * block_size

            if scheme[y][x]:
                coords = (pos_x, pos_y, pos_x + block_size, pos_y + block_size) 
                draw.rectangle(coords, color)
    return image


def generate_scheme_avatar(blocks: int, seed: str) -> list[list[int]]:
    random.seed(seed)

    scheme = [[0 for _ in range(blocks)] for _ in range(blocks)]
    for y in enumerate(scheme):
        for x in enumerate(y[1][:ceil(len(scheme) / 2)]):  # Here we're passing half of the scheme   
            if random.randint(0, 1):
                scheme[y[0]][x[0]] = 1
                scheme[y[0]][-x[0]-1] = 1
    
    return scheme


def main():
    seed = input('Type your seed phrase: ')
    hash = hashlib.sha256(seed.encode()).hexdigest()

    image = Image.new(
        mode='RGB',
        size=tuple(GAP_OUT * 2 + BLOCK_SIZE * BLOCK_QUANTITY for _ in range(2)),
        color=BACKGROUND_COLOR
    )

    scheme = generate_scheme_avatar(BLOCK_QUANTITY, hash)

    # Here the hash is converted to decimal notation and its first 9 digits are taken,
    # which are used to get the color definition
    color = tuple(100 + int(str(int(f'0x{hash}', 16))[i*3:i*3+3]) % 101 for i in range(3))

    image = generate_avatar(image, GAP_OUT, BLOCK_SIZE, BLOCK_QUANTITY, scheme, color)

    root_path = Path(__file__).parent.parent.absolute()  # Work directory
    os.mkdir(root_path / AVATAR_PATH)

    avatar_quantity = len(os.listdir(root_path / AVATAR_PATH))  # Number of avatars
    avatar_photo = f'avatar_{avatar_quantity + 1}.png'  # Photo name
    avatar_path = root_path / AVATAR_PATH / avatar_photo  # Avatar path

    with open(avatar_path, 'wb') as file:
        image.save(file, 'PNG')
    
    print(f'Your avatar have been saved into "{avatar_path}"')


if __name__ == '__main__':
    main()
