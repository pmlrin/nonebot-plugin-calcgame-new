from pathlib import Path

from nonebot import require

from .calc_main import CalcGame

require("nonebot_plugin_htmlrender")
from nonebot_plugin_htmlrender import template_to_pic


class KeyProperty:
    def __init__(self, color: str, display_text: str) -> None:
        self.color = color
        self.display_text = display_text


async def html_to_image(game: CalcGame) -> bytes:
    unuse_key_color = "#bdc3c7"
    portal_sign = "▼"
    lock_sign = "▣"
    portal_up = [" " for _ in range(9)]
    portal_down = [" " for _ in range(9)]
    portal_up[game.portal[1]] = portal_sign
    portal_up[game.lock_position] = lock_sign
    portal_down[game.portal[0]] = portal_sign
    current_value = list(str(game.current_value)[::-1]) + [" " for _ in range(9)]
    key = [KeyProperty(unuse_key_color, "") for _ in range(9)]
    for i in range(len(game.options)):
        key[i] = KeyProperty(
            color=game.options[i].background_color,
            display_text=game.options[i].display_format(),
        )

    return await template_to_pic(
        template_path=str(Path(__file__).parent / "template"),
        template_name="calc_img.html",
        templates={
            "level": game.level,
            "step_limit": game.step_limit,
            "target_value": game.target_value,
            "portal_up": portal_up,
            "portal_down": portal_down,
            "current_value": current_value,
            "key": key,
        },
    )
