import numpy as np
from softcolor import MorphologyInCIELab


def remove_and_inpaint(image, tophats_se=None, inpainting_se=None):

    if tophats_se is None:
        tophats_se = [se_bar(side_enclosing_square_in_px=9, orientation_in_degrees=a)
                      for a in np.linspace(start=0, stop=180, num=8, endpoint=False)]
    if inpainting_se is None:
        inpainting_se = np.ones(5)

    morphology = MorphologyInCIELab()
    tophats_as_list = [morphology.tophat_closing(image, structuring_element=se)
                       for se in tophats_se]
    tophats = np.concatenate(tophats_as_list, axis=3)

    curvilinear_detector = np.max(tophats, axis=3) - np.min(tophats, axis=3)
    curvilinear_mask = curvilinear_detector > 0.1

    inpaint, inpaint_steps = morphology.inpaint_with_steps(image, structuring_element=inpainting_se)

    steps = [v for tupl in zip(tophats_se, tophats_as_list) for v in tupl] + [curvilinear_detector, curvilinear_mask] + list(inpaint_steps)

    return inpaint, steps

def se_bar(side_enclosing_square_in_px, orientation_in_degrees):
    return None