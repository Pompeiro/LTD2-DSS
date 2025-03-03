import pathlib
import shutil
from pathlib import Path
from typing import Annotated

import cv2 as cv
import numpy as np
import pyautogui
from fastapi import APIRouter, Query, Response
from fastapi.responses import FileResponse

from app.api.deps import SessionDep
from app.core.config import settings
from app.enums import ArenaGrid, ShopGrid
from app.models import Unit
from app.playground_area_coordinates import grid
from app.views import sandbox_view

IMAGES_DIR = "app/images"
STATIC_IMAGES_SANDBOX_DIR = Path("app/images/static/sandbox")
router = APIRouter(prefix="/images", tags=["images"])


@router.get("/")
async def make_ss(display: Annotated[int, Query(ge=1, le=2)] = 2) -> Response:
    regions = {1: (0, 0, 1920, 1080), 2: (1920, 0, 1920, 1080)}
    screenshot = pyautogui.screenshot(region=regions.get(display))
    screenshot.save(f"{IMAGES_DIR}/my_screenshot.png")
    cv_screenshot = cv.cvtColor(np.array(screenshot), cv.COLOR_RGB2BGR)
    cv.rectangle(
        cv_screenshot,
        (ArenaGrid.X1, ArenaGrid.Y1),
        (ArenaGrid.X2, ArenaGrid.Y2),
        (0, 255, 0),
        3,
    )
    cv.rectangle(
        cv_screenshot,
        (ShopGrid.X1, ShopGrid.Y1),
        (ShopGrid.X2, ShopGrid.Y2),
        (0, 125, 50),
        3,
    )
    cv.imwrite(f"{IMAGES_DIR}/cv_screenshot.png", cv_screenshot)
    return FileResponse(f"{IMAGES_DIR}/cv_screenshot.png")


@router.get("/match-template", response_model=None)
async def match_template(return_image: bool) -> Response | list[str]:
    img_rgb = cv.imread(f"{IMAGES_DIR}/my_screenshot.png")
    img_rgb = img_rgb[
        ArenaGrid.Y1 - ArenaGrid.MARGIN : ArenaGrid.Y2 + ArenaGrid.MARGIN,
        ArenaGrid.X1 - ArenaGrid.MARGIN : ArenaGrid.X2 + ArenaGrid.MARGIN,
    ]
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    icons = pathlib.Path(f"{IMAGES_DIR}/icons")
    matched_units = []
    for icon in icons.iterdir():
        if icon.name == ".gitignore":
            continue
        template = cv.imread(str(icon), 0)
        template = cv.resize(template, (25, 25))
        w, h = template.shape[::-1]
        res = cv.matchTemplate(img_gray, template, cv.TM_SQDIFF_NORMED)
        threshold = 0.15
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


@router.get("/match-template-shop", response_model=None)
async def match_template_shop(
    return_image: bool,
    image_path: str = f"{IMAGES_DIR}/my_screenshot.png",
    grid: ArenaGrid | ShopGrid = ShopGrid,
    image_result_path: str = f"{IMAGES_DIR}/res1.png",
) -> Response | list[str]:
    img_rgb = cv.imread(image_path)
    img_rgb = img_rgb[
        grid.Y1 - grid.MARGIN : grid.Y2 + grid.MARGIN,
        grid.X1 - grid.MARGIN : grid.X2 + grid.MARGIN,
    ]
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    icons = pathlib.Path(f"{IMAGES_DIR}/icons")
    matched_units = []
    for icon in icons.iterdir():
        if icon.name == ".gitignore":
            continue
        template = cv.imread(str(icon), 0)
        template = template[16:64, 0:64]
        # template = cv.resize(template, dsize=(grid.object_to_compare_size, grid.object_to_compare_size))
        w, h = template.shape[::-1]
        res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
        threshold = 0.63
        loc = np.where(res >= threshold)
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
        cv.imwrite(image_result_path, img_rgb)
    if return_image is True:
        return FileResponse(image_result_path)
    return matched_units


@router.get("/copy-icons")
async def copy_icons(session: SessionDep) -> list[str]:
    file_destination = f"{IMAGES_DIR}/icons"
    enabled_units = (
        session.query(Unit)
        .filter(Unit.is_enabled == True)  # noqa: E712
        .all()
    )
    icons_to_copy = [enabled_unit.icon_path for enabled_unit in enabled_units]
    for icon in icons_to_copy:
        file_src = pathlib.Path(
            settings.LTD2_ICONS_PATH
            + icon.replace("Icons/", "").replace(
                "PriestessOfTheAbyss", "PriestessoftheAbyss"
            )
        )  # local icon game files are named differently than in LDT2 CDN
        file_dst = pathlib.Path(file_destination)
        shutil.copy(file_src, file_dst)
    pathlib.Path(f"{file_destination}/PriestessoftheAbyss.png").rename(
        f"{file_destination}/PriestessOfTheAbyss.png"
    )  # local icon game files are named differently than in LDT2 CDN
    return icons_to_copy


@router.get("/add-playground-grid", response_model=None)
async def add_playground_grid(
    image_path: str = f"{STATIC_IMAGES_SANDBOX_DIR}/playground_area.png",
    image_result_path: str = f"{IMAGES_DIR}/res1.png",
) -> Response | list[str]:
    img_rgb = cv.imread(image_path)
    full_square_img = cv.imread(STATIC_IMAGES_SANDBOX_DIR.joinpath("full_square.png"))
    # mini_square_img = cv.imread(STATIC_IMAGES_SANDBOX_DIR.joinpath("mini_square.png"))

    # Point = namedtuple("Point", ["w", "h"])
    # tl = Point(w=66,h=6)
    # bl = Point(w=0,h=578)
    # br = Point(w=485,h=584)
    # tr = Point(w=420,h=5)

    start = (65, 4)
    # end = (484, 584)
    full_square_height, full_square_width = full_square_img.shape[:2]
    # mini_square_height, mini_square_width = mini_square_img.shape[:2]
    area_rows_full = 14
    area_columns_full = 9
    # area_rows_mini = 14 * 2
    # area_columns_mini = 9 * 2

    for j, _row in enumerate(range(area_rows_full)):
        for i, _column in enumerate(range(area_columns_full)):
            cv.rectangle(
                img_rgb,
                start,
                (
                    start[0] + i * full_square_width + full_square_width,
                    start[1] + j * full_square_height + full_square_height,
                ),
                (0, 255, 0),
                1,
            )
    cv.imwrite(image_result_path, img_rgb)

    for j, _row in enumerate(range(area_rows_full)):
        for i, _column in enumerate(range(area_columns_full)):
            cv.rectangle(
                img_rgb,
                start,
                (
                    start[0] + i * full_square_width + full_square_width,
                    start[1] + j * full_square_height + full_square_height,
                ),
                (0, 255, 0),
                1,
            )
    cv.imwrite(image_result_path, img_rgb)
    return FileResponse(image_result_path)


@router.get("/add-playground-grid-with-perspective", response_model=None)
async def add_playground_grid_with_perspective(
    image_path: str = f"{STATIC_IMAGES_SANDBOX_DIR}/playground.png",
    image_result_path: str = f"{IMAGES_DIR}/res1.png",
) -> Response | list[str]:
    img_rgb = cv.imread(image_path)
    for i, row in enumerate(grid):
        for column in row:
            cv.rectangle(
                img=img_rgb,
                pt1=column.tl,
                pt2=column.br,
                color=(0, 255 - i * 30, i * 45),
                thickness=1,
            )
            cv.drawMarker(
                img=img_rgb,
                position=column.center,
                color=(0, 255 - i * 30, i * 45),
                thickness=1,
            )
    cv.imwrite(image_result_path, img_rgb)
    return FileResponse(image_result_path)


@router.get("/add-shop-towers-buttons-markers", response_model=None)
async def add_shop_towers_buttons_markers(
    image_path: str = f"{STATIC_IMAGES_SANDBOX_DIR}/playground.png",
    image_result_path: str = f"{IMAGES_DIR}/res1.png",
) -> Response | list[str]:
    img_rgb = cv.imread(image_path)
    towers = sandbox_view.shop_towers_buttons.towers
    for tower in towers:
        cv.drawMarker(
            img=img_rgb, position=tower.center, color=(0, 255, 0), thickness=4
        )
    cv.imwrite(image_result_path, img_rgb)
    return FileResponse(image_result_path)
