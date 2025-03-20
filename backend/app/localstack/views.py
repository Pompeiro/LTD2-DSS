import logging
import numpy as np
from pathlib import Path

from app.enums import ArenaGrid, ShopGrid
import cv2 as cv
import pyautogui
from pydantic import BaseModel

from app.localstack.images import (
    make_screenshot_by_given_display,
    match_template_center,
)
from app.playground_area_coordinates import GridRectangle, grid

IMAGES_DIR = "app/images"
STATIC_IMAGES_DIR = "app/images/static"
STATIC_IMAGES_MAIN_MENU_DIR: Path = Path(f"{STATIC_IMAGES_DIR}/main_menu")
STATIC_IMAGES_SOLO_DIR: Path = Path(f"{STATIC_IMAGES_DIR}/solo")
STATIC_IMAGES_LEARN_DIR: Path = Path(f"{STATIC_IMAGES_DIR}/learn")
STATIC_IMAGES_CHOOSE_LEGION_DIR: Path = Path(f"{STATIC_IMAGES_DIR}/choose_legion")
STATIC_IMAGES_SANDBOX_DIR: Path = Path(f"{STATIC_IMAGES_DIR}/sandbox")
PLAYGROUND_PATH: Path = Path(f"{STATIC_IMAGES_SANDBOX_DIR}/playground.png")


class ActionableElement(BaseModel):
    image_path: Path | None
    center: tuple[int, int]

    def click(self, is_second_display: bool = True):
        x, y = self.center
        if is_second_display:
            x = x + 1920
        pyautogui.click(x, y)

class ActionableElementWithRectangle(ActionableElement):
    tl: tuple[int, int]
    br: tuple[int, int]


def expect_to_be_in_view(
    haystack_path: Path, needle: ActionableElement, threshold: int = 5
) -> bool:
    make_screenshot_by_given_display(path=haystack_path)
    center = match_template_center(
        haystack_path=haystack_path, needle_path=needle.image_path
    )
    x, y = center
    needle_x, needle_y = needle.center
    fit_x = needle_x - threshold <= x < needle_x + threshold
    fit_y = needle_y - threshold <= y < needle_y + threshold
    result = fit_x and fit_y
    logging.info("Current needle: %s", needle.image_path.stem)
    logging.info("Is needle in view?: %s", result)
    return result


class MainMenuNavigationButtons(BaseModel):
    multiplayer: ActionableElement = ActionableElement(
        image_path=STATIC_IMAGES_MAIN_MENU_DIR.joinpath("multiplayer_button.png"),
        center=(261, 268),
    )
    solo: ActionableElement = ActionableElement(
        image_path=STATIC_IMAGES_MAIN_MENU_DIR.joinpath("solo_button.png"),
        center=(263, 344),
    )
    learn: ActionableElement = ActionableElement(
        image_path=STATIC_IMAGES_MAIN_MENU_DIR.joinpath("learn_button.png"),
        center=(131, 412),
    )
    profile: ActionableElement = ActionableElement(
        image_path=STATIC_IMAGES_MAIN_MENU_DIR.joinpath("profile_button.png"),
        center=(146, 464),
    )
    leaderboards: ActionableElement = ActionableElement(
        image_path=STATIC_IMAGES_MAIN_MENU_DIR.joinpath("leaderboards_button.png"),
        center=(214, 514),
    )
    shop: ActionableElement = ActionableElement(
        image_path=STATIC_IMAGES_MAIN_MENU_DIR.joinpath("shop_button.png"),
        center=(122, 568),
    )
    guild: ActionableElement = ActionableElement(
        image_path=STATIC_IMAGES_MAIN_MENU_DIR.joinpath("guild_button.png"),
        center=(129, 621),
    )

    quit_: ActionableElement = ActionableElement(
        image_path=STATIC_IMAGES_MAIN_MENU_DIR.joinpath("quit_button.png"),
        center=(36, 1059),
    )

    bottom_buttons: ActionableElement = ActionableElement(
        image_path=STATIC_IMAGES_MAIN_MENU_DIR.joinpath("bottom_buttons.png"),
        center=(203, 1058),
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


class SoloViewNavigationButtons(BaseModel):
    campaign: ActionableElement = ActionableElement(
        image_path=STATIC_IMAGES_SOLO_DIR.joinpath("campaign_button.png"),
        center=(672, 688),
    )
    ai: ActionableElement = ActionableElement(
        image_path=STATIC_IMAGES_SOLO_DIR.joinpath("ai_button.png"), center=(960, 688)
    )
    weekly_challenge: ActionableElement = ActionableElement(
        image_path=STATIC_IMAGES_SOLO_DIR.joinpath("weekly_challenge_button.png"),
        center=(1245, 690),
    )
    back: ActionableElement = ActionableElement(
        image_path=STATIC_IMAGES_SOLO_DIR.joinpath("back_to_main_menu_button.png"),
        center=(1794, 995),
    )


class SoloView(BaseModel):
    static_screenshot: Path = Path(f"{STATIC_IMAGES_SOLO_DIR}/solo.png")
    dynamic_screenshot: Path = Path(f"{STATIC_IMAGES_SOLO_DIR}/solo_dynamic.png")
    navigation_buttons: SoloViewNavigationButtons = SoloViewNavigationButtons()

    def expect_to_be_in_view(self) -> bool:
        return expect_to_be_in_view(
            haystack_path=self.dynamic_screenshot, needle=self.navigation_buttons.ai
        )


solo_view = SoloView()


class LearnViewNavigationButtons(BaseModel):
    tutorial: ActionableElement = ActionableElement(
        image_path=STATIC_IMAGES_LEARN_DIR.joinpath("tutorial_button.png"),
        center=(531, 699),
    )
    top_games: ActionableElement = ActionableElement(
        image_path=STATIC_IMAGES_LEARN_DIR.joinpath("top_games_button.png"),
        center=(815, 680),
    )
    codex: ActionableElement = ActionableElement(
        image_path=STATIC_IMAGES_LEARN_DIR.joinpath("codex_button.png"),
        center=(1103, 689),
    )
    sandbox: ActionableElement = ActionableElement(
        image_path=STATIC_IMAGES_LEARN_DIR.joinpath("sandbox_button.png"),
        center=(1391, 690),
    )
    back: ActionableElement = ActionableElement(
        image_path=STATIC_IMAGES_LEARN_DIR.joinpath("back_to_main_menu_button.png"),
        center=(1794, 997),
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
        image_path=STATIC_IMAGES_CHOOSE_LEGION_DIR.joinpath("element_button.png"),
        center=(530, 434),
    )
    forsaken: ActionableElement = ActionableElement(
        image_path=STATIC_IMAGES_CHOOSE_LEGION_DIR.joinpath("forsaken_button.png"),
        center=(815, 435),
    )
    grove: ActionableElement = ActionableElement(
        image_path=STATIC_IMAGES_CHOOSE_LEGION_DIR.joinpath("grove_button.png"),
        center=(1103, 434),
    )
    mech: ActionableElement = ActionableElement(
        image_path=STATIC_IMAGES_CHOOSE_LEGION_DIR.joinpath("mech_button.png"),
        center=(1389, 434),
    )
    atlantean: ActionableElement = ActionableElement(
        image_path=STATIC_IMAGES_CHOOSE_LEGION_DIR.joinpath("atlantean_button.png"),
        center=(530, 800),
    )
    nomad: ActionableElement = ActionableElement(
        image_path=STATIC_IMAGES_CHOOSE_LEGION_DIR.joinpath("nomad_button.png"),
        center=(815, 799),
    )
    shrine: ActionableElement = ActionableElement(
        image_path=STATIC_IMAGES_CHOOSE_LEGION_DIR.joinpath("shrine_button.png"),
        center=(1103, 799),
    )
    divine: ActionableElement = ActionableElement(
        image_path=STATIC_IMAGES_CHOOSE_LEGION_DIR.joinpath("divine_button.png"),
        center=(1389, 801),
    )
    mastermind: ActionableElement = ActionableElement(
        image_path=STATIC_IMAGES_CHOOSE_LEGION_DIR.joinpath("mastermind_button.png"),
        center=(994, 958),
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
            needle=self.navigation_buttons.mastermind,
        )


choose_legion_view = ChooseLegionView()


class ShopTowersButtons(BaseModel):
    offset_marker: tuple[int, int] = (629, 1027)
    offset_x: int = 71
    offset_tl: tuple[int, int] = (597, 996)
    offset_br: tuple[int, int] = (661, 1060)
    tower_1: ActionableElementWithRectangle = ActionableElementWithRectangle(tl=(offset_x * 0 + offset_tl[0], offset_tl[1]), br=(offset_x * 0 + offset_br[0], offset_br[1]),
        image_path=None, center=(offset_x * 0 + offset_marker[0], 0 + offset_marker[1])
    )
    tower_2:  ActionableElementWithRectangle = ActionableElementWithRectangle(tl=(offset_x * 1 + offset_tl[0], offset_tl[1]), br=(offset_x * 1 + offset_br[0], offset_br[1]),
        image_path=None, center=(offset_x * 1 + offset_marker[0], 0 + offset_marker[1])
    )
    tower_3: ActionableElementWithRectangle = ActionableElementWithRectangle(tl=(offset_x * 2 + offset_tl[0], offset_tl[1]), br=(offset_x * 2 + offset_br[0], offset_br[1]),
        image_path=None, center=(offset_x *  2 + offset_marker[0], 0 + offset_marker[1])
    )
    tower_4: ActionableElementWithRectangle = ActionableElementWithRectangle(tl=(offset_x * 3 + offset_tl[0], offset_tl[1]), br=(offset_x * 3 + offset_br[0], offset_br[1]),
        image_path=None, center=(offset_x *  3 + offset_marker[0], 0 + offset_marker[1])
    )
    tower_5: ActionableElementWithRectangle = ActionableElementWithRectangle(tl=(offset_x * 4 + offset_tl[0], offset_tl[1]), br=(offset_x * 4 + offset_br[0], offset_br[1]),
        image_path=None, center=(offset_x * 4 + offset_marker[0], 0 + offset_marker[1])
    )
    tower_6: ActionableElementWithRectangle = ActionableElementWithRectangle(tl=(offset_x * 5 + offset_tl[0], offset_tl[1]), br=(offset_x * 5 + offset_br[0], offset_br[1]),
        image_path=None, center=(offset_x * 5 + offset_marker[0], 0 + offset_marker[1])
    )

    towers: list[ActionableElementWithRectangle] = [
        tower_1,
        tower_2,
        tower_3,
        tower_4,
        tower_5,
        tower_6,
    ]


class EventHistoryCoordinates(BaseModel):
    region: tuple[int, int] = (950, 332, 340, 580)
    tl: tuple[int, int] = (950, 332)
    br: tuple[int, int] = (340, 580)


class SandboxView(BaseModel):
    static_screenshot: Path = Path(f"{STATIC_IMAGES_SANDBOX_DIR}/sandbox.png")
    dynamic_screenshot: Path = Path(f"{STATIC_IMAGES_SANDBOX_DIR}/sandbox_dynamic.png")
    ready_button: ActionableElement = ActionableElement(
        image_path=STATIC_IMAGES_SANDBOX_DIR.joinpath("ready_button.png"),
        center=(959, 186),
    )
    start_button: ActionableElement = ActionableElement(
        image_path=STATIC_IMAGES_SANDBOX_DIR.joinpath("start_button.png"),
        center=(710, 36),
    )
    pause_button: ActionableElement = ActionableElement(
        image_path=STATIC_IMAGES_SANDBOX_DIR.joinpath("pause_button.png"),
        center=(961, 134),
    )
    play_button: ActionableElement = ActionableElement(
        image_path=STATIC_IMAGES_SANDBOX_DIR.joinpath("play_button.png"),
        center=(961, 133),
    )
    clear_button: ActionableElement = ActionableElement(
        image_path=STATIC_IMAGES_SANDBOX_DIR.joinpath("clear_button.png"),
        center=(762, 36),
    )
    upgrade_king_menu_button: ActionableElement = ActionableElement(
        image_path=STATIC_IMAGES_SANDBOX_DIR.joinpath("upgrade_king_menu_button.png"),
        center=(549, 1009),
    )
    wave_phase_indicator: ActionableElement = ActionableElement(
        image_path=STATIC_IMAGES_SANDBOX_DIR.joinpath("wave_phase_indicator.png"),
        center=(961, 109),
    )

    event_history_text: ActionableElement = ActionableElement(
        image_path=STATIC_IMAGES_SANDBOX_DIR.joinpath("event_history_text.png"),
        center=(1004, 344),
    )
    event_history_coordinates: EventHistoryCoordinates = EventHistoryCoordinates()

    shop_towers_buttons: ShopTowersButtons = ShopTowersButtons()
    grid: list[list[GridRectangle]] = grid

    def expect_ready_button_to_be_in_view(self) -> bool:
        return expect_to_be_in_view(
            haystack_path=self.dynamic_screenshot, needle=self.ready_button
        )

    def expect_wave_phase_indicator_to_be_in_view(self) -> bool:
        return expect_to_be_in_view(
            haystack_path=self.dynamic_screenshot, needle=self.wave_phase_indicator
        )

    def add_shop_towers_buttons_markers(
        self,
        image_path: Path = Path(f"app/images/screenshot.png"),
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
        image_path: Path = Path(f"app/images/screenshot.png"),
        image_result_path: Path = Path(f"{IMAGES_DIR}/res1.png"),
    ) -> Path:
        img = cv.imread(str(image_path))
        towers = self.shop_towers_buttons.towers
        for tower in towers:
            cv.rectangle(
                img=img, pt1=tower.tl,pt2=tower.br, color=(0, 255, 0), thickness=4
            )
        cv.imwrite(str(image_result_path), img)
        return image_result_path

    def match_template_shop(self,
        image_path: str = f"{IMAGES_DIR}/screenshot.png",
        grid: ArenaGrid | ShopGrid = ShopGrid,
        image_result_path: str = f"{IMAGES_DIR}/res1.png",
    ) -> list[str]:
        img_rgb = cv.imread(image_path)
        towers = self.shop_towers_buttons.towers

        icons = Path(f"{IMAGES_DIR}/icons")
        matched_units = []
        for tower in towers:
           tower_img =cv.cvtColor(img_rgb[tower.tl[1] : tower.br[1],
                                                    tower.tl[0] : tower.br[0]], cv.COLOR_BGR2GRAY)
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
                    if mask[pt[1] + int(round(h / 2)), pt[0] + int(round(w / 2))] != 255:
                        mask[pt[1] : pt[1] + h, pt[0] : pt[0] + w] = 255
                        cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 1)
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
