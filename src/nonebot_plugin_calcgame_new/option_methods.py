from . import game_error as GameError  # noqa: N812
from .option_types import OptionBaseMethod, OptionCategory, OptionType


class AddOption(OptionBaseMethod):
    """将当前数值与参数中的第一个值的整数进行相加，作为新的当前数值。"""

    def __init__(
        self,
        values: tuple[int, ...] = (),
    ) -> None:
        super().__init__(
            option_type=OptionType.ADD,
            option_values=values,
            display_template="+{}",
            help_message_template="将当前数值加上{}。",
            option_value_count=1,
        )

    def method(self) -> None:
        self.value_int += self.option_values[0]


class SubtractOption(OptionBaseMethod):
    """将当前数值与参数中的第一个值的整数进行相减，作为新的当前数值。"""

    def __init__(
        self,
        values: tuple[int, ...] = (),
    ) -> None:
        super().__init__(
            option_type=OptionType.SUBTRACT,
            option_values=values,
            display_template="-{}",
            help_message_template="将当前数值减去{}。",
            option_value_count=1,
        )

    def method(self) -> None:
        self.value_int -= self.option_values[0]


class MultiplyOption(OptionBaseMethod):
    """将当前数值与参数中的第一个值的整数进行相乘，作为新的当前数值。"""

    def __init__(
        self,
        values: tuple[int, ...] = (),
    ) -> None:
        super().__init__(
            option_type=OptionType.MULTIPLY,
            option_values=values,
            display_template="×{}",  # noqa: RUF001
            help_message_template="将当前数值乘以{}。",
            option_value_count=1,
        )

    def method(self) -> None:
        self.value_int *= self.option_values[0]


class DivideOption(OptionBaseMethod):
    """将当前数值与参数中的第一个值的整数进行相除，作为新的当前数值。必须保证可以整除。"""

    def __init__(
        self,
        values: tuple[int, ...] = (),
    ) -> None:
        super().__init__(
            option_type=OptionType.DIVIDE,
            option_values=values,
            display_template="÷{}",
            help_message_template="将当前数值除以{}，必须保证可以整除。",
            option_value_count=1,
        )

    def method(self) -> None:
        if self.value_int % self.option_values[0] != 0:
            raise GameError.NotDivisibleError((self.value_int, self.option_values[0]))
        self.value_int //= self.option_values[0]


class BackspaceOption(OptionBaseMethod):
    """删除当前数值的最后一位数字。"""

    def __init__(self) -> None:
        super().__init__(
            option_type=OptionType.BACKSPACE,
            display_template="<<",
            help_message_template="将当前数值的最后一位数字删除。",
            background_color="#DB7633",
            option_value_count=0,
        )

    def method(self) -> None:
        self.value_int //= 10


class PushOption(OptionBaseMethod):
    """在当前数值的末尾添加一个数字。"""

    def __init__(
        self,
        values: tuple[int, ...] = (),
    ) -> None:
        super().__init__(
            option_type=OptionType.PUSH,
            option_values=values,
            display_template="{}",
            help_message_template="将{}添加到当前数值的末尾。",
            background_color="#7B1FA2",
            option_value_count=1,
        )

    def method(self) -> None:
        self.value_str += str(self.option_values[0])


class ReplaceOption(OptionBaseMethod):
    """将当前数值的所有第一个值替换为第二个值。"""

    def __init__(
        self,
        values: tuple[int, ...] = (),
    ) -> None:
        super().__init__(
            option_type=OptionType.REPLACE,
            option_values=values,
            display_template="{}=>{}",
            help_message_template="将当前数值的所有“{}”替换为“{}”。",
            background_color="#DB7633",
            option_value_count=2,
        )

    def method(self) -> None:
        if len(self.option_values) > 1:
            self.value_str = self.value_str.replace(
                str(self.option_values[0]), str(self.option_values[1])
            )


class SortAscendingOption(OptionBaseMethod):
    """将当前数值的数码按升序排列。"""

    def __init__(self) -> None:
        super().__init__(
            option_type=OptionType.SORTASCENDING,
            display_template="Sort<",
            help_message_template="将当前数值的数码按升序排列。",
            background_color="#DB7633",
            option_value_count=0,
        )

    def method(self) -> None:
        if self.value_str.startswith("-"):
            self.value_str = "-" + "".join(sorted(self.value_str[1:]))
        else:
            self.value_str = "".join(sorted(self.value_str))


class SortDescendingOption(OptionBaseMethod):
    """将当前数值的数码按降序排列。"""

    def __init__(self) -> None:
        super().__init__(
            option_type=OptionType.SORTDESCENDING,
            display_template="Sort>",
            help_message_template="将当前数值的数码按降序排列。",
            background_color="#DB7633",
            option_value_count=0,
        )

    def method(self) -> None:
        if self.value_str.startswith("-"):
            self.value_str = "-" + "".join(sorted(self.value_str[1:], reverse=True))
        else:
            self.value_str = "".join(sorted(self.value_str, reverse=True))


class PowerOption(OptionBaseMethod):
    """将当前数值取某次幂作为新的当前数值。"""

    def __init__(
        self,
        values: tuple[int, ...] = (),
    ) -> None:
        super().__init__(
            option_type=OptionType.POWER,
            option_values=values,
            display_template="^{}",
            help_message_template="将当前数值的{}次幂作为新的当前数值。",
            option_value_count=1,
        )

    def method(self) -> None:
        self.value_int **= self.option_values[0]


class ToggleOption(OptionBaseMethod):
    """将当前数值取相反数。"""

    def __init__(self) -> None:
        super().__init__(
            option_type=OptionType.TOGGLE,
            display_template="+/-",
            help_message_template="将当前数值取相反数。",
            background_color="#DB7633",
            option_value_count=0,
        )

    def method(self) -> None:
        self.value_int *= -1


class ReverseOption(OptionBaseMethod):
    """将当前数值的数字顺序反转。"""

    def __init__(self) -> None:
        super().__init__(
            option_type=OptionType.REVERSE,
            display_template="Reverse",
            help_message_template="将当前数值的数字顺序反转。",
            background_color="#DB7633",
            option_value_count=0,
        )

    def method(self) -> None:
        if self.value_str.startswith("-"):
            self.value_str = "-" + self.value_str[:0:-1]
        else:
            self.value_str = self.value_str[::-1]


class SumOption(OptionBaseMethod):
    """将当前数值的各位数字相加作为新的当前数值。"""

    def __init__(self) -> None:
        super().__init__(
            option_type=OptionType.SUM,
            display_template="Sum",
            help_message_template="将当前数值的各位数字相加作为新的当前数值。",
            background_color="#DB7633",
            option_value_count=0,
        )

    def method(self) -> None:
        try:
            if self.value_str.startswith("-"):
                self.value_int = -sum(int(i) for i in self.value_str[1:])
            else:
                self.value_int = sum(int(i) for i in self.value_str)
        except ValueError as e:
            raise GameError.ConvertIntError(self.value_str) from e


class ShiftLeftOption(OptionBaseMethod):
    """将当前数值的数字顺序向左移动一位，最左边的数字移到最右边。"""

    def __init__(self) -> None:
        super().__init__(
            option_type=OptionType.SHIFTLEFT,
            display_template="&lt;Shift",
            help_message_template="将当前数值的数字顺序向左移动一位，最左边的数字移到最右边。",
            background_color="#DB7633",
            option_value_count=0,
        )

    def method(self) -> None:
        sign = -1 if self.value_str.startswith("-") else 1
        self.value_str = self.value_str.lstrip("-")
        self.value_str = (
            self.value_str[1:] + self.value_str[0]
            if len(self.value_str) > 1
            else self.value_str
        )
        if sign == -1:
            self.value_str = "-" + self.value_str


class ShiftRightOption(OptionBaseMethod):
    """将当前数值的数字顺序向右移动一位，最右边的数字移到最左边。"""

    def __init__(self) -> None:
        super().__init__(
            option_type=OptionType.SHIFTRIGHT,
            display_template="Shift>",
            help_message_template="将当前数值的数字顺序向右移动一位，最右边的数字移到最左边。",
            background_color="#DB7633",
            option_value_count=0,
        )

    def method(self) -> None:
        sign = -1 if self.value_str.startswith("-") else 1
        self.value_str = self.value_str.lstrip("-")
        self.value_str = (
            self.value_str[-1] + self.value_str[:-1]
            if len(self.value_str) > 1
            else self.value_str
        )
        if sign == -1:
            self.value_str = "-" + self.value_str


class MirrorOption(OptionBaseMethod):
    """将当前数值反转后插入到原数值后面。"""

    def __init__(self) -> None:
        super().__init__(
            option_type=OptionType.MIRROR,
            display_template="Mirror",
            help_message_template="将当前数值反转后插入到原数值后面。",
            background_color="#DB7633",
            option_value_count=0,
        )

    def method(self) -> None:
        if self.value_str.startswith("-"):
            self.value_str = self.value_str + self.value_str[:0:-1]
        else:
            self.value_str = self.value_str + self.value_str[::-1]


class ModifyOption(OptionBaseMethod):
    """将具有一个参数的操作的值都增加某个数。"""

    def __init__(
        self,
        values: tuple[int, ...] = (),
    ) -> None:
        super().__init__(
            option_type=OptionType.MODIFY,
            option_values=values,
            display_template="[+]{}",
            help_message_template="将具有一个参数的操作的值都增加{}。",
            background_color="#DB7633",
            option_value_count=1,
        )

    def special_method(self) -> int:
        """获取 MODIFY 操作的修改值，默认为参数中的第一个值，如果没有参数则默认为 0"""
        return self.option_values[0] if len(self.option_values) > 0 else 0


class StoreOption(OptionBaseMethod):
    """0. 将存储的数值插入到当前数值的末尾；\n 1. 将当前数值存储起来。"""

    def __init__(
        self,
        values: tuple[int, ...] = (),
    ) -> None:
        super().__init__(
            option_type=OptionType.STORE,
            display_template="Store{}",
            help_message_template="【需要额外参数】\n 0. 将存储的数值{}插入到当前数值的末尾；\n 1. 将当前数值存储起来。",  # noqa: E501
            background_color="#7B1FA2",
            option_value_count=0,
        )
        self.special_values = values

    def method(self) -> None:
        if len(self.option_values) > 0:
            self.value_str += str(self.option_values[0])
        else:
            raise GameError.StoreEmptyError

    def special_method(self) -> int:
        """设置 STORE 操作的存储值为当前数值，并返回该操作的消耗。"""
        if self.value_int < 0:
            raise GameError.StoreNegativeError(self.value_int)
        self.option_values = (self.value_int,)
        return self.special_values[0]


class Inv10Option(OptionBaseMethod):
    """将当前数值每个数字 d 替换为 10-d，但 0 不变。"""

    def __init__(self) -> None:
        super().__init__(
            option_type=OptionType.INV10,
            display_template="Inv10",
            help_message_template="将当前数值每个数字 d 替换为 10-d，但 0 不变。",
            background_color="#DB7633",
            option_value_count=0,
        )

    def method(self) -> None:
        try:
            if self.value_str.startswith("-"):
                self.value_str = "-" + "".join(
                    str(10 - int(i)) if i != "0" else "0" for i in self.value_str[1:]
                )
            else:
                self.value_str = "".join(
                    str(10 - int(i)) if i != "0" else "0" for i in self.value_str
                )
        except ValueError as e:
            raise GameError.ConvertIntError(self.value_str) from e


class CutOption(OptionBaseMethod):
    """将当前数值中所有的某数字删除。"""

    def __init__(
        self,
        values: tuple[int, ...] = (),
    ) -> None:
        super().__init__(
            option_type=OptionType.CUT,
            option_values=values,
            display_template="Cut{}",
            help_message_template="将当前数值中所有“{}”删除。",
            background_color="#DB7633",
            option_value_count=1,
        )

    def method(self) -> None:
        self.value_str = self.value_str.replace(str(self.option_values[0]), "")


class CursorRoundOption(OptionBaseMethod):
    """将给定参数位置处的数字进行四舍五入。"""

    def __init__(self) -> None:
        super().__init__(
            option_type=OptionType.CURSOR_ROUND,
            display_template="Round",
            help_message_template="【需要额外参数】\n 将给定参数位置处的数字进行四舍五入。",  # noqa: E501
            background_color="#318DD9",
            option_value_count=0,
        )

    def method(self) -> None:
        if self.cursor_position < 2 or self.cursor_position > len(  # noqa: PLR2004
            self.value_str.lstrip("-")
        ):  # 如果取个位位置，无效，所以范围从 2 开始。
            raise GameError.CursorOutOfRangeError(
                (self.cursor_position, 2, len(self.value_str.lstrip("-")))
            )
        # 光标位置为 n 时，表示光标在当前数值的第 n 位（个位为 1，十位为 2，以此类推）。
        # 如果光标位置的低一位数字大于等于 5，则将光标位置的数字加 1，否则保持不变。
        # 然后将光标位置之后的数字全部置为 0。
        index = -self.cursor_position
        sign = -1 if self.value_str.startswith("-") else 1
        self.value_str = self.value_str.lstrip("-")
        try:
            self.value_int = int(self.value_str)
        except ValueError as e:
            raise GameError.ConvertIntError(self.value_str) from e
        if self.value_str[index + 1] >= "5":
            self.value_int += 10 ** (self.cursor_position - 1)
        self.value_int //= 10 ** (self.cursor_position - 1)
        self.value_int *= 10 ** (self.cursor_position - 1)
        self.value_int *= sign
        self.value_str = str(self.value_int)


class CursorDeleteOption(OptionBaseMethod):
    """将给定参数位置处的数字删除。"""

    def __init__(self) -> None:
        super().__init__(
            option_type=OptionType.CURSOR_DELETE,
            display_template="Delete",
            help_message_template="【需要额外参数】\n 将给定参数位置处的数字删除。",
            background_color="#318DD9",
            option_value_count=0,
        )

    def method(self) -> None:
        if self.cursor_position < 1 or self.cursor_position > len(
            self.value_str.lstrip("-")
        ):
            raise GameError.CursorOutOfRangeError(
                (self.cursor_position, 1, len(self.value_str.lstrip("-")))
            )
        index = -self.cursor_position
        list_value = list(self.value_str)
        del list_value[index]
        self.value_str = "".join(list_value)


class CursorInsertOption(OptionBaseMethod):
    """将给定参数位置处插入某个数字。"""

    def __init__(
        self,
        values: tuple[int, ...] = (),
    ) -> None:
        super().__init__(
            option_type=OptionType.CURSOR_INSERT,
            option_values=values,
            display_template="Insert{}",
            help_message_template="【需要额外参数】\n 将给定参数位置处插入{}。",
            background_color="#318DD9",
            option_value_count=1,
        )

    def method(self) -> None:
        if self.cursor_position < 0 or self.cursor_position > len(
            self.value_str.lstrip("-")
        ):
            raise GameError.CursorOutOfRangeError(
                (self.cursor_position, 1, len(self.value_str.lstrip("-")))
            )
        index = -self.cursor_position if self.cursor_position > 0 else 0
        if index == 0:
            self.value_str = self.value_str + str(self.option_values[0])
        else:
            self.value_str = (
                self.value_str[:index]
                + str(self.option_values[0])
                + self.value_str[index:]
            )


class CursorAddOption(OptionBaseMethod):
    """将给定参数位置处的数字与某个数字进行相加（自动对 10 取模）。"""

    def __init__(
        self,
        values: tuple[int, ...] = (),
    ) -> None:
        super().__init__(
            option_type=OptionType.CURSOR_ADD,
            option_values=values,
            display_template="+{}",
            help_message_template="【需要额外参数】\n 将给定参数位置处的数字与{}进行相加（自动对 10 取模）。",  # noqa: E501
            background_color="#318DD9",
            option_value_count=1,
        )

    def method(self) -> None:
        if self.cursor_position < 1 or self.cursor_position > len(
            self.value_str.lstrip("-")
        ):
            raise GameError.CursorOutOfRangeError(
                (self.cursor_position, 1, len(self.value_str.lstrip("-")))
            )
        index = -self.cursor_position
        try:
            current_digit = int(self.value_str[index])
            add_value = self.option_values[0]
            new_digit = (current_digit + add_value) % 10
        except ValueError as e:
            raise GameError.ConvertIntError(self.value_str[index]) from e
        list_value = list(self.value_str)
        list_value[index] = str(new_digit)
        self.value_str = "".join(list_value)


class CursorSubOption(OptionBaseMethod):
    """将给定参数位置处的数字与某个数进行相减（自动对 10 取模）。"""

    def __init__(
        self,
        values: tuple[int, ...] = (),
    ) -> None:
        super().__init__(
            option_type=OptionType.CURSOR_SUB,
            option_values=values,
            display_template="-{}",
            help_message_template="【需要额外参数】\n 将给定参数位置处的数字与{}进行相减（自动对 10 取模）。",  # noqa: E501
            background_color="#318DD9",
            option_value_count=1,
        )

    def method(self) -> None:
        if self.cursor_position < 1 or self.cursor_position > len(
            self.value_str.lstrip("-")
        ):
            raise GameError.CursorOutOfRangeError(
                (self.cursor_position, 1, len(self.value_str.lstrip("-")))
            )
        index = -self.cursor_position
        try:
            current_digit = int(self.value_str[index])
            sub_value = self.option_values[0]
            new_digit = ((current_digit - sub_value) % 10 + 10) % 10
        except ValueError as e:
            raise GameError.ConvertIntError(self.value_str[index]) from e
        list_value = list(self.value_str)
        list_value[index] = str(new_digit)
        self.value_str = "".join(list_value)


class CursorShiftOption(OptionBaseMethod):
    """将当前数值的数字顺序向左或向右移动相应次数。正向左，负向右。"""

    def __init__(self) -> None:
        super().__init__(
            option_type=OptionType.CURSOR_SHIFT,
            display_template="Shift",
            background_color="#318DD9",
            help_message_template="【需要额外参数】\n 将当前数值的数字顺序向左或向右移动相应次数。正向左，负向右。",  # noqa: E501
            option_value_count=0,
        )

    def method(self) -> None:
        # cursor_position 若为正，相当于 ShiftLeftOption 相应次数
        # cursor_position 若为负，相当于 ShiftRightOption 相应次数
        sign = 1 if self.value_int >= 0 else -1
        self.value_str = self.value_str.lstrip("-")
        for _ in range(abs(self.cursor_position)):
            if self.cursor_position >= 0:
                # 实现 ShiftLeftOption 的行为
                self.value_str = (
                    self.value_str[1:] + self.value_str[0]
                    if len(self.value_str) > 1
                    else self.value_str
                )
            else:
                # 实现 ShiftRightOption 的行为
                self.value_str = (
                    self.value_str[-1] + self.value_str[:-1]
                    if len(self.value_str) > 1
                    else self.value_str
                )
        if sign == -1:
            self.value_str = "-" + self.value_str


class CursorReplaceOption(OptionBaseMethod):
    """将给定参数位置处的数字替换为某个数。"""

    def __init__(
        self,
        values: tuple[int, ...] = (),
    ) -> None:
        super().__init__(
            option_type=OptionType.CURSOR_REPLACE,
            option_values=values,
            display_template="Replace{}",
            help_message_template="【需要额外参数】\n 将给定参数位置处的数字替换为{}。",
            background_color="#318DD9",
            option_value_count=1,
        )

    def method(self) -> None:
        if self.cursor_position < 1 or self.cursor_position > len(
            self.value_str.lstrip("-")
        ):
            raise GameError.CursorOutOfRangeError(
                (self.cursor_position, 1, len(self.value_str.lstrip("-")))
            )
        index = -self.cursor_position
        list_value = list(self.value_str)
        list_value[index] = str(self.option_values[0])
        self.value_str = "".join(list_value)


class CursorLockOption(OptionBaseMethod):
    """锁定当前数值光标位置处的数字，使其在进行下一步操作时不会改变。"""

    def __init__(self) -> None:
        super().__init__(
            option_type=OptionType.CURSOR_LOCK,
            display_template="Lock",
            help_message_template="【需要额外参数】\n 锁定当前数值光标位置处的数字，使其在进行下一步操作时不会改变。",  # noqa: E501
            background_color="#318DD9",
            option_value_count=0,
        )
        self.lock_position = 0

    def method(self) -> None:
        if self.cursor_position < 1 or self.cursor_position > len(
            self.value_str.lstrip("-")
        ):
            raise GameError.CursorOutOfRangeError(
                (self.cursor_position, 1, len(self.value_str.lstrip("-")))
            )
        self.lock_position = self.cursor_position

    def special_method(self) -> int:
        """获取 CURSOR_LOCK 操作的锁定位置，并清空锁定位置。"""
        ret = self.lock_position
        self.lock_position = 0
        return ret


class OptionFactory:
    """操作工厂类，根据操作类型和参数创建对应的实例。"""

    @staticmethod
    def create_option(
        option_type: OptionType,
        option_values: tuple[int, ...] = (),
    ) -> OptionBaseMethod:
        option_classes = {
            OptionType.ADD: AddOption,
            OptionType.SUBTRACT: SubtractOption,
            OptionType.MULTIPLY: MultiplyOption,
            OptionType.DIVIDE: DivideOption,
            OptionType.BACKSPACE: BackspaceOption,
            OptionType.PUSH: PushOption,
            OptionType.REPLACE: ReplaceOption,
            OptionType.SORTASCENDING: SortAscendingOption,
            OptionType.SORTDESCENDING: SortDescendingOption,
            OptionType.POWER: PowerOption,
            OptionType.TOGGLE: ToggleOption,
            OptionType.REVERSE: ReverseOption,
            OptionType.SUM: SumOption,
            OptionType.SHIFTLEFT: ShiftLeftOption,
            OptionType.SHIFTRIGHT: ShiftRightOption,
            OptionType.MIRROR: MirrorOption,
            OptionType.MODIFY: ModifyOption,
            OptionType.STORE: StoreOption,
            OptionType.INV10: Inv10Option,
            OptionType.CUT: CutOption,
            OptionType.CURSOR_ROUND: CursorRoundOption,
            OptionType.CURSOR_DELETE: CursorDeleteOption,
            OptionType.CURSOR_INSERT: CursorInsertOption,
            OptionType.CURSOR_ADD: CursorAddOption,
            OptionType.CURSOR_SUB: CursorSubOption,
            OptionType.CURSOR_REPLACE: CursorReplaceOption,
            OptionType.CURSOR_SHIFT: CursorShiftOption,
            OptionType.CURSOR_LOCK: CursorLockOption,
        }
        if option_type not in option_classes:
            raise GameError.InvalidOptionTypeError(option_type)
        if option_type in OptionCategory().no_values:
            return option_classes[option_type]()
        return option_classes[option_type](values=option_values)
