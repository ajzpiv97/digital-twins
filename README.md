# 🚀 Digital Twin: Rocket Engine Failure Detection & Response

This project is an advanced, interactive digital twin dashboard built with **Streamlit** and powered by the **Prometheux Engine (Vadalog)**. It visualizes and simulates complex telemetry data, dependency graphs, and failure propagation chains for critical aerospace hardware components (like the High-Pressure Oxidizer Turbopump - HPOTP).

## ✨ Key Features & Highlights

### 1. 📊 Intelligent Dashboard & KPIs
- **System Overview:** Immediately highlights the current state of the engine, including Monitored Components, Critical Hotspots, and high-risk nodes based on network centrality.
- **Vadalog Reasoning Integration:** Features a persistent tracking system indicating the exact timestamp of the last executed reasoning pipeline (`last_run.txt`).
- **Seamless Refresh:** A side-panel button allows authorized users to re-run the `prometheux_chain` SDK on the backend, recalculating centrality, shortest paths, and hotspot metadata on the fly.

### 2. 🌍 Interactive Topology & Diagnostics
- **Network Graph Rendering:** Uses PyVis to generate a highly interactive dependency and severity graph. Nodes are color-coded (Red = Critical Hotspots, Orange = Downstream Impact, Green = Healthy) and sized dynamically based on their importance.
- **Parent/Child Relationships:** Easily explore downstream dependencies via expanding dataframes, mapping out how single components relate to the broader system topology.

### 3. 🌋 Dynamic Failure Propagation Tracing
- **Visual Timelines:** A native Streamlit timeline UI traces exact failure propagation sequences (e.g., from `TEMP_SENSOR_C` failing, rippling down to the `MAIN_COMBUSTION_CHAMBER`).
- **Signature Selection:** Intelligent dropdowns allow you to isolate and trace specific "Root Cause Signatures" without cluttering the screen.

### 4. 🛠️ Actionable Root Cause Analysis (RCA) Simulation
- **Personnel Routing:** Translates abstract data anomalies into human tasks. It maps failing components directly to their explicitly assigned engineering leads and response teams.
- **Simulated Resolution Flow:** An interactive "Page Team & Send Diagnostic Report" button allows users to "resolve" an active issue. 
    - The system actively uses `st.session_state` to instantly filter out resolved anomalies.
    - Components instantly vanish from the Hotspot list, Topology graph, Centrality metrics, and top-level KPIs, simulating a dynamically healing system.
- **State Reset:** A local override button on the sidebar allows users to reset the simulated memory and bring all historical anomalies back for repeated demonstrations.

## 🗂️ Project Structure

- `app/main.py`: The core Streamlit entry point, handling layout, Dataframe loading, top-level KPI rendering, and state management filters.
- `app/views/`:
  - `live_diagnostics.py`: The primary 2-column interface housing the Topology Graph and the Propagation Trace.
  - `root_cause_analysis.py`: The secondary interface for reviewing system triggers and interacting with the Personnel Routing tools.
- `app/components/`:
  - `graphs.py`: PyVis interactive network generation.
  - `propagation.py`: Vertical sequence timelines.
  - `refresh.py`: Logic for executing Vadalog cloud programs and resetting simulated local states.
- `src/digital_twin/`: Houses the backend data structures, mock data fallback logic (`data_loader.py`), settings management (`settings.py`), and system loggers.

## 🚀 Running the App

### Prerequisites
- Python 3.12+ (as specified in `pyproject.toml`)
- Install the package and its dependencies in editable mode:
  ```bash
  pip install -e .
  ```

### Running Locally
To launch the dashboard using mock/fallback data without requiring active platform credentials:

```bash
cd app
streamlit run main.py
```

*Note: In local mode, the "Refresh Analysis" button is replaced with a "Reset Local Simulation State" button.*

### Running with Live Prometheux Platform
To enable live re-calculations using actual Vadalog reasoning:

1. Copy `.env.example` to `.env` (if applicable) or set your variables directly.
2. Ensure you have the following environment variables configured:
   - `APP_ENV=platform`
   - `PMTX_TOKEN=your_secure_token`
   - `PMTX_PROJECT=your_project_name`
3. Run the application:
```bash
streamlit run app/main.py
```