## A settings python program

from typing import List, Optional

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pydantic import BaseModel


# Base plot settings
class PlotSettings(BaseModel):
    """Base settings for all plots."""

    title: str = ""
    xlabel: str = ""
    ylabel: str = ""
    figsize: tuple = (10, 6)
    rotation: int = 0
    legend_title: Optional[str] = None


# Colored plot settings
class ColoredPlotSettings(PlotSettings):
    """Settings for plots with color palettes and a default color grey."""

    color_palette: str = "coolwarm"
    color_color: str = "silver"


class MessageCalculations(BaseModel):
    """Settings for message calculations."""

    function_column: str = "Function"
    message_column: str = "message"
    message_length_column: str = "message_length"
