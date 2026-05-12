## Assignment 5: Transfer Learning (CNN & Transformer)

This repository contains two robust Transfer Learning pipelines applied to Computer Vision and Natural Language Processing. Both models were trained using GPU acceleration (NVIDIA T4) in Google Colab.

### 1. Image Classification: Duck vs. Chicken (`TL_img.ipynb`)
- **Objective:** Fine-tune a pre-trained **ResNet18** Convolutional Neural Network to distinguish between images of ducks and chickens.
- **Dataset:** ~1,500 images from a public Kaggle dataset, cleanly segregated.
- **Methodology:** Froze the base layers, replaced the final fully-connected layer (`fc`) to output 2 classes, and trained using the Adam optimizer for 25 epochs.
- **Performance:** - **Test Accuracy:** **94%**
  - **F1-Scores:** Chicken (0.95), Duck (0.92)
  - **Training Time:** ~1 minute 17 seconds
- **Conclusion:** The model demonstrated excellent feature extraction capabilities with highly stable validation metrics in the later epochs, proving the efficiency of transfer learning on domain-specific visual tasks.

### 2. Text Classification: Sentiment Analysis (`TL_txt.ipynb`)
- **Objective:** Fine-tune **DistilBERT** (a Transformer model) to classify text into Negative, Neutral, and Positive sentiments.
- **Dataset:** A 5,000-row stratified sample of tweets from the Kaggle Sentiment Analysis Dataset.
- **Methodology:** Text was tokenized via `AutoTokenizer` (padding/truncation to 128 tokens) and trained over 5 epochs using the Hugging Face `Trainer` API.
- **Performance:**
  - **Test Accuracy:** **80%** (Evaluated on 1,000 unseen test samples)
  - **F1-Scores:** Negative (0.79), Neutral (0.77), Positive (0.83)
  - **Training Time:** ~4 minutes 28 seconds
- **Conclusion:** The Transformer effectively mapped the sentiment spectrum. It accurately identified distinct sentiments (Positive/Negative) while demonstrating logical, expected boundaries around the highly subjective 'Neutral' class.
