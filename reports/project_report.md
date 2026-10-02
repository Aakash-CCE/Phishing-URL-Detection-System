# Project Report: Phishing URL Detection System

## 1. Abstract
The exponential growth of internet services has been accompanied by a corresponding rise in sophisticated cyber threats, with phishing attacks being among the most prevalent and damaging. Phishing URLs are designed to deceive end-users into revealing sensitive information such as login credentials and financial details by mimicking legitimate websites. This project presents a robust, automated Phishing URL Detection System that leverages Machine Learning to classify web addresses as Legitimate, Suspicious, or Phishing. Using a Random Forest classifier paired with a specialized feature extraction pipeline, the system evaluates 16 distinct lexical and structural characteristics of a URL without requiring page content rendering. A synthetic dataset of 3,000 URLs was generated to train and validate the model, achieving an accuracy of 99.17%. The solution is packaged into an interactive, user-friendly Streamlit web application, ensuring real-time analysis and explainable AI insights for end-users.

## 2. Introduction
In today's interconnected digital landscape, cyber threats pose a severe risk to individuals and organizations alike. Social engineering attacks have become the primary vector for system compromises, data breaches, and financial fraud. Among these, phishing—the fraudulent practice of sending communications purporting to be from reputable companies—remains the most widely used tactic. The foundational element of almost every phishing attack is the malicious URL. 

The importance of proactive URL analysis cannot be overstated. Traditional defenses often rely on reactive blocklists, which are inherently flawed because they cannot identify newly registered or zero-day phishing domains. As attackers automate the rapid generation of deceptive URLs using sophisticated obfuscation techniques, manual verification by security analysts has become an impossible task. Consequently, there is an industry-wide push toward automated, intelligent detection systems capable of identifying malicious intent based purely on the structural and lexical properties of a link. This project addresses that need by proposing an accessible, machine-learning-driven Phishing URL Detection System designed to serve as an initial line of defense, empowering users to verify links instantly before interaction.

## 3. Problem Statement
Phishing attacks are responsible for massive financial losses and massive data breaches globally every year. Despite increasing user awareness, attackers continue to successfully bypass standard security filters by manipulating URLs. They employ techniques such as typo-squatting, using IP addresses instead of domains, appending excessive subdomains, and utilizing misleading keywords (e.g., "secure-login"). 

The core problem is the lack of real-time, explainable, and accessible URL verification tools for the average internet user. Existing solutions are either enterprise-grade firewalls inaccessible to regular users, or browser warnings that only trigger after a site has been widely reported. There is a pressing need for a lightweight, automated system capable of deconstructing a URL, extracting its underlying features, and using advanced pattern recognition to classify its threat level instantly—preventing the user from ever loading the malicious content.

## 4. Objectives
The primary objectives of this project are:
1. To design and implement a robust feature extraction pipeline capable of parsing 16 distinct structural and lexical attributes from any given URL.
2. To generate a well-balanced synthetic dataset representing legitimate, suspicious, and phishing URLs for training purposes.
3. To train and optimize a Random Forest Machine Learning model for accurate URL classification.
4. To evaluate the model using standard metrics (Accuracy, Precision, Recall, F1-Score, Confusion Matrix).
5. To build a highly interactive, user-friendly web dashboard using Streamlit for real-time user input and analysis.
6. To provide explainable AI insights, showing users exactly which features of the URL contributed to its final threat classification.
7. To establish a modular and extensible codebase that allows for future integration with real-world threat intelligence feeds.

## 5. Scope
**Included in Scope:**
* Lexical and structural feature extraction from URL strings.
* Machine learning model training using a synthesized dataset.
* Categorization of URLs into three classes: Legitimate, Suspicious, and Phishing.
* Web-based user interface for manual URL testing and metric visualization.
* Explainable outputs highlighting risk factors in user-provided URLs.

**Excluded from Scope:**
* Web page content analysis (HTML, JavaScript, or DOM parsing).
* Image processing or logo recognition of the target website.
* WHOIS database lookups and domain registration history analysis.
* Real-time network traffic interception.
* Automated takedown requests of malicious domains.

## 6. Existing System
Currently, the most common methods for detecting phishing URLs include manual inspection, blacklist/whitelist filtering, and browser-based warnings (like Google Safe Browsing). 
* **Manual Inspection:** Highly unreliable, as modern attackers use URL shorteners and unicode characters that appear identical to legitimate domains to the human eye.
* **Blacklists:** Databases of known malicious URLs. While highly accurate with a low false-positive rate, they are purely reactive. A phishing site typically remains active and undetected for several hours or days before being added to a blacklist, exposing early victims to the attack (Zero-day problem).
* **Browser Warnings:** Often rely on the aforementioned blacklists, meaning they suffer from the same latency in threat detection. 

These limitations highlight the necessity for a proactive, heuristic, and machine-learning-based approach that detects anomalies based on the behavior and structure of the URL itself rather than relying entirely on historical reputation.

## 7. Proposed System
The Proposed System is a hybrid approach combining deterministic rule-based feature extraction with probabilistic machine learning. By dissecting a URL into its constituent parts (protocol, domain, path, parameters), the system calculates a specialized feature vector. This vector is then fed into a pre-trained Random Forest classifier.

**Advantages over Existing Systems:**
* **Proactive Detection:** Can identify zero-day phishing URLs based on suspicious patterns even if the URL has never been seen before.
* **No Network Overhead:** Because it relies solely on the lexical structure, the system does not need to visit the potentially dangerous website, ensuring zero risk of drive-by downloads.
* **Explainability:** Unlike black box solutions, this system highlights exactly *why* a URL was flagged (e.g., "Contains an IP address," "Uses multiple hyphens").
* **Speed:** Lexical feature extraction and ML inference take fractions of a second, enabling real-time analysis.

## 8. System Requirements
**Hardware Requirements:**
* **Processor:** Intel Core i3 / AMD Ryzen 3 or higher (2.0 GHz+)
* **RAM:** Minimum 4GB (8GB recommended for smoother model training)
* **Storage:** 500 MB of available disk space

**Software Requirements:**
* **Operating System:** Windows 10/11, macOS, or Linux (Ubuntu/Debian)
* **Programming Language:** Python 3.8 or above
* **Core Libraries:** Pandas, NumPy, Scikit-learn, Joblib
* **Visualization/UI:** Streamlit, Matplotlib, Plotly
* **Browser:** Any modern web browser (Google Chrome, Mozilla Firefox, Microsoft Edge)

## 9. Methodology
The project follows a standard Data Science and Machine Learning lifecycle:
1. **Data Collection & Generation:** A Python script generates a synthetic dataset of 3,000 URLs. Logic is applied to simulate the characteristics of real legitimate sites and known phishing structures.
2. **Feature Extraction:** The raw URL text is parsed. Regular expressions and string manipulation techniques extract 16 numerical/boolean features.
3. **Data Preprocessing:** The dataset is split into training (80%) and testing (20%) subsets. Missing values are handled, and feature scaling is evaluated.
4. **Model Training:** A Random Forest classifier is initialized and fit to the training data. The model learns the complex, non-linear relationships between the features and the target labels.
5. **Evaluation:** The model is tested against the unseen 20% of data to generate performance metrics.
6. **Deployment:** The trained model is serialized using Joblib. The Streamlit web application loads this model to serve predictions via a graphical interface.

## 10. Feature Extraction
The core of the system's intelligence lies in the 16 features extracted from every URL. 

| # | Feature Name | Description | Rationale |
|---|---|---|---|
| 1 | url_length | Total character count of the URL string. | Phishing URLs often use excessively long URLs to hide the actual domain from the user. |
| 2 | num_dots | Count of '.' characters in the URL. | Excessive dots indicate deeply nested subdomains, a common phishing tactic. |
| 3 | num_hyphens | Count of '-' characters in the URL. | Phishers use hyphens in typo-squatting (e.g., pay-pal-secure.com). |
| 4 | num_digits | Total numerical digits in the URL. | High digit count correlates with malicious, auto-generated or IP-based links. |
| 5 | num_special_chars | Count of special characters (@, !, ~, &, %, #, $, ^, *). | Unusual special characters indicate obfuscation techniques. |
| 6 | has_ip_address | Boolean: 1 if domain is an IPv4 address. | Legitimate sites use domain names; IPs are highly suspicious. |
| 7 | has_https | Boolean: 1 if protocol is HTTPS. | Lack of HTTPS is a strong negative indicator of legitimacy. |
| 8 | num_subdomains | Number of dot-separated subdomains (dots in hostname − 1). | Attackers nest subdomains (e.g., login.secure.paypal.com.malicious.com) to simulate legitimacy. |
| 9 | has_at_symbol | Boolean: 1 if '@' is present in the URL. | Browsers ignore everything before '@', a trick used to mask the real destination. |
| 10 | is_shortened | Boolean: 1 if domain matches known URL shorteners (bit.ly, tinyurl.com, t.co, etc.). | URL shorteners hide the true destination domain from the victim. |
| 11 | num_params | Count of query parameters (number of '=' in query string). | Complex tracking parameters can be used for session hijacking and data exfiltration. |
| 12 | path_length | Character length of the URL path component. | Deep directory structures are common in obfuscated phishing kits. |
| 13 | has_suspicious_keywords | Boolean: 1 if URL contains keywords like 'login', 'verify', 'update', 'account', etc. | Social engineering heavily relies on urgency and action-oriented keywords. |
| 14 | domain_length | Character count of the hostname/domain. | Unusually long domains are often algorithmically generated (DGAs). |
| 15 | num_slashes | Count of '/' characters in the URL. | Excessive slashes indicate deep path nesting or redirect chains. |
| 16 | has_double_slash_redirect | Boolean: 1 if '//' occurs in the path (after the protocol scheme). | Used in redirection attacks to send users to external sites. |

## 11. Machine Learning Algorithm
The system utilizes the **Random Forest Classifier** for categorization.

* **How it works:** Random Forest is an ensemble learning method. It constructs a multitude of decision trees during training. For classification tasks, the output of the Random Forest is the class selected by the majority of the trees (voting). It uses a technique called bagging (Bootstrap Aggregating) to train each tree on a random subset of the data.
* **Why it was chosen:**
  * **High Accuracy & Robustness:** By averaging multiple trees, it reduces the risk of overfitting compared to a single decision tree.
  * **Handles Non-Linearity:** URL features often have complex, non-linear relationships.
  * **Feature Importance:** Random Forest inherently calculates the importance of each feature during training, which is crucial for our requirement of Explainable AI.
* **Training Process:** The model was initialized using Scikit-learn (`RandomForestClassifier`). Hyperparameters such as `n_estimators` (number of trees) and `max_depth` were tuned to optimize performance on the synthetic dataset.

## 12. Implementation
The project is modularized into distinct Python scripts:
* `data/generate_dataset.py`: Contains custom rules to programmatically generate 3,000 URLs with varying feature permutations to simulate the three classes.
* `src/feature_extraction.py`: Implements a `FeatureExtractor` class. Using the `urllib.parse` and `re` (Regex) libraries, it converts a raw string into a dictionary of the 16 features.
* `src/train_model.py`: Loads the CSV dataset, drops string columns, handles `train_test_split`, trains the `RandomForestClassifier`, evaluates it, and saves it via `joblib.dump()`.
* `app.py`: The Streamlit frontend. It loads the `.joblib` model, provides a text input for the user, calls the `FeatureExtractor`, predicts the outcome, and uses Streamlit's layout components (columns, charts) to display results.

## 13. Testing
Automated testing is crucial for ensuring the reliability of feature extraction rules. The `pytest` framework is utilized.

| Test Case | Description | Expected Output | Status |
|---|---|---|---|
| TC01 | Extract IP address correctly | True for 'http://192.168.1.1' | PASS |
| TC02 | Detect '@' symbol masking | True for 'http://google.com@evil.com' | PASS |
| TC03 | Identify legitimate domains | Class 0 (Legitimate) | PASS |
| TC04 | Catch URL shorteners | True for 'https://bit.ly/123' | PASS |
| TC05 | Handle missing protocols | Auto-append or handle gracefully | PASS |

## 14. Results and Analysis
Upon training the model with the generated dataset, the following performance metrics were observed on the test set:

* **Accuracy:** **99.17%** - This represents the overall percentage of URLs classified correctly.
* **Precision:** **99.17%** - Out of all URLs predicted as Phishing, this percentage was actually Phishing. High precision minimizes false alarms.
* **Recall:** **99.17%** - Out of all actual Phishing URLs, the model successfully caught this percentage. High recall is critical in security to minimize false negatives.
* **F1-Score:** **99.17%** - The harmonic mean of Precision and Recall, providing a single metric for model performance.

**Confusion Matrix (Test Set — 600 samples):**

|  | Predicted Legitimate | Predicted Phishing | Predicted Suspicious |
|---|---|---|---|
| **Actual Legitimate** | 239 | 0 | 1 |
| **Actual Phishing** | 0 | 196 | 4 |
| **Actual Suspicious** | 0 | 0 | 160 |

**Confusion Matrix Analysis:**
* **True Positives (TP):** Phishing URLs correctly identified.
* **True Negatives (TN):** Legitimate URLs correctly identified.
* **False Positives (FP):** Legitimate URLs incorrectly flagged as phishing (nuisance to users).
* **False Negatives (FN):** Phishing URLs incorrectly marked as safe (highest danger).
The model demonstrated a particularly low False Negative rate, which aligns with the security-first objective of the system.

**Feature Importance:**
The Random Forest model identified the following top-5 most important features:
1. **has_suspicious_keywords** (25.1%) — The strongest single predictor of malicious intent.
2. **has_https** (16.9%) — Absence of HTTPS is a strong negative signal.
3. **num_digits** (16.3%) — High digit count correlates with IP-based and auto-generated URLs.
4. **path_length** (7.4%) — Longer paths are associated with phishing kits.
5. **num_hyphens** (6.4%) — Excessive hyphens indicate typo-squatting domains.

## 15. Limitations
* **Synthetic Dataset Dependency:** The model is trained on a synthetically generated dataset rather than live, real-world data, which may restrict its ability to generalize to completely novel attack vectors.
* **Lack of Content Inspection:** The system operates blindly regarding the actual visual or HTML content of the website. A compromised legitimate domain (where the URL looks normal but the page is malicious) will evade detection.
* **Absence of Real-time Threat Feeds:** The model does not currently query live blacklists like PhishTank, missing out on known bad domains that lack obvious structural red flags.
* **Zero-day Vulnerabilities:** Highly sophisticated, newly crafted phishing techniques that perfectly mimic legitimate lexical structures cannot be definitively caught by static rules.
* **No Network Context:** It does not analyze TLS certificate validity, WHOIS registration age, or server location, which are strong indicators of domain legitimacy.

## 16. Future Scope
* **Integration with Threat Intelligence API:** Connecting the app to services like VirusTotal, PhishTank, or OpenPhish for a hybrid (Lexical + Reputation) detection engine.
* **Deep Learning Implementation:** Upgrading from Random Forest to neural networks (like LSTMs or Transformers) capable of learning intricate character-level sequences within the URL.
* **Browser Extension Development:** Porting the Python backend into a Chrome/Firefox extension that automatically scans URLs in real-time before the page loads.
* **Web Scraping for Content Analysis:** Utilizing NLP (Natural Language Processing) to scan the HTML text of the target page for urgency keywords and fake login forms.
* **Visual Similarity Analysis:** Implementing computer vision (e.g., using OpenCV) to compare the rendered webpage's logo and layout against known brands to detect impersonation.
* **API Microservice:** Containerizing the ML model using Docker and serving it via FastAPI to allow other developers to integrate the detection engine into their apps.

## 17. Conclusion
The Phishing URL Detection System successfully demonstrates the viability of utilizing Machine Learning, specifically Random Forest, to analyze and classify web links based entirely on their lexical and structural properties. By successfully extracting 16 critical features from raw strings, the system can identify malicious intent with high accuracy, circumventing the delays and zero-day vulnerabilities associated with traditional blacklist approaches. 

The integration of the model into a Streamlit web application ensures that the tool is accessible to end-users without requiring technical expertise. Furthermore, the emphasis on explainable AI—showing users exactly why a link is deemed suspicious—serves an important educational purpose, helping to raise general cybersecurity awareness. While limitations exist regarding content inspection and synthetic training data, the project establishes a robust foundation. With future integrations of real-time threat intelligence and deep learning models, this system can evolve into a highly formidable defense mechanism against one of the internet's most pervasive threats.

## 18. References
1. Scikit-learn Developers. (2023). *Scikit-learn: Machine Learning in Python*. Retrieved from https://scikit-learn.org/
2. Streamlit Inc. (2023). *Streamlit Documentation*. Retrieved from https://docs.streamlit.io/
3. Open Web Application Security Project (OWASP). (2022). *Phishing Attacks and Mitigation*. Retrieved from https://owasp.org/www-community/attacks/phishing
4. UCI Machine Learning Repository. (2020). *Phishing Websites Dataset*. Retrieved from https://archive.ics.uci.edu/ml/datasets/phishing+websites
5. Jain, A. K., & Gupta, B. B. (2017). *Phishing Detection: Analysis of Visual Similarity Based Approaches*. Security and Communication Networks.
6. Mohammad, R. M., Thabtah, F., & McCluskey, L. (2015). *Phishing Websites Features*. School of Computing and Engineering, University of Huddersfield.
7. Breiman, L. (2001). *Random Forests*. Machine Learning, 45(1), 5-32.
8. Python Software Foundation. (2023). *urllib.parse — Parse URLs into components*. Retrieved from https://docs.python.org/3/library/urllib.parse.html
