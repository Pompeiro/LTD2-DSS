import logging
import time
from pathlib import Path

import pyautogui
from pydantic import BaseModel

from app.api.routes.arenas_client import (
    compare_arena_vs_stage_stats,
    update_arena,
)
from app.api.routes.creatures_client import sort_units_as_counters_by_stage
from app.localstack.images import (
    make_region_screenshot_by_actionable_element,
    ocr_by_path,
    ocr_digits_by_path,
)
from app.localstack.models import ActionableElement, Grid
from app.localstack.views import sandbox_view
from app.playground_area_coordinates import grid

STATIC_IMAGES_SANDBOX_DIR = Path("app/images/static/sandbox")


class GameState(BaseModel):
    current_gold: int = 0
    current_income: int = 0
    current_mythium: int = 0
    current_workers: int = 0
    current_fighter_value: int = 0

    next_wave: int = 0

    def get_value_of_actionable_element(
        self, actionable_element: ActionableElement
    ) -> int:
        path = make_region_screenshot_by_actionable_element(
            actionable_element=actionable_element
        )
        if actionable_element == sandbox_view.current_workers_text:
            actionable_element.draw_rectangle()
        digits = ocr_digits_by_path(path=path)
        return digits

    def update_current_gold(self) -> None:
        self.current_gold = self.get_value_of_actionable_element(
            actionable_element=sandbox_view.current_gold_text
        )

    def update_current_income(self) -> None:
        self.current_income = self.get_value_of_actionable_element(
            actionable_element=sandbox_view.current_income_text
        )

    def update_current_mythium(self) -> None:
        self.current_mythium = self.get_value_of_actionable_element(
            actionable_element=sandbox_view.current_mythium_text
        )

    def update_current_workers(self) -> None:
        self.current_workers = self.get_value_of_actionable_element(
            actionable_element=sandbox_view.current_workers_text
        )

    def update_current_fighter_value(self) -> None:
        self.current_fighter_value = self.get_value_of_actionable_element(
            actionable_element=sandbox_view.current_fighter_value_text
        )

    def update_next_wave(self) -> None:
        self.next_wave = self.get_value_of_actionable_element(
            actionable_element=sandbox_view.until_wave_text
        )

    def update_whole_game_state(self) -> None:
        self.update_current_gold()
        self.update_current_income()
        self.update_current_mythium()
        self.update_current_workers()
        # self.update_current_fighter_value()
        self.update_next_wave()


game_state = GameState()


def click_to_activate_game_window() -> None:
    pyautogui.click(x=1920 + 100, y=250)


def fill_whole_grid_with_towers() -> None:
    click_to_activate_game_window()
    for i, row in enumerate(grid.grid):
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
    for row in grid.grid:
        if placed_towers_counter == tower_amount:
            break
        for column in row:
            sandbox_view.shop_towers_buttons.towers[tower_position].click()
            column.click()
            column.click()
            placed_towers_counter = placed_towers_counter + 1
            if placed_towers_counter == tower_amount:
                break


def place_towers_on_columns_by_tower_position_and_tower_amount(
    tower_position: int, tower_amount: int
) -> None:
    click_to_activate_game_window()
    placed_towers_counter = 0
    transposed_grid = list(zip(*grid.grid, strict=False))
    for row in transposed_grid:
        if placed_towers_counter == tower_amount:
            break
        for column in row:
            sandbox_view.shop_towers_buttons.towers[tower_position].click()
            column.click()
            column.click()
            placed_towers_counter = placed_towers_counter + 1
            if placed_towers_counter == tower_amount:
                break


def place_towers_on_opposite_columns_by_tower_position_and_tower_amount(
    tower_position: int, tower_amount: int
) -> None:
    click_to_activate_game_window()
    placed_towers_counter = 0
    transposed_grid = list(zip(*grid.grid, strict=False))
    for i, row in enumerate(transposed_grid):
        if placed_towers_counter == tower_amount:
            break
        for j in range(0, len(row) * 2):
            board_row = j // 2
            column = transposed_grid[-1 * (i + 1)][board_row]
            if j % 2 == 0:
                column = transposed_grid[i][board_row]

            sandbox_view.shop_towers_buttons.towers[tower_position].click()
            column.click()
            column.click()
            placed_towers_counter = placed_towers_counter + 1
            if placed_towers_counter == tower_amount:
                break


def place_towers_on_opposite_columns_by_tower_id(tower_id: str) -> None:
    click_to_activate_game_window()
    transposed_grid: Grid = list(zip(*grid.grid, strict=True))
    tower_placed = False
    for i, row in enumerate(transposed_grid):
        for j in range(0, len(row) * 2):
            board_row = j // 2
            column = transposed_grid[-1 * (i + 1)][board_row]
            if j % 2 == 0:
                column = transposed_grid[i][board_row]
            if column.unit_id is None:
                column.place_tower_by_id(tower_to_place_id=tower_id)
                tower_placed = True
            if tower_placed is True:
                break
        if tower_placed is True:
            break


def send_chat_message_by_message(message: str) -> None:
    pyautogui.press("Enter")
    time.sleep(0.05)
    pyautogui.typewrite(message=message)
    time.sleep(0.25)  # avoid button to still be pressed
    pyautogui.press("Enter")
    return None


def set_game_playback_by_playback_value(playback_value: float = 10.0) -> None:
    click_to_activate_game_window()
    send_chat_message_by_message(message=f"-playback {playback_value}")
    return None


def set_sandbox_to_initial_state() -> None:
    click_to_activate_game_window()
    send_chat_message_by_message(message="-playback 1.0")
    send_chat_message_by_message(message="-wave 0")
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
    place_towers_on_opposite_columns_by_tower_position_and_tower_amount(
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
    leak_wave = int(extract_numbers(wait_until_text_splitted)) - 1
    logging.info("Wave that leak happened: %d", leak_wave)
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


def flow_based_on_stats():
    set_initial_sandbox_view_position()

    place_towers_on_opposite_columns_by_tower_id(tower_id="windhawk_unit_id")
    place_towers_on_opposite_columns_by_tower_id(tower_id="windhawk_unit_id")

    set_game_playback_by_playback_value(playback_value=7)
    sandbox_view.start_button.click()

    wave_status = False
    for _ in range(5):
        while wave_status is False:
            wave_status = sandbox_view.expect_wave_phase_indicator_to_be_in_view()
            logging.info("This is not wave phase")

        while wave_status is True:
            logging.info("This is still wave phase")
            wave_status = sandbox_view.expect_wave_phase_indicator_to_be_in_view()

        logging.info("wave phase finished")
        sandbox_view.pause_button.click()

        game_state.update_whole_game_state()
        units = grid.get_all_units_id()
        arena = update_arena(units=units, arena_id=1, clear_units=True)
        compare_result = compare_arena_vs_stage_stats(
            arena_id=1, stage_id=game_state.next_wave
        )
        print(arena)
        print(compare_result)

        while compare_result.arena_vs_stage_seconds_to_kill_diff >= 7:
            set_game_playback_by_playback_value(playback_value=0.5)
            place_towers_on_opposite_columns_by_tower_id(tower_id="windhawk_unit_id")
            units = grid.get_all_units_id()
            update_arena(units=units, arena_id=1, clear_units=True)
            compare_result = compare_arena_vs_stage_stats(
                arena_id=1, stage_id=game_state.next_wave
            )
            logging.info("placed additional windhawk")

        sandbox_view.play_button.click()
        set_game_playback_by_playback_value(playback_value=7)


def _place_counter_tower_for_next_stage_by_next_stage(
    next_stage: int, arena_vs_stage_seconds_to_kill_diff_threshold: float
) -> None:
    counters = sort_units_as_counters_by_stage(stage=next_stage)
    compare_result = compare_arena_vs_stage_stats(
        arena_id=1, stage_id=game_state.next_wave
    )
    while (
        compare_result.arena_vs_stage_seconds_to_kill_diff
        >= arena_vs_stage_seconds_to_kill_diff_threshold
    ):
        set_game_playback_by_playback_value(playback_value=0.5)
        place_towers_on_opposite_columns_by_tower_id(tower_id=counters[0].id)
        units = grid.get_all_units_id()
        update_arena(units=units, arena_id=1, clear_units=True)
        compare_result = compare_arena_vs_stage_stats(
            arena_id=1, stage_id=game_state.next_wave
        )
        logging.info("placed additional %s", counters[0].id)


def flow_based_on_next_wave_type():
    set_sandbox_to_initial_state()

    game_state.update_whole_game_state()
    update_arena(units=[], arena_id=1, clear_units=True)

    arena_vs_stage_seconds_to_kill_diff_threshold = 7
    _place_counter_tower_for_next_stage_by_next_stage(
        next_stage=1,
        arena_vs_stage_seconds_to_kill_diff_threshold=arena_vs_stage_seconds_to_kill_diff_threshold,
    )
    set_game_playback_by_playback_value(playback_value=7)
    sandbox_view.start_button.click()

    wave_status = False
    for current_stage in range(1, 10, 1):
        while wave_status is False:
            wave_status = sandbox_view.expect_wave_phase_indicator_to_be_in_view()
            logging.info("This is not wave phase")

        while wave_status is True:
            logging.info("This is still wave phase")
            wave_status = sandbox_view.expect_wave_phase_indicator_to_be_in_view()

        logging.info("wave phase finished")
        sandbox_view.pause_button.click()

        game_state.update_whole_game_state()
        units = grid.get_all_units_id()
        logging.info("Current game state next wave %s", game_state.next_wave)
        logging.info("Current game state next wave by for loop %s", current_stage + 1)
        if game_state.next_wave - (current_stage + 1):
            logging.error("Next wave was not recognized properly")
        update_arena(units=units, arena_id=1, clear_units=True)

        if game_state.next_wave >= 6:
            arena_vs_stage_seconds_to_kill_diff_threshold = 10 - (
                game_state.next_wave * 1.5
            )

        set_game_playback_by_playback_value(playback_value=0.5)
        _place_counter_tower_for_next_stage_by_next_stage(
            next_stage=game_state.next_wave,
            arena_vs_stage_seconds_to_kill_diff_threshold=arena_vs_stage_seconds_to_kill_diff_threshold,
        )

        sandbox_view.play_button.click()
        set_game_playback_by_playback_value(playback_value=7)


def check_wave_indicator() -> bool:
    return sandbox_view.expect_wave_phase_indicator_to_be_in_view()


def set_initial_sandbox_view_position() -> None:
    click_to_activate_game_window()
    pyautogui.press("F1")
    time.sleep(0.3)
    pyautogui.scroll(-500)
    return None
