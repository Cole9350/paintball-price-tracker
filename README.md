# Paintball Price Tracker

## Overview
A Python-based web scraper that tracks the prices of paintball gear from various online retailers and stores the data in a MongoDB Atlas database.

## Features
- Scrapes paintball product prices from multiple sources
- Stores historical price data in MongoDB
- Ensures only one entry per product per day to avoid redundant updates
- Can be scheduled to run automatically in the cloud

## Project Structure
```
paintball-price-tracker/
│-- src/                      # Main source code folder
│   │-- lambda_function.py     # Main price scraper
│   │-- requirements.txt      # Python dependencies
│   │-- .env                  # Environment variables (ignored in Git)
│   │-- .venv/                # Virtual environment (ignored in Git)
│-- tests/                    # Folder for test scripts (if applicable)
│-- README.md                 # Project documentation
│-- .gitignore                # Git ignore rules
```

## Setup Instructions
1. **Clone the repository**
   ```bash
   git clone https://github.com/cole9350/paintball-price-tracker.git
   cd paintball-price-tracker
   ```

2. **Create and activate a virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # macOS/Linux
   .venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r src/requirements.txt
   ```

4. **Configure MongoDB connection**
   - Create a `.env` file inside the `src/` directory and add:
     ```
     MONGO_URI=mongodb+srv://yourusername:yourpassword@yourcluster.mongodb.net/yourdb
     ```

5. **Run the scraper manually**
   ```bash
   python src/lambda_function.py
   ```

## Deployment Plan
- Deploy the script to a cloud platform (e.g., AWS Lambda, Google Cloud Functions, or a cron job on a VM).
- Automate the execution to run daily.
- Monitor logs and database performance.

---

Feel free to update this README as needed before pushing to GitHub!
