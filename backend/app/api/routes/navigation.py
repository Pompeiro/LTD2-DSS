import time
from pathlib import Path
from typing import Annotated

import cv2 as cv
import numpy as np
from fastapi import APIRouter, Query, Response
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse

from app.models import Message
from app.views import (
    choose_legion_view,
    learn_view,
    main_menu_view,
    make_ss_sync,
    match_template_center,
    sandbox_view,
    solo_view,
)

IMAGES_DIR = "app/images"
STATIC_IMAGES_DIR = "app/images/static"
STATIC_IMAGES_MAIN_MENU_DIR = Path("app/images/static/main_menu")
STATIC_IMAGES_SOLO_DIR = Path("app/images/static/solo")
STATIC_IMAGES_LEARN_DIR = Path("app/images/static/learn")
STATIC_IMAGES_CHOOSE_LEGION_DIR = Path("app/images/static/choose_legion")
STATIC_IMAGES_SANDBOX_DIR = Path("app/images/static/sandbox")


router = APIRouter(prefix="/navigation", tags=["navigation"])


@router.get("/")
async def make_ss(
    save_to: Path, display: Annotated[int, Query(ge=1, le=2)] = 2
) -> Response:
    make_ss_sync(save_to=save_to, display=display)
    return FileResponse(save_to)


@router.get("/match-template", response_model=None)
async def match_template(return_image: bool) -> Response | list[str]:
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
    if return_image is True:
        return FileResponse(f"{IMAGES_DIR}/res.png")
    return matched_units


@router.post("/find-center", response_model=None)
async def find_center(
    return_image: bool,
    image_to_find_path: Path = sandbox_view.event_history_text.image_path,
) -> Response | tuple[int, int]:
    center = match_template_center(
        haystack_path=sandbox_view.static_screenshot, needle_path=image_to_find_path
    )
    if return_image is True:
        return FileResponse(f"{IMAGES_DIR}/res.png")
    return center


@router.post("/navigate-from-main-to-solo-view", response_model=Message)
async def navigate_from_main_to_solo_view() -> Message:
    if main_menu_view.expect_to_be_in_view() is True:
        main_menu_view.navigation_buttons.solo.click()
        time.sleep(1)
        if solo_view.expect_to_be_in_view() is True:
            return Message(message="Navigated to solo view successfuly")

    raise HTTPException(status_code=400, detail="Navigated to solo view failed")


@router.post("/navigate-from-main-to-learn-view", response_model=Message)
async def navigate_from_main_to_learn_view() -> Message:
    if main_menu_view.expect_to_be_in_view() is True:
        main_menu_view.navigation_buttons.learn.click()
        time.sleep(1)
        if learn_view.expect_to_be_in_view() is True:
            return Message(message="Navigated to learn view successfuly")

    raise HTTPException(status_code=400, detail="Navigated to learn view failed")


@router.post("/navigate-from-learn-to-choose-legion-view", response_model=Message)
async def navigate_from_learn_to_choose_legion_view() -> Message:
    if learn_view.expect_to_be_in_view() is True:
        learn_view.navigation_buttons.sandbox.click()
        time.sleep(30)
        if choose_legion_view.expect_to_be_in_view() is True:
            return Message(message="Navigated to learn view successfuly")

    raise HTTPException(status_code=400, detail="Navigated to learn view failed")


@router.post("/choose-legion-view-choose-element-legion", response_model=Message)
async def choose_legion_view_choose_element_legion() -> Message:
    if choose_legion_view.expect_to_be_in_view() is True:
        choose_legion_view.navigation_buttons.element.click()
        time.sleep(5)
        if choose_legion_view.expect_to_be_in_view() is True:
            return Message(message="Navigated to learn view successfuly")

    raise HTTPException(status_code=400, detail="Navigated to learn view failed")
