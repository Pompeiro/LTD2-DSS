from app.localstack.navigation import (
    choose_legion_view_choose_element_legion,
    navigate_from_learn_to_choose_legion_view,
    navigate_from_main_to_learn_view,
)
from app.localstack.views import sandbox_view


def navigate_from_main_to_sandbox():
    navigate_from_main_to_learn_view()
    navigate_from_learn_to_choose_legion_view()
    choose_legion_view_choose_element_legion()


def main():
    f = sandbox_view
    g = f.match_template_shop()
    print(g)
    navigate_from_main_to_sandbox()


if __name__ == "__main__":
    main()
