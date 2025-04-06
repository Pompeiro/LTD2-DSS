from pathlib import Path

import cv2 as cv
import pyautogui
from pydantic import BaseModel, computed_field


class Point(BaseModel):
    x: int
    y: int


class Rectangle(BaseModel):
    tl: Point
    br: Point

    @computed_field
    def width(self) -> int:
        return self.br.x - self.tl.x

    @computed_field
    def height(self) -> int:
        return self.br.y - self.tl.y

    @computed_field
    def center(self) -> Point:
        x: int = self.tl.x + (self.width // 2)
        y: int = self.tl.y + (self.height // 2)
        return Point(x=x, y=y)

    @computed_field
    def region(self) -> tuple[int, int, int, int]:
        return (self.tl.x, self.tl.y, self.br.x, self.br.y)

    @computed_field
    def region_relative(self) -> tuple[int, int, int, int]:
        return (self.tl.x, self.tl.y, self.width, self.height)


class GridTile(BaseModel):
    rectangle: Rectangle
    unit_id: str | None = None

    def place_tower_by_id(
        self,
        tower_to_place_id: str,
        current_shop_towers: tuple[str] = (
            "proton_unit_id",
            "aqua_spirit_unit_id",
            "windhawk_unit_id",
            "mudman_unit_id",
            "disciple_unit_id",
            "fire_lord_unit_id",
        ),
        is_second_display: bool = True,
    ) -> None:
        hotkeys: list[str] = ["q", "w", "e", "r", "t", "y"]
        current_shop_tower_to_hotkey_map = dict(
            zip(current_shop_towers, hotkeys, strict=False)
        )
        pyautogui.press(current_shop_tower_to_hotkey_map.get(tower_to_place_id))

        x, y = self.rectangle.center.dict().values()
        if is_second_display:
            x = x + 1920
        pyautogui.click(x, y)
        pyautogui.click(x, y)

        self.unit_id = tower_to_place_id 



    def click(self, is_second_display: bool = True):
        x, y = self.rectangle.center.dict().values()
        if is_second_display:
            x = x + 1920
        pyautogui.click(x, y)


class Grid(BaseModel):
    grid: list[list[GridTile]]

    @computed_field
    def grid_flatten_list(self) -> list[GridTile]:
        return sum(self.grid, [])

    def get_all_occupied_tiles(self) -> list[str]:
        return list(
            filter(lambda tile: tile.unit_id is not None, self.grid_flatten_list)
        )

    def get_all_units_id(self) -> list[str]:
        return [tile.unit_id for tile in self.get_all_occupied_tiles()]
        return list(
            filter(lambda tile: tile.unit_id is not None, self.grid_flatten_list)
        )


class ActionableElement(BaseModel):
    rectangle: Rectangle
    image_path: Path | None = None
    is_occupied: bool = False

    def click(self, is_second_display: bool = True):
        x, y = self.rectangle.center.dict().values()
        if is_second_display:
            x = x + 1920
        pyautogui.click(x, y)

    def select_region(self, is_second_display: bool = True):
        tl_x, tl_y, br_x, br_y = self.rectangle.region
        if is_second_display:
            tl_x = tl_x + 1920
            br_x = br_x + 1920
        pyautogui.mouseDown(tl_x, tl_y)
        pyautogui.moveTo(br_x, br_y)
        pyautogui.mouseUp()

    def draw_rectangle(self):
        cv.imwrite(
            self.image_path,
            cv.rectangle(
                img=cv.imread(self.image_path),
                pt1=(0, 0),
                pt2=(self.rectangle.width - 1, self.rectangle.height - 1),
                color=(255, 255, 255),
            ),
        )
