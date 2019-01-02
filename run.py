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

    folder_plots = f'results/{datetime.datetime.now():%Y-%m-%d %H-%M-%S}'

    image = io.imread('images/Hairs1.jpg')
    image_hairless, steps = remove_and_inpaint(image)
    plot([image, image_hairless],
         folder=folder_plots,
         name='00 Summary',
         save=True, save_each_independently=True)
    plot(steps,
         folder=folder_plots,
         name='01 Steps',
         save=True, save_each_independently=True)
