import logging
import math

import numpy as np
from skimage import img_as_float
from softcolor import MorphologyInCIELab

logger = logging.getLogger(__name__)


def remove_and_inpaint(image, tophats_se=None, inpainting_se=None):
    image = img_as_float(image)

    if tophats_se is None:
        logger.info('Creating structuring elements for top hat.')
        tophats_se = bank_of_structuring_elements(side_enclosing_square_in_px=9, num_orientations=8)
    if inpainting_se is None:
        logger.info('Creating structuring element for inpainting.')
        inpainting_se = np.ones((5, 5), dtype='float32')

    morphology = MorphologyInCIELab()

    tophats_as_list = []
    for idx, se in enumerate(tophats_se):
        logger.info(f'Computing top-hat {idx+1:02d}/{len(tophats_se):02d}.')
        tophats_as_list.append(morphology.tophat_closing(image, structuring_element=se))

    tophats = np.stack(tophats_as_list, axis=2)     # THs are 2D, so are to be stacked on 3rd dim.

    logger.info('Computing curvilinear detector output.')
    curvilinear_detector = np.max(tophats, axis=2) - np.min(tophats, axis=2)
    curvilinear_detector -= np.min(curvilinear_detector)
    if np.max(curvilinear_detector) > 0:
        curvilinear_detector /= np.max(curvilinear_detector)

    curvilinear_mask = curvilinear_detector > 0.1

    image_to_inpaint = image.copy()
    image_to_inpaint[curvilinear_mask] = np.nan

    logger.info('Inpainting image.')
    inpainted_image, inpaint_steps = morphology.inpaint_with_steps(image_to_inpaint, structuring_element=inpainting_se)

    tophats_as_list_normalized = [t - np.min(t) for t in tophats_as_list]
    tophats_as_list_normalized = [t/np.max(t) for t in tophats_as_list_normalized]
    image_to_inpaint[np.isnan(image_to_inpaint)] = 1    # Inpaint with white for visualization

    steps = [v for tupl in zip(tophats_se, tophats_as_list_normalized) for v in tupl] + \
            [curvilinear_detector, curvilinear_mask] + \
            [s for s in inpaint_steps]

    return inpainted_image, steps


def bank_of_structuring_elements(side_enclosing_square_in_px, num_orientations):
    return [se_bar(side_enclosing_square_in_px=side_enclosing_square_in_px, orientation_in_degrees=a)
            for a in np.linspace(start=0, stop=180, num=num_orientations, endpoint=False)]


def se_bar(side_enclosing_square_in_px, orientation_in_degrees):
    se_sz = side_enclosing_square_in_px
    sz_ct = side_enclosing_square_in_px // 2
    m = -math.tan(math.radians(orientation_in_degrees))
    [coord_x, coord_y] = np.meshgrid(range(-sz_ct, se_sz-sz_ct), range(-sz_ct, se_sz-sz_ct))

    if m > 1e15:
        distance_to_line = np.abs(coord_x)
    else:
        distance_to_line = np.abs(m * coord_x - coord_y) / math.sqrt(m ** 2 + 1)

    variance = max(1/2, se_sz/14)
    structuring_element = np.exp(-distance_to_line**2 / (2*variance))
    return structuring_element
