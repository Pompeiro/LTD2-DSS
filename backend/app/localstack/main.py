import logging

from app.localstack.navigation import (
    choose_legion_view_choose_element_legion,
    navigate_from_learn_to_choose_legion_view,
    navigate_from_main_to_learn_view,
)
from app.localstack.sandbox_actions import (
    find_tower_amount_to_hold_until_given_leak_wave,
place_towers_on_opposite_columns_by_tower_position_and_tower_amount
)

from app.localstack.views import sandbox_view

def navigate_from_main_to_sandbox():
    navigate_from_main_to_learn_view()
    navigate_from_learn_to_choose_legion_view()
    choose_legion_view_choose_element_legion()


logging.basicConfig(level=logging.INFO)


def main():
    f = sandbox_view.grid
    place_towers_on_opposite_columns_by_tower_position_and_tower_amount(2,5)
    import ipdb
    ipdb.set_trace()
    # f.expect_ready_button_to_be_in_view()
    # path = make_screenshot_of_wave_until_text()
    # text = ocr_by_path(path=path)
    # import ipdb
    # ipdb.set_trace()
    navigate_from_main_to_sandbox()
    find_tower_amount_to_hold_until_given_leak_wave(tower_position=5, leak_wave=8)
    import ipdb

    ipdb.set_trace()
    # navigate_from_main_to_sandbox()

    # set_initial_sandbox_view_position()


if __name__ == "__main__":
    main()
