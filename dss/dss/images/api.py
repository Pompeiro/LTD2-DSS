import pathlib
import shutil

import cv2 as cv  # type: ignore[import]
import numpy as np
import pyautogui
from fastapi import APIRouter, Depends, Response
from fastapi.responses import FileResponse
from sqlmodel import Session

from dss.dependencies import get_session
from dss.settings import settings

from ..units import Unit
from .enums import ArenaGrid

router = APIRouter(prefix="/images", tags=["images"])


@router.get("/")
async def make_ss() -> Response:
    screenshot = pyautogui.screenshot(region=(0, 0, 1920, 1080))  # type: ignore[attr-defined]
    screenshot.save("dss/dss/images/my_screenshot.png")
    cv_screenshot = cv.cvtColor(np.array(screenshot), cv.COLOR_RGB2BGR)
    cv.rectangle(
        cv_screenshot,
        (ArenaGrid.X1, ArenaGrid.Y1),
        (ArenaGrid.X2, ArenaGrid.Y2),
        (0, 255, 0),
        3,
    )
    cv.imwrite("dss/dss/images/cv_screenshot.png", cv_screenshot)
    return FileResponse("dss/dss/images/cv_screenshot.png")


@router.get("/match-template")
async def match_template(return_image: bool) -> Response | list[str]:
    img_rgb = cv.imread("dss/dss/images/my_screenshot.png")
    img_rgb = img_rgb[
        ArenaGrid.Y1 - ArenaGrid.MARGIN : ArenaGrid.Y2 + ArenaGrid.MARGIN,
        ArenaGrid.X1 - ArenaGrid.MARGIN : ArenaGrid.X2 + ArenaGrid.MARGIN,
    ]
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    icons = pathlib.Path("dss/dss/images/icons")
    matched_units = []
    for icon in icons.iterdir():
        if icon.name == ".gitignore":
            continue
        template = cv.imread(str(icon), 0)
        template = cv.resize(template, (25, 25))
        w, h = template.shape[::-1]
        res = cv.matchTemplate(img_gray, template, cv.TM_SQDIFF_NORMED)
        threshold = 0.08
        loc = np.where(res <= threshold)
        mask = np.zeros(img_rgb.shape[:2], np.uint8)
        for pt in zip(*loc[::-1]):
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
        cv.imwrite("dss/dss/images/res.png", img_rgb)
    if return_image is True:
        return FileResponse("dss/dss/images/res.png")
    return matched_units


@router.get("/copy-icons")
async def copy_icons(session: Session = Depends(get_session)) -> list[Unit]:
    enabled_units = (
        session.query(Unit)
        .filter(Unit.is_enabled == True)  # pylint: disable=singleton-comparison
        .all()
    )
    icons_to_copy = [enabled_unit.icon_path for enabled_unit in enabled_units]
    for icon in icons_to_copy:
        file_src = pathlib.Path(
            settings.ltd2_icons_path
            + icon.replace("Icons/", "").replace(
                "PriestessOfTheAbyss", "PriestessoftheAbyss"
            )
        )  # local icon game files are named differently than in LDT2 CDN
        file_dst = pathlib.Path("dss/dss/images/icons")
        shutil.copy(file_src, file_dst)
    pathlib.Path("dss/dss/images/icons/PriestessoftheAbyss.png").rename(
        "dss/dss/images/icons/PriestessOfTheAbyss.png"
    )  # local icon game files are named differently than in LDT2 CDN
    return icons_to_copy
