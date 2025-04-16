# 💬 WhatsApp Gespreksanalyse Project

Dit project biedt een uitgebreide toolkit voor de analyse en visualisatie van WhatsApp gespreksdata. Het analyseert communicatiepatronen, berichtlengtes, timing en interacties tussen deelnemers in WhatsApp-gesprekken.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-green.svg)
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
        │   ├── model.py                  # Module om de textclustering te analyseren
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

- **Python 3.10+**: Basis programmeertaal
- **pandas**: Krachtige dataframes voor dataverwerking en -manipulatie
- **matplotlib & seaborn**: Uitgebreide visualisatiebibliotheken
- **tomllib**: Beheer van configuratiebestanden in TOML-formaat
- **pathlib**: Moderne manier voor bestandssysteembewerkingen
- **scikit-learn**: Voor clusteranalyse en machine learning componenten

## 🚀 Installatie

1. Clone de repository:
   ```bash
   git clone https://github.com/StolkHU/DAV_HU_AS.git
   cd DAV_HU_AS
   ```

2. Maak een virtuele omgeving aan (optioneel maar aanbevolen):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

3. Installeer de benodigde packages met uv:
   ```bash
   uv install
   ```

   Als u geen uv heeft, kunt u het installeren via:
   ```bash
   pip install uv
   ```

## 🔍 Gegevensvoorbereiding

1. Plaats een geconverteerd WhatsApp-bestand in de `data/raw/` map.
   
   Voor het converteren van WhatsApp-exports naar een bruikbaar formaat kunt u de whatsapp-analyzer vanaf https://github.com/raoulg/MADS-DAV gebruiken voor uitgebreide conversieopties.

2. Update `config.toml` met de juiste bestandsnamen en locaties:
   ```toml
   raw = "data/raw"
   processed = "data/processed"
   current = "hockeyteam.parq"   # Uw bestandsnaam hier
   ```

3. Update de visualisatie-instellingen in `config.toml` naar wens:
   ```toml
   [comparing_categories]
   figsize = [10, 6]
   suptitle = "Mijn analyse titel"
   suptitle_fontsize = 16
   ```

## 📊 Visualisaties genereren

### Alle visualisaties in één keer genereren

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

# Visualiseer de resultaten
fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(hourly_avg['hour'], hourly_avg['message_length'], color='skyblue')
ax.set_title('Gemiddelde berichtlengte per uur', fontsize=16)
ax.set_xlabel('Uur van de dag')
ax.set_ylabel('Gemiddelde berichtlengte')
ax.set_xticks(range(0, 24))
plt.tight_layout()

# Sla het resultaat op
fig.savefig('img/custom_hourly_analysis.png')
logger.info("Analyse succesvol voltooid en opgeslagen")

print("Aangepaste analyse is voltooid en opgeslagen in img/custom_hourly_analysis.png")
```

## 📝 Aanpassen van visualisaties

U kunt eenvoudig de bestaande visualisaties aanpassen of nieuwe maken. Hier is een voorbeeld van het aanpassen van de kleurenschema's:

```python
# Voorbeeld: De ColoredBarPlot klasse gebruiken met aangepaste kleuren
from wa_analysis.settings.colored_bar_chart import ColoredBarPlot
from wa_analysis.settings.settings import PlotSettings
import pandas as pd

# Uw data voorbereiden
data = pd.DataFrame({
    'Groep': ['A', 'B', 'C', 'D'],
    'Waarde': [10, 15, 7, 12]
})

# Instellingen laden (of een eigen instantie maken)
settings = PlotSettings("custom_section")

# Maak de plot met aangepaste kleuren
plot = ColoredBarPlot(settings.settings)
(plot
  .set_rotation(45)  # Roteer de x-as labels
  .plot(
      data=data,
      x_column='Groep',
      y_column='Waarde',
      add_value_labels=True,
      palette=['#ff6b6b', '#48dbfb', '#1dd1a1', '#f368e0']  # Aangepaste kleuren
  )
  .save_plot("mijn_aangepaste_plot.png")
)
```

## 📊 Visualisatie-voorbeelden

### Vergelijking van categorieën
![Example](img/Comparing%20Categories_v1.png)
*Deze visualisatie toont dat stafleden gemiddeld veel langere berichten sturen dan spelers. Dit suggereert dat stafleden vaak meer gedetailleerde informatie moeten overbrengen.*

### Tijdreeksanalyse 
![Example](img/Time%20Series_v1.png)
*Deze visualisatie toont een duidelijke toename in het delen van foto's na de geboorte van een kind in november 2022. Het percentage foto's steeg van gemiddeld 5% naar bijna 15% in de kwartalen na de geboorte.*

## 📈 Prestaties en optimalisaties

Het project implementeert verschillende optimalisaties:

- **Caching van verwerkte data**: Verwerkte data wordt opgeslagen voor hergebruik om herhaalde berekeningen te voorkomen
- **Logging**: Uitgebreide logging voor debugging en performance-monitoring
- **Modulair ontwerp**: Componenten kunnen onafhankelijk worden gebruikt voor maximale flexibiliteit

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