
# 🌍 AI Trip Planner – Agentic Travel & Expense Planning System

An **agentic AI-powered travel planning application** that generates **comprehensive end-to-end travel itineraries**, including detailed cost breakdowns, daily budgets, weather insights, and destination planning.

This project demonstrates **modern agentic AI engineering** using **FastAPI, LangGraph, LangChain, and Streamlit**, with a strong focus on **tool-based reasoning, graph-driven workflows, and robust handling of real-world LLM inputs**.

---
## 🎥 Demo Video

A demo video demonstrates:

https://github.com/user-attachments/assets/c1dd50ce-c26f-4399-8531-c7afebc9b40e

---

## 🚀 Features

- ✈️ **Travel Planning**
  - Day-by-day itinerary
  - Tourist & off-beat locations
  - Activities and transportation guidance

- 💰 **Expense & Budget Planning**
  - Hotel cost estimation
  - Total trip expense calculation
  - Per-day budget estimation
  - Currency conversion

- 🌦️ **Weather Insights**
  - Current weather
  - Weather forecast support

- 🧠 **Agentic Workflow**
  - LangGraph-based agent
  - Explicit tool binding (no hallucinated tools)
  - Defensive numeric parsing for LLM safety

- 🖥️ **User Interface**
  - FastAPI backend
  - Streamlit frontend

---

## 🧠 Agent Design Philosophy

This project is **not a simple prompt-based chatbot**.

It follows a **graph-based agent architecture**, where:
- The LLM performs structured reasoning
- Only **explicitly registered tools** can be called
- Tool hallucinations are prevented via:
  - Tool binding
  - Capability-aligned system prompts
- Numeric inputs are sanitized to handle realistic LLM outputs like:
  - `"3500 INR"`
  - `"₹1200 per night"`
  - `"about 5000"`

This design makes the system **robust, predictable, and production-oriented**.

---

## 🧩 Project Architecture

```
AI_TRIP_PLANNER/
│
├── agent/
│   ├── __init__.py
│   └── agentic_workflow.py        # LangGraph agent definition
│
├── config/
│   ├── __init__.py
│   └── config.yaml                # Centralized configuration
│
├── notebook/
│   └── experiments.ipynb          # Experiments & prototyping
│
├── prompt_library/
│   ├── __init__.py
│   └── prompt.py                  # System prompt
│
├── tools/
│   ├── __init__.py
│   ├── arithmetic_op_tool.py
│   ├── currency_conversion_tool.py
│   ├── expense_calculator_tool.py
│   ├── place_search_tool.py
│   └── weather_info_tool.py
│
├── utils/
│   ├── __init__.py
│   ├── config_loader.py
│   ├── currency_converter.py
│   ├── expense_calculator.py
│   ├── model_loader.py
│   ├── number_parser.py
│   ├── place_info_search.py
│   ├── save_to_document.py
│   └── weather_info.py
│
├── main.py                        # FastAPI entry point
├── streamlit_app.py               # Streamlit UI
├── requirements.txt
├── pyproject.toml
├── setup.py
├── README.md
└── my_graph.png                   # Agent workflow visualization
```

---

## 🧰 Tools Overview

All agent capabilities are implemented as **LangChain-compatible tools** under the `tools/` directory.

### ➗ `arithmetic_op_tool.py`
Provides basic arithmetic operations such as addition and multiplication.  
All numeric inputs are sanitized using a centralized parser to handle LLM-generated strings safely.

---

### 💱 `currency_conversion_tool.py`
Handles currency conversion using external exchange-rate APIs.  
Used for international travel cost estimation and budget normalization.

---

### 💸 `expense_calculator_tool.py`
Provides high-level trip expense calculations:
- Total hotel cost
- Overall trip expense
- Per-day budget estimation

Designed specifically for JSON-based LLM tool calls.

---

### 📍 `place_search_tool.py`
Handles place-related planning such as:
- Attractions
- Restaurants
- Activities
- Transportation options

Supports multiple providers and structured fallbacks.

---

### 🌦️ `weather_info_tool.py`
Fetches weather-related information to support better itinerary planning.

---

## ⚙️ Tech Stack

- **Python 3.10+**
- **FastAPI**
- **Streamlit**
- **LangChain**
- **LangGraph**
- **Groq API**
- **Uvicorn**

---

## 🛠️ Setup & Installation (Run Locally)

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/SUJALGOYALL/AI_Trip_Planner.git
cd AI_Trip_Planner
```

---

### 2️⃣ Create & Activate Virtual Environment

```bash
python -m venv env
```

**Windows**
```bash
env\Scripts\activate
```

**Linux / macOS**
```bash
source env/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Configure Environment Variables (Required)

Create a `.env` file in the project root and add **all required API keys**:

```env
GROQ_API_KEY="Your api key"
GOOGLE_API_KEY="Your api key"
GPLACES_API_KEY="Your api key"
FOURSQUARE_API_KEY=""
TAVILAY_API_KEY="Your api key"
OPENWEATHERMAP_API_KEY="Your api key"
EXCHANGE_RATE_API_KEY="Your api key"
LANGCHAIN_API_KEY=""
```

⚠️ All API keys must be configured for the corresponding tools to function correctly.

---

## ▶️ Running the Application

### 🔹 Start Backend (FastAPI)

```bash
uvicorn main:app --reload --port 8000
```

Backend will be available at:
```
http://127.0.0.1:8000
```

---

### 🔹 Start Frontend (Streamlit)

Open a new terminal (with the same virtual environment activated):

```bash
streamlit run streamlit_app.py
```

Streamlit UI will open at:
```
http://localhost:8501
```

---

## 🧪 Example Queries

- Plan a trip from Bhagalpur (Bihar) to Jagannath Puri (Odisha) for 4 days
- Plan a 10-day trip to Paris from India
- Estimate budget for a 5-day trip to Goa

---

## 🧠 Key Engineering Learnings

- Graph-based agent workflows
- Tool–LLM contract enforcement
- Prompt–capability alignment
- Defensive numeric parsing
- Production-style agent design

---

## 📌 Future Improvements

- Real-time transportation APIs
- Map-based itinerary visualization
- Multi-agent planning
- Cloud deployment (Docker + AWS/GCP)

---

## 👤 Author

**Sujal Goyal**  
Engineering Student | AI & ML Enthusiast

---

### 🔑 Final Takeaway

This project showcases a **tool-driven, graph-based AI agent** designed with explicit constraints, robust input handling, and real-world engineering practices.
