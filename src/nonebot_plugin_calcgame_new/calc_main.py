from . import game_error as GameError  # noqa: N812
from .option_types import OptionBaseMethod, OptionType


class CalcGame:
    """计算器：游戏的核心类，包含游戏的主要逻辑和状态管理。"""

    def __init__(  # noqa: PLR0913
        self,
        level: int = 0,
        current_value: int = 0,
        target_value: int = 0,
        step_limit: int = 0,
        options: tuple[OptionBaseMethod, ...] = (),
        portal: tuple[int, int] = (0, 0),
    ) -> None:
        self.level = level
        self.current_value = current_value
        self.target_value = target_value
        self.step_limit = step_limit
        self.options = options
        self.portal = portal
        self.portal_log = []
        self.lock_position = 0

    def judge_win(self) -> bool:
        """判断玩家是否达成目标，赢得游戏。"""
        return self.current_value == self.target_value

    def judge_lose(self) -> bool:
        """判断玩家是否失败。"""
        return self.step_limit <= 0 and not self.judge_win()

    def apply_option(
        self,
        option: list[str],
    ) -> None:
        """应用玩家选择的操作，并更新游戏状态。
        参数 option 是一个字符串列表，包含玩家输入的操作编号和可能的额外参数。
        长度为 1 或 2 且字符串可转换为数字为合法。"""
        try:
            option_index = int(option[0])
            extra_param = int(option[1]) if len(option) > 1 else 0
        except ValueError as e:
            raise GameError.InvalidInputError(option[0]) from e

        if option_index < 1 or option_index > len(self.options):
            raise GameError.InvalidInputError(option[0])

        option_index -= 1  # 将用户输入的选项编号转换为从 0 开始的索引

        if not isinstance(self.options[option_index], OptionBaseMethod):
            raise GameError.InvalidInputError(option[0])

        self.options[option_index].set_value(
            value_int=self.current_value,
            cursor_position=extra_param,
            lock_position=self.lock_position,
            portal=self.portal,
        )

        if self.options[option_index].option_type == OptionType.MODIFY:
            # 如果操作类型是 MODIFY，则执行修改行为。
            modify_value = self.options[option_index].special_method()
            for i in range(len(self.options)):
                self.options[i].react_modify(modify_value)
            self.step_limit -= self.options[option_index].expend

        elif self.options[option_index].option_type == OptionType.CURSOR_LOCK:
            # 如果操作类型是 CURSOR_LOCK，则执行光标锁定行为。
            self.options[option_index].method()
            self.lock_position = self.options[option_index].special_method()
            self.step_limit -= self.options[option_index].expend

        elif (
            self.options[option_index].option_type == OptionType.STORE
            and extra_param != 0
        ):
            # 如果操作类型是 STORE，则执行存储行为。
            self.step_limit -= self.options[option_index].special_method()

        else:
            self.options[option_index].method()
            self.step_limit -= self.options[option_index].expend
            self.current_value, self.portal_log = self.options[option_index].get_value()
            self.lock_position = 0
