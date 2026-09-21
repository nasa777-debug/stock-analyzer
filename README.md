# Stock Analyzer Platform — Learning Lab Rebuild

A Flask + MySQL simulated investing platform redesigned around **stock learning**, a searchable **stock dictionary**, an educational **Learning Agent**, market simulation, technical indicators and virtual trading.

## What changed

- Rebuilt the visual system with a responsive glassmorphism UI, gradients, animated reveals and smoother interactions.
- Added **Learn / Stock Dictionary** with beginner and intermediate concepts.
- Added **Stock Learning Agent** backed by the local knowledge base; no LLM key is required for the demo.
- Added company snapshots and learning context to the Market Lab.
- Preserved login, portfolio, simulated buy/sell, transaction history and Chart.js visualizations.
- Kept the Flask + SQLAlchemy + Railway MySQL architecture and existing high-level file structure.

## Structure

```text
stock-analyzer/
├── static/
│   ├── css/style.css
│   └── js/
│       ├── app.js
│       └── charts.js
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── market.html
│   ├── learn.html
│   ├── agent.html
│   └── transactions.html
├── app.py
├── database.py
├── simulator.py
├── requirements.txt
├── schema.sql
└── test_app.py
```

## Run locally

```bash
pip install -r requirements.txt
python app.py
```

For Railway/Vercel, keep the existing `DATABASE_URL` environment variable. If it is a PyMySQL connection, use the `mysql+pymysql://` SQLAlchemy prefix.

## Educational disclaimer

This project uses simulated prices and is intended for learning and experimentation. It is not financial advice and should not be used as a basis for real-money investment decisions.
