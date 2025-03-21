import logging
import time
from pathlib import Path

import easyocr
import pyautogui

from app.localstack.images import make_screenshot_by_given_region_and_display
from app.localstack.views import sandbox_view

STATIC_IMAGES_SANDBOX_DIR = Path("app/images/static/sandbox")


def click_to_activate_game_window() -> None:
    pyautogui.click(x=1920 + 100, y=100)


def fill_whole_grid_with_towers() -> None:
    click_to_activate_game_window()
    for i, row in enumerate(sandbox_view.grid):
        for column in row:
            if i == 7:
                i = 6
            sandbox_view.shop_towers_buttons.towers[i].click()
            column.click()
            column.click()
    return None


def place_towers_by_tower_position_and_tower_amount(
    tower_position: int, tower_amount: int
) -> None:
    click_to_activate_game_window()
    placed_towers_counter = 0
    for row in sandbox_view.grid:
        if placed_towers_counter == tower_amount:
            break
        for column in row:
            sandbox_view.shop_towers_buttons.towers[tower_position].click()
            column.click()
            column.click()
            placed_towers_counter = placed_towers_counter + 1
            if placed_towers_counter == tower_amount:
                break


def set_game_playback_by_playback_value(playback_value: float = 5.0) -> None:
    click_to_activate_game_window()
    pyautogui.press("Enter")
    pyautogui.typewrite(message=f"-playback {playback_value}")
    pyautogui.press("Enter")
    return None


def open_and_filter_event_log() -> Path:
    click_to_activate_game_window()

    pyautogui.keyDown("tab")
    pyautogui.press("winleft")

    path = make_screenshot_by_given_region_and_display(
        region=sandbox_view.event_history_coordinates.region,
        display=2,
        path=STATIC_IMAGES_SANDBOX_DIR.joinpath("event_history_log.png"),
    )

    pyautogui.keyUp("tab")

    reader = easyocr.Reader(["en"])

    results = reader.readtext(str(path), detail=False)
    filtered_results = list(filter(lambda x: "leak" in x, results))

    return filtered_results


def place_towers_and_wait_until_leak(
    tower_position: int, tower_amount: int
) -> list[str]:
    place_towers_by_tower_position_and_tower_amount(
        tower_position=tower_position, tower_amount=tower_amount
    )
    set_game_playback_by_playback_value(playback_value=5.0)
    sandbox_view.start_button.click()

    filtered_results = []
    while len(filtered_results) < 1:
        time.sleep(1)
        wave_status = True
        while wave_status is True:
            time.sleep(0.04)
            logging.info("This is still wave phase")
            wave_status = sandbox_view.expect_wave_phase_indicator_to_be_in_view()

        logging.info("wave phase finished")
        sandbox_view.pause_button.click()

        filtered_results = open_and_filter_event_log()

        sandbox_view.play_button.click()

    sandbox_view.pause_button.click()

    return filtered_results


def check_wave_indicator() -> bool:
    return sandbox_view.expect_wave_phase_indicator_to_be_in_view()


def ocr_event_history_log() -> list[str]:
    reader = easyocr.Reader(["en"])
    results = reader.readtext(
        str(STATIC_IMAGES_SANDBOX_DIR.joinpath("event_history_log.png")), detail=False
    )
    filtered_results = list(filter(lambda x: "leak" in x, results))
    return filtered_results


def set_initial_sandbox_view_position() -> None:
    click_to_activate_game_window()
    pyautogui.press("F1")
    time.sleep(0.3)
    pyautogui.scroll(-500)
    return None
