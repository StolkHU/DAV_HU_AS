# 💬 WhatsApp Gespreksanalyse Project

Dit project biedt een uitgebreide toolkit voor de analyse en visualisatie van WhatsApp gespreksdata. Het analyseert communicatiepatronen, berichtlengtes, timing en interacties tussen deelnemers in WhatsApp-gesprekken.

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![Pandas](https://img.shields.io/badge/Pandas-2.2+-green.svg)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Latest-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Projectoverzicht

Door Adriaan Stolk (1517495)  
Hogeschool Utrecht  
Cursus: Data Analysis & Visualisation

## ✨ Functionaliteiten

Het project genereert vijf verschillende visualisaties voor inzicht in WhatsApp-conversaties:

1. **📊 Vergelijking van categorieën** - Analyseert berichtlengtes per functie/rol in een hockeyteam
2. **📈 Tijdreeksanalyse** - Toont trends in berichttypen over kwartalen (bijv. foto's na geboorte)
3. **⏱️ Distributieanalyse** - Visualiseert responstijden tussen berichten
4. **🔄 Relatieanalyse** - Toont interactiepatronen tussen verschillende rollen/posities
5. **👥 Clusteranalyse** - Groepeert gebruikers op basis van communicatiestijl

## 📊 Visualisatie-voorbeelden

### Vergelijking van categorieën
![Example](img/Comparing%20Categories.png)
*Deze visualisatie toont dat stafleden gemiddeld veel langere berichten sturen dan spelers. Dit suggereert dat stafleden vaak meer gedetailleerde informatie moeten overbrengen.*

### Tijdreeksanalyse 
![Example](img/Time%20Series.png)
*Deze visualisatie toont een duidelijke toename in het delen van foto's na de geboorte van een kind in november 2022. Het percentage foto's steeg van gemiddeld 5% naar 12% in de kwartalen na de geboorte.*

## 🚀 Installatie

Deze installatiehandleiding gaat uit van een UNIX-systeem (macOS of Linux). Als u de mogelijkheid heeft om een VM te gebruiken, raadpleeg dan de referentiemap voor lab-setups. Voor wie op een Windows-machine werkt, gebruik Git Bash wanneer er wordt verwezen naar een terminal of CLI (command line interface).

### 1. Installeer Python met uv

Uv is een snelle pakketmanager voor Python. Let op: uv kan al geïnstalleerd zijn op uw VM.

1. Controleer of uv al is geïnstalleerd met:
   ```bash
   which uv
   ```
   Als het een locatie teruggeeft, bijvoorbeeld `/Users/user/.cargo/bin/uv`, dan is uv geïnstalleerd.

2. Zo niet, installeer uv met:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
   Voor macOS en Linux. Voor Windows, raadpleeg de uv-documentatie.

3. Start een nieuwe terminal en test met `which uv` of de installatie is gelukt.

### 2. Clone de Git repository

Voer in de terminal uit:
```bash
git clone https://github.com/StolkHU/DAV_HU_AS.git
```

### 3. Maak een virtuele omgeving aan en activeer deze (optioneel maar aanbevolen)

```bash
cd DAV_HU_AS
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 4. Installeer alle dependencies

Als u een uv.lock bestand heeft in het project:
```bash
uv sync
```

Of installeer alle dependencies met:
```bash
uv pip install -e .
```

Of voor ontwikkelaars, inclusief development tools:
```bash
uv pip install -e ".[dev]"
```

## 🔍 Gegevensvoorbereiding

1. Plaats een geconverteerd WhatsApp-bestand in de `data/raw/` map.
   
   Voor het converteren van WhatsApp-exports naar een bruikbaar formaat kunt u de whatsapp-analyzer vanaf https://github.com/raoulg/MADS-DAV gebruiken voor uitgebreide conversieopties.

2. Pas `config.toml` aan met de juiste bestandsnamen en locaties. Belangrijke instellingen zijn:
   ```toml
   raw = "data/raw"
   processed = "data/processed"
   current = "whatsapp.parq"  # Uw bestandsnaam hier
   role_file = "Roles.json"
   logging = "logs/code"
   output_folder = "img"
   # ... andere instellingen
   ```

3. Pas de visualisatie-instellingen in `config.toml` naar wens aan. Bijvoorbeeld voor de categorie-vergelijking:
   ```toml
   [comparing_categories]
   figsize = [10, 8]
   suptitle = "Kort maar krachtig: De communicatiekloof tussen veld en zijlijn"
   title = "Terwijl stafleden uitweiden, houden spelers het kort(er)"
   # ... andere instellingen
   ```

## 📊 Visualisaties genereren

### Alle visualisaties in één keer genereren

Zorg ervoor dat uw virtuele omgeving is geactiveerd (als u deze gebruikt):
```bash
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

Voer vervolgens uit:
```bash
python main.py
```

Alle gegenereerde visualisaties worden opgeslagen in de `img/` map zoals gespecificeerd in `config.toml`.

### Specifieke visualisaties maken

U kunt een specifieke visualisatie genereren door de bijbehorende functie rechtstreeks aan te roepen:

```python
# Alleen de categorie-vergelijking genereren
from wa_analysis.visualisation.comparing_categories import make_comparing_categories
make_comparing_categories()

# Alleen de tijdreeksanalyse genereren
from wa_analysis.visualisation.time_series import make_timeseries
make_timeseries()
```

### Snelle demo

Voor een snelle test, na het installeren van de dependencies:

```bash
# Een minimale config.toml maken met noodzakelijke instellingen
echo 'raw = "data/raw"
processed = "data/processed"
current = "whatsapp.parq"
output_folder = "img"' > config.toml

# Plaats een WhatsApp-export in data/raw

# Voer een visualisatie uit
python -c "from wa_analysis.visualisation.comparing_categories import make_comparing_categories; make_comparing_categories()"
```

## 🧪 Demo: Aan de slag

Hier volgt een volledig voorbeeld van hoe u uw eigen WhatsApp-data kunt analyseren:

```python
# Voorbeeld: Maak een aangepaste berichtlengte-analyse

import pandas as pd
import matplotlib.pyplot as plt
from wa_analysis.data_loading.config import ConfigLoader
from wa_analysis.data_loading.processor import DataProcessor
from wa_analysis.settings.settings import PlotSettings
from wa_analysis.settings.logger import Logger

# Initialiseer de logger
logger = Logger().get_logger()
logger.info("Start aangepaste analyse")

# Laad de configuratie
config_loader = ConfigLoader()
# De configuratie wordt geladen uit config.toml en bevat alle instellingen
# voor datalocaties, bestandspaden en visualisatie-eigenschappen
print(f"Output folder: {config_loader.config['output_folder']}")
print(f"Current datafile: {config_loader.config['current']}")

# Verwerk de ruwe data
processor = DataProcessor(
    config=config_loader.config, 
    datafile=config_loader.datafile_hockeyteam
)
processed_df = processor.add_columns()
logger.info(f"Data verwerkt: {processed_df.shape}")

# Voer een aangepaste analyse uit
# Bijvoorbeeld: gemiddelde berichtlengte per uur van de dag
processed_df['hour'] = processed_df['timestamp'].dt.hour
hourly_avg = processed_df.groupby('hour')['message_length'].mean().reset_index()

# Visualisatie-instellingen laden uit config.toml
# Dit laat zien hoe de settings uit het config-bestand gebruikt worden
settings = PlotSettings("custom_analysis")
fig_settings = settings.get_settings()
figsize = fig_settings.get('figsize', [12, 6])
title = fig_settings.get('title', 'Gemiddelde berichtlengte per uur')
title_fontsize = fig_settings.get('title_fontsize', 16)

# Visualiseer de resultaten
fig, ax = plt.subplots(figsize=figsize)
ax.bar(hourly_avg['hour'], hourly_avg['message_length'], color='skyblue')
ax.set_title(title, fontsize=title_fontsize)
ax.set_xlabel('Uur van de dag')
ax.set_ylabel('Gemiddelde berichtlengte')
ax.set_xticks(range(0, 24))
plt.tight_layout()

# Sla het resultaat op in de map gespecificeerd in config.toml
output_path = f"{config_loader.config['output_folder']}/custom_hourly_analysis.png"
fig.savefig(output_path)
logger.info(f"Analyse succesvol voltooid en opgeslagen in {output_path}")

print(f"Aangepaste analyse is voltooid en opgeslagen in {output_path}")
```

## 📝 Aanpassen van visualisaties

U kunt eenvoudig de bestaande visualisaties aanpassen of nieuwe maken. Dit kan in de code van de visualitie zelf of via de config.toml.

## 📁 Projectstructuur

```
DAV_HU_AS/
│
├── config.toml                           # Configuratiebestand met instellingen
├── main.py                               # Hoofdscript om alle visualisaties te genereren
│
├── data/
│   ├── raw/                              # Ruwe geëxporteerde WhatsApp data
│   └── processed/                        # Verwerkte datasets (automatisch gegenereerd)
│
├── logs/
│   └── code/                             # Logbestanden van code-uitvoering
│
├── img/                                  # Outputmap voor gegenereerde visualisaties
│
└── src/                                  # Broncode
    └── wa_analysis/                      # WhatsApp analyse modules
        ├── data_analysis/                # Modules voor het laden en verwerken van data
        │   └── model.py                  # Module om de textclustering te analyseren
        │
        ├── data_loading/                 # Modules voor het laden en verwerken van data
        │   ├── config.py                 # Configuratielader
        │   ├── dataloader.py             # Basisklasse voor het laden van data
        │   ├── processor.py              # Verwerking van ruwe data
        │   └── merger.py                 # Samenvoegen van dataframes
        │
        ├── settings/                     # Instellingen en utilities
        │   ├── baseplot.py               # Basisklasse voor visualisaties
        │   ├── colored_bar_chart.py      # Gekleurde staafdiagrammen
        │   ├── logger.py                 # Logging functionaliteit
        │   └── settings.py               # Visualisatie-instellingsbeheer
        │
        └── visualisation/ # Visualisatiemodules
            ├── comparing_categories.py   # Vergelijking van berichtlengtes
            ├── clustering.py             # Clusteranalyse van gebruikers
            ├── distribution.py           # Distributieanalyse
            ├── relationships.py          # Relationele analyse
            └── time_series.py            # Tijdreeksanalyse
```

## 🛠️ Gebruikte technologieën

- **Python 3.12+**: Basis programmeertaal
- **pandas**: Krachtige dataframes voor dataverwerking en -manipulatie
- **matplotlib & seaborn**: Uitgebreide visualisatiebibliotheken
- **tomllib**: Beheer van configuratiebestanden in TOML-formaat
- **pathlib**: Moderne manier voor bestandssysteembewerkingen
- **scikit-learn**: Voor clusteranalyse en machine learning componenten
- **sentence-transformers**: Voor tekstembedding
- **plotly**: Voor interactieve visualisaties
- **torch**: Voor machine learning modellen
- **transformers**: Voor NLP taken en tekstverwerking
- **loguru**: Voor uitgebreide logging functionaliteit

## 📦 Projectdependencies

De dependencies voor dit project zijn gedefinieerd in een `pyproject.toml` bestand. De belangrijkste dependencies zijn:

```toml
[project]
name = "dav-hu-as"
version = "0.1.0"
description = "This is the code for the assignments of Adriaan Stolk for the course Data Analysis and Visualization"
requires-python = ">=3.12"
dependencies = [
    "fastparquet>=2024.11.0",
    "loguru>=0.7.3",
    "matplotlib>=3.10.1",
    "numpy>=2.2.3",
    # ... andere dependencies
]

[dependency-groups]
dev = [
    "black>=25.1.0",
    "isort>=6.0.1",
    "mypy>=1.15.0",
    "ruff>=0.9.9",
    # ... andere development dependencies
]
```

U kunt dit gebruiken met tools zoals pip, uv of hatch om de benodigde afhankelijkheden te installeren zoals beschreven in de installatie-instructies.

## 💻 Ontwikkeltools en linters

Dit project gebruikt moderne ontwikkeltools voor codekwaliteit:

- **black**: Code formatter die zorgt voor consistente stijl
- **isort**: Automatisch ordenen van imports
- **mypy**: Statische typechecker voor Python
- **ruff**: Snelle Python linter voor code kwaliteitscontrole
- **hatch**: Modern project beheer en packaging tool

Deze tools kunnen geïnstalleerd worden met:

```bash
pip install black isort mypy ruff hatch
```

Of als u uv gebruikt:

```bash
uv add black isort mypy ruff hatch --dev
```

### Lefthook

Dit project gebruikt Lefthook voor git hooks management. Lefthook zorgt ervoor dat code-kwaliteitscontroles automatisch worden uitgevoerd vóór commits.

Installatie:
```bash
pip install lefthook
lefthook install
```

Lefthook voert bij elke commit automatisch de volgende controles uit:
- Code formattering met `black`
- Import sortering met `isort`
- Linting met `ruff`
- Typecontrole met `mypy`

### .gitignore

Het project bevat een `.gitignore` bestand dat veelvoorkomende Python bestanden uitsluit van versiebeheer, zoals:
- Python bytecode en cachebestanden
- Virtuele omgevingen
- Gegenereerde bestanden en logs
- IDE-specifieke mappen

### uv.lock

Het `uv.lock` bestand wordt gegenereerd door de UV package manager en bevat exacte versies van alle dependencies voor reproduceerbare builds. Om een exacte omgeving te reconstrueren met het lock-bestand:

```bash
uv sync
```

## 📄 Configuratiebestanden en tools overzicht

In één oogopslag:

### Configuratiebestanden
- **config.toml**: Bevat paden, bestandsnamen en visualisatie-instellingen voor het project.
- **pyproject.toml**: Definieert projectmetadata, dependencies en build-instructies.
- **uv.lock**: Bevat exacte versies van alle afhankelijkheden voor reproduceerbare builds.
- **.gitignore**: Specificeert bestanden en mappen die Git moet negeren.
- **lefthook.yml**: Configureert pre-commit hooks voor automatische code-kwaliteitscontroles.

### Code kwaliteitstools
- **black**: Formatteert Python-code volgens een consistente stijl.
- **isort**: Sorteert imports op een gestandaardiseerde manier.
- **ruff**: Snelle linter voor het identificeren van veelvoorkomende Python-problemen.
- **mypy**: Statische typechecker voor Python.

## 📝 Logging

Het project gebruikt een uitgebreid loggingsysteem op basis van de `loguru` bibliotheek, waardoor ontwikkelaars en gebruikers:

1. Gedetailleerde informatie krijgen over de uitvoering van code
2. Problemen gemakkelijker kunnen diagnosticeren
3. Performance-metingen kunnen verzamelen

### Log structuur en locatie

Logbestanden worden opgeslagen in de `logs/code/` map zoals gespecificeerd in `config.toml`. Een typisch logbestand bevat timestamp, logniveau, en gedetailleerde berichten:

```
2025-04-18 15:30:22.241 | INFO     | wa_analysis.data_loading.processor:process_data:42 - Verwerking van datafile gestart
2025-04-18 15:30:23.154 | DEBUG    | wa_analysis.data_loading.processor:add_columns:78 - Berekening van message_length gestart
2025-04-18 15:30:24.012 | INFO     | wa_analysis.data_loading.processor:add_columns:92 - Feature engineering voltooid: 5 nieuwe kolommen toegevoegd
2025-04-18 15:30:24.510 | WARNING  | wa_analysis.visualisation.time_series:make_timeseries:133 - Ontbrekende waarden gedetecteerd in tijdreeks
```

## 🔍 Probleemoplossing

### Veelvoorkomende problemen

1. **Importfouten:** Als u importfouten krijgt, controleer dan of u de virtuele omgeving correct heeft geactiveerd en of u het project uitvoert vanuit de hoofdmap.

   ```bash
   cd /pad/naar/DAV_HU_AS
   source venv/bin/activate  # of venv\Scripts\activate op Windows
   ```

2. **Ontbrekende mappen:** Als u fouten krijgt over ontbrekende mappen, maak deze dan handmatig aan:

   ```bash
   mkdir -p data/raw data/processed logs/code img
   ```

3. **Plotweergaveproblemen:** Als u problemen heeft met het weergeven van plots, probeer dan:

   ```python
   import matplotlib
   matplotlib.use('Agg')  # Voor omgevingen zonder GUI
   ```

### Pakketconflicten

Als u pakketconflicten tegenkomt, is het aanbevolen om een schone virtuele omgeving te maken:

```bash
# Verwijder oude venv
rm -rf venv  # Linux/macOS
rmdir /s /q venv  # Windows

# Maak nieuwe venv
python -m venv venv
source venv/bin/activate  # of venv\Scripts\activate op Windows
pip install --upgrade pip
pip install -e .
```

## 🔮 Toekomstige uitbreidingen

Mogelijke verbeteringen en uitbreidingen:

- 🧠 **Sentimentanalyse**: Het analyseren van de emotionele toon van berichten
- 🖥️ **Interactieve visualisaties**: Dashboard-implementatie met Plotly/Dash
- 🌐 **Meertalige ondersteuning**: Betere ondersteuning voor niet-Nederlandse berichten
- 📊 **Netwerkanalyse**: Visualiseren van communicatienetwerken tussen deelnemers
- 🔄 **Continue integratie**: Automatische tests en deployments

## 🤝 Bijdragen

Dit project is ontwikkeld als onderdeel van de cursus Data Analysis & Visualisation aan de Hogeschool Utrecht. Bijdragen en suggesties zijn welkom via issues of pull requests.

## 📜 Licentie

Dit project is beschikbaar onder de MIT-licentie.