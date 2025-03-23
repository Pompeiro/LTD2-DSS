from pathlib import Path

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
