# Candidate Test Guidance:

## Overview
This take-home test evaluates a candidate’s modeling skills through 2 main exercises:

- Theoretical model building from requirements
- Optimization problem solving

Candidates are allowed to use AI tools to support their work. However, during the interview, you should be prepared to explain the concepts, modeling choices, and solution approach you used in your submission.

## Submission Instructions ✅
Please submit your work by following these steps:

1. Create a new private fork of this repository using the naming convention: 
```
submission_yourfullname
```
Example : submission_peterparker

2. You may edit the code and commit to your private fork repo multiple times during your work. But remember to add me `convex-optima` as collaborator!

3. Your final version must be committed before the interview 12 hours with the exact commit message:
```
final_submission
```
4. Forget to add collaborator or commit without the final message will be considered as failed test.

## Scoring 🧮
- Theoretical model building exercise: 30 points
- Optimization exercise: 70 points

Bonus: up to 20 extra points for identifying/fixing setup errors

## Folder Structure

``` 
├── README.md
├── requirements.txt
├── excercise_1.ipynb
├── excercise_2.ipynb
└── code
    ├── model.py
    └── auxiliary.py
```

## Install dependencies with:

```sh
conda env create -f requirements.yml 
``` 

