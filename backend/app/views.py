from pathlib import Path
from typing import Annotated

import cv2 as cv
import pyautogui
from fastapi import Query
from pydantic import BaseModel

from app.playground_area_coordinates import GridRectangle, grid

IMAGES_DIR = "app/images"
STATIC_IMAGES_DIR = "app/images/static"
STATIC_IMAGES_MAIN_MENU_DIR = Path("app/images/static/main_menu")
STATIC_IMAGES_SOLO_DIR = Path("app/images/static/solo")
STATIC_IMAGES_LEARN_DIR = Path("app/images/static/learn")
STATIC_IMAGES_CHOOSE_LEGION_DIR = Path("app/images/static/choose_legion")
STATIC_IMAGES_SANDBOX_DIR = Path("app/images/static/sandbox")


class ActionableElement(BaseModel):
    image_path: Path | None
    center: tuple[int, int]

    def click(self, is_second_display: bool = True):
        x, y = self.center
        if is_second_display:
            x = x + 1920
        pyautogui.click(x, y)


def expect_to_be_in_view(
    haystack_path: Path, needle: ActionableElement, threshold: int = 5
) -> bool:
    make_ss_sync(save_to=haystack_path)
    center = match_template_center(
        haystack_path=haystack_path, needle_path=needle.image_path
    )
    x, y = center
    needle_x, needle_y = needle.center
    fit_x = needle_x - threshold <= x < needle_x + threshold
    fit_y = needle_y - threshold <= y < needle_y + threshold
    return fit_x and fit_y


def make_ss_sync(save_to: Path, display: Annotated[int, Query(ge=1, le=2)] = 2):
    regions = {1: (0, 0, 1920, 1080), 2: (1920, 0, 1920, 1080)}
    screenshot = pyautogui.screenshot(region=regions.get(display))
    screenshot.save(save_to)


def match_template_center(haystack_path: Path, needle_path: Path) -> tuple[int, int]:
    haystack_img = cv.imread(haystack_path, cv.IMREAD_UNCHANGED)
    needle_img = cv.imread(needle_path, cv.IMREAD_UNCHANGED)

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
    offset: tuple[int, int] = (629, 1027)
    tower_1: ActionableElement = ActionableElement(
        image_path=None, center=(0 + offset[0], 0 + offset[1])
    )
    tower_2: ActionableElement = ActionableElement(
        image_path=None, center=(71 + offset[0], 0 + offset[1])
    )
    tower_3: ActionableElement = ActionableElement(
        image_path=None, center=(71 * 2 + offset[0], 0 + offset[1])
    )
    tower_4: ActionableElement = ActionableElement(
        image_path=None, center=(71 * 3 + offset[0], 0 + offset[1])
    )
    tower_5: ActionableElement = ActionableElement(
        image_path=None, center=(71 * 4 + offset[0], 0 + offset[1])
    )
    tower_6: ActionableElement = ActionableElement(
        image_path=None, center=(355 + offset[0], 0 + offset[1])
    )

    towers: list[ActionableElement] = [
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


sandbox_view = SandboxView()
