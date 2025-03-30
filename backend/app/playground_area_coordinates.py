from app.localstack.models import GridTile, Point, Rectangle

OFFSET = (718, 348)

ROW_1_Y = 5 + OFFSET[1]

ROW_1_1_X = 65 + OFFSET[0]
rectangle_1_1: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_1_1_X, y=ROW_1_Y), br=Point(x=ROW_1_1_X + 38, y=ROW_1_Y + 31)
    )
)
ROW_1_2_X = 104 + OFFSET[0]
rectangle_1_2: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_1_2_X, y=ROW_1_Y), br=Point(x=ROW_1_2_X + 38, y=ROW_1_Y + 31)
    )
)
ROW_1_3_X = 143 + OFFSET[0]
rectangle_1_3: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_1_3_X, y=ROW_1_Y), br=Point(x=ROW_1_3_X + 40, y=ROW_1_Y + 31)
    )
)
ROW_1_4_X = 183 + OFFSET[0]
rectangle_1_4: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_1_4_X, y=ROW_1_Y), br=Point(x=ROW_1_4_X + 40, y=ROW_1_Y + 31)
    )
)
ROW_1_5_X = 222 + OFFSET[0]
rectangle_1_5: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_1_5_X, y=ROW_1_Y), br=Point(x=ROW_1_5_X + 41, y=ROW_1_Y + 31)
    )
)
ROW_1_6_X = 262 + OFFSET[0]
rectangle_1_6: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_1_6_X, y=ROW_1_Y), br=Point(x=ROW_1_6_X + 40, y=ROW_1_Y + 31)
    )
)
ROW_1_7_X = 301 + OFFSET[0]
rectangle_1_7: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_1_7_X, y=ROW_1_Y), br=Point(x=ROW_1_7_X + 41, y=ROW_1_Y + 31)
    )
)
ROW_1_8_X = 341 + OFFSET[0]
rectangle_1_8: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_1_8_X, y=ROW_1_Y), br=Point(x=ROW_1_8_X + 41, y=ROW_1_Y + 31)
    )
)
ROW_1_9_X = 381 + OFFSET[0]
rectangle_1_9: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_1_9_X, y=ROW_1_Y), br=Point(x=ROW_1_9_X + 41, y=ROW_1_Y + 31)
    )
)

row_1 = [
    rectangle_1_1,
    rectangle_1_2,
    rectangle_1_3,
    rectangle_1_4,
    rectangle_1_5,
    rectangle_1_6,
    rectangle_1_7,
    rectangle_1_8,
    rectangle_1_9,
]

ROW_2_Y = 36 + OFFSET[1]

ROW_2_1_X = 61 + OFFSET[0]
rectangle_2_1: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_2_1_X, y=ROW_2_Y), br=Point(x=ROW_2_1_X + 39, y=ROW_2_Y + 33)
    )
)
ROW_2_2_X = 101 + OFFSET[0]
rectangle_2_2: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_2_2_X, y=ROW_2_Y), br=Point(x=ROW_2_2_X + 41, y=ROW_2_Y + 32)
    )
)
ROW_2_3_X = 142 + OFFSET[0]
rectangle_2_3: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_2_3_X, y=ROW_2_Y), br=Point(x=ROW_2_3_X + 40, y=ROW_2_Y + 33)
    )
)
ROW_2_4_X = 182 + OFFSET[0]
rectangle_2_4: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_2_4_X, y=ROW_2_Y), br=Point(x=ROW_2_4_X + 41, y=ROW_2_Y + 32)
    )
)
ROW_2_5_X = 222 + OFFSET[0]
rectangle_2_5: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_2_5_X, y=ROW_2_Y), br=Point(x=ROW_2_5_X + 42, y=ROW_2_Y + 32)
    )
)
ROW_2_6_X = 262 + OFFSET[0]
rectangle_2_6: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_2_6_X, y=ROW_2_Y), br=Point(x=ROW_2_6_X + 42, y=ROW_2_Y + 32)
    )
)
ROW_2_7_X = 301 + OFFSET[0]
rectangle_2_7: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_2_7_X, y=ROW_2_Y), br=Point(x=ROW_2_7_X + 42, y=ROW_2_Y + 33)
    )
)
ROW_2_8_X = 343 + OFFSET[0]
rectangle_2_8: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_2_8_X, y=ROW_2_Y), br=Point(x=ROW_2_8_X + 42, y=ROW_2_Y + 33)
    )
)
ROW_2_9_X = 384 + OFFSET[0]
rectangle_2_9: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_2_9_X, y=ROW_2_Y), br=Point(x=ROW_2_9_X + 43, y=ROW_2_Y + 32)
    )
)

row_2 = [
    rectangle_2_1,
    rectangle_2_2,
    rectangle_2_3,
    rectangle_2_4,
    rectangle_2_5,
    rectangle_2_6,
    rectangle_2_7,
    rectangle_2_8,
    rectangle_2_9,
]

ROW_3_Y = 68 + OFFSET[1]

ROW_3_1_X = 57 + OFFSET[0]
rectangle_3_1: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_3_1_X, y=ROW_3_Y), br=Point(x=ROW_3_1_X + 41, y=ROW_3_Y + 34)
    )
)
ROW_3_2_X = 98 + OFFSET[0]
rectangle_3_2: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_3_2_X, y=ROW_3_Y), br=Point(x=ROW_3_2_X + 41, y=ROW_3_Y + 35)
    )
)
ROW_3_3_X = 139 + OFFSET[0]
rectangle_3_3: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_3_3_X, y=ROW_3_Y), br=Point(x=ROW_3_3_X + 42, y=ROW_3_Y + 35)
    )
)
ROW_3_4_X = 180 + OFFSET[0]
rectangle_3_4: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_3_4_X, y=ROW_3_Y), br=Point(x=ROW_3_4_X + 42, y=ROW_3_Y + 35)
    )
)
ROW_3_5_X = 222 + OFFSET[0]
rectangle_3_5: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_3_5_X, y=ROW_3_Y), br=Point(x=ROW_3_5_X + 42, y=ROW_3_Y + 35)
    )
)
ROW_3_6_X = 263 + OFFSET[0]
rectangle_3_6: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_3_6_X, y=ROW_3_Y), br=Point(x=ROW_3_6_X + 43, y=ROW_3_Y + 35)
    )
)
ROW_3_7_X = 304 + OFFSET[0]
rectangle_3_7: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_3_7_X, y=ROW_3_Y), br=Point(x=ROW_3_7_X + 43, y=ROW_3_Y + 35)
    )
)
ROW_3_8_X = 346 + OFFSET[0]
rectangle_3_8: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_3_8_X, y=ROW_3_Y), br=Point(x=ROW_3_8_X + 42, y=ROW_3_Y + 34)
    )
)
ROW_3_9_X = 387 + OFFSET[0]
rectangle_3_9: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_3_9_X, y=ROW_3_Y), br=Point(x=ROW_3_9_X + 42, y=ROW_3_Y + 35)
    )
)

row_3 = [
    rectangle_3_1,
    rectangle_3_2,
    rectangle_3_3,
    rectangle_3_4,
    rectangle_3_5,
    rectangle_3_6,
    rectangle_3_7,
    rectangle_3_8,
    rectangle_3_9,
]


ROW_4_Y = 102 + OFFSET[1]

ROW_4_1_X = 53 + OFFSET[0]
rectangle_4_1: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_4_1_X, y=ROW_4_Y), br=Point(x=ROW_4_1_X + 42, y=ROW_4_Y + 35)
    )
)
ROW_4_2_X = 95 + OFFSET[0]
rectangle_4_2: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_4_2_X, y=ROW_4_Y), br=Point(x=ROW_4_2_X + 42, y=ROW_4_Y + 36)
    )
)
ROW_4_3_X = 137 + OFFSET[0]
rectangle_4_3: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_4_3_X, y=ROW_4_Y), br=Point(x=ROW_4_3_X + 43, y=ROW_4_Y + 36)
    )
)
ROW_4_4_X = 179 + OFFSET[0]
rectangle_4_4: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_4_4_X, y=ROW_4_Y), br=Point(x=ROW_4_4_X + 44, y=ROW_4_Y + 35)
    )
)
ROW_4_5_X = 221 + OFFSET[0]
rectangle_4_5: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_4_5_X, y=ROW_4_Y), br=Point(x=ROW_4_5_X + 44, y=ROW_4_Y + 36)
    )
)
ROW_4_6_X = 262 + OFFSET[0]
rectangle_4_6: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_4_6_X, y=ROW_4_Y), br=Point(x=ROW_4_6_X + 45, y=ROW_4_Y + 36)
    )
)
ROW_4_7_X = 306 + OFFSET[0]
rectangle_4_7: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_4_7_X, y=ROW_4_Y), br=Point(x=ROW_4_7_X + 43, y=ROW_4_Y + 35)
    )
)
ROW_4_8_X = 347 + OFFSET[0]
rectangle_4_8: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_4_8_X, y=ROW_4_Y), br=Point(x=ROW_4_8_X + 44, y=ROW_4_Y + 36)
    )
)
ROW_4_9_X = 390 + OFFSET[0]
rectangle_4_9: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_4_9_X, y=ROW_4_Y), br=Point(x=ROW_4_9_X + 43, y=ROW_4_Y + 35)
    )
)

row_4 = [
    rectangle_4_1,
    rectangle_4_2,
    rectangle_4_3,
    rectangle_4_4,
    rectangle_4_5,
    rectangle_4_6,
    rectangle_4_7,
    rectangle_4_8,
    rectangle_4_9,
]

ROW_5_Y = 136 + OFFSET[1]

ROW_5_1_X = 48 + OFFSET[0]
rectangle_5_1: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_5_1_X, y=ROW_5_Y), br=Point(x=ROW_5_1_X + 43, y=ROW_5_Y + 38)
    )
)
ROW_5_2_X = 91 + OFFSET[0]
rectangle_5_2: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_5_2_X, y=ROW_5_Y), br=Point(x=ROW_5_2_X + 44, y=ROW_5_Y + 38)
    )
)
ROW_5_3_X = 135 + OFFSET[0]
rectangle_5_3: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_5_3_X, y=ROW_5_Y), br=Point(x=ROW_5_3_X + 43, y=ROW_5_Y + 38)
    )
)
ROW_5_4_X = 178 + OFFSET[0]
rectangle_5_4: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_5_4_X, y=ROW_5_Y), br=Point(x=ROW_5_4_X + 44, y=ROW_5_Y + 39)
    )
)
ROW_5_5_X = 221 + OFFSET[0]
rectangle_5_5: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_5_5_X, y=ROW_5_Y), br=Point(x=ROW_5_5_X + 44, y=ROW_5_Y + 39)
    )
)
ROW_5_6_X = 264 + OFFSET[0]
rectangle_5_6: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_5_6_X, y=ROW_5_Y), br=Point(x=ROW_5_6_X + 44, y=ROW_5_Y + 40)
    )
)
ROW_5_7_X = 306 + OFFSET[0]
rectangle_5_7: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_5_7_X, y=ROW_5_Y), br=Point(x=ROW_5_7_X + 45, y=ROW_5_Y + 39)
    )
)
ROW_5_8_X = 349 + OFFSET[0]
rectangle_5_8: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_5_8_X, y=ROW_5_Y), br=Point(x=ROW_5_8_X + 46, y=ROW_5_Y + 38)
    )
)
ROW_5_9_X = 393 + OFFSET[0]
rectangle_5_9: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_5_9_X, y=ROW_5_Y), br=Point(x=ROW_5_9_X + 45, y=ROW_5_Y + 37)
    )
)

row_5 = [
    rectangle_5_1,
    rectangle_5_2,
    rectangle_5_3,
    rectangle_5_4,
    rectangle_5_5,
    rectangle_5_6,
    rectangle_5_7,
    rectangle_5_8,
    rectangle_5_9,
]

ROW_6_Y = 174 + OFFSET[1]

ROW_6_1_X = 45 + OFFSET[0]
rectangle_6_1: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_6_1_X, y=ROW_6_Y), br=Point(x=ROW_6_1_X + 44, y=ROW_6_Y + 39)
    )
)
ROW_6_2_X = 89 + OFFSET[0]
rectangle_6_2: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_6_2_X, y=ROW_6_Y), br=Point(x=ROW_6_2_X + 44, y=ROW_6_Y + 39)
    )
)
ROW_6_3_X = 132 + OFFSET[0]
rectangle_6_3: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_6_3_X, y=ROW_6_Y), br=Point(x=ROW_6_3_X + 45, y=ROW_6_Y + 38)
    )
)
ROW_6_4_X = 176 + OFFSET[0]
rectangle_6_4: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_6_4_X, y=ROW_6_Y), br=Point(x=ROW_6_4_X + 45, y=ROW_6_Y + 39)
    )
)
ROW_6_5_X = 220 + OFFSET[0]
rectangle_6_5: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_6_5_X, y=ROW_6_Y), br=Point(x=ROW_6_5_X + 45, y=ROW_6_Y + 39)
    )
)
ROW_6_6_X = 265 + OFFSET[0]
rectangle_6_6: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_6_6_X, y=ROW_6_Y), br=Point(x=ROW_6_6_X + 45, y=ROW_6_Y + 40)
    )
)
ROW_6_7_X = 308 + OFFSET[0]
rectangle_6_7: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_6_7_X, y=ROW_6_Y), br=Point(x=ROW_6_7_X + 46, y=ROW_6_Y + 39)
    )
)
ROW_6_8_X = 352 + OFFSET[0]
rectangle_6_8: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_6_8_X, y=ROW_6_Y), br=Point(x=ROW_6_8_X + 46, y=ROW_6_Y + 39)
    )
)
ROW_6_9_X = 396 + OFFSET[0]
rectangle_6_9: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_6_9_X, y=ROW_6_Y), br=Point(x=ROW_6_9_X + 45, y=ROW_6_Y + 39)
    )
)

row_6 = [
    rectangle_6_1,
    rectangle_6_2,
    rectangle_6_3,
    rectangle_6_4,
    rectangle_6_5,
    rectangle_6_6,
    rectangle_6_7,
    rectangle_6_8,
    rectangle_6_9,
]


ROW_7_Y = 212 + OFFSET[1]

ROW_7_1_X = 40 + OFFSET[0]
rectangle_7_1: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_7_1_X, y=ROW_7_Y), br=Point(x=ROW_7_1_X + 45, y=ROW_7_Y + 41)
    )
)
ROW_7_2_X = 85 + OFFSET[0]
rectangle_7_2: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_7_2_X, y=ROW_7_Y), br=Point(x=ROW_7_2_X + 46, y=ROW_7_Y + 41)
    )
)
ROW_7_3_X = 130 + OFFSET[0]
rectangle_7_3: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_7_3_X, y=ROW_7_Y), br=Point(x=ROW_7_3_X + 45, y=ROW_7_Y + 42)
    )
)
ROW_7_4_X = 175 + OFFSET[0]
rectangle_7_4: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_7_4_X, y=ROW_7_Y), br=Point(x=ROW_7_4_X + 45, y=ROW_7_Y + 41)
    )
)
ROW_7_5_X = 220 + OFFSET[0]
rectangle_7_5: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_7_5_X, y=ROW_7_Y), br=Point(x=ROW_7_5_X + 46, y=ROW_7_Y + 41)
    )
)
ROW_7_6_X = 266 + OFFSET[0]
rectangle_7_6: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_7_6_X, y=ROW_7_Y), br=Point(x=ROW_7_6_X + 45, y=ROW_7_Y + 40)
    )
)
ROW_7_7_X = 311 + OFFSET[0]
rectangle_7_7: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_7_7_X, y=ROW_7_Y), br=Point(x=ROW_7_7_X + 45, y=ROW_7_Y + 41)
    )
)
ROW_7_8_X = 356 + OFFSET[0]
rectangle_7_8: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_7_8_X, y=ROW_7_Y), br=Point(x=ROW_7_8_X + 46, y=ROW_7_Y + 41)
    )
)

ROW_7_9_X = 400 + OFFSET[0]
rectangle_7_9: GridTile = GridTile(
    rectangle=Rectangle(
        tl=Point(x=ROW_7_9_X, y=ROW_7_Y), br=Point(x=ROW_7_9_X + 46, y=ROW_7_Y + 41)
    )
)

row_7 = [
    rectangle_7_1,
    rectangle_7_2,
    rectangle_7_3,
    rectangle_7_4,
    rectangle_7_5,
    rectangle_7_6,
    rectangle_7_7,
    rectangle_7_8,
    rectangle_7_9,
]


grid = [row_1, row_2, row_3, row_4, row_5, row_6, row_7]
