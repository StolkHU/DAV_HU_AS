import logging
import tomllib
from pathlib import Path
from typing import Any, Dict, Optional


class Logger:
    """
    A reusable logging class for WhatsApp data analysis.

    This class sets up a logger that can be imported and used across
    multiple Python modules in the WhatsApp visualization project.
    """

    _instance: Optional["Logger"] = None  # Singleton pattern

    def __new__(cls, *args: Any, **kwargs: Any) -> "Logger":
        """Implement singleton pattern to ensure only one logger exists."""
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(
        self, config_path: str = "./config.toml", log_level: int = logging.INFO
    ) -> None:
        """
        Initialize the logger using configuration from a TOML file.

        Args:
            config_path: Path to the TOML configuration file
            log_level: The logging level (default: logging.INFO)
        """
        # Only initialize once (singleton pattern)
        if getattr(self, "_initialized", False):
            return

        self.logger: logging.Logger = logging.getLogger("whatsapp_analysis")
        self.logger.setLevel(log_level)

        # Load configuration
        self.config_file: Path = Path(config_path).resolve()
        try:
            with self.config_file.open("rb") as f:
                self.config: Dict[str, Any] = tomllib.load(f)
        except (FileNotFoundError, tomllib.TOMLDecodeError) as e:
            raise ValueError(f"Failed to load config file: {e}")

        # Set up log file
        root: Path = Path("./").resolve()
        log_folder: Path = root / Path(self.config.get("logging", "logs"))

        # Create log directory if it doesn't exist
        log_folder.mkdir(parents=True, exist_ok=True)

        # Get log filename from config or use default
        log_file: str = self.config.get("log_file", "whatsapp_analysis.log")
        log_path: Path = log_folder / log_file

        # Create and configure file handler
        file_handler: logging.FileHandler = logging.FileHandler(log_path, mode="w")
        formatter: logging.Formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)

        # Add console handler too (optional - for immediate feedback)
        console_handler: logging.StreamHandler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        # Add handlers to logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

        self.logger.info(f"Logger initialized. Log file: {log_path}")
        self._initialized = True

    def get_logger(self) -> logging.Logger:
        """Get the configured logger instance."""
        return self.logger

    def get_config(self) -> Dict[str, Any]:
        """Get the loaded configuration."""
        return self.config
