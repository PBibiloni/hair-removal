import datetime
import logging
import sys

from skimage import io

from core import remove_and_inpaint
from utils import plot


if __name__ == '__main__':
    # Display all logs on console
    logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    folder_plots = f'results/{datetime.datetime.now():%Y-%m-%d %H-%M-%S}/'

    for name in ['Hairs1', 'Hairs2', 'Hairs3']:
        image = io.imread(f'images/{name}.jpg')
        image_hairless, steps = remove_and_inpaint(image)
        plot([image, image_hairless],
             folder=folder_plots + f'{name}/',
             name='01 Summary',
             save=True, save_each_independently=True)
        plot(steps,
             folder=folder_plots + f'{name}/',
             name='02 Steps',
             save=True, save_each_independently=True)
