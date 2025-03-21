import logging

from app.localstack.navigation import (
    choose_legion_view_choose_element_legion,
    navigate_from_learn_to_choose_legion_view,
    navigate_from_main_to_learn_view,
)
from app.localstack.sandbox_actions import (
    place_towers_and_wait_until_leak,
)


def navigate_from_main_to_sandbox():
    navigate_from_main_to_learn_view()
    navigate_from_learn_to_choose_legion_view()
    choose_legion_view_choose_element_legion()


logging.basicConfig(level=logging.INFO)


def main():
    place_towers_and_wait_until_leak(1, 3)
    # navigate_from_main_to_sandbox()


if __name__ == "__main__":
    main()
