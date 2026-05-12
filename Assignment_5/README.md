# Assignment 5: Transfer Learning (CNN & Transformer)

This repository contains two Transfer Learning approaches applied to different domains: Computer Vision (Images) and Natural Language Processing (Text).

## 1. Image Classification: Duck vs. Chicken (`TL_img.ipynb`)
- **Objective:** Fine-tune a pre-trained **ResNet18** Convolutional Neural Network to distinguish between images of ducks and chickens.
- **Data:** Custom dataset scraped from DuckDuckGo, consisting of ~200 images, balanced and cleaned.
- **Results:** - Achieved **85% Accuracy** on an unseen test set.
  - The model achieved 100% precision on the chicken class and 100% recall on the duck class, demonstrating strong feature extraction despite a very small dataset size.

## 2. Text Classification: Sentiment Analysis (`TL_txt.ipynb`)
- **Objective:** Fine-tune the pre-trained **DistilBERT** Transformer to classify text into Negative, Neutral, and Positive sentiments.
- **Data:** A subset of 3,000 tweets from the Kaggle Sentiment Analysis Dataset.
- **Results:**
  - Achieved **76% Accuracy** overall.
  - The model effectively learned the sentiment spectrum. Analysis of the Confusion Matrix revealed that extreme misclassifications (Negative as Positive, or vice versa) were extremely rare (less than 3% of errors), with the majority of ambiguity residing logically in the 'Neutral' class borderlines.
