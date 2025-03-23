import logging
from pathlib import Path

import cv2 as cv
import numpy as np
from pydantic import BaseModel

from app.enums import ArenaGrid, ShopGrid
from app.localstack.images import (
    make_screenshot_by_given_display,
    make_screenshot_by_given_region_and_display,
    match_template_center,
    match_template_threshold,
)
from app.localstack.models import ActionableElement, Point, Rectangle
from app.playground_area_coordinates import grid

IMAGES_DIR = "app/images"
STATIC_IMAGES_DIR = "app/images/static"
STATIC_IMAGES_MAIN_MENU_DIR: Path = Path(f"{STATIC_IMAGES_DIR}/main_menu")
STATIC_IMAGES_SOLO_DIR: Path = Path(f"{STATIC_IMAGES_DIR}/solo")
STATIC_IMAGES_LEARN_DIR: Path = Path(f"{STATIC_IMAGES_DIR}/learn")
STATIC_IMAGES_CHOOSE_LEGION_DIR: Path = Path(f"{STATIC_IMAGES_DIR}/choose_legion")
STATIC_IMAGES_SANDBOX_DIR: Path = Path(f"{STATIC_IMAGES_DIR}/sandbox")
PLAYGROUND_PATH: Path = Path(f"{STATIC_IMAGES_SANDBOX_DIR}/playground.png")


def expect_to_be_in_view(
    haystack_path: Path, needle: ActionableElement, threshold: int = 5
) -> bool:
    make_screenshot_by_given_display(path=haystack_path)
    center = match_template_center(
        haystack_path=haystack_path, needle_path=needle.image_path
    )
    x, y = center
    fit_x = (
        needle.rectangle.center.x - threshold
        <= x
        < needle.rectangle.center.x + threshold
    )
    fit_y = (
        needle.rectangle.center.y - threshold
        <= y
        < needle.rectangle.center.y + threshold
    )
    result = fit_x and fit_y

    logging.info("Is needle in view?: %s", result)
    return result


def expect_to_be_in_view_region_area(
    haystack_path: Path, needle: ActionableElement
) -> bool:
    make_screenshot_by_given_region_and_display(
        region=needle.rectangle.region_relative, display=2, path=haystack_path
    )
    result = match_template_threshold(
        haystack_path=haystack_path, needle_path=needle.image_path
    )
    logging.info("Current needle: %s", needle.image_path.stem)
    logging.info("Is needle in REGION view?: %s", result)
    return result


class MainMenuNavigationButtons(BaseModel):
    multiplayer: ActionableElement = ActionableElement(
        rectangle=Rectangle(
            tl=Point(x=75, y=242),
            br=Point(x=446, y=296),
        ),
        image_path=STATIC_IMAGES_MAIN_MENU_DIR.joinpath("multiplayer_button.png"),
    )

    solo: ActionableElement = ActionableElement(
        rectangle=Rectangle(
            tl=Point(x=78, y=322),
            br=Point(x=456, y=376),
        ),
        image_path=STATIC_IMAGES_MAIN_MENU_DIR.joinpath("solo_button.png"),
    )

    learn: ActionableElement = ActionableElement(
        rectangle=Rectangle(
            tl=Point(x=78, y=394),
            br=Point(x=190, y=430),
        ),
        image_path=STATIC_IMAGES_MAIN_MENU_DIR.joinpath("learn_button.png"),
    )


class MainMenuView(BaseModel):
    static_screenshot: Path = Path(f"{STATIC_IMAGES_MAIN_MENU_DIR}/main_menu.png")
    dynamic_screenshot: Path = Path(
        f"{STATIC_IMAGES_MAIN_MENU_DIR}/main_menu_dynamic.png"
    )
    navigation_buttons: MainMenuNavigationButtons = MainMenuNavigationButtons()

    def expect_to_be_in_view(self) -> bool:
        return expect_to_be_in_view(
            haystack_path=self.dynamic_screenshot, needle=self.navigation_buttons.solo
        )


main_menu_view = MainMenuView()


class LearnViewNavigationButtons(BaseModel):
    sandbox: ActionableElement = ActionableElement(
        rectangle=Rectangle(
            tl=Point(x=1338, y=680),
            br=Point(x=1444, y=700),
        ),
        image_path=STATIC_IMAGES_LEARN_DIR.joinpath("sandbox_button.png"),
    )
    back: ActionableElement = ActionableElement(
        rectangle=Rectangle(
            tl=Point(x=1760, y=984),
            br=Point(x=1828, y=1010),
        ),
        image_path=STATIC_IMAGES_LEARN_DIR.joinpath("back_to_main_menu_button.png"),
    )


class LearnView(BaseModel):
    static_screenshot: Path = Path(f"{STATIC_IMAGES_LEARN_DIR}/learn.png")
    dynamic_screenshot: Path = Path(f"{STATIC_IMAGES_LEARN_DIR}/learn_dynamic.png")
    navigation_buttons: LearnViewNavigationButtons = LearnViewNavigationButtons()

    def expect_to_be_in_view(self) -> bool:
        return expect_to_be_in_view(
            haystack_path=self.dynamic_screenshot,
            needle=self.navigation_buttons.sandbox,
        )


learn_view = LearnView()


class ChooseLegionViewNavigationButtons(BaseModel):
    element: ActionableElement = ActionableElement(
        rectangle=Rectangle(
            tl=Point(x=480, y=426),
            br=Point(x=580, y=444),
        ),
        image_path=STATIC_IMAGES_CHOOSE_LEGION_DIR.joinpath("element_button.png"),
    )


class ChooseLegionView(BaseModel):
    static_screenshot: Path = Path(
        f"{STATIC_IMAGES_CHOOSE_LEGION_DIR}/choose_legion.png"
    )
    dynamic_screenshot: Path = Path(
        f"{STATIC_IMAGES_CHOOSE_LEGION_DIR}/choose_legion_dynamic.png"
    )
    navigation_buttons: ChooseLegionViewNavigationButtons = (
        ChooseLegionViewNavigationButtons()
    )

    def expect_to_be_in_view(self) -> bool:
        return expect_to_be_in_view(
            haystack_path=self.dynamic_screenshot,
            needle=self.navigation_buttons.element,
        )


choose_legion_view = ChooseLegionView()


class ShopTowersButtons(BaseModel):
    offset_x: int = 71
    offset_tl: Point = Point(x=597, y=996)
    offset_br: Point = Point(x=661, y=1060)

    tower_1: ActionableElement = ActionableElement(
        rectangle=Rectangle(
            tl=Point(x=offset_x * 0 + offset_tl.x, y=offset_tl.y),
            br=Point(x=offset_x * 0 + offset_br.x, y=offset_br.y),
        )
    )

    tower_2: ActionableElement = ActionableElement(
        rectangle=Rectangle(
            tl=Point(x=offset_x * 1 + offset_tl.x, y=offset_tl.y),
            br=Point(x=offset_x * 1 + offset_br.x, y=offset_br.y),
        )
    )

    tower_3: ActionableElement = ActionableElement(
        rectangle=Rectangle(
            tl=Point(x=offset_x * 2 + offset_tl.x, y=offset_tl.y),
            br=Point(x=offset_x * 2 + offset_br.x, y=offset_br.y),
        )
    )

    tower_4: ActionableElement = ActionableElement(
        rectangle=Rectangle(
            tl=Point(x=offset_x * 3 + offset_tl.x, y=offset_tl.y),
            br=Point(x=offset_x * 3 + offset_br.x, y=offset_br.y),
        )
    )

    tower_5: ActionableElement = ActionableElement(
        rectangle=Rectangle(
            tl=Point(x=offset_x * 4 + offset_tl.x, y=offset_tl.y),
            br=Point(x=offset_x * 4 + offset_br.x, y=offset_br.y),
        )
    )

    tower_6: ActionableElement = ActionableElement(
        rectangle=Rectangle(
            tl=Point(x=offset_x * 5 + offset_tl.x, y=offset_tl.y),
            br=Point(x=offset_x * 5 + offset_br.x, y=offset_br.y),
        )
    )

    towers: list[ActionableElement] = [
        tower_1,
        tower_2,
        tower_3,
        tower_4,
        tower_5,
        tower_6,
    ]


class SandboxView(BaseModel):
    static_screenshot: Path = Path(f"{STATIC_IMAGES_SANDBOX_DIR}/sandbox.png")
    dynamic_screenshot: Path = Path(f"{STATIC_IMAGES_SANDBOX_DIR}/sandbox_dynamic.png")
    event_text_screenshot: Path = Path(f"{STATIC_IMAGES_SANDBOX_DIR}/event_text.png")
    ready_button: ActionableElement = ActionableElement(
        rectangle=Rectangle(
            tl=Point(x=922, y=180),
            br=Point(x=964, y=196),
        ),
        image_path=STATIC_IMAGES_SANDBOX_DIR.joinpath("ready_button.png"),
    )

    start_button: ActionableElement = ActionableElement(
        rectangle=Rectangle(
            tl=Point(x=696, y=28),
            br=Point(x=726, y=42),
        ),
        image_path=STATIC_IMAGES_SANDBOX_DIR.joinpath("start_button.png"),
    )
    clear_button: ActionableElement = ActionableElement(
        rectangle=Rectangle(
            tl=Point(x=746, y=28),
            br=Point(x=780, y=42),
        ),
        image_path=STATIC_IMAGES_SANDBOX_DIR.joinpath("clear_button.png"),
    )

    pause_button: ActionableElement = ActionableElement(
        rectangle=Rectangle(
            tl=Point(x=950, y=126),
            br=Point(x=972, y=144),
        ),
        image_path=STATIC_IMAGES_SANDBOX_DIR.joinpath("pause_button.png"),
    )

    play_button: ActionableElement = ActionableElement(
        rectangle=Rectangle(
            tl=Point(x=950, y=126),
            br=Point(x=972, y=146),
        ),
        image_path=STATIC_IMAGES_SANDBOX_DIR.joinpath("play_button.png"),
    )
    full_hp_bar: ActionableElement = ActionableElement(
        rectangle=Rectangle(
            tl=Point(x=748, y=70),
            br=Point(x=876, y=98),
        ),
        image_path=STATIC_IMAGES_SANDBOX_DIR.joinpath("full_hp_bar.png"),
    )

    wave_phase_indicator: ActionableElement = ActionableElement(
        rectangle=Rectangle(tl=Point(x=954, y=105), br=Point(x=970, y=121)),
        image_path=STATIC_IMAGES_SANDBOX_DIR.joinpath("wave_phase_indicator.png"),
    )

    event_history_log: ActionableElement = ActionableElement(
        rectangle=Rectangle(tl=Point(x=950, y=332), br=Point(x=1290, y=912)),
        image_path=STATIC_IMAGES_SANDBOX_DIR.joinpath("event_history_log.png"),
    )
    event_text: ActionableElement = ActionableElement(
        rectangle=Rectangle(tl=Point(x=64, y=380), br=Point(x=382, y=580)),
        image_path=STATIC_IMAGES_SANDBOX_DIR.joinpath("event_text.png"),
    )

    shop_towers_buttons: ShopTowersButtons = ShopTowersButtons()
    grid: list[list[ActionableElement]] = grid

    def expect_ready_button_to_be_in_view(self) -> bool:
        return expect_to_be_in_view(
            haystack_path=self.dynamic_screenshot, needle=self.ready_button
        )

    def expect_wave_phase_indicator_to_be_in_view(self) -> bool:
        return expect_to_be_in_view_region_area(
            haystack_path=self.dynamic_screenshot, needle=self.wave_phase_indicator
        )

    def add_shop_towers_buttons_markers(
        self,
        image_path: Path = Path("app/images/screenshot.png"),
        image_result_path: Path = Path(f"{IMAGES_DIR}/res1.png"),
    ) -> Path:
        img = cv.imread(str(image_path))
        towers = self.shop_towers_buttons.towers
        for tower in towers:
            cv.drawMarker(
                img=img, position=tower.center, color=(0, 255, 0), thickness=4
            )
        cv.imwrite(str(image_result_path), img)
        return image_result_path

    def add_shop_towers_buttons_rectangles(
        self,
        image_path: Path = Path("app/images/screenshot.png"),
        image_result_path: Path = Path(f"{IMAGES_DIR}/res1.png"),
    ) -> Path:
        img = cv.imread(str(image_path))
        towers = self.shop_towers_buttons.towers
        for tower in towers:
            cv.rectangle(
                img=img, pt1=tower.tl, pt2=tower.br, color=(0, 255, 0), thickness=4
            )
        cv.imwrite(str(image_result_path), img)
        return image_result_path

    def match_template_shop(
        self,
        image_path: str = f"{IMAGES_DIR}/screenshot.png",
        grid: ArenaGrid | ShopGrid = ShopGrid,
        image_result_path: str = f"{IMAGES_DIR}/res1.png",
    ) -> list[str]:
        img_rgb = cv.imread(image_path)
        towers = self.shop_towers_buttons.towers

        icons = Path(f"{IMAGES_DIR}/icons")
        matched_units = []
        for tower in towers:
            tower_img = cv.cvtColor(
                img_rgb[tower.tl[1] : tower.br[1], tower.tl[0] : tower.br[0]],
                cv.COLOR_BGR2GRAY,
            )
            for icon in icons.iterdir():
                if icon.name == ".gitignore":
                    continue
                template = cv.imread(str(icon), 0)
                w, h = template.shape[::-1]
                res = cv.matchTemplate(tower_img, template, cv.TM_CCOEFF_NORMED)
                threshold = 0.63
                loc = np.where(res >= threshold)
                mask = np.zeros(img_rgb.shape[:2], np.uint8)
                for pt in zip(*loc[::-1], strict=False):
                    if (
                        mask[pt[1] + int(round(h / 2)), pt[0] + int(round(w / 2))]
                        != 255
                    ):
                        mask[pt[1] : pt[1] + h, pt[0] : pt[0] + w] = 255
                        cv.rectangle(
                            img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 1
                        )
                        cv.putText(
                            img_rgb,
                            icon.name.split(".")[0],
                            tower.center,
                            cv.FONT_HERSHEY_SIMPLEX,
                            0.5,
                            (122, 255, 55),
                        )
                        matched_units.append(f"Icons/{icon.name}")

        cv.imwrite(image_result_path, img_rgb)
        return matched_units


sandbox_view = SandboxView()
