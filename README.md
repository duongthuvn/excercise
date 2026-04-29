# Candidate Test Guidance:

## Overview
This take-home test evaluates a candidate’s modeling skills through 2 main exercises:

- Theoretical model building from requirements
- Optimization problem solving

Candidates are allowed to use AI tools to support their work. However, during the interview, you should be prepared to explain the concepts, modeling choices, and solution approach you used in your submission.

## Scoring 🧮
- Theoretical model building exercise: 30 points
- Optimization exercise: 70 points

Bonus: up to 20 extra points for identifying/fixing setup errors

## Folder Structure

``` 
├── README.md
├── requirements.txt
├── cutting_optima.ipynb
├── inventory_optima.ipynb
└── code
    ├── model.py
    └── auxiliary.py
```

## Install dependencies with:

```sh
conda env create -f requirements.yml 
``` 

## Submission Instructions ✅
Please submit your work by following these steps:

1. Create a new branch in this repository using the naming convention: 
```
submission_yourfullname
```
Example : submission_duonganhthu

2. You may commit to this branch multiple times during your work.

3. Your final version must be committed with the exact commit message:
```
final_submission
```