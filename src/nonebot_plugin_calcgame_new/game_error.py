class CalcGameError(Exception):
    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self) -> str:
        return repr(self.value)


class ConvertIntError(CalcGameError):
    def __init__(self, value: str = "0") -> None:
        if value == "0":
            super().__init__("无法将输入转换为整数。")
        else:
            super().__init__(f"无法将 '{value}' 转换为整数。")


class InvalidInputError(CalcGameError):
    def __init__(self, value: str) -> None:
        super().__init__(f"无效的输入: '{value}'。")


class NotDivisibleError(CalcGameError):
    def __init__(self, value: tuple = ()) -> None:
        super().__init__(f"数值 {value[0]} 不能被 {value[1]} 整除。")


class OptionValueNumberError(CalcGameError):
    def __init__(self, value: tuple = ()) -> None:
        super().__init__(f"{value[0]} 操作参数数量不匹配。当前参数值: {value[1]}。")


class CurrentNumTooBigError(CalcGameError):
    def __init__(self, value: int) -> None:
        super().__init__(f"当前数值 {value} 超过了允许的范围。")


class StoreNegativeError(CalcGameError):
    def __init__(self, value: int) -> None:
        super().__init__(f"Store 操作：存储数值 {value} 不能为负数。")


class StoreEmptyError(CalcGameError):
    def __init__(self) -> None:
        super().__init__("Store 操作：目前没有存储任何数值，无法进行插入操作。")


class CursorOutOfRangeError(CalcGameError):
    def __init__(self, value: tuple = ()) -> None:
        super().__init__(
            f"光标位置 {value[0]} 不在合法范围内（{value[1]} 至 {value[2]}）。"
        )


class InvalidOptionTypeError(CalcGameError):
    def __init__(self, value: object) -> None:
        super().__init__(f"无效的操作类型: {value}。")


class GameDataPraserError(CalcGameError):
    def __init__(self, value: str) -> None:
        super().__init__(f"游戏数据解析错误: {value}。")
