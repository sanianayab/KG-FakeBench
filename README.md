# KG-FakeBench: Generating and Detecting Knowledge-Graph-Grounded Fake Information with LLMs

KG-FakeBench is a large-scale benchmark for evaluating large language models (LLMs) on **AI-generated misinformation** under controlled factual deviations.

The benchmark leverages **knowledge graphs (KGs)** to generate misinformation that is *factually incorrect yet semantically plausible*, and introduces a **KG-consistent evidence framework** for structured, evidence-based detection.

📄 Paper: *coming soon*

---

## 🔑 Key Contributions

- **KG-Grounded Benchmark**  
  A large-scale dataset generated via structured KG deviations, ensuring **fine-grained control over factual plausibility** and transparent provenance.

- **KG-Consistent Evidence Detection**  
  A structured pipeline that extracts **(s, r, o) triples** and uses them as external evidence for LLM-based verification.

- **Comprehensive Evaluation**  
  Evaluation across standard, CoT, and KG-grounded prompting shows that external evidence improves detection reliability and reveals model behavior and bias.

---

## 📊 Dataset

- **28,900 synthetic samples**
  - 14,450 high-plausibility
  - 14,450 low-plausibility  
- **1,239 real samples**

The dataset is derived from **WikiGraphs**, ensuring structured and verifiable factual grounding.

📂 See [`data/`](data/) for details.

---

## 🧠 Methodology

KG-FakeBench consists of two main components:

### 🔹 1. KG-Driven Fake Information Generation
- Extract reference triples ⟨s, r, o⟩ from KG  
- Generate fake triples ⟨s, r, o′⟩ with controlled plausibility  
- Use LLMs to synthesize natural language misinformation  

### 🔹 2. KG-Consistent Evidence Detection
- Tokenize and normalize input statements  
- Retrieve candidate entities via similarity matching  
- Ground statements into KG triples  
- Use **triple-based prompting** for factual verification  

---
## 📂 Repository Structure

<pre>
KG-FakeBench/
├── data/                                   # Dataset (fake + real samples)
├── code/
│   ├── KG-Driven Fake Information Generation/   # Generation pipeline
│   ├── KG-Consistent Evidence Detection/        # Detection pipeline
├── README.md
</pre>

---

## ⚙️ Code

The implementation is divided into:

- **KG-Driven Fake Information Generation**  
- **KG-Consistent Evidence Detection**

📂 See [`code/`](code/) for details.

---

## ⚠️ Disclaimer

This dataset contains **synthetic misinformation** generated for research purposes only.  
It is intended to support the development of **robust and trustworthy detection systems**.

---

## 🔗 Resources

- 📦 Dataset: [`data/`](data/)
- ⚙️ Code: [`code/`](code/)

---

## 🤝 Contributing

Contributions are welcome. Please open an issue or submit a pull request.

