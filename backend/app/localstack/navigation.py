import time
from pathlib import Path

import cv2 as cv
import numpy as np

from app.localstack.views import (
    choose_legion_view,
    learn_view,
    main_menu_view,
)

IMAGES_DIR = "app/images"
STATIC_IMAGES_DIR = "app/images/static"
STATIC_IMAGES_MAIN_MENU_DIR: Path = Path(f"{STATIC_IMAGES_DIR}/main_menu")
STATIC_IMAGES_SOLO_DIR: Path = Path(f"{STATIC_IMAGES_DIR}/solo")
STATIC_IMAGES_LEARN_DIR: Path = Path(f"{STATIC_IMAGES_DIR}/learn")
STATIC_IMAGES_CHOOSE_LEGION_DIR: Path = Path(f"{STATIC_IMAGES_DIR}/choose_legion")
STATIC_IMAGES_SANDBOX_DIR: Path = Path(f"{STATIC_IMAGES_DIR}/sandbox")


def navigate_from_main_to_learn_view() -> bool:
    if main_menu_view.expect_to_be_in_view() is True:
        main_menu_view.navigation_buttons.learn.click()
        time.sleep(1)
        return learn_view.expect_to_be_in_view()
    return False


def navigate_from_learn_to_choose_legion_view() -> bool:
    if learn_view.expect_to_be_in_view() is True:
        learn_view.navigation_buttons.sandbox.click()
        time.sleep(30)
        return choose_legion_view.expect_to_be_in_view()
    return False


def choose_legion_view_choose_element_legion() -> bool:
    if choose_legion_view.expect_to_be_in_view() is True:
        choose_legion_view.navigation_buttons.element.click()
        time.sleep(5)
        return choose_legion_view.expect_to_be_in_view()
    return False


###
async def match_template() -> list[str]:
    img_rgb = cv.imread(main_menu_view.static_screenshot)
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    icons = STATIC_IMAGES_MAIN_MENU_DIR
    matched_units = []
    for icon in icons.iterdir():
        if icon.name == ".gitignore":
            continue
        template = cv.imread(str(icon), 0)
        w, h = template.shape[::-1]
        res = cv.matchTemplate(img_gray, template, cv.TM_SQDIFF_NORMED)
        threshold = 0.05
        loc = np.where(res <= threshold)
        mask = np.zeros(img_rgb.shape[:2], np.uint8)
        for pt in zip(*loc[::-1], strict=False):
            if mask[pt[1] + int(round(h / 2)), pt[0] + int(round(w / 2))] != 255:
                mask[pt[1] : pt[1] + h, pt[0] : pt[0] + w] = 255
                cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 1)
                cv.putText(
                    img_rgb,
                    icon.name.split(".")[0],
                    (pt[0] + w, pt[1] + h),
                    cv.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (122, 255, 55),
                )
                matched_units.append(f"Icons/{icon.name}")
        cv.imwrite(f"{IMAGES_DIR}/res.png", img_rgb)
    return matched_units
