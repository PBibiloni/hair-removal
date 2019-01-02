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
        tophats_se = [se_bar(side_enclosing_square_in_px=9, orientation_in_degrees=a)
                      for a in np.linspace(start=0, stop=180, num=8, endpoint=False)]
    if inpainting_se is None:
        logger.info('Creating structuring element for inpainting.')
        inpainting_se = np.ones(5)

    morphology = MorphologyInCIELab()

    tophats_as_list = []
    for idx, se in enumerate(tophats_se):
        logger.info(f'Computing top-hat {idx:02d}/{len(tophats_se):02d}.')
        tophats_as_list.append(morphology.tophat_closing(image, structuring_element=se))

    tophats = np.stack(tophats_as_list, axis=2)     # Since THs are monochannel (2D), so are to be stacked on 3rd.

    logger.info('Computing curvilinear detector output.')
    curvilinear_detector = np.max(tophats, axis=2) - np.min(tophats, axis=2)
    curvilinear_mask = curvilinear_detector > 0.1

    logger.info('Inpainting image.')
    inpainted_image, inpaint_steps = morphology.inpaint_with_steps(image, structuring_element=inpainting_se)

    steps = [v for tupl in zip(tophats_se, tophats_as_list) for v in tupl] + \
            [curvilinear_detector, curvilinear_mask] + \
            [s for s in inpaint_steps]

    return inpainted_image, steps


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
