# 📘 GDP Analytics Pipeline  

### 📌 Project Overview  
This project implements a modular GDP analytics pipeline using the **Dependency Inversion Principle (DIP)** and a clean package structure.  

The system has been refactored from a script-based approach into a layered architecture where:  
- **Core module** owns the business logic and defines structural contracts.  
- **Input module** provides pluggable data sources (CSV & Excel).  
- **Output module** provides pluggable data sinks (Console & Graphics).  
- **Main module** acts as the orchestrator and performs dependency injection.  

The Core remains fully agnostic of data persistence and ingestion formats.  

---

## 🏗️ Architecture  

```
project_root/
│
├── main.py
├── config.json
│
├── core/
│   ├── __init__.py
│   ├── contracts.py
│   └── engine.py
│
├── plugins/
│   ├── __init__.py
│   ├── inputs.py
│   └── outputs.py
│
└── data/
```

---

### 🔹 Core Module (Domain Layer)  
The Core is the authority of the system.  

It defines two structural interfaces using `typing.Protocol`:  

**1️⃣ DataSink (Outbound Abstraction)**  
```python
class DataSink(Protocol):
    def write(self, records: List[dict]) -> None:
        ...
```
- The Core calls this interface to send processed results outward.  

**2️⃣ PipelineService (Inbound Abstraction)**  
```python
class PipelineService(Protocol):
    def execute(self, raw_data: List[Any]) -> None:
        ...
```
- Input modules use this interface to send raw data into the Core.  

**3️⃣ TransformationEngine**  
- Implements `PipelineService`  
- Contains all business logic  
- Receives a `DataSink` via constructor injection  
- Does not import or depend on any concrete writers  

---

### 🔹 Input Module (Source Layer)  
Provides multiple data ingestion strategies.  

**Implemented sources:**  
- `CSVReader`  
- `ExcelReader`  

Each reader:  
- Accepts a `PipelineService` in its constructor  
- Reads raw data from file  
- Passes data to `execute()` method of the injected service  

Readers are completely unaware of the Core’s internal logic.  

---

### 🔹 Output Module (Sink Layer)  
Provides pluggable output implementations.  

**Implemented sinks:**  
- `ConsoleWriter`  
- `GraphicsChartWriter`  

Each writer:  
- Implements the `write()` method  
- Satisfies the `DataSink` protocol defined in Core  
- Does not depend on Core internals  

---

### 🔹 Main Module (Orchestrator)  
`main.py` acts as the Bootstrap layer.  

**Responsibilities:**  
- Loads `config.json`  
- Selects input and output drivers via dictionary-based factory  
- Instantiates the chosen sink  
- Instantiates the Core engine (injecting sink)  
- Instantiates the input source (injecting engine)  
- Starts execution  

Dependency injection is performed here.  

---

## 🔁 Dependency Flow  

```
Input → PipelineService ← Core → DataSink ← Output
                 ↑
                Main (wires everything)
```

All dependencies point toward Core abstractions.  

---

## 🏆 Dependency Inversion Compliance  

This implementation strictly follows the Golden Rules:  
- ✅ **Inbound Abstraction** → Input depends only on `PipelineService`.  
- ✅ **Outbound Abstraction** → Core depends only on `DataSink`.  
- ✅ **Ownership of Contracts** → Protocols are defined exclusively in Core.  
- ✅ **No Circular Imports** → All wiring is performed in `main.py`.  

---

## ⚙️ Configuration (`config.json`)  

The system behavior can be changed without modifying Core logic.  

**Example:**
```json
{
  "input_type": "excel",
  "output_type": "console",
  "file_path": "data/gdp_data.xlsx",
  "region": "Asia",
  "year": 2020,
  "start_year": 2010,
  "end_year": 2020,
  "decline_years": 3
}
```

Switching from Excel to CSV or Console to Graphics requires only a config change.  

---

## 📊 Outputs Generated  
The system produces:  
- Top 10 Countries by GDP  
- Bottom 10 Countries by GDP  
- GDP Growth Rate per Country (range)  
- Average GDP by Continent  
- Total Global GDP Trend  
- Fastest Growing Continent  
- Countries with Consistent GDP Decline  
- Continent Contribution to Global GDP  

All transformation logic remains inside the Core.  

---

## 🧠 Design Principles Used  
- Dependency Inversion Principle (DIP)  
- Structural Typing via `typing.Protocol`  
- Modular Package Design  
- Dictionary-Based Factory Pattern  
- Dependency Injection  
- Functional Data Transformations (Phase 1 preserved)  

---

## ▶️ How to Run  
```bash
python main.py
```

**Ensure:**  
- `config.json` is properly configured  
- Data file exists in `/data` folder  

---

## 📌 Key Technologies Used  
- Python 3  
- `typing.Protocol`  
- JSON configuration parsing  
- Matplotlib (for graphical output)  
- Pandas (for Excel/CSV ingestion)  
