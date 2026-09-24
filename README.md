\# Phishing URL Detector



A real-time phishing URL detection system that uses machine learning to identify whether a URL is \*\*safe, suspicious, or potentially phishing\*\*.



The project combines a machine learning model with a Flask backend and Chrome extension to make URL analysis practical during everyday browsing.



\## What it does



\* Extracts security-related features from URLs

\* Uses a trained machine learning model for classification

\* Provides predictions through a Flask backend

\* Integrates with a Chrome extension for quick URL checking

\* Classifies URLs as safe, suspicious, or phishing



\## Tech Stack



\* \*\*Python\*\*

\* \*\*Flask\*\*

\* \*\*Machine Learning\*\*

\* \*\*Pandas\*\*

\* \*\*Scikit-learn\*\*

\* \*\*HTML / JavaScript\*\*

\* \*\*Chrome Extension\*\*



\## Project Structure



```text

phishing-detector/

│

├── backend/

│   ├── app.py

│   ├── feature\_extractor.py

│   ├── train\_model.py

│   ├── test.py

│   └── model.pkl

│

├── data/

│   ├── raw/

│   │   └── urls.csv

│   └── processed/

│       └── features.csv

│

├── extension/

│   ├── background.js

│   ├── manifest.json

│   ├── popup.html

│   └── popup.js

│

├── frontend/

│   └── index.html

│

└── model.pkl

```



\## How it works



```text

URL

&#x20;↓

Feature Extraction

&#x20;↓

Machine Learning Model

&#x20;↓

Risk Classification

&#x20;↓

Safe / Suspicious / Phishing

```



The Chrome extension communicates with the backend to analyze URLs and return the classification result.



\## Running the Project



\### 1. Clone the repository



```bash

git clone https://github.com/404sneha/phishing-detector.git

cd phishing-detector

```



\### 2. Install dependencies



```bash

pip install -r requirements.txt

```



\### 3. Start the Flask backend



```bash

python backend/app.py

```



\### 4. Load the Chrome extension



1\. Open Chrome and go to `chrome://extensions`

2\. Enable \*\*Developer mode\*\*

3\. Select \*\*Load unpacked\*\*

4\. Choose the `extension` folder



\## Why I built this



Phishing attacks often rely on users trusting malicious URLs. This project explores how machine learning and browser-level integration can be used to provide an additional layer of protection by analyzing URLs before users interact with them.



\## Future Improvements



\* Improve model performance with larger and more diverse datasets

\* Add URL reputation and threat-intelligence feeds

\* Improve the browser extension UI

\* Add explainable risk indicators for detected URLs

\* Deploy the backend as a cloud service



\## Author



\*\*Sneha Chaturvedi\*\*



B.Tech Information Technology | Cybersecurity



