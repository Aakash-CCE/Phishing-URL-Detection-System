# 🛡️ Phishing URL Detection System

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg)
![scikit-learn](https://img.shields.io/badge/scikit--learn-Machine%20Learning-F7931E.svg)

## Project Description
The Phishing URL Detection System is a machine learning-based cybersecurity tool designed to analyze and classify web addresses (URLs) as Legitimate, Suspicious, or Phishing. Built for students, researchers, and general internet users, it solves the critical problem of identifying malicious links before users click on them, thus mitigating the risk of credential theft, financial fraud, and malware infections. The system provides an interactive web dashboard for real-time URL analysis and visualizes the exact reasons behind its predictions.

## Problem Statement
Phishing attacks remain one of the most common and damaging cybersecurity threats worldwide. According to recent cybersecurity reports, a significant majority of cyber incidents begin with a phishing link, often distributed via email, SMS, or social media. Attackers continuously evolve their techniques, crafting URLs that closely mimic legitimate websites to deceive users. Manual inspection of URLs is insufficient, error-prone, and unscalable. There is an urgent need for automated, intelligent systems that can rapidly analyze URL structures and identify malicious patterns to protect end-users effectively.

## Objectives
1. Build a robust system to accurately classify URLs into three categories: Legitimate, Suspicious, or Phishing.
2. Extract meaningful lexical and structural features from URLs without needing to load the page content.
3. Train a Machine Learning model (Random Forest) that provides explainable and reliable results.
4. Create an intuitive, user-friendly web interface for easy interaction.
5. Provide actionable insights and feature importance to educate users on what makes a URL suspicious.

## Features
* **16 URL Feature Extraction:** Analyzes URL length, presence of symbols, domain structure, and more.
* **Random Forest ML Model:** Uses an ensemble learning method for high accuracy and robustness.
* **Hybrid Rule-Based + ML Approach:** Combines deterministic heuristics with probabilistic machine learning.
* **Streamlit Web Dashboard:** Modern, responsive UI for seamless URL testing.
* **Explainable Predictions:** Breaks down exactly which features contributed to the threat score.
* **Model Performance Metrics:** Interactive visualization of accuracy, confusion matrix, and precision/recall.
* **Test Suite:** Includes automated testing scripts to validate feature extraction and model inference.

## Technology Stack

| Component | Technology Used | Purpose |
| --- | --- | --- |
| **Language** | Python 3.8+ | Core programming language |
| **Data Manipulation** | Pandas, NumPy | Data processing and feature engineering |
| **Machine Learning** | Scikit-learn | Model building, training, and evaluation |
| **Visualization** | Matplotlib, Plotly | Interactive charts and graphs |
| **Web Framework** | Streamlit | Frontend application UI |
| **Model Serialization**| Joblib | Saving and loading the trained ML model |

## System Requirements
* **Operating System:** Windows, macOS, or Linux
* **Software:** Python 3.8 or higher, pip package manager
* **Hardware:** Minimum 4GB RAM, 500MB free disk space
* **Browser:** Any modern web browser (Chrome, Firefox, Edge, Safari)

## Installation & Setup

```bash
# Clone or download the project
cd "Phishing URL Detection System"

# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Generate dataset (if not present)
python data/generate_dataset.py

# Train the model
python -m src.train_model

# Run the application
streamlit run app.py
```

## Project Structure
```text
Phishing URL Detection System/
│
├── app.py                     # Main Streamlit web application
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
│
├── data/
│   ├── generate_dataset.py    # Script to create the synthetic dataset
│   └── url_dataset.csv        # Generated dataset (after running script)
│
├── models/
│   └── random_forest.joblib   # Trained ML model (saved after training)
│
├── src/
│   ├── feature_extraction.py  # Logic for extracting 16 features from URLs
│   ├── train_model.py         # Model training and evaluation pipeline
│   └── inference.py           # Prediction logic for new URLs
│
├── reports/
│   └── project_report.md      # Detailed academic project report
│
└── tests/
    ├── test_features.py       # Unit tests for feature extraction
    └── test_model.py          # Integration tests for model prediction
```

## Dataset
* **Source:** Synthetic, self-generated dataset specifically designed for educational purposes.
* **Size:** 3000 URLs in total (1200 legitimate, 800 suspicious, 1000 phishing).
* **Important Note:** No real malicious URLs are used in this dataset to ensure safety during the development and testing phases.
* **Features Extracted:**

| Feature | Description |
| --- | --- |
| URL Length | Total character count of the URL |
| Subdomain Count | Number of subdomains present |
| Use of IP | Whether an IP address is used instead of a domain name |
| '@' Symbol | Presence of the '@' symbol (often used to obscure URLs) |
| '-' in Domain | Presence of hyphens in the domain name |
| Multiple Subdirs | Unusually high number of subdirectories in the path |
| Suspicious TLD | TLDs commonly associated with spam (e.g., .xyz, .top) |
| HTTPS Protocol | Whether the URL uses secure HTTPS |
| Double Slash | Presence of '//' within the path |
| Shortening Service | Matches common URL shorteners (bit.ly, t.co) |
| Non-Standard Port | Use of ports other than 80 or 443 |
| Suspicious Words | Presence of words like "login", "update", "verify" |
| Length of Domain | Character length of the primary domain |
| Number of Digits | Total count of numerical digits in the URL |
| Number of Parameters| Count of query parameters (?) |
| Punycode | Use of internationalized domain names (xn--) |

## How to Train the Model
1. Open your terminal and ensure your virtual environment is active.
2. Generate the data: `python data/generate_dataset.py`
3. Execute the training script: `python -m src.train_model`
4. The script will output the accuracy and save the trained model to `models/random_forest.joblib`.

## How to Run the Application
1. Ensure the model has been trained (see above).
2. Start the Streamlit server: `streamlit run app.py`
3. Your default web browser will open (usually to `http://localhost:8501`).
4. Enter a URL into the input field and click "Analyze URL" to see the prediction and feature breakdown.

## Sample Input/Output

**Example 1: Legitimate URL**
* **Input:** `https://www.github.com/microsoft/vscode`
* **Expected Output:**
  * Classification: Legitimate
  * Threat Score: ~[XX.XX%]
  * Insight: Standard domain, uses HTTPS, no suspicious keywords.

**Example 2: Phishing URL**
* **Input:** `http://192.168.1.55/update-paypal-account-verify`
* **Expected Output:**
  * Classification: Phishing
  * Threat Score: ~[XX.XX%]
  * Insight: IP address used, no HTTPS, suspicious keywords ("update", "verify") present.

## Testing
To ensure system reliability, a test suite is provided.
* **Command:** `pytest tests/` (assuming pytest is installed via requirements)
* **Sample Test Results:**
  * `test_ip_address_detection`: PASS
  * `test_at_symbol_extraction`: PASS
  * `test_model_loading`: PASS

## Screenshots
*(Add these screenshots to a `docs/images/` folder and link them here for the final submission)*
1. Dashboard home page
2. Legitimate URL analysis result
3. Phishing URL analysis result
4. Suspicious URL analysis result
5. Model metrics section
6. Confusion matrix
7. Feature importance chart
8. Test results table
9. Feature analysis details

## Limitations
* **Synthetic Dataset:** Uses a synthetic dataset; may not capture the full complexity of real-world, in-the-wild phishing URLs.
* **URL-Based Only:** Analyzes only the URL string, completely ignoring webpage content, DOM structure, or injected scripts.
* **No Real-Time Feed:** Lacks integration with live phishing databases (like PhishTank) to catch newly reported malicious links.
* **Data Quality Dependency:** Model accuracy is strictly bounded by the quality and representativeness of the training data.
* **Zero-Day Phishing:** Cannot perfectly detect entirely new, zero-day phishing patterns that do not trigger any known lexical rules.

## Future Scope
* Integration with real-time phishing databases (PhishTank, OpenPhish).
* Transitioning to deep learning models (LSTM, Transformer) for sequence analysis.
* Development of a dedicated Browser Extension for real-time user protection.
* Creating a RESTful API endpoint for third-party application integration.
* Incorporating Page Content Analysis (NLP on HTML/text).
* Integration with WHOIS lookup data for domain age and registration details.
* Automated real-time URL monitoring and retraining pipelines.

## PPT Demonstration Suggestions
For a 10-15 minute project viva presentation:
1. **Title slide:** Project name, team members, supervisor.
2. **Problem Statement:** Why phishing is dangerous and difficult to stop.
3. **Objectives:** What the project aims to achieve.
4. **System Architecture:** High-level flow from URL input to prediction.
5. **Feature Extraction:** Highlight key lexical features extracted.
6. **ML Algorithm:** Why Random Forest was chosen and how it works.
7. **Live Demo:** Switch to the Streamlit app and test 3 different URLs.
8. **Results & Metrics:** Show accuracy, F1-score, and confusion matrix.
9. **Testing:** Brief overview of the automated test suite.
10. **Limitations & Future Scope:** Honest assessment of current boundaries.
11. **Conclusion:** Final summary of the project's impact.
12. **Q&A:** Open floor for questions.

## References
* Scikit-learn documentation: https://scikit-learn.org/
* Streamlit documentation: https://docs.streamlit.io/
* OWASP Phishing resources: https://owasp.org/www-community/attacks/phishing
* UCI ML Repository (Phishing Datasets): https://archive.ics.uci.edu/ml/datasets.php

## License
MIT License

Copyright (c) 2024 Phishing URL Detection System Authors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
