import datetime
import logging
import math
import os

import numpy as np
from matplotlib import pyplot as plt
from skimage import io, img_as_uint

logger = logging.getLogger(__name__)


def plot(list_images, show=True, save=False, save_each_independently=False, folder=None, name=None, extension='.png'):
    if isinstance(list_images, np.ndarray):
        list_images = [list_images]

    if len(list_images) > 9:
        for i in range(math.ceil(len(list_images)/9)):
            plot(list_images[9*i:9*(i+1)], show=show, save=save, save_each_independently=save_each_independently,
                 folder=folder, name=f'{name} {i:02d}', extension=extension)
    else:
        size_by_num_plots = {
            1: (1, 1),
            2: (1, 2),
            3: (1, 2),
            4: (2, 2),
            6: (2, 3),
            1e10: (3, math.ceil(len(list_images)/3)),
        }
        sz = {key: value for key, value in size_by_num_plots.items() if key > len(list_images)}
        sz = min(sz.items(), key=lambda t: t[1])[1]

        fig, axs = plt.subplots(nrows=sz[0], ncols=sz[1])
        [ax.axis('off') for ax in axs.flat]
        for idx, img in enumerate(list_images):
            # Show bool images
            if img.dtype == 'bool':
                img = img_as_uint(img)
            # Visualize missing values as 1's (RGB's white)
            mask_nans = np.nan(img)
            if np.any(mask_nans):
                img = img.copy()
                img[mask_nans] = 1
            ax = axs.flat[idx]
            im = ax.imshow(img)
            if img.ndim == 2:
                fig.colorbar(im, ax=ax, cmap='gray')
        fig.tight_layout()

        if show:
            fig.show()
        if save:
            if folder is None:
                folder = f'results/{datetime.datetime.now():%Y-%m-%d %H-%M-%S}'
            os.makedirs(folder, exist_ok=True)
            fig.savefig(fname=folder + '/' + name + extension)
            if save_each_independently:
                for idx, single_image in enumerate(list_images):
                    os.makedirs(f'{folder}/{name}', exist_ok=True)
                    try:
                        if single_image.dtype == 'bool':
                            single_image = img_as_uint(single_image)
                        io.imsave(arr=single_image, fname=f'{folder}/{name}/{name} - {idx:02d}{extension}')
                    except ValueError as e:
                        logger.warning(f'Could not save image. Error: {e}')
        plt.close(fig=fig)
