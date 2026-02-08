# 🌍 GDP Analytics Dashboard

A modular Python project for **loading, cleaning, processing, and visualizing GDP data** by region and year. The system reads a configuration file, computes statistics, and renders a multi-chart analytical dashboard using Matplotlib.

---

## 📁 Project Structure

```
project/
│
├── dashboard.py        # Main dashboard & visualization logic
├── DataLoader.py       # Data loading and validation
├── DataProcesser.py    # Data cleaning, filtering, and statistics
├── utility.py          # Helper utility functions
├── config.json         # Configuration file
├── gdp_with_continent_filled.xlsx
└── README.md
```

---

## ⚙️ Configuration (`config.json`)

The dashboard behavior is fully controlled using a JSON configuration file.

```json
{
  "region": "Europe",
  "year": 1998,
  "operation": "average",
  "output": "sum"
}
```

### Configuration Fields

| Key         | Type    | Description                                      |
| ----------- | ------- | ------------------------------------------------ |
| `region`    | string  | Continent/region to analyze (e.g., Europe, Asia) |
| `year`      | integer | Year of GDP analysis                             |
| `operation` | string  | Statistical operation (`sum` or `average`)       |
| `output`    | string  | Reserved for future output handling              |

---

## 📦 Modules Documentation

---

## 🔧 `utility.py`

### `safeExtend(lst, value)`

Safely appends a value to a list. If the value itself is a list, it extends instead of nesting.

```python
def safeExtend(lst, value):
    if isinstance(value, list):
        lst.extend(value)
    else:
        lst.append(value)
    return lst
```

**Purpose:**
Used to dynamically construct column lists without worrying about list nesting.

---

## 📥 `DataLoader.py`

Handles loading and validation of the GDP dataset.

### `loadData()`

Loads the Excel dataset.

### `validateData(loadedData)`

Ensures:

* Dataset has expected dimensions (266 × 70)
* Required columns (countries, continent, years) exist

### `restructureData(loadedData)`

Extracts only expected columns and returns the **Raw Data Set (RDS)**.

### `loadModule()`

Pipeline function that:

1. Loads data
2. Validates structure
3. Restructures dataset

Returns the raw dataset (`rds`).

---

## 🧹 `DataProcesser.py`

Responsible for cleaning, filtering, and computing statistics.

### `fields`

A list of years from **1960 to 2024** used for time-series processing.

---

### `fillNull(index, rds)`

Fills missing GDP values for a country by replacing `NaN` with the **mean GDP** of valid years.

---

### `cleanData(rds)`

Applies `fillNull` across all rows to produce a **cleaned dataset**.

---

### `filterAttributes(index, ds, year)`

Extracts selected attributes:

* Country Name
* Country Code
* Continent
* GDP for selected year

---

### `filterData(ds, region, year)`

Filters the dataset by region and year.

Returns a **Filtered Data Set (FDS)**.

---

### `statistics(fds, op, year)`

Computes statistics on filtered GDP values.

| Operation | Result    |
| --------- | --------- |
| `sum`     | Total GDP |
| `average` | Mean GDP  |

---

### `processModule(rds, region, year)`

Complete processing pipeline:

1. Clean raw data
2. Filter by region and year

---

## 📊 `dashboard.py`

The main visualization and orchestration module.

### Responsibilities

* Reads & validates configuration
* Loads and processes data
* Computes statistics
* Renders a **4-panel dashboard** with a styled header

---

## 🖥 Dashboard Layout

### 🟦 Header Section

Displays:

* Dashboard title
* Selected region, year, operation
* Computed GDP statistic

Rendered using a dedicated Matplotlib axis with a colored background.

---

### 📈 Visualizations

| Position     | Chart Type   | Description                                      |
| ------------ | ------------ | ------------------------------------------------ |
| Top-left     | Bar Chart    | GDP per country                                  |
| Top-right    | Pie Chart    | GDP distribution (labels hidden for slices <10°) |
| Bottom-left  | Line Chart   | Total regional GDP over years                    |
| Bottom-right | Scatter Plot | GDP trend points                                 |

---

## ▶️ How to Run

```bash
python dashboard.py
```

Ensure:

* `config.json` exists
* `gdp_with_continent_filled.xlsx` is present
* Required Python packages are installed

---

## 📚 Dependencies

* Python 3.x
* pandas
* matplotlib

Install dependencies:

```bash
pip install pandas matplotlib
```

---

## ✅ Key Features

* Modular architecture
* Configuration-driven analysis
* Automatic data cleaning
* Clear, multi-view dashboard
* Professional visualization practices

---

## 🚀 Future Improvements

* Interactive dashboards (Plotly / Dash)
* Export visualizations to files
* Support multiple regions simultaneously
* Enhanced error handling

---

Happy analyzing! 📊✨
