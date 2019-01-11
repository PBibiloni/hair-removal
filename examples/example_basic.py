import datetime
import logging
import sys

import numpy as np
from skimage import io

from examples.utils import plot
from hair_removal import bank_of_structuring_elements, remove_and_inpaint

if __name__ == '__main__':
    # Display all logs on console
    logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    folder_plots = f'results/{datetime.datetime.now():%Y-%m-%d %H-%M-%S}/'

    tophats_se = bank_of_structuring_elements(side_enclosing_square_in_px=9, num_orientations=4)
    inpainting_se = np.ones((3, 3), dtype='float32')

    for name in ['Hairs1', 'Hairs2', 'Hairs3']:
        image = io.imread(f'images/{name}.jpg')
        image_hairless, steps = remove_and_inpaint(image, tophats_se=tophats_se, inpainting_se=inpainting_se)
        plot([image, image_hairless],
             folder=folder_plots + f'{name}/',
             name='01 Summary',
             save=True, save_each_independently=True)
        plot(steps,
             folder=folder_plots + f'{name}/',
             name='02 Steps',
             save=True, save_each_independently=True)
