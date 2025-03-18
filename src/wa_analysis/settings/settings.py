## A settings python program

import tomllib
from dataclasses import dataclass
from pathlib import Path

from pydantic import BaseModel


@dataclass
class Settings:
    suptitle: str
    suptitle_fontsize: str
    suptitle_fontweight: str
    title: str
    title_fontsize: int
    title_fontstyle: str
    xlabel: str
    ylabel: str
    axis_off: bool
    grid_on: bool
    legend_on: bool
    output_folder: Path
    color_palette: str
    color: str


class PlotSettings:
    def __init__(self, section: str):
        self.settings = self.load_settings(section)

    def set_config(self):
        configfile = Path("config.toml").resolve()
        with configfile.open("rb") as f:
            self.config = tomllib.load(f)

    def load_settings(self, section: str) -> Settings:
        self.set_config()
        config_visual = self.config[section]

        return Settings(
            suptitle=config_visual["suptitle"],
            suptitle_fontsize=config_visual.get("suptitle_fontsize"),
            suptitle_fontweight=config_visual.get("suptitle_fontweight"),
            title=config_visual["title"],
            title_fontsize=config_visual.get("title_fontsize"),
            title_fontstyle=config_visual.get("title_style"),
            xlabel=config_visual["xlabel"],
            ylabel=config_visual["ylabel"],
            axis_off=config_visual.get("axis_off", False),
            grid_on=config_visual.get("grid_on", False),
            legend_on=config_visual.get("legend_on", False),
            output_folder=Path(self.config["output_folder"]),
            color_palette=config_visual.get("color_palette"),
            color=config_visual.get("color"),
        )

    def apply_settings(self, ax):
        ax.set_title(self.settings.title)
        ax.set_xlabel(self.settings.xlabel)
        ax.set_ylabel(self.settings.ylabel)
        if self.settings.axis_off:
            ax.set_axis_off()
        if self.settings.grid_on:
            ax.grid(True)
        if self.settings.legend_on:
            ax.legend()


class MessageCalculations(BaseModel):
    """Settings for message calculations."""

    function_column: str = "Function"
    message_column: str = "message"
    message_length_column: str = "message_length"
