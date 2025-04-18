import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from pydantic import BaseModel

from wa_analysis.settings.logger import Logger

# Setup logger
logger = Logger().get_logger()


@dataclass
class Settings:
    """Settings for plot configuration."""

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
    legend_title: str = "Legend Title"
    output_folder: Optional[Path] = None
    color_palette: Optional[Union[str, List[str]]] = None
    color: Optional[Union[str, List[str]]] = None
    save_as: str = "Unnamed visual.png"
    figtext: Optional[str] = None
    figtext_x: Optional[float] = None
    figtext_y: Optional[float] = None
    figtext_fontsize: int = 12
    figtext_ha: str = "left"
    figtext_va: str = "center"
    subplot_adjust_bottom: Optional[float] = None


class PlotSettings:
    """Class for managing plot settings from configuration files."""

    def __init__(self, section: str) -> None:
        logger.info(f"Initialiseren PlotSettings voor sectie: {section}")
        self.config: Dict[str, Any] = {}
        self.settings: Settings = self.load_settings(section)
        logger.debug(f"PlotSettings geladen voor sectie: {section}")

    @property
    def legend_title(self) -> str:
        """Property accessor for legend_title from settings"""
        return self.settings.legend_title

    def set_config(self) -> Dict[str, Any]:
        """
        Laad configuratie uit config.toml met foutafhandeling

        Returns:
            Dict[str, Any]: De geladen configuratie
        """
        logger.info("Laden configuratie uit config.toml")
        configfile: Path = Path("config.toml").resolve()
        logger.debug(f"Configuratiepad: {configfile}")

        # Controleer of het configuratiebestand bestaat
        if not configfile.exists():
            error_msg: str = f"Configuratiebestand niet gevonden: {configfile}"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)

        try:
            with configfile.open("rb") as f:
                self.config = tomllib.load(f)
                logger.debug(f"Configuratie geladen met {len(self.config)} secties")
                return self.config
        except Exception as e:
            error_msg: str = f"Fout bij het laden van configuratie: {e}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)

    def load_settings(self, section: str) -> Settings:
        """
        Laad visuele instellingen voor een specifieke sectie

        Args:
            section: Sectienaam in het configuratiebestand

        Returns:
            Settings: Object met plot-instellingen
        """
        logger.info(f"Laden instellingen voor sectie: {section}")

        # Laad configuratie als dit nog niet is gebeurd
        if not self.config:
            self.set_config()

        # Controleer of de sectie bestaat
        if section not in self.config:
            error_msg: str = f"Sectie '{section}' niet gevonden in configuratie"
            logger.error(error_msg)
            raise KeyError(error_msg)

        config_visual: Dict[str, Any] = self.config[section]
        logger.debug(
            f"Visuele configuratie gevonden met {len(config_visual)} instellingen"
        )

        # Controleer of output_folder is gedefinieerd
        output_folder: Optional[Path] = None
        output_folder_str: Optional[str] = self.config.get("output_folder")
        if output_folder_str:
            output_folder = Path(output_folder_str)
            logger.debug(f"Output folder: {output_folder}")
            # Maak de output folder aan als deze niet bestaat
            output_folder.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Output folder aangemaakt/gecontroleerd: {output_folder}")

        # Maak Settings object
        settings = Settings(
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
            legend_title=config_visual.get("legend_title", "Legend Title"),
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

        logger.info(f"Instellingen voor sectie '{section}' succesvol geladen")
        return settings

    def apply_settings(self, ax: plt.Axes, suptitle: Optional[str] = None) -> None:
        """
        Pas instellingen toe op de gegeven axes

        Args:
            ax: Matplotlib Axes object
            suptitle: Optionele suptitle die de configuratie kan overschrijven
        """
        logger.info("Toepassen instellingen op axes")

        try:
            # Titel instellen
            ax.set_title(
                self.settings.title,
                fontsize=self.settings.title_fontsize,
                fontstyle=self.settings.title_fontstyle or "normal",
            )
            logger.debug(f"Titel ingesteld: {self.settings.title}")

            # X-as labels
            ax.set_xlabel(
                self.settings.xlabel,
                fontsize=self.settings.xlabel_fontsize,
                fontweight=self.settings.xlabel_fontweight,
            )
            logger.debug(f"X-label ingesteld: {self.settings.xlabel}")

            # Y-as labels
            ax.set_ylabel(
                self.settings.ylabel,
                fontsize=self.settings.ylabel_fontsize,
                fontweight=self.settings.ylabel_fontweight,
            )
            logger.debug(f"Y-label ingesteld: {self.settings.ylabel}")

            # As uitzetten indien gewenst
            if self.settings.axis_off:
                ax.set_axis_off()
                logger.debug("Assen uitgezet")

            # Grid toevoegen indien gewenst
            if self.settings.grid_on:
                ax.grid(True)
                logger.debug("Grid ingeschakeld")

            # Legenda toevoegen indien gewenst
            if self.settings.legend_on and len(ax.get_legend_handles_labels()[0]) > 0:
                ax.legend(title=self.settings.legend_title)
                logger.debug(
                    f"Legenda toegevoegd met titel: {self.settings.legend_title}"
                )
            else:
                logger.debug(
                    "Geen legenda toegevoegd (geen gelabelde elementen of legend_on=False)"
                )

            # Suptitle toevoegen
            if suptitle or self.settings.suptitle:
                title_text: str = suptitle or self.settings.suptitle
                ax.figure.suptitle(
                    title_text,
                    fontsize=self.settings.suptitle_fontsize,
                    fontweight=self.settings.suptitle_fontweight or "normal",
                    y=0.94,
                )
                logger.debug(f"Suptitle ingesteld: {title_text}")

            logger.info("Instellingen succesvol toegepast op axes")

        except Exception as e:
            logger.error(f"Fout bij het toepassen van instellingen: {str(e)}")
            raise

    def save_plot(self, fig: plt.Figure, filename: Optional[str] = None) -> None:
        """
        Sla de plot op met geconfigureerde instellingen

        Args:
            fig: Matplotlib figure object
            filename: Optionele bestandsnaam die de configuratie kan overschrijven
        """
        logger.info("Opslaan plot")

        try:
            # Gebruik de opgegeven filename of de naam uit configuratie
            save_filename: str = filename or self.settings.save_as
            logger.debug(f"Bestandsnaam voor opslaan: {save_filename}")

            # Zorg dat de output folder bestaat
            if self.settings.output_folder:
                save_path: Path = self.settings.output_folder / save_filename
                logger.debug(f"Volledig pad voor opslaan: {save_path}")
            else:
                save_path = Path(save_filename)
                logger.debug(f"Relatief pad voor opslaan: {save_path}")

            # Maak de directory aan indien nodig
            save_path.parent.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Directory gecontroleerd: {save_path.parent}")

            # Sla de figuur op
            fig.savefig(save_path, bbox_inches="tight")
            logger.info(
                f"Plot opgeslagen als: {save_filename} in de map {self.settings.output_folder}"
            )
            print(
                f"Plot opgeslagen als: {save_filename} in de map {self.settings.output_folder}"
            )

        except Exception as e:
            logger.error(f"Fout bij het opslaan van de plot: {str(e)}")
            raise


class ColoredPlotSettings(PlotSettings):
    """Extended settings class specifically for colored plots."""

    pass


class MessageCalculations(BaseModel):
    """Settings for message calculations."""

    function_column: str = "Position"
    message_column: str = "message"
    message_length_column: str = "message_length"
