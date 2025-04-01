## A settings python program

import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union

from pydantic import BaseModel


@dataclass
class Settings:
    suptitle: Optional[str] = None
    suptitle_fontsize: Optional[int] = None
    suptitle_fontweight: Optional[str] = None
    title: str = "Untitled"
    title_fontsize: int = 12
    title_fontstyle: Optional[str] = None
    xlabel: str = "X"
    xlabel_fontsize: int = 12
    xlabel_fontweight: str = "bold"
    xlabel_rotation: int = 0
    ylabel: str = "Y"
    ylabel_fontsize: int = 12
    ylabel_fontweight: str = "bold"
    axis_off: bool = False
    grid_on: bool = False
    legend_on: bool = False
    output_folder: Optional[Path] = None
    color_palette: Optional[Union[str, list]] = None
    color: Optional[Union[str, list]] = None
    save_as: str = "Unnamed visual.png"
    figtext: str = None
    figtext_x: Union[float, None] = None
    figtext_y: Union[float, None] = None
    figtext_fontsize: int = 12
    figtext_ha: str = "left"
    figtext_va: str = "center"
    subplot_adjust_bottom: Union[float, None] = None


class PlotSettings:
    def __init__(self, section: str):
        self.config: dict = {}
        self.settings: Settings = self.load_settings(section)

    def set_config(self):
        """
        Laad configuratie uit config.toml met foutafhandeling
        """
        configfile = Path("config.toml").resolve()

        # Controleer of het configuratiebestand bestaat
        if not configfile.exists():
            raise FileNotFoundError(f"Configuratiebestand niet gevonden: {configfile}")

        try:
            with configfile.open("rb") as f:
                self.config = tomllib.load(f)
        except Exception as e:
            raise RuntimeError(f"Fout bij het laden van configuratie: {e}")

    def load_settings(self, section: str) -> Settings:
        """
        Laad visuele instellingen voor een specifieke sectie
        """
        # Laad configuratie als dit nog niet is gebeurd
        if not self.config:
            self.set_config()

        # Controleer of de sectie bestaat
        if section not in self.config:
            raise KeyError(f"Sectie '{section}' niet gevonden in configuratie")

        config_visual = self.config[section]

        # Controleer of output_folder is gedefinieerd
        output_folder = self.config.get("output_folder")
        if output_folder:
            output_folder = Path(output_folder)
            # Maak de output folder aan als deze niet bestaat
            output_folder.mkdir(parents=True, exist_ok=True)

        return Settings(
            suptitle=config_visual.get("suptitle"),
            suptitle_fontsize=config_visual.get("suptitle_fontsize"),
            suptitle_fontweight=config_visual.get("suptitle_fontweight"),
            title=config_visual.get("title", "Untitled"),
            title_fontsize=config_visual.get("title_fontsize", 12),
            title_fontstyle=config_visual.get("title_style"),
            xlabel=config_visual.get("xlabel", "X"),
            xlabel_fontsize=config_visual.get("xlabel_fontsize", 12),
            xlabel_fontweight=config_visual.get("xlabel_fontweight", "bold"),
            xlabel_rotation=config_visual.get("xlabel_rotation"),
            ylabel=config_visual.get("ylabel", "Y"),
            ylabel_fontsize=config_visual.get("ylabel_fontsize", 12),
            ylabel_fontweight=config_visual.get("ylabel_fontweight", "bold"),
            axis_off=config_visual.get("axis_off", False),
            grid_on=config_visual.get("grid_on", False),
            legend_on=config_visual.get("legend_on", False),
            output_folder=output_folder,
            color_palette=config_visual.get("color_palette"),
            color=config_visual.get("color"),
            save_as=config_visual.get("save_as", "Unnamed visual.png"),
            figtext=config_visual.get("figtext"),
            figtext_x=config_visual.get("figtext_x"),
            figtext_y=config_visual.get("figtext_y"),
            figtext_fontsize=config_visual.get("figtext_fontsize", 12),
            figtext_ha=config_visual.get("figtext_ha", "left"),
            figtext_va=config_visual.get("figtext_va", "center"),
            subplot_adjust_bottom=config_visual.get("subplot_adjust_bottom"),
        )

    def apply_settings(self, ax, suptitle: Optional[str] = None):
        """
        Pas instellingen toe op de gegeven axes
        """
        # Titel instellen
        ax.set_title(
            self.settings.title,
            fontsize=self.settings.title_fontsize,
            fontstyle=self.settings.title_fontstyle or "normal",
        )

        # X-as labels
        ax.set_xlabel(
            self.settings.xlabel,
            fontsize=self.settings.xlabel_fontsize,
            fontweight=self.settings.xlabel_fontweight,
        )

        # Y-as labels
        ax.set_ylabel(
            self.settings.ylabel,
            fontsize=self.settings.ylabel_fontsize,
            fontweight=self.settings.ylabel_fontweight,
        )

        # As uitzetten indien gewenst
        if self.settings.axis_off:
            ax.set_axis_off()

        # Grid toevoegen indien gewenst
        if self.settings.grid_on:
            ax.grid(True)

        # Legenda toevoegen indien gewenst
        if self.settings.legend_on:
            ax.legend()

        # Suptitle toevoegen
        if suptitle or self.settings.suptitle:
            ax.figure.suptitle(
                suptitle or self.settings.suptitle,
                fontsize=self.settings.suptitle_fontsize,
                fontweight=self.settings.suptitle_fontweight or "normal",
            )

    def save_plot(self, fig, filename: Optional[str] = None):
        """
        Sla de plot op met geconfigureerde instellingen

        :param fig: Matplotlib figure object
        :param filename: Optionele bestandsnaam die de configuratie kan overschrijven
        """
        # Gebruik de opgegeven filename of de naam uit configuratie
        save_filename = filename or self.settings.save_as

        # Zorg dat de output folder bestaat
        if self.settings.output_folder:
            save_path = self.settings.output_folder / save_filename
        else:
            save_path = Path(save_filename)

        # Maak de directory aan indien nodig
        save_path.parent.mkdir(parents=True, exist_ok=True)

        # Sla de figuur op
        fig.savefig(save_path)
        print(f"Plot opgeslagen als: {save_path}")


class MessageCalculations(BaseModel):
    """Settings for message calculations."""

    function_column: str = "Function"
    message_column: str = "message"
    message_length_column: str = "message_length"
