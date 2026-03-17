<div align="center">
    <a href="https://v2.nonebot.dev/store">
    <img src="https://raw.githubusercontent.com/fllesser/nonebot-plugin-template/refs/heads/resource/.docs/NoneBotPlugin.svg" width="310" alt="logo"></a>

## ✨ nonebot-plugin-calcgame-new ✨
[![LICENSE](https://img.shields.io/github/license/pmlrin/nonebot-plugin-calcgame-new.svg)](./LICENSE)
[![pypi](https://img.shields.io/pypi/v/nonebot-plugin-calcgame-new.svg)](https://pypi.python.org/pypi/nonebot-plugin-calcgame-new)
[![python](https://img.shields.io/badge/python-3.10|3.11|3.12|3.13-blue.svg)](https://www.python.org)
[![uv](https://img.shields.io/badge/package%20manager-uv-black?style=flat-square&logo=uv)](https://github.com/astral-sh/uv)
<br/>
[![ruff](https://img.shields.io/badge/code%20style-ruff-black?style=flat-square&logo=ruff)](https://github.com/astral-sh/ruff)
[![pre-commit](https://results.pre-commit.ci/badge/github/pmlrin/nonebot-plugin-calcgame-new/master.svg)](https://results.pre-commit.ci/latest/github/pmlrin/nonebot-plugin-calcgame-new/master)

</div>

## 📖 介绍

是 `nonebot-plugin-calc-game` 的重构版！

这是利用机器人复刻 计算器：游戏 的一个插件。游戏玩法：通过给出的操作方式由当前数字达到计算目标。目前有 319 关。

反馈请加作者 QQ：2378975755。注明 插件反馈。若有关卡投稿亦可加 QQ，注明 关卡投稿。关卡应包含完整的关卡要素，并给出最优解。

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-calcgame-new --upgrade
使用 **pypi** 源安装

    nb plugin install nonebot-plugin-calcgame-new --upgrade -i "https://pypi.org/simple"
使用**清华源**安装

    nb plugin install nonebot-plugin-calcgame-new --upgrade -i "https://pypi.tuna.tsinghua.edu.cn/simple"


</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details open>
<summary>uv</summary>

    uv add nonebot-plugin-calcgame-new
安装仓库 master 分支

    uv add git+https://github.com/pmlrin/nonebot-plugin-calcgame-new@master
</details>

<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-calcgame-new
安装仓库 master 分支

    pdm add git+https://github.com/pmlrin/nonebot-plugin-calcgame-new@master
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-calcgame-new
安装仓库 master 分支

    poetry add git+https://github.com/pmlrin/nonebot-plugin-calcgame-new@master
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_calcgame_new"]

</details>

<details>
<summary>使用 nbr 安装(使用 uv 管理依赖可用)</summary>

[nbr](https://github.com/fllesser/nbr) 是一个基于 uv 的 nb-cli，可以方便地管理 nonebot2

    nbr plugin install nonebot-plugin-calcgame-new
使用 **pypi** 源安装

    nbr plugin install nonebot-plugin-calcgame-new -i "https://pypi.org/simple"
使用**清华源**安装

    nbr plugin install nonebot-plugin-calcgame-new -i "https://pypi.tuna.tsinghua.edu.cn/simple"

</details>


## ⚙️ 配置

本插件没有配置项。

## 🎉 使用
### 指令表

进入游戏前：

|     指令      | 权限 | 需要@ | 范围 |       说明       |
| :-----------: | :--: | :---: | :--: | :--------------: |
|    `/calc`    | 群员 |  否   | 均可 | 随机抽取一个谜题 |
| `/calc <num>` | 群员 |  否   | 均可 |   抽取指定谜题   |
| `/calc 帮助`  | 群员 |  否   | 均可 |   发送游戏规则   |

进入游戏后：

|     指令     | 权限 | 需要@ | 范围 |                     说明                     |
| :----------: | :--: | :---: | :--: | :------------------------------------------: |
| `<操作方式>` | 群员 |  否   | 均可 | 执行你发送的操作方式（一般为 1 或 2 个数字） |
|    `帮助`    | 群员 |  否   | 均可 |         发送本关所涉及操作方式的用法         |
|    `退出`    | 群员 |  否   | 均可 |                 退出本局游戏                 |


### 🎨 效果图
![](https://github.com/pmlrin/nonebot-plugin-calcgame-new/blob/master/example.png)
