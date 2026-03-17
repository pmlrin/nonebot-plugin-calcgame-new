from . import game_error as GameError  # noqa: N812
from .option_types import OptionBaseMethod, OptionType


class CalcGame:
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
        return self.current_value == self.target_value

    def judge_lose(self) -> bool:
        return self.step_limit <= 0 and not self.judge_win()

    def get_type(self, option_index: int) -> OptionType:
        return self.options[option_index].option_type

    def apply_option(
        self,
        option_index: int,
        extra_param: int = 0,
    ) -> None:
        if option_index < 0 or option_index >= len(self.options):
            raise GameError.InvalidOptionTypeError(option_index + 1)

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
