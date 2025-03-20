from app.localstack.navigation import navigate_from_main_to_learn_view, navigate_from_main_to_solo_view, navigate_from_learn_to_choose_legion_view, choose_legion_view_choose_element_legion
from app.localstack.sandbox_actions import check_wave_indicator, place_towers_flow, fill_whole_grid_with_towers,  ocr_event_history_log, set_initial_sandbox_view_position, place_towers_by_tower_position_and_tower_amount, set_game_playback_by_playback_value
from app.localstack.images import match_template_shop, make_screenshot_by_given_display
from app.localstack.views import sandbox_view
def navigate_from_main_to_sandbox():
    navigate_from_main_to_learn_view()
    navigate_from_learn_to_choose_legion_view()
    choose_legion_view_choose_element_legion()

def main():
    f=sandbox_view
    g=f.match_template_shop()
    navigate_from_main_to_sandbox()

    

if __name__ == "__main__":
    main()
