import logging

from app.localstack.images import (
    make_region_screenshot_by_actionable_element,
)
from app.localstack.navigation import (
    choose_legion_view_choose_element_legion,
    navigate_from_learn_to_choose_legion_view,
    navigate_from_main_to_learn_view,
)
from app.localstack.sandbox_actions import (
    flow_based_on_stats,
)
from app.localstack.views import sandbox_view


def navigate_from_main_to_sandbox():
    navigate_from_main_to_learn_view()
    navigate_from_learn_to_choose_legion_view()
    choose_legion_view_choose_element_legion()


logging.basicConfig(level=logging.INFO)


def main():
    # f = read_creatures()
    # g = read_creatures_by_stage(5)
    # gg = calculate_stage_stats(5)
    flow_based_on_stats(1, 3)

    import ipdb

    ipdb.set_trace()
    f = sandbox_view

    make_region_screenshot_by_actionable_element(actionable_element=f.current_gold_text)
    # f.expect_ready_button_to_be_in_view()
    # path = make_screenshot_of_wave_until_text()
    # text = ocr_by_path(path=path)
    # import ipdb
    # ipdb.set_trace()
    navigate_from_main_to_sandbox()
    # set_initial_sandbox_view_position()
    # place_towers_and_wait_until_leak_hp_bar(1, 30)
    # set_sandbox_to_initial_state()
    # find_tower_amount_to_hold_until_given_leak_wave(tower_position=1, leak_wave=5)
    import ipdb

    ipdb.set_trace()
    # navigate_from_main_to_sandbox()

    # set_initial_sandbox_view_position()


if __name__ == "__main__":
    main()
