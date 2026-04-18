# 💀 APEX ROUTE - Autonomous Logistics AI

**Autonomous Logistics AI // Team Requiem**

A sophisticated AI-powered logistics optimization system that analyzes shipment routes in real-time, gathering intelligence, assessing risk, and recommending intelligent rerouting decisions using LangGraph agents.

---

## 🎯 Overview

APEX ROUTE is a cutting-edge logistics platform that leverages multi-agent AI to revolutionize supply chain management. The system processes shipment data, integrates real-world intelligence (weather patterns, news events), calculates dynamic risk profiles, and autonomously recommends optimal routing decisions.

**Key Features:**
- ✅ Real-time shipment route analysis
- ✅ Multi-agent agentic workflow (LangGraph)
- ✅ Intel gathering from weather & news APIs
- ✅ Dynamic risk assessment
- ✅ Intelligent dispatcher recommendations
- ✅ Modern web interface with React/Next.js
- ✅ FastAPI backend with CORS support

---

## 📁 Project Structure

```
apex_route/
├── backend/                          # FastAPI backend server
│   ├── main.py                      # FastAPI application entry point
│   ├── requirements.txt             # Python dependencies
│   ├── check_models.py              # Model validation utilities
│   ├── test_run.py                  # Test suite
│   └── apex_engine/                 # Core agentic engine
│       ├── __init__.py
│       ├── graph.py                 # LangGraph workflow definition
│       ├── state.py                 # State schema for agents
│       ├── nodes.py                 # Agent node implementations
│       └── tools.py                 # Tool utilities for agents
│
├── frontend/                         # Next.js React frontend
│   ├── app/
│   │   ├── page.tsx                 # Command Center main UI
│   │   ├── layout.tsx               # Root layout
│   │   └── globals.css              # Global styles
│   ├── public/                      # Static assets
│   ├── package.json                 # Node.js dependencies
│   ├── tsconfig.json                # TypeScript configuration
│   ├── next.config.ts               # Next.js configuration
│   ├── tailwind.config.js           # Tailwind CSS config
│   ├── eslint.config.mjs            # ESLint rules
│   └── .gitignore                   # Frontend git ignore rules
│
├── .gitignore                        # Root git ignore rules
└── README.md                         # This file
```

---

## 🏗️ Architecture

### Backend Flow (LangGraph Workflow)

```
ShipmentRequest
    ↓
[INTEL GATHERER] → Fetches weather & news data
    ↓
[RISK ORACLE] → Calculates risk level from intel
    ↓
    └─→ Risk ≥ 0.7? ──YES→ [DISPATCHER] → Recommends reroute → END
                │
                └─→ NO → END (Route is safe)
```

### Tech Stack

**Backend:**
- FastAPI (Web framework)
- LangGraph (Agent orchestration)
- Pydantic (Data validation)
- Python 3.10+

**Frontend:**
- Next.js 16.2+
- React 19.2+
- TypeScript 5+
- Tailwind CSS 4+

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or higher
- Node.js 18+ and npm/yarn
- Git

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows
   # or
   source venv/bin/activate      # On Mac/Linux
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   # Create a .env file in the backend directory
   # .env
   OPENWEATHER_API_KEY=your_api_key_here
   GCP_API_KEY=your_gcp_key_here
   ```

5. **Run the backend server:**
   ```bash
   uvicorn main:app --reload
   ```
   Backend will be available at `http://localhost:8000`
   - API docs: `http://localhost:8000/docs`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Run development server:**
   ```bash
   npm run dev
   ```
   Frontend will be available at `http://localhost:3000`

4. **Build for production:**
   ```bash
   npm run build
   npm start
   ```

---

## 🔌 API Reference

### Analyze Route Endpoint

**Endpoint:** `POST /api/analyze_route`

**Request Body:**
```json
{
  "shipment_id": "REQ-774-ALPHA",
  "current_location": "Miami Port",
  "destination": "Rotterdam"
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "shipment_id": "REQ-774-ALPHA",
    "current_location": "Miami Port",
    "destination": "Rotterdam",
    "weather_data": "Clear skies",
    "news_data": "Port disruptions reported",
    "risk_level": 0.65,
    "recommended_action": "Route via alternate port"
  }
}
```

**Status Codes:**
- `200` - Analysis completed successfully
- `422` - Invalid request data
- `500` - Server error during analysis

---

## 🧠 Agent Architecture

### Intel Gatherer Node
- Queries external APIs (weather, news)
- Retrieves real-time data about route conditions
- Enriches shipment context with environmental intelligence

### Risk Oracle Node
- Analyzes gathered intelligence
- Computes dynamic risk scores (0.0 - 1.0)
- Factors in multiple risk parameters

### Dispatcher Node
- Triggered when risk level ≥ 0.7
- Recommends alternative routes or actions
- Provides actionable insights for logistics team

---

## 🎨 Frontend Features

### Command Center UI
- **Initialize Scan Panel:**
  - Shipment ID input
  - Current location coordinates
  - Destination port specification
  - Analysis trigger button

- **Live AI Telemetry Panel:**
  - Real-time threat detection display
  - Risk level visualization (color-coded)
  - Recommended action display
  - Error handling and feedback

---

## 🔐 Security & Environment Variables

**Important:** Never commit sensitive credentials to version control.

**Required Environment Variables:**
```bash
# backend/.env
OPENWEATHER_API_KEY=<your_openweather_api_key>
GCP_API_KEY=<your_gcp_service_account_key>
```

**Security Best Practices:**
- `.env` files are excluded via `.gitignore`
- Use strong, unique API keys
- Rotate keys regularly if exposed
- Never share `.env` files
- Use environment variables in production

---

## 🧪 Testing

### Run Backend Tests
```bash
cd backend
pytest test_run.py -v
```

### Check Models
```bash
cd backend
python check_models.py
```

### Frontend Linting
```bash
cd frontend
npm run lint
```

---

## 📊 State Schema

The LangGraph workflow uses a centralized state that flows through all agents:

```python
class SupplyChainState(TypedDict):
    shipment_id: str
    current_location: str
    destination: str
    weather_data: Optional[str]
    news_data: Optional[str]
    risk_level: Optional[float]
    recommended_action: Optional[str]
```

---

## 🚨 Error Handling

### Common Issues

**Backend won't start:**
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # Mac/Linux

# Use different port
uvicorn main:app --port 8001
```

**Frontend can't connect to backend:**
- Verify backend is running on `http://127.0.0.1:8000`
- Check CORS configuration in `backend/main.py`
- Ensure frontend is accessing the correct API endpoint

**API key errors:**
- Verify `.env` file exists in backend directory
- Check API key validity and permissions
- Ensure keys are not expired

---

## 📝 Development Workflow

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make changes and commit:**
   ```bash
   git add .
   git commit -m "Add your feature description"
   ```

3. **Push to GitHub:**
   ```bash
   git push -u origin feature/your-feature-name
   ```

4. **Open a Pull Request**

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:
- Fork the repository
- Create a feature branch
- Write clear commit messages
- Ensure code is properly tested
- Submit a pull request with detailed description

---

## 📄 License

This project is proprietary. All rights reserved.

---

## 👥 Team

**APEX ROUTE** - Built by Team Requiem

---

## 📞 Support & Questions

For issues, questions, or suggestions:
1. Check existing GitHub issues
2. Review the API documentation at `http://localhost:8000/docs`
3. Contact the development team

---

## 🔄 Recent Changes

- ✅ Git history cleaned for security
- ✅ Environment variables properly gitignored
- ✅ Cursor pointers added to UI for better UX
- ✅ Comprehensive README created

---

## 🎓 Learning Resources

- [LangGraph Documentation](https://python.langchain.com/docs/langgraph/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)

---

**Last Updated:** April 18, 2026

🚀 Ready to revolutionize logistics with AI!
