### Code for running the project ###

# Import packages
import sys
import traceback
from datetime import datetime

# Import modules
from wa_analysis.settings.logger import Logger
from wa_analysis.visualisation.clustering import make_clustering
from wa_analysis.visualisation.comparing_categories import \
    make_comparing_categories
from wa_analysis.visualisation.distribution import make_distribution
from wa_analysis.visualisation.relationships import make_relationships
from wa_analysis.visualisation.time_series import make_timeseries


def setup_logging():
    """
    Configureer logging voor het project.
    Gebruikt de bestaande Logger klasse.

    Returns:
        logger: Geconfigureerde logger
    """
    # Gebruik de bestaande Logger klasse
    logger_instance = Logger()
    return logger_instance.get_logger()


def run_visualization(name, func, logger):
    """
    Voer een visualisatiefunctie uit met foutafhandeling.

    Args:
        name: Naam van de visualisatie
        func: Functie die de visualisatie maakt
        logger: Logger voor log berichten

    Returns:
        Success status (True/False)
    """
    logger.info(f"Start visualisatie: {name}")
    start_time = datetime.now()

    try:
        # Voer de visualisatiefunctie uit
        func()

        elapsed = datetime.now() - start_time
        logger.info(
            f"Visualisatie {name} voltooid in {elapsed.total_seconds():.2f} seconden"
        )
        return True

    except Exception as e:
        elapsed = datetime.now() - start_time
        logger.error(
            f"Fout in visualisatie {name} na {elapsed.total_seconds():.2f} seconden: {e}"
        )
        logger.error(traceback.format_exc())
        return False


def run_project():
    """
    Voer het volledige project uit.
    """
    # Setup logging
    logger = setup_logging()
    logger.info("Start WhatsApp Analyse project")

    # Maak een lijst van alle visualisaties
    visualizations = [
        ("comparing_categories", make_comparing_categories),
        ("timeseries", make_timeseries),
        ("distribution", make_distribution),
        ("relationships", make_relationships),
        ("clustering", make_clustering),
    ]

    # Houd bij welke visualisaties succesvol waren
    success_count = 0

    # Voer elke visualisatie uit met foutafhandeling
    for name, func in visualizations:
        if run_visualization(name, func, logger):
            success_count += 1

    # Rapporteer eindresultaat
    total = len(visualizations)
    logger.info(
        f"Project voltooid: {success_count}/{total} visualisaties succesvol gemaakt"
    )

    if success_count < total:
        logger.warning(
            "Niet alle visualisaties konden worden gemaakt. Zie bovenstaande fouten."
        )

    return success_count == total


if __name__ == "__main__":
    # Voer het project uit
    success = run_project()

    # Stel juiste exit code in
    sys.exit(0 if success else 1)
