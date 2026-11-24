# Elevvo Internship - Level 2 Tasks

This repository tracks my solutions for the Elevvo Python Programming & AI internship (Level 2). It covers the three required tasks: file automation, object-oriented design, and an end-to-end NLP classification pipeline.

## Repository layout

```text
Elevvo-Internship/
├── File Organizer/
│   ├── files.py
│   ├── test_organizer.py
│   └── README.md
├── Inventory Management/
│   ├── inventory.py
│   ├── test_inventory.py
│   └── README.md
└── SMS Spam Classification/
    ├── pipeline.py
    ├── sms_spam_classification.ipynb
    ├── spam_classifier.joblib
    ├── sms-spam-collection.csv
    ├── test_pipeline.py
    └── README.md
```

## Tasks overview

### Task 1: Automated File Organizer
A script that sorts files in a chosen directory into subfolders by extension. It includes conflict resolution to avoid overwriting existing files, reports every move in the console, and includes error handling for permission issues and empty directories.

### Task 2: Object-Oriented Inventory Management System
An inventory tracker built with Python classes. It uses a base `Product` class with validation properties to block negative stock, plus an expiring product subclass that tracks shelf life. Includes stock adjustments, low-inventory alerts, and formatted inventory reports.

### Task 3: SMS Spam Classification Pipeline
A text classification pipeline that separates spam messages from legitimate texts (ham). It uses TF-IDF and Logistic Regression trained on the SMS Spam Collection dataset, evaluates performance against class imbalance using precision, recall, and confusion matrices, and exports the final model with `joblib`.
