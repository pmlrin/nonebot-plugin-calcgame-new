from enum import Enum, auto
from typing import Any

from . import game_error as GameError  # noqa: N812


# 定义游戏中各类操作的枚举类型
class OptionType(Enum):
    ERROR = auto()
    ADD = auto()
    SUBTRACT = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    BACKSPACE = auto()
    PUSH = auto()
    REPLACE = auto()
    SORTASCENDING = auto()
    SORTDESCENDING = auto()
    POWER = auto()
    TOGGLE = auto()
    REVERSE = auto()
    SUM = auto()
    SHIFTLEFT = auto()
    SHIFTRIGHT = auto()
    MIRROR = auto()
    MODIFY = auto()
    STORE = auto()
    INV10 = auto()
    CUT = auto()
    CURSOR_ROUND = auto()
    CURSOR_DELETE = auto()
    CURSOR_INSERT = auto()
    CURSOR_ADD = auto()
    CURSOR_SUB = auto()
    CURSOR_SHIFT = auto()
    CURSOR_REPLACE = auto()
    CURSOR_LOCK = auto()


class OptionCategory:
    def __init__(self) -> None:
        self.no_values = (
            OptionType.BACKSPACE,
            OptionType.SORTASCENDING,
            OptionType.SORTDESCENDING,
            OptionType.TOGGLE,
            OptionType.REVERSE,
            OptionType.SUM,
            OptionType.SHIFTLEFT,
            OptionType.SHIFTRIGHT,
            OptionType.MIRROR,
            OptionType.INV10,
            OptionType.CURSOR_ROUND,
            OptionType.CURSOR_DELETE,
            OptionType.CURSOR_SHIFT,
            OptionType.CURSOR_LOCK,
        )
        self.one_value = (
            OptionType.ADD,
            OptionType.SUBTRACT,
            OptionType.MULTIPLY,
            OptionType.DIVIDE,
            OptionType.PUSH,
            OptionType.POWER,
            OptionType.CUT,
            OptionType.CURSOR_INSERT,
            OptionType.CURSOR_ADD,
            OptionType.CURSOR_SUB,
            OptionType.CURSOR_REPLACE,
        )
        self.cursor_options = (
            OptionType.CURSOR_ROUND,
            OptionType.CURSOR_DELETE,
            OptionType.CURSOR_INSERT,
            OptionType.CURSOR_ADD,
            OptionType.CURSOR_SUB,
            OptionType.CURSOR_SHIFT,
            OptionType.CURSOR_REPLACE,
            OptionType.CURSOR_LOCK,
        )
        self.special_options = (
            OptionType.STORE,
            OptionType.MODIFY,
            OptionType.CURSOR_LOCK,
        )


# 定义游戏中各类操作的行为基类
class OptionBaseMethod:
    def __init__(  # noqa: PLR0913
        self,
        option_type: OptionType = OptionType.ERROR,
        # 该操作的类型，具体操作类型由 OptionType 枚举定义。
        expend: int = 1,
        # 该操作的消耗，默认为 1
        option_values: tuple[int, ...] = (),
        # 该操作的参数，默认为空元组。参数的具体含义和使用方式由具体操作决定。
        option_value_count: int = 0,
        # 该操作的参数数量，默认为 0。参数数量用于验证传入参数的正确性。
        display_template: str = "",
        # 该操作的显示模板，默认为空字符串。可以包含占位符用于显示参数值。
        background_color: str = "#778899",
        # 该操作的背景颜色，默认为灰色。背景颜色用于在游戏界面上展示该操作的背景色。
        help_message_template: str = "",
        # 该操作的帮助信息模板，默认为空字符串。提供该操作的说明和使用方法。
    ) -> None:
        self.option_type = option_type
        self.expend = expend
        self.option_values = option_values
        self.option_value_count = option_value_count
        self.display_template = display_template
        self.background_color = background_color
        self.help_message_template = help_message_template
        self.special_values = ()
        if self.option_value_count != len(self.option_values):
            raise GameError.OptionValueNumberError(
                (self.option_type, self.option_values)
            )

    def method(self) -> None:
        pass

    def special_method(self) -> Any:
        pass

    def display_format(self) -> str:
        if len(self.option_values) == 0:
            return self.display_template
        return self.display_template.format(*self.option_values)

    def help_message_format(self) -> str:
        if len(self.option_values) == 0:
            return self.help_message_template
        return self.help_message_template.format(*self.option_values)

    def react_modify(self, option_value_add: int = 0) -> None:
        # 该方法用于处理 MODIFY 操作的反应行为，接受一个参数 value_add，表示要添加到当前数值上的值。  # noqa: E501
        if self.option_type in OptionCategory().one_value:
            self.option_values = (self.option_values[0] + option_value_add,)

    def set_value(
        self,
        value_int: int,
        cursor_position: int = 0,
        # 光标位置，默认为 0，表示无光标。
        # 光标位置为 n 时，表示光标在当前数值的第 n 位（个位为 1，十位为 2，以此类推）。
        lock_position: int = 0,
        # 锁位，默认为 0，表示不锁位。锁位为 n 时，表示锁定当前数值的第 n 位
        # （个位为 1，十位为 2，以此类推），在进行操作时该位的数字不会改变。
        portal: tuple[int, int] = (0, 0),
        # 传送门，默认为 (0, 0)，表示没有传送门。传送门为 (a, b) 时
        # 表示当数值的位数超过 a 位时，将第 a 位的数字传送到第 b 位上。
    ) -> None:
        # 设置当前数值，并记录之前的数值以便进行锁位和传送门操作
        self.value_int = value_int
        self.value_str = str(value_int)
        self.before_value_int = self.value_int
        self.before_value_str = self.value_str
        self.cursor_position = cursor_position
        self.lock_position = lock_position
        self.portal = portal

    def get_value(self) -> tuple[int, str]:
        portal_log = ""  # 记录传送门操作的日志，用于在游戏界面上展示传送门的变化过程

        if self.value_int >= 10**9 or self.value_int <= -(10**8):
            # 数值过大，无法继续进行操作。
            # 抛出 CurrentNumTooBigError 异常。
            raise GameError.CurrentNumTooBigError(self.value_int)

        if self.before_value_str != self.value_str:
            # 如果当前数值的字符串表示与之前的不同，说明 method 以字符串形式修改数字。
            # 需要将其转换为整数。
            try:
                self.value_int = int(self.value_str)
            except ValueError as e:
                raise GameError.ConvertIntError(self.value_str) from e
        self.value_str = str(self.value_int)

        sign = 1 if self.value_int >= 0 else -1
        self.value_str = self.value_str.lstrip("-")
        self.value_int = int(self.value_str)

        if self.portal != (0, 0) and len(self.value_str) >= self.portal[0]:
            # 如果传送门不为 (0, 0) 且当前数值的位数大于等于传送门的第一项，说明需要进行传送门操作。  # noqa: E501
            # 将当前数值的字符串表示转换为列表，取出传送门第一项处的数字，将其置空，再将列表转换回字符串。  # noqa: E501
            # 将取出的数字乘以 10 的 (传送门第二项 - 1) 次方后加到当前数值上，再将当前数值转换为字符串。  # noqa: E501
            # 重复此过程直到当前数值的位数不超过传送门的第一项。
            portal_log += self.value_str
            while len(self.value_str) >= self.portal[0]:
                value_list = list(self.value_str)
                value_add = value_list[-self.portal[0]]
                value_list[-self.portal[0]] = ""
                self.value_str = "".join(value_list)
                try:
                    self.value_int = int(self.value_str) + int(value_add) * (
                        10 ** (self.portal[1] - 1)
                    )
                except ValueError as e:
                    raise GameError.ConvertIntError(self.value_str) from e
                self.value_str = str(self.value_int)
                portal_log += f" => {self.value_str}"

        if self.lock_position > 0:
            # 如果锁位大于 0，说明需要进行锁位操作。
            # 将当前数值的字符串表示转换为列表，修改锁位处的数字为之前的数值锁位处，再将列表转换回字符串。  # noqa: E501
            value_list = list(self.value_str)
            while len(value_list) < self.lock_position:
                value_list.insert(0, "0")
            value_list[-self.lock_position] = self.before_value_str[-self.lock_position]
            self.lock_position = 0
            self.value_str = "".join(value_list)
            try:
                self.value_int = int(self.value_str)
            except ValueError as e:
                raise GameError.ConvertIntError(self.value_str) from e

        self.value_int *= sign

        return self.value_int, portal_log
