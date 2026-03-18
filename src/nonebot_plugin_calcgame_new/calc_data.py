import re
from typing import TypedDict

from . import game_error as GameError  # noqa: N812
from .option_types import OptionType


class CalcGameDataType(TypedDict):
    """关卡数据类型定义"""

    level: int
    target_value: int
    step_limit: int
    current_value: int
    options: list[tuple[OptionType, tuple[int, ...]]]
    portal: tuple[int, int]


class CalcGameData:
    """关卡数据类，包含关卡数据和数据解析方法"""

    def __init__(self) -> None:
        self.calc_data = [
            ["level", "target_value", "step_limit", "current_value"],
            [1, 8, 3, 0, "+2", "+3"],
            [2, 200, 4, 0, "+10", "*4"],
            [3, 24, 3, 2, "*2", "*3"],
            [4, 4, 4, 125, "<<", "*2"],
            [5, 5, 4, 125, "<<", "*2"],
            [6, 95, 3, 25, "push5", "+4", "/5"],
            [7, 59, 3, 25, "push5", "+4", "/5"],
            [8, 32, 4, 155, "push2", "*2", "<<"],
            [9, 24, 4, 155, "push2", "*2", "<<"],
            [10, 144, 3, 11, "push2", "*12", "<<"],
            [11, 3, 4, 15, "push6", "+5", "<<", "/7"],
            [12, 96, 3, 200, "push1", "+12", "*3", "<<"],
            [13, 63, 3, 200, "push1", "+12", "*3", "<<"],
            [14, 33, 4, 200, "push1", "+12", "*3", "<<"],
            [15, 62, 3, 550, "+6", "1=>2", "<<"],
            [16, 321, 4, 123, "2=>3", "13=>21"],
            [17, 1970, 3, 1985, "sort>", "*2", "<<"],
            [18, 1234, 3, 16, "sort>", "*2", "push7"],
            [19, 333, 4, 4321, "sort<", "2=>3", "1=>3", "<<"],
            [20, 275, 4, 97231, "sort<", "<<", "9=>5"],
            [21, 19, 3, 303, "sort<", "+1", "*3"],
            [22, 100, 3, 303, "sort<", "+1", "*3"],
            [23, 111, 4, 423, "sort<", "/2", "<<", "push1"],
            [24, 123, 4, 423, "sort<", "/2", "<<", "push1"],
            [25, 963, 4, 30, "sort>", "/5", "+6", "push3"],
            [26, 321, 4, 30, "sort>", "/5", "+6", "push3"],
            [27, 4, 3, 3, "+4", "*4", "/4"],
            [28, 5, 3, 4, "+3", "*3", "/3"],
            [29, 9, 4, 50, "/5", "*3", "<<"],
            [30, 100, 3, 99, "-8", "*11", "<<"],
            [31, 23, 4, 171, "*2", "-9", "<<"],
            [32, 24, 6, 0, "+5", "*3", "*5", "<<"],
            [33, 2, 5, 0, "+4", "*9", "<<"],
            [34, 9, 4, 0, "+2", "/3", "push1"],
            [35, 10, 4, 15, "push0", "+2", "/5"],
            [36, 93, 4, 0, "+6", "*7", "6=>9"],
            [37, 2321, 6, 0, "push1", "push2", "1=>2", "2=>3"],
            [38, 24, 5, 0, "+9", "*2", "8=>4"],
            [39, 29, 5, 11, "/2", "+3", "1=>2", "2=>9"],
            [40, 20, 5, 36, "+3", "/3", "1=>2"],
            [41, 15, 4, 2, "/3", "push1", "*2", "4=>5"],
            [42, 414, 4, 1234, "23=>41", "24=>14", "12=>24", "14=>2"],
            [43, -85, 4, 0, "+6", "push5", "-7"],
            [44, 9, 3, 0, "-1", "-2", "^2"],
            [45, -13, 4, 0, "+3", "-7", "+/-"],
            [46, 52, 5, 44, "+9", "/2", "*4", "+/-"],
            [47, 10, 5, 9, "+5", "*5", "+/-"],
            [48, 12, 5, 14, "push6", "+5", "/8", "+/-"],
            [49, 13, 4, 55, "+9", "+/-", "<<"],
            [50, 245, 5, 0, "-3", "push5", "*4", "+/-"],
            [51, 126, 6, 111, "*3", "-9", "+/-", "<<"],
            [52, 3, 5, 34, "-5", "+8", "/7", "+/-"],
            [53, 4, 5, 25, "-4", "*-4", "/3", "/8"],
            [54, 101, 3, 100, "push1", "+9", "rev"],
            [55, 51, 3, 0, "+6", "+9", "rev"],
            [56, 101, 3, 100, "push1", "+9", "rev"],
            [57, 100, 4, 1101, "-1", "rev"],
            [58, 58, 4, 0, "+4", "*4", "-3", "rev"],
            [59, 21, 3, 15, "+9", "*5", "rev"],
            [60, 13, 5, 100, "/2", "rev"],
            [61, 102, 4, 0, "push10", "*4", "+5", "rev"],
            [62, 7, 4, 0, "push2", "+1", "/3", "rev"],
            [63, 9, 5, 8, "*3", "push1", "/5", "rev"],
            [64, 13, 5, 0, "+7", "+8", "+9", "rev"],
            [65, 123, 6, 0, "+3", "push1", "-2", "rev"],
            [66, 424, 5, 0, "push6", "+8", "rev"],
            [67, 81, 5, 7, "-9", "*3", "+4", "+/-", "rev"],
            [68, -43, 5, 0, "-5", "+7", "-9", "rev"],
            [69, 28, 7, 0, "+6", "-3", "rev", "<<"],
            [70, 136, 5, 0, "push1", "+2", "*3", "rev"],
            [71, -25, 5, 0, "+4", "rev", "+/-", "*3"],
            [72, -5, 5, 0, "+7", "*3", "rev", "+/-"],
            [73, 41, 4, 88, "/4", "-4", "rev"],
            [74, 101, 5, 100, "push0", "*2", "2=>10", "0=>1", "rev"],
            [75, 424, 7, 0, "/2", "push5", "5=>4", "rev"],
            [76, 100, 5, 99, "push9", "/9", "rev", "1=>0"],
            [77, 30, 5, 8, "push2", "-4", "2=>3", "rev"],
            [78, 222, 5, 101, "-1", "rev", "0=>2"],
            [79, 500, 5, 36, "*4", "/3", "1=>5", "rev"],
            [80, 196, 8, 0, "push1", "+12", "*13", "rev", "<<"],
            [81, 101, 5, 50, "1=>10", "+50", "rev", "5=>1"],
            [82, 2048, 6, 1, "push2", "*4", "*10", "rev"],
            [83, 123, 5, 12, "push12", "+1", "12=>2", "rev"],
            [84, 55, 6, 86, "+2", "+14", "rev", "0=>5"],
            [85, 4, 3, 1231, "sum", "3=>1", "2=>3"],
            [86, 45, 5, 0, "*9", "push4", "*3", "3=>5", "sum"],
            [87, 28, 5, 424, "*4", "4=>6", "sum"],
            [88, 8, 4, 3, "push3", "+33", "sum", "3=>1"],
            [89, 44, 4, 24, "/2", "push4", "1=>2", "sum"],
            [90, 143, 4, 142, "*9", "+9", "44=>43", "sum"],
            [91, 1, 5, 24, "/3", "*4", "5=>10", "sum"],
            [92, 100, 5, 4, "push3", "*3", "+1", "sum"],
            [93, 8, 5, 93, "+4", "*3", "sum"],
            [94, 16, 5, 5, "*5", "/2", "sum", "5=>2"],
            [95, 64, 4, 128, "*4", "/4", "sum", "5=>16"],
            [96, 121, 6, 59, "push1", "*5", "15=>51", "sum"],
            [97, 5, 6, 18, "*2", "/3", "12=>21", "sum"],
            [98, 30, 4, 9, "-5", "*-6", "+/-", "sum"],
            [99, -17, 5, 105, "-5", "/5", "*4", "+/-", "sum"],
            [100, 11, 6, 36, "-6", "/3", "+/-", "sum"],
            [101, 64, 5, 3, "+3", "sum", "^3", "0=>1"],
            [102, 11, 5, 2, "*2", "push10", "sum", "^3", "10=>1"],
            [103, 121, 3, 101, "+2", "shift>", "<shift"],
            [104, 1999, 4, 98, "push1", "push9", "89=>99", "shift>"],
            [105, 129, 4, 70, "*3", "push9", "shift>"],
            [106, 210, 5, 120, "+1", "<shift", "+/-"],
            [107, 210, 5, 1001, "+2", "shift>", "12=>0"],
            [108, 501, 3, 100, "+5", "push0", "<shift"],
            [109, 3, 4, 212, "+11", "3=>1", "sum", "<shift"],
            [110, 121, 4, 356, "-2", "/3", "shift>"],
            [111, 13, 6, 2152, "25=>12", "21=>3", "12=>5", "shift>", "rev"],
            [112, 520, 5, 1025, "shift>", "50=>0", "25=>525", "51=>5"],
            [113, 19, 6, 91, "+5", "mir", "sum"],
            [114, 116, 4, 22, "-3", "push6", "mir", "sum"],
            [115, 20, 7, 125, "6=>2", "push0", "mir", "sum"],
            [116, 3, 4, 22, "sum", "/2", "mir", "<<"],
            [117, 1111, 5, 0, "+2", "*6", "mir", "21=>11"],
            [118, 2020, 8, -1, "*3", "+8", "+2", "rev", "mir"],
            [119, 112, 6, 13, "99=>60", "/3", "*3", "mir", "shift>"],
            [120, 18, 5, 140, "-3", "+9", "/12", "mir", "<<"],
            [121, 33, 4, 17, "*2", "-4", "mir", "<shift"],
            [122, 20, 7, 125, "mir", "sum"],
            [123, 14, 4, 0, "push1", "+2", "[+]1"],
            [124, 101, 5, 0, "push2", "+5", "[+]2"],
            [125, 28, 5, 0, "push1", "+2", "[+]3"],
            [126, 42, 5, 0, "-2", "+5", "*2", "[+]1"],
            [127, 25, 5, 0, "+2", "*3", "-3", "[+]2"],
            [128, 41, 4, 5, "+4", "+8", "*3", "[+]2"],
            [129, 31, 5, 33, "*4", "+2", "+3", "[+]1", "sum"],
            [130, 268, 5, 25, "+8", "*2", "*5", "[+]1"],
            [131, 121, 4, 0, "+1", "store"],
            [132, 122, 4, 12, "store", "rev", "<<"],
            [133, 17, 5, 0, "+2", "/3", "rev", "store"],
            [134, 1234, 4, 23, "*2", "-5", "store", "<shift"],
            [135, 1025, 6, 125, "*2", "store", "<<"],
            [136, 115, 5, 23, "-8", "store", "+/-"],
            [137, 16, 4, 15, "store", "11=>33", "rev", "sum"],
            [138, 61, 7, 0, "push5", "<<", "sum", "store"],
            [139, 101, 5, 0, "*6", "push5", "shift>", "store", "3=>1"],
            [140, 12525, 5, 125, "push1", "/5", "rev", "store"],
            [141, 17, 6, 70, "8=>1", "/2", "push0", "store", "sum"],
            [142, 101, 4, 12, "21=>0", "12=>1", "store", "mir"],
            [143, 3001, 7, 9, "39=>93", "/3", "store", "31=>00"],
            [144, 2, 3, 1, "-1", "inv10"],
            [145, 15, 3, 14, "+5", "*5", "inv10"],
            [146, 12, 3, 21, "-7", "*5", "inv10"],
            [147, 13, 4, 67, "+3", "rev", "inv10"],
            [148, 88, 5, 23, "-4", "-2", "rev", "inv10"],
            [149, 105, 4, 5, "*3", "/9", "store", "inv10"],
            [150, 23, 4, 24, "+6", "*3", "rev", "inv10"],
            [151, 17, 4, 7, "+3", "*3", "*4", "inv10"],
            [152, 21, 5, 35, "*9", "/5", "13=>10", "inv10"],
            [153, 18, 5, 9, "*3", "sum", "inv10"],
            [154, 101, 5, 12, "+4", "inv10", "sum"],
            [155, 99, 6, 26, "push2", "sum", "inv10"],
            [156, 13, 7, 15, "sum", "inv10", "mir"],
            [157, 99, 6, 78, "1=>6", "6=>11", "/6", "inv10", "rev"],
            [158, 9, 4, 34, "*6", "inv10", "<<"],
            [159, 872, 8, 0, "push8", "88=>34", "inv10", "<<"],
            [160, 33, 5, 5, "*7", "+8", "-9", "*2", "inv10"],
            [161, 23, 4, 12, "*5", "sum", "store", "inv10"],
            [162, 1991, 4, 1, "store", "inv10"],
            [163, 26, 4, 12, "<<", "sum", "store", "inv10"],
            [164, 48, 6, 51, "+6", "*3", "inv10", "rev", "4=>6"],
            [165, 1, 6, 0, "+5", "*3", "/6", "inv10", "rev"],
            [166, 777, 5, 369, "99=>63", "63=>33", "inv10", "36=>93", "39=>33"],
            [167, 10, 3, 99, "push1", "-1"],
            [168, 64, 2, 9, "push4", "push6"],
            [169, 35, 3, 50, "+5", "*3", "*5"],
            [170, 131, 4, 306, "push3", "+1", "*2"],
            [171, 123, 5, 321, "/2", "push1", "push3", "push0"],
            [172, 150, 4, 525, "+1", "push6", "push7", "/2"],
            [173, 212, 4, 301, "push10", "-2", "push3"],
            [174, 13, 4, 99, "sum", "mir", "inv10"],
            [175, 822, 5, 25, "mir", "push5", "store", "<<"],
            [176, 516, 4, 45, "+10", "mir", "rev"],
            [177, 212, 4, 238, "28=>21", "-5", "inv10", "shift>"],
            [178, 90, 5, 58, "*6", "inv10", "shift>"],
            [179, 500, 5, 189, "+8", "*4", "push9", "inv10", "7=>0"],
            [180, 321, 4, 234, "push9", "+9", "53=>32"],
            [181, 123, 4, 333, "push1", "push3", "/2", "[+]1"],
            [182, 777, 3, 613, "push5", "*2", "+3", "rev", "inv10"],
            [183, 550, 6, 60, "+5", "*5", "push2", "inv10"],
            [184, 4321, 5, 1234, "24=>13", "12=>32", "13=>21", "23=>32", "23=>43"],
            [185, 750, 6, 4, "+6", "push4", "*3", "inv10"],
            [186, 3507, 6, 3002, "push7", "3=>5", "inv10", "shift>"],
            [187, 21, 3, 0, "+15", "sum"],
            [188, 1, 3, 20, "cut1", "*5", "+1"],
            [189, 2, 3, 33, "cut1", "+3", "*3"],
            [190, 6, 4, 4454, "cut4", "+2", "+4", "<<"],
            [191, 72, 3, 6996, "+3", "cut9"],
            [192, 15, 3, 12345, "cut1", "/3"],
            [193, 2, 5, 99999, "cut1", "9=>3", "3=>1", "-8"],
            [194, 123, 2, 10203, "(del)"],
            [195, 40, 3, 55, "*2", "*4", "(del)"],
            [196, 234, 2, 4, "(insert2)", "(insert3)", "(insert34)"],
            [197, 48, 3, 14, "(del)", "(insert2)", "*2"],
            [198, 120, 3, 1, "(insert2)", "*5", "*4"],
            [199, 45, 3, 3, "+2", "*3", "(insert1)"],
            [200, 7, 3, 4505, "(insert2)", "cut5", "+2", "(del)"],
            [201, 3, 3, 64, "rev", "-2", "/2"],
            [202, 21, 3, 64, "rev", "-2", "/2"],
            [203, 52, 4, 12, "rev", "*5", "(del)"],
            [204, 15, 3, 12, "rev", "*5", "(del)"],
            [205, 555, 3, 125, "rev", "2=>5", "+1"],
            [206, 11, 4, 84, "rev", "+2", "cut4", "(insert1)"],
            [207, 2, 4, 84, "rev", "+2", "cut4", "(insert1)"],
            [208, 200, 2, 10, "(round)", "(insert5)"],
            [209, 1000, 2, 90, "(round)", "(insert5)"],
            [210, 40, 3, 24, "(round)", "4=>3", "*2"],
            [211, 500, 2, 2150, "(round)", "rev"],
            [212, 1600, 3, 35, "(round)", "*5", "5=>12"],
            [213, 44, 3, 352, "(round)", "rev", "push4"],
            [214, 900, 3, 2189, "(round)", "rev", "+1"],
            [215, 2222, 2, 2024, "(+2)", "(-2)"],
            [216, 18, 3, 21, "(+2)", "4=>8", "rev"],
            [217, 136, 3, 100, "(+2)", "+8"],
            [218, 0, 2, 25, "(+5)", "+25"],
            [219, 90, 3, 12, "(+4)", "*4", "+2"],
            [220, 1000, 3, 555, "(+9)", "*2"],
            [221, 900, 3, 555, "(+9)", "*2"],
            [222, 250, 4, 50, "(+4)", "(del)", "(insert1)", "*4"],
            [223, 500, 4, 50, "(+4)", "(del)", "(insert1)", "*4"],
            [224, 3456, 4, 650, "(-2)", "(insert3)"],
            [225, 1750, 4, 1990, "(+8)", "(del)", "(+5)", "(round)"],
            [226, 150, 4, 1990, "(+8)", "(del)", "(+5)", "(round)"],
            [227, -6, 4, 62, "+/-", "(+2)", "-12"],
            [228, -12, 4, 208, "+/-", "+2", "(del)", "/2"],
            [229, -8, 5, 47, "+/-", "+5", "/2"],
            [230, 14, 5, 10, "+/-", "+8", "*3"],
            [231, 66, 5, 10, "+/-", "+8", "*3"],
            [232, 40, 5, 41, "+/-", "push1", "<<", "+2"],
            [233, 21, 5, 41, "+/-", "push1", "<<", "+2"],
            [234, 151, 3, 121, "(move)", "+3"],
            [235, 5, 3, 84, "(move)", "+2"],
            [236, 125, 2, 215, "(move)", "rev"],
            [237, 678, 3, 918, "(move)", "<<", "1=>67"],
            [238, 306, 2, 1206, "(move)", "/2"],
            [239, 22, 3, 55, "(move)", "*2"],
            [240, 102, 4, 214, "(move)", "-1", "/2"],
            [241, 25, 4, 5252, "(move)", "cut1", "25=>15", "52=>12"],
            [242, 305, 5, 152, "(move)", "+2", "rev", "(round)"],
            [243, 0, 3, 1213, "sum", "cut1", "+4"],
            [244, 8, 4, 1111, "sum", "*4", "push1"],
            [245, 35, 5, 5000, "sum", "rev", "+4"],
            [246, 1199, 5, 90, "mir", "<shift", "push10"],
            [247, 2112, 4, 123, "mir", "sum", "rev"],
            [248, 1000, 4, 201, "mir", "rev", "cut2", "-1"],
            [249, 3223, 4, 9933, "mir", "cut1", "/3", "31=>2"],
            [250, 275, 5, 2, "mir", "rev", "*5"],
            [251, 360, 5, 10, "[+]1", "*2"],
            [252, 15, 5, 3, "[+]1", "+2", "mir", "sum"],
            [253, 20, 5, 10, "[+]2", "*3", "cut1"],
            [254, 123, 3, 82, "[+]1", "/2", "*2"],
            [255, 6, 5, 13, "[+]1", "(+2)", "43=>2"],
            [256, 1, 5, 222, "[+]2", "(insert3)", "sum", "56=>10"],
            [257, 501, 1, 101, "(rep5)", "(rep55)"],
            [258, 22, 4, 65, "(rep6)", "(+1)", "+5", "/5"],
            [259, 64, 4, 20, "(rep6)", "mir", "sum"],
            [260, 332, 3, 144, "(rep1)", "/3", "inv10"],
            [261, 321, 3, 144, "(rep1)", "/3", "inv10"],
            [262, 82, 4, 108, "(rep8)", "+2", "sum", "mir"],
            [263, 32, 4, 108, "(rep8)", "+2", "sum", "mir"],
            [264, 181, 4, 108, "(rep8)", "+2", "sum", "mir"],
            [265, 9, 4, 410, "inv10", "*3", "sum", "<<"],
            [266, 7, 3, 13, "inv10", "/5", "3=>5"],
            [267, 19, 3, 13, "inv10", "/5", "3=>5"],
            [268, 13, 4, 180, "inv10", "sort<", "+2", "rev"],
            [269, 8, 4, 180, "inv10", "sort<", "+2", "rev"],
            [270, 50, 4, 154, "inv10", "9=>5", "+6", "(del)"],
            [271, 40, 3, 154, "inv10", "9=>5", "+6", "(del)"],
            [272, 1, 3, 369, "inv10", "sum", "+2"],
            [273, 99, 4, 369, "inv10", "sum", "+2"],
            [274, 80, 3, 369, "inv10", "sum", "+2"],
            [275, 66, 4, 145, "inv10", "sum", "*3", "(rep2)"],
            [276, 40, 4, 145, "inv10", "sum", "*3", "(rep2)"],
            [277, 60, 3, 475, "inv10", "<<", "(rep2)", "(round)"],
            [278, 70, 4, 475, "inv10", "<<", "(rep2)", "(round)"],
            [279, 80, 4, 475, "inv10", "<<", "(rep2)", "(round)"],
            [280, 18, 4, 8, "STORE", "+2", "<<"],
            [281, 101, 4, 8, "STORE", "+2", "<<"],
            [282, 1212, 5, 33, "STORE", "sum"],
            [283, 126, 5, 33, "STORE", "sum"],
            [284, 12, 4, 10, "STORE", "(+5)", "sum"],
            [285, 710, 5, 10, "STORE", "(+5)", "sum"],
            [286, 2112, 4, 123, "STORE", "rev", "<<"],
            [287, 131, 5, 118, "STORE", "+2", "<<"],
            [288, 33, 6, 118, "STORE", "+2", "<<"],
            [289, 123, 6, 118, "STORE", "+2", "<<"],
            [290, 25, 2, 15, "(lock)", "+12"],
            [291, 28, 2, 125, "(lock)", "sum"],
            [292, 108, 2, 125, "(lock)", "sum"],
            [293, 2400, 3, 1975, "(lock)", "(round)", "(+5)"],
            [294, 7070, 3, 1975, "(lock)", "(round)", "(+5)"],
            [295, 2222, 3, 12, "(lock)", "mir", "rev"],
            [296, 13, 4, 35, "(lock)", "(insert7)", "sum"],
            [297, 9, 4, 35, "(lock)", "(insert7)", "sum"],
            [298, 48, 5, 2222, "(lock)", "cut2", "/5"],
            [299, 21, 2, 55, "push5", "*2"],
            [300, 16, 2, 55, "push5", "*2"],
            [301, 121, 4, 14, "mir", "push1", "sum"],
            [302, 111, 4, 14, "mir", "push1", "sum"],
            [303, 992, 2, 91, "inv10", "STORE", "mir"],
            [304, 920, 3, 91, "inv10", "STORE", "mir"],
            [305, 2, 4, 91, "inv10", "STORE", "mir"],
            [306, 525, 5, 15, "inv10", "STORE", "<<"],
            [307, 220, 5, 15, "inv10", "STORE", "<<"],
            [308, 78, 2, 77, "mir", "(rep4)", "<<", "sum"],
            [309, 99, 4, 77, "mir", "(rep4)", "<<", "sum"],
            [310, 2, 3, 77, "mir", "(rep4)", "<<", "sum"],
            [311, 500, 3, 77, "mir", "(rep4)", "<<", "sum"],
            [312, 860, 4, 77, "mir", "(rep4)", "<<", "sum"],
            [313, 456, 4, 77, "mir", "(rep4)", "<<", "sum"],
            [314, 888, 4, 77, "mir", "(rep4)", "<<", "sum"],
            [315, 93, 5, 9, "push9", "push1", "sort<", "cut0", "(insert2)"],
            [316, 131, 6, 9, "push9", "push1", "sort<", "cut0", "(insert2)"],
            [317, 1, 4, 9, "push9", "push1", "sort<", "cut0", "(insert2)"],
            [318, 9933, 6, 9, "push9", "push1", "sort<", "cut0", "(insert2)"],
            [319, 31, 6, 9, "push9", "push1", "sort<", "cut0", "(insert2)"],
        ]

        self.portal_data = {
            167: (3, 1),
            168: (3, 2),
            169: (3, 2),
            170: (4, 1),
            171: (4, 1),
            172: (4, 1),
            173: (4, 1),
            174: (4, 2),
            175: (4, 2),
            176: (4, 2),
            179: (4, 1),
            180: (4, 1),
            181: (4, 1),
            182: (4, 1),
            183: (4, 2),
            185: (4, 2),
            186: (5, 1),
            299: (3, 1),
            300: (3, 1),
            301: (4, 1),
            302: (4, 1),
            303: (4, 1),
            304: (4, 1),
            305: (4, 1),
            306: (4, 1),
            307: (4, 1),
            308: (4, 1),
            309: (4, 1),
            310: (4, 1),
            311: (4, 1),
            312: (4, 1),
            313: (4, 1),
            314: (4, 1),
            315: (5, 1),
            316: (5, 1),
            317: (5, 1),
            318: (5, 1),
            319: (5, 1),
        }

        self.help_msg = """计算器：游戏 帮助
/calc 选择随机关卡，/calc [关卡编号] 选择指定关卡，/calc 帮助 查看帮助。
游戏玩法：通过给出的操作方式由当前数字达到计算目标。
达到目标数字即为胜利。步数用尽且未达到目标数字即为失败。
只需要输入相应数字即可进行相应操作。某些操作需要额外输入一个数字。
游戏时输入“帮助”查看本局游戏帮助，“退出”结束游戏。"""

    def get_level_count(self) -> int:
        """获取关卡数量"""
        return len(self.calc_data) - 1

    def extract_numbers(self, s: str, count: int) -> list[int]:
        """从字符串中匹配给定数量的数字，可以匹配负数。"""
        numbers = re.findall(r"-?\d+", s)
        ret_list = [int(n) for n in numbers[:count]]
        if len(ret_list) != count:
            raise GameError.GameDataPraserError(  # noqa: TRY003
                f"期望提取 {count} 个数字，实际提取到 {len(ret_list)} 个。"
            )
        return ret_list

    def data_praser(self, index: int) -> CalcGameDataType:  # noqa: C901, PLR0912, PLR0915
        """根据关卡索引解析关卡数据，返回一个结构化的 CalcGameDataType 对象。"""

        if index < 1 or index > self.get_level_count():  # 关卡索引从 1 开始，0 是占位符
            raise GameError.GameDataPraserError(  # noqa: TRY003
                f"关卡范围为 1-{self.get_level_count()}，{index} 超出范围。"
            )

        raw_data = self.calc_data[index]
        try:
            prased_data = CalcGameDataType(
                {
                    "level": int(raw_data[0]),
                    "target_value": int(raw_data[1]),
                    "step_limit": int(raw_data[2]),
                    "current_value": int(raw_data[3]),
                    "options": [],
                    "portal": (0, 0),
                }
            )
            if index in self.portal_data:
                prased_data["portal"] = self.portal_data[index]
            raw_data[4] = raw_data[4]
        except ValueError as e:
            raise GameError.ConvertIntError from e
        except IndexError as e:
            raise GameError.GameDataPraserError(  # noqa: TRY003
                f"关卡 {index} 的数据不完整: {raw_data}"
            ) from e

        for option in raw_data[4:]:
            if option.startswith("(") and option.endswith(")"):
                cur_option = option[1:-1]  # 去掉括号
                if cur_option == "round":
                    prased_data["options"].append((OptionType.CURSOR_ROUND, ()))
                elif cur_option == "del":
                    prased_data["options"].append((OptionType.CURSOR_DELETE, ()))
                elif cur_option == "move":
                    prased_data["options"].append((OptionType.CURSOR_SHIFT, ()))
                elif cur_option == "lock":
                    prased_data["options"].append((OptionType.CURSOR_LOCK, ()))
                elif "insert" in cur_option:
                    insert_num = self.extract_numbers(cur_option, 1)[0]
                    prased_data["options"].append(
                        (OptionType.CURSOR_INSERT, (insert_num,))
                    )
                elif "rep" in cur_option:
                    rep_num = self.extract_numbers(cur_option, 1)[0]
                    prased_data["options"].append(
                        (OptionType.CURSOR_REPLACE, (rep_num,))
                    )
                elif "+" in cur_option:
                    plus_num = self.extract_numbers(cur_option, 1)[0]
                    prased_data["options"].append((OptionType.CURSOR_ADD, (plus_num,)))
                elif "-" in cur_option:
                    minus_num = self.extract_numbers(cur_option, 1)[0] * -1
                    prased_data["options"].append((OptionType.CURSOR_SUB, (minus_num,)))
                else:
                    raise GameError.InvalidOptionTypeError(option)
            elif option == "<<":
                prased_data["options"].append((OptionType.BACKSPACE, ()))
            elif option == "sort<":
                prased_data["options"].append((OptionType.SORTASCENDING, ()))
            elif option == "sort>":
                prased_data["options"].append((OptionType.SORTDESCENDING, ()))
            elif option == "+/-":
                prased_data["options"].append((OptionType.TOGGLE, ()))
            elif option == "rev":
                prased_data["options"].append((OptionType.REVERSE, ()))
            elif option == "sum":
                prased_data["options"].append((OptionType.SUM, ()))
            elif option == "<shift":
                prased_data["options"].append((OptionType.SHIFTLEFT, ()))
            elif option == "shift>":
                prased_data["options"].append((OptionType.SHIFTRIGHT, ()))
            elif option == "mir":
                prased_data["options"].append((OptionType.MIRROR, ()))
            elif option == "store":
                prased_data["options"].append((OptionType.STORE, (0,)))
            elif option == "STORE":
                prased_data["options"].append((OptionType.STORE, (1,)))
            elif option == "inv10":
                prased_data["options"].append((OptionType.INV10, ()))
            elif option.startswith("+"):
                plus_num = self.extract_numbers(option, 1)[0]
                prased_data["options"].append((OptionType.ADD, (plus_num,)))
            elif option.startswith("-"):
                minus_num = self.extract_numbers(option, 1)[0] * -1
                prased_data["options"].append((OptionType.SUBTRACT, (minus_num,)))
            elif option.startswith("*"):
                mul_num = self.extract_numbers(option, 1)[0]
                prased_data["options"].append((OptionType.MULTIPLY, (mul_num,)))
            elif option.startswith("/"):
                div_num = self.extract_numbers(option, 1)[0]
                prased_data["options"].append((OptionType.DIVIDE, (div_num,)))
            elif option.startswith("push"):
                push_num = self.extract_numbers(option, 1)[0]
                prased_data["options"].append((OptionType.PUSH, (push_num,)))
            elif "=>" in option:
                from_num, to_num = self.extract_numbers(option, 2)
                prased_data["options"].append((OptionType.REPLACE, (from_num, to_num)))
            elif option.startswith("^"):
                pow_num = self.extract_numbers(option, 1)[0]
                prased_data["options"].append((OptionType.POWER, (pow_num,)))
            elif option.startswith("[+]"):
                plus_num = self.extract_numbers(option, 1)[0]
                prased_data["options"].append((OptionType.MODIFY, (plus_num,)))
            elif option.startswith("cut"):
                cut_num = self.extract_numbers(option, 1)[0]
                prased_data["options"].append((OptionType.CUT, (cut_num,)))
            else:
                raise GameError.InvalidOptionTypeError(option)
        return prased_data
