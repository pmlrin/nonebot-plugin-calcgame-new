import random

from nonebot import get_plugin_config, require
from nonebot.params import ArgPlainText
from nonebot.plugin import PluginMetadata, inherit_supported_adapters

require("nonebot_plugin_alconna")
from nonebot.typing import T_State
from nonebot_plugin_alconna import (
    Alconna,
    AlconnaMatches,
    Args,
    Arparma,
    Option,
    on_alconna,
)
from nonebot_plugin_alconna.uniseg import UniMessage

from . import game_error as GameError  # noqa: N812
from .calc_data import CalcGameData
from .calc_main import CalcGame
from .config import Config
from .img_render import html_to_image
from .option_methods import OptionFactory

__plugin_meta__ = PluginMetadata(
    name="计算器：游戏",
    description="这是利用机器人复刻 计算器：游戏 的一个插件。通过给出的操作方式由当前数字达到计算目标。",  # noqa: E501
    usage="/calc [number] [帮助] \n进入游戏后：[操作方式] [帮助] [退出]",
    type="application",  # library
    homepage="https://github.com/pmlrin/nonebot-plugin-calcgame-new",
    config=Config,
    supported_adapters=inherit_supported_adapters(
        "nonebot_plugin_alconna", "nonebot_plugin_htmlrender"
    ),
    # supported_adapters={"~onebot.v11"}, # 仅 onebot
    extra={"author": "pmlrin <Yurchiu@outlook.com>"},
)

config = get_plugin_config(Config)

calc = on_alconna(
    Alconna(
        "/calc",
        Args["number?", int],
        Option(
            "帮助",
        ),
    )
)


@calc.handle()
async def _(state: T_State, result: Arparma = AlconnaMatches()) -> None:
    help_msg = """游戏玩法：通过给出的操作方式由当前数字达到目标数字。
达到目标数字即为胜利。步数用尽且未达到目标数字即为失败。
只需要输入相应数字即可进行相应操作。某些操作需要额外输入一个数字。
游戏时输入“帮助”查看本局游戏帮助，“退出”结束游戏。"""
    user_num = random.randint(1, CalcGameData().get_level_count())
    if result.find("帮助"):
        await calc.finish(help_msg)
    if result.find("number"):
        user_num = result.query[int]("number")
        user_num = user_num if user_num is not None else 0
    try:
        game_data = CalcGameData().data_praser(user_num)
        game_main = CalcGame(
            level=game_data["level"],
            current_value=game_data["current_value"],
            target_value=game_data["target_value"],
            step_limit=game_data["step_limit"],
            options=tuple(
                OptionFactory().create_option(option_data[0], option_data[1])
                for option_data in game_data["options"]
            ),
            portal=game_data["portal"],
        )
        img_bytes = await html_to_image(game_main)
    except (
        GameError.ConvertIntError,
        GameError.GameDataPraserError,
        GameError.InvalidOptionTypeError,
        GameError.OptionValueNumberError,
    ) as e:
        await calc.finish(e.value + "请重新开始游戏。")
    message = UniMessage.image(raw=img_bytes)
    state["game_main"] = game_main
    state["receipt"] = await message.send()


@calc.got("option_index")
async def handle_option(state: T_State, option_index: str = ArgPlainText()) -> None:  # noqa: C901, PLR0912
    game_main: CalcGame = state["game_main"]
    if option_index == "退出":
        await state["receipt"].recall()
        await calc.finish("游戏已退出。")
    if option_index == "帮助":
        help_msg = "帮助信息："
        for index, option in enumerate(game_main.options, start=1):
            help_msg += f"\n第{index}个操作：\n {option.help_message_format()}"
        await calc.reject(help_msg)
    try:
        option = option_index.strip().split()
        if len(option) == 0 or len(option) > 2:  # 最多两个数字 # noqa: PLR2004
            raise GameError.InvalidInputError(option_index)  # noqa: TRY301
        try:
            param1 = int(option[0]) - 1
            if len(option) == 2:  # noqa: PLR2004
                param2 = int(option[1])
                game_main.apply_option(param1, param2)
            else:
                game_main.apply_option(param1)
        except ValueError as e:
            raise GameError.InvalidInputError(option_index) from e
    except (
        GameError.InvalidInputError,
        GameError.CursorOutOfRangeError,
        GameError.InvalidOptionTypeError,
        GameError.NotDivisibleError,
        GameError.StoreNegativeError,
        GameError.StoreEmptyError,
    ) as e:
        await calc.reject(e.value + "请重新输入操作。")
    except (
        GameError.CurrentNumTooBigError,
        GameError.ConvertIntError,
    ) as e:
        await state["receipt"].recall()
        await calc.finish(e.value + "游戏结束。")
    img_bytes = await html_to_image(game_main)
    message = UniMessage.image(raw=img_bytes)
    await state["receipt"].recall()
    state["game_main"] = game_main
    state["receipt"] = await message.send()
    portal_log = game_main.portal_log
    if len(portal_log) > 0:
        portal_msg = "本次操作触发了传送门，数字的变化过程如下："
        for log in portal_log:
            portal_msg += log
        await calc.send(portal_msg)
    if game_main.judge_win():
        await calc.finish("恭喜你赢了！")
    elif game_main.judge_lose():
        await calc.finish("很遗憾你输了！")
    else:
        await calc.reject()
