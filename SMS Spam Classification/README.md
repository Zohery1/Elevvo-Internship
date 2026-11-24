# SMS Spam Classification Pipeline

A machine learning pipeline that classifies SMS messages into `ham` (legitimate) or `spam`. Built with scikit-learn, TF-IDF vectorization, and Logistic Regression.

## Dataset and credit

- Dataset: [SMS Spam Collection](https://huggingface.co/datasets/codesignal/sms-spam-collection) via Hugging Face (CC BY 4.0).
- Columns used: `label` and `message`.
- Class distribution: Heavily imbalanced with `ham` making up roughly 87% of messages and `spam` representing roughly 13%.

## Evaluation and class imbalance

In a dataset where roughly 87% of samples belong to the majority class (`ham`), an uninformative model that labels every message as legitimate achieves 87% raw accuracy while catching 0% of spam. 

For that reason, evaluation relies on:
- Stratified train/test split (fixed random seed) to preserve the class ratio in both splits.
- Majority-class baseline to set a realistic performance floor.
- Precision: out of all messages flagged as spam, how many were actually spam (measuring false alarms).
- Recall: out of all actual spam messages, how many were detected.
- F1-Score: harmonic mean of precision and recall.
- Confusion matrix: to inspect false positives (legitimate texts wrongly flagged) and false negatives (missed spam).

## Pipeline design

1. Exploratory data analysis: inspect message length, sample texts, and label proportions.
2. Feature extraction: `TfidfVectorizer` fit only on training data to avoid data leakage.
3. Classifier: `LogisticRegression` with tuned regularization.
4. Model persistence: save the trained scikit-learn pipeline using `joblib` for deployment.

## Tech stack

- Python 3
- Pandas
- Scikit-learn
- Joblib
