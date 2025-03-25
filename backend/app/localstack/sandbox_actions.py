import logging
import time
from pathlib import Path

import pyautogui

from app.localstack.images import (
    make_region_screenshot_by_actionable_element,
    ocr_by_path,
)
from app.localstack.views import sandbox_view

STATIC_IMAGES_SANDBOX_DIR = Path("app/images/static/sandbox")


def click_to_activate_game_window() -> None:
    pyautogui.click(x=1920 + 100, y=250)


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


def send_chat_message_by_message(message: str) -> None:
    pyautogui.press("Enter")
    time.sleep(0.05)
    pyautogui.typewrite(message=message)
    pyautogui.press("Enter")
    return None


def set_game_playback_by_playback_value(playback_value: float = 10.0) -> None:
    click_to_activate_game_window()
    send_chat_message_by_message(message=f"-playback {playback_value}")
    return None


def set_sandbox_to_initial_state() -> None:
    click_to_activate_game_window()
    send_chat_message_by_message(message="-playback 1.0")
    send_chat_message_by_message(message="-wave 1")
    send_chat_message_by_message(message="-clear")
    is_play_bnutton_in_view = sandbox_view.expect_play_button_to_be_in_view()
    pyautogui.press("F1")
    time.sleep(4)
    if is_play_bnutton_in_view is True:
        sandbox_view.play_button.click()
    sandbox_view.playground_hover_area.select_region()
    time.sleep(0.5)
    pyautogui.press("Y")
    send_chat_message_by_message(message="-wave 1")
    send_chat_message_by_message(message="-clear")
    send_chat_message_by_message(message="-heal")
    set_initial_sandbox_view_position()
    return None


def make_screenshot_of_event_history_log() -> Path:
    click_to_activate_game_window()

    pyautogui.keyDown("tab")
    pyautogui.press("winleft")

    path = make_region_screenshot_by_actionable_element(
        actionable_element=sandbox_view.event_history_log
    )

    pyautogui.keyUp("tab")

    return path


def make_screenshot_of_event_text() -> Path:
    pyautogui.press("F2")
    path = make_region_screenshot_by_actionable_element(
        actionable_element=sandbox_view.event_text
    )
    return path


def make_screenshot_of_wave_until_text() -> Path:
    path = make_region_screenshot_by_actionable_element(
        actionable_element=sandbox_view.until_wave_text
    )
    return path


def place_towers_and_wait_until_leak_ocr(
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

        event_text_path = make_screenshot_of_event_text()
        filtered_results = ocr_by_path(path=event_text_path)
        # event_history_log_path = make_screenshot_of_event_history_log()
        # ocr_by_path(path=event_history_log_path)

        sandbox_view.play_button.click()

    sandbox_view.pause_button.click()

    return filtered_results


def extract_numbers(text: str) -> str:
    return "".join(filter(str.isdigit, text))


def place_towers_and_wait_until_leak_hp_bar(
    tower_position: int, tower_amount: int
) -> int:
    place_towers_by_tower_position_and_tower_amount(
        tower_position=tower_position, tower_amount=tower_amount
    )
    set_game_playback_by_playback_value(playback_value=7)
    sandbox_view.start_button.click()

    time.sleep(1)
    is_full_hp = True
    while is_full_hp is True:
        time.sleep(0.5)
        logging.info("Hp bar is full")
        is_full_hp = sandbox_view.expect_full_hp_bar_to_be_in_view()

    wave_status = True
    while wave_status is True:
        logging.info("This is still wave phase")
        wave_status = sandbox_view.expect_wave_phase_indicator_to_be_in_view()

    path = make_screenshot_of_wave_until_text()
    text = ocr_by_path(path=path, filter_word="W")
    logging.info("Leak happened, waiting for %s", text)
    wait_until_text_splitted = text[0]
    leak_wave = int(extract_numbers(wait_until_text_splitted))
    logging.info("Wave that leak happened: %d", leak_wave - 1)
    sandbox_view.pause_button.click()

    return leak_wave


def find_tower_amount_to_hold_until_given_leak_wave(
    tower_position: int, leak_wave: int
) -> int:
    current_leak_wave = 0
    tower_amount = 1
    while current_leak_wave < leak_wave:
        set_initial_sandbox_view_position()
        current_leak_wave = place_towers_and_wait_until_leak_hp_bar(
            tower_position=tower_position, tower_amount=tower_amount
        )
        set_sandbox_to_initial_state()
        tower_amount = tower_amount + 1
        logging.info("current_leak_wave is: %s", current_leak_wave)
        logging.info("leak_wave is: %s", leak_wave)
        logging.info("current_leak_wave < leak_wave %s", current_leak_wave < leak_wave)

    return tower_amount - 1


def check_wave_indicator() -> bool:
    return sandbox_view.expect_wave_phase_indicator_to_be_in_view()


def set_initial_sandbox_view_position() -> None:
    click_to_activate_game_window()
    pyautogui.press("F1")
    time.sleep(0.3)
    pyautogui.scroll(-500)
    return None
