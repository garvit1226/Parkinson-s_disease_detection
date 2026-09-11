# Parkinson's Disease Detection — FastAPI + HTML/CSS/JS

## Folder structure

```text
parkinsons_fastapi_project/
├── main.py
├── requirements.txt
├── README.md
├── model/
│   ├── svm_model.pkl      <-- upload your trained SVM here
│   └── scaler.pkl         <-- upload your fitted scaler here
├── dataset/
│   └──                 <-- put your dataset here
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── script.js
```

## Setup

Create/activate a virtual environment if desired, then:

```bash
pip install -r requirements.txt
```



## Run

From the project root:

```bash
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

## Important

The website sends 22 values to the SVM in this exact order:

1. MDVP:Fo(Hz)
2. MDVP:Fhi(Hz)
3. MDVP:Flo(Hz)
4. MDVP:Jitter(%)
5. MDVP:Jitter(Abs)
6. MDVP:RAP
7. MDVP:PPQ
8. Jitter:DDP
9. MDVP:Shimmer
10. MDVP:Shimmer(dB)
11. Shimmer:APQ3
12. Shimmer:APQ5
13. MDVP:APQ
14. Shimmer:DDA
15. NHR
16. HNR
17. RPDE
18. DFA
19. spread1
20. spread2
21. D2
22. PPE

This order MUST match the feature order used when training your SVM and fitting your scaler.


