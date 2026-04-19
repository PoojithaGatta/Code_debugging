# Code Intelligence & Document Understanding  

##  Introduction  
This project presents an the following:  
- **Code Generation**  
- **Code Debugging**  
- **Document Understanding**  

It leverages **Transformer-based models (CodeT5, BART, LED, DiT, LLaMA)** to automate software development and document analysis tasks efficiently.

---

## 🔹 Code Generation Results  

| Model   | BLEU Score | ROUGE Score | METEOR | BERTScore (F1) |
|--------|-----------|------------|--------|----------------|
| CodeT5 | 0.78      | 0.81       | 0.76   | 0.84           |
| BART   | 0.74      | 0.79       | 0.72   | 0.80           |

✅ **Best Model: CodeT5**

---

## 🔹 Code Debugging  

### Performance Graph  
![Debugging Graph](Code_Debugging/images/result.png)  

---

## 🔹 Document Understanding  

The system integrates **Document Classification + Summarization** using Vision and Language Transformers.

### Key Performance  
- Classification Accuracy: **~99%**  
- LED outperforms BART in summarization (higher semantic accuracy and layout fidelity) :contentReference[oaicite:1]{index=1}  

---

## 🔹 Evaluation Results  

### Confusion Matrix  
![Confusion Matrix](Document_Understanding/Results/confusion_matrix.png)  

### Classification Report  
![Classification Report](Document_Understanding/Results/classification_report.png)  

### Model Evaluation Graph  
![Evaluation Graph](Document_Understanding/Results/evaluation_graph.png)  

---

## 🔹 Embeddings & FAISS Index  
Stored embeddings and FAISS index used in the system are available here:  
🔗 https://drive.google.com/drive/folders/120ApkMXuY033KxfYh-DQJ98lPTRrAbiV  

---

