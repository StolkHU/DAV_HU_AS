# WhatsApp Gespreksanalyse Project

Dit project biedt een uitgebreide toolkit voor de analyse en visualisatie van WhatsApp gespreksdata. Het analyseert communicatiepatronen, berichtlengtes, timing en interacties tussen deelnemers in WhatsApp-gesprekken.

## Projectoverzicht

Door Adriaan Stolk (1517495)  
Hogeschool Utrecht  
Cursus: Data Analysis & Visualisation

## Functionaliteiten

Het project genereert vijf verschillende visualisaties voor inzicht in WhatsApp-conversaties:

1. **Vergelijking van categorieën** - Analyseert berichtlengtes per functie/rol in een hockeyteam
2. **Tijdreeksanalyse** - Toont trends in berichttypen over kwartalen (bijv. foto's na geboorte)
3. **Distributieanalyse** - Visualiseert responstijden tussen berichten
4. **Relatieanalyse** - Toont interactiepatronen tussen verschillende rollen/posities
5. **Clusteranalyse** - Groepeert gebruikers op basis van communicatiestijl

## Projectstructuur

```
DAV_HU_AS/
│
├── config.toml           # Configuratiebestand met instellingen
├── main.py               # Hoofdscript om alle visualisaties te genereren
│
├── data/
│   ├── raw/              # Ruwe geëxporteerde WhatsApp data
│   └── processed/        # Verwerkte datasets (automatisch gegenereerd)
│
├── logs/
│   └── code/             # Logbestanden van code-uitvoering
│
├── img/                  # Outputmap voor gegenereerde visualisaties
│
└── src/                  # Broncode
    └── wa_analysis/      # WhatsApp analyse modules
        ├── data_loading/ # Modules voor het laden en verwerken van data
        │   ├── config.py         # Configuratielader
        │   ├── dataloader.py     # Basisklasse voor het laden van data
        │   ├── processor.py      # Verwerking van ruwe data
        │   └── merger.py         # Samenvoegen van dataframes
        │
        ├── settings/     # Instellingen en utilities
        │   ├── baseplot.py       # Basisklasse voor visualisaties
        │   ├── colored_bar_chart.py # Gekleurde staafdiagrammen
        │   ├── logger.py         # Logging functionaliteit
        │   └── settings.py       # Visualisatie-instellingsbeheer
        │
        └── visualisation/ # Visualisatiemodules
            ├── comparing_categories.py # Vergelijking van berichtlengtes
            ├── clustering.py      # Clusteranalyse van gebruikers
            ├── distribution.py    # Distributieanalyse
            ├── relationships.py   # Relationele analyse
            └── time_series.py     # Tijdreeksanalyse
```

## Gebruikte technologieën

- **Python 3.10+**
- **pandas**: Dataverwerking en -manipulatie
- **matplotlib & seaborn**: Datavisualisatie
- **tomllib**: Configuratiebeheer
- **pathlib**: Bestandssysteembewerkingen

## Installatie

1. Clone de repository:
   ```bash
   git clone https://github.com/StolkHU/DAV_HU_AS.git
   cd DAV_HU_AS

2. Installeer de benodigde packages met uv:
   ```bash
   uv install
   ```

## Gebruik

### Gegevensvoorbereiding

1. Plaats een geconverteerd WhatsApp-bestand in de `data/raw/` map (zie https://github.com/raoulg/MADS-DAV om een download van WhatsApp-data te processen)
2. Update `config.toml` met de juiste bestandsnamen en locaties
3. Update `config.toml` met specifieke wensen per visualisatie (zoals lettertype groottes of andere styling)

### Alle visualisaties genereren

```bash
python main.py
```

Gegenereerde visualisaties worden opgeslagen in de `img/` map zoals gespecificeerd in `config.toml`.

### Een specifieke visualisatie maken

Je kunt een specifieke visualisatie genereren door de bijbehorende functie rechtstreeks aan te roepen, bijvoorbeeld:

```python
from wa_analysis.visualisation.comparing_categories import make_comparing_categories
make_comparing_categories()
```

## Dataset

Dit project analyseert twee WhatsApp chatgeschiedenissen:
1. Een hockeyteamchat met spelers en staf
2. Een privéchat tussen partners

De analyses tonen verschillende communicatiepatronen in beide contexten. Het is ook mogelijk om eigen data in het project te laden.

## Visualisatie-voorbeelden

### Vergelijking van categorieën
![Example](img/Comparing%20Categories_v1.png)
*Deze visualisatie toont dat stafleden gemiddeld veel langere berichten sturen dan spelers.*

### Tijdreeksanalyse 
![Example](img/Time%20Series_v1.png)
*Deze visualisatie toont een toename in het delen van foto's na de geboorte van een kind.*

## Toekomstige uitbreidingen

Mogelijke verbeteringen en uitbreidingen:
- Sentimentanalyse van berichten
- Interactieve visualisaties met Plotly
- Uitgebreidere natuurlijke taalverwerking
- Ondersteuning voor meerdere talen
- Netwerkanalyse van communicatiepatronen

## Bijdragen

Dit project is ontwikkeld als onderdeel van de cursus Data Analysis & Visualisation aan de Hogeschool Utrecht. Bijdragen en suggesties zijn welkom via issues of pull requests.
