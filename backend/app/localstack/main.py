import logging

from app.localstack.navigation import (
    choose_legion_view_choose_element_legion,
    navigate_from_learn_to_choose_legion_view,
    navigate_from_main_to_learn_view,
)
from app.localstack.sandbox_actions import (
    place_towers_and_wait_until_leak,
)
from app.localstack.views import sandbox_view


def navigate_from_main_to_sandbox():
    navigate_from_main_to_learn_view()
    navigate_from_learn_to_choose_legion_view()
    choose_legion_view_choose_element_legion()


logging.basicConfig(level=logging.INFO)


def main():
    f = sandbox_view
    f.expect_ready_button_to_be_in_view()
    place_towers_and_wait_until_leak(1, 3)
    # navigate_from_main_to_sandbox()

    # set_initial_sandbox_view_position()


if __name__ == "__main__":
    main()
