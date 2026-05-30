# Forest Land Valuation System

Predicts the market price of forested cadastral parcels in Estonia using a LightGBM regression model.

## Data sources

- **SQLite database** (`../metsad.sqlite`) — property sales records (cadastral number, area, county, sale date, price)
- **Metsaregister XML files** (`../metsaregister_xml/`, `../metsaregister_cache/`) — forest stand geometry used to derive parcel centroid coordinates (EPSG:3301)
- **Estonian soil map WFS** (`inspire.geoportaal.ee`) — soil type fetched per parcel centroid; responses cached in `cache/soil_type/`

## Setup

```bash
conda activate silva
pip install -r requirements.txt
```

## Pipeline

### 1. Preprocess

Reads the SQLite DB and XML files, outputs `data/training_data.parquet`.

```bash
bash reg_preprocess.sh
# or: python -m regression.preprocess
```

### 2. Train

Trains a LightGBM model on the parquet data and saves it to `regression/models/saved_models/latest_model.pkl`.

```bash
bash reg_train.sh
# or: python -m regression.train
```

### 3. Evaluate

```bash
python -m regression.evaluate
```

## Features

| Feature | Description |
|---|---|
| `area` | Parcel area |
| `maakond` | County (one-hot encoded) |
| `sale_date` | Sale date as seconds offset from 2025-01-01 |
| `epsg_x` / `epsg_y` | Parcel centroid in EPSG:3301 |
| `soilbodylabel` | Soil type code from Estonian soil map (e.g. `Go`) |
| `soil_profile` | Soil profile designation from `gml_name` (e.g. `pl30-80`) |
| `soil_mod` | Soil modifiers from `gml_name` (e.g. `r₁ls₃`) |

## Project structure

```
├── configs/            # Model hyperparameters
├── data/               # Processed training data
├── cache/
│   └── soil_type/      # WFS response cache (git-ignored)
├── regression/
│   ├── preprocess.py   # SQLite + XML + WFS → parquet
│   ├── train.py        # Model training
│   ├── evaluate.py     # Model evaluation
│   └── features/       # Feature engineering pipeline
├── tools/
│   ├── various.py      # XML parsing, coordinate utilities
│   └── soil_type.py    # Soil type WFS fetch + cache + parse
├── rule_based/         # Rule-based valuation layers (WIP)
├── hybrid/             # Ensemble of rule-based + regression (WIP)
└── evaluation/         # Cross-model comparison tools (WIP)
```
