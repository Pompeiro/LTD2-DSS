import pathlib
from pathlib import Path

import cv2 as cv
import numpy as np
import pyautogui
import pytesseract

from app.enums import ArenaGrid, ShopGrid
from app.localstack.models import ActionableElement
from app.playground_area_coordinates import grid

IMAGES_DIR: str = "app/images"
SCREENSHOT_BASE_PATH: Path = Path(f"{IMAGES_DIR}/screenshot.png")
ARENA_GRID_PATH: Path = Path(f"{IMAGES_DIR}/arena_grid.png")
SHOP_GRID_PATH: Path = Path(f"{IMAGES_DIR}/shop_grid.png")
STATIC_IMAGES_SANDBOX_DIR: Path = Path(f"{IMAGES_DIR}/static/sandbox")
PLAYGROUND_PATH: Path = Path(f"{STATIC_IMAGES_SANDBOX_DIR}/playground.png")
PLAYGROUND_AREA_PATH: Path = Path(f"{STATIC_IMAGES_SANDBOX_DIR}/playground_area.png")
PLAYGROUND_AREA_WITH_GRID_PATH: Path = Path(
    f"{IMAGES_DIR}/playground_area_with_grid.png"
)
EVENT_HISTORY_LOG_PATH: Path = Path(
    f"{STATIC_IMAGES_SANDBOX_DIR}/event_history_log.png"
)


def make_screenshot_by_given_display(
    display: int = 2, path: Path = SCREENSHOT_BASE_PATH
) -> Path:
    regions = {1: (0, 0, 1920, 1080), 2: (1920, 0, 1920, 1080)}
    screenshot = pyautogui.screenshot(region=regions.get(display))
    cv_screenshot = cv.cvtColor(np.array(screenshot), cv.COLOR_RGB2BGR)

    cv.imwrite(filename=str(path), img=cv_screenshot)
    return path


def make_region_screenshot_by_actionable_element(
    actionable_element: ActionableElement,
) -> Path:
    path = make_screenshot_by_given_region_and_display(
        region=actionable_element.rectangle.region_relative,
        display=2,
        path=actionable_element.image_path,
    )

    return path


def make_screenshot_by_given_region_and_display(
    region: tuple[int, int, int, int],
    display: int = 2,
    path: Path = EVENT_HISTORY_LOG_PATH,
) -> Path:
    regions = {1: (0, 0, 1920, 1080), 2: (1920, 0, 0, 0)}
    region_on_given_display = tuple(
        map(
            sum,
            zip(
                regions.get(display),
                region,
                strict=False,
            ),
        )
    )

    screenshot = pyautogui.screenshot(region=region_on_given_display)
    screenshot.save(path)
    return path


def rectangle_on_given_grid(path: Path, grid: ArenaGrid | ShopGrid) -> Path:
    screenshot_with_rectangle = cv.rectangle(
        cv.imread(str(path)),
        (grid.X1, grid.Y1),
        (grid.X2, grid.Y2),
        (0, 255, 0),
        3,
    )
    cv.imwrite(filename=str(path), img=screenshot_with_rectangle)
    return path


def rectangle_on_shop_grid(
    path: Path = SHOP_GRID_PATH, grid: ArenaGrid | ShopGrid = ShopGrid
) -> Path:
    return rectangle_on_given_grid(path=path, grid=grid)


def rectangle_on_arena_grid(
    path: Path = ARENA_GRID_PATH, grid: ArenaGrid | ShopGrid = ArenaGrid
) -> Path:
    return rectangle_on_given_grid(path=path, grid=grid)


def add_playground_grid(
    image_path: Path = Path(PLAYGROUND_AREA_PATH),
    image_result_path: Path = Path(PLAYGROUND_AREA_WITH_GRID_PATH),
) -> Path:
    img_rgb = cv.imread(str(image_path))
    full_square_img = cv.imread(
        str(STATIC_IMAGES_SANDBOX_DIR.joinpath("full_square.png"))
    )
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
    return image_result_path


def add_playground_grid_with_perspective(
    image_path: Path = PLAYGROUND_PATH,
    image_result_path: Path = Path(f"{IMAGES_DIR}/res1.png"),
) -> Path:
    img = cv.imread(str(image_path))
    for i, row in enumerate(grid):
        for column in row:
            cv.rectangle(
                img=img,
                pt1=column.tl,
                pt2=column.br,
                color=(0, 255 - i * 30, i * 45),
                thickness=1,
            )
            cv.drawMarker(
                img=img,
                position=column.center,
                color=(0, 255 - i * 30, i * 45),
                thickness=1,
            )
    cv.imwrite(str(image_result_path), img)
    return image_result_path


def ocr_by_path(
    path: Path = EVENT_HISTORY_LOG_PATH, filter_word: str = ""
) -> list[str]:
    config = r"--oem 3 --psm 6"
    img_cv = cv.imread(str(path))
    img_rgb = cv.cvtColor(img_cv, cv.COLOR_BGR2RGB)

    result = pytesseract.image_to_string(img_rgb, config=config)

    results = result.split("\n")
    filtered_results = list(filter(lambda x: filter_word in x, results))

    return filtered_results


def match_template_center(haystack_path: Path, needle_path: Path) -> tuple[int, int]:
    haystack_img = cv.imread(str(haystack_path), cv.COLOR_BGR2GRAY)
    needle_img = cv.imread(str(needle_path), cv.COLOR_BGR2GRAY)
    result = cv.matchTemplate(haystack_img, needle_img, cv.TM_CCOEFF_NORMED)

    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

    top_left = max_loc

    needle_h, needle_w = needle_img.shape[:2]

    center_x = top_left[0] + needle_w // 2
    center_y = top_left[1] + needle_h // 2

    center = (center_x, center_y)

    bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)
    cv.rectangle(haystack_img, top_left, bottom_right, (0, 255, 0), 2)
    cv.circle(haystack_img, center, 5, (0, 0, 255), -1)
    cv.imwrite(f"{IMAGES_DIR}/res.png", haystack_img)
    return center


def match_template_threshold(haystack_path: Path, needle_path: Path) -> bool:
    haystack_img = cv.imread(str(haystack_path), cv.COLOR_BGR2GRAY)
    needle_img = cv.imread(str(needle_path), cv.COLOR_BGR2GRAY)
    result = cv.matchTemplate(haystack_img, needle_img, cv.TM_CCOEFF_NORMED)

    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

    if max_val >= 0.9:
        top_left = max_loc

        needle_h, needle_w = needle_img.shape[:2]

        center_x = top_left[0] + needle_w // 2
        center_y = top_left[1] + needle_h // 2

        center = (center_x, center_y)

        bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)
        cv.rectangle(haystack_img, top_left, bottom_right, (0, 255, 0), 2)
        cv.circle(haystack_img, center, 5, (0, 0, 255), -1)
        cv.imwrite(f"{IMAGES_DIR}/res.png", haystack_img)
        return True
    return False


###########################################
def match_template() -> list[str]:
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
    return matched_units


def match_template_shop(
    image_path: str = f"{IMAGES_DIR}/my_screenshot.png",
    grid: ArenaGrid | ShopGrid = ShopGrid,
    image_result_path: str = f"{IMAGES_DIR}/res1.png",
) -> list[str]:
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
    return matched_units
