# KG-FakeBench Code

This folder contains the implementation of the **KG-FakeBench framework**, including both the **generation pipeline** for creating KG-grounded misinformation and the **detection pipeline** for evidence-based verification.

---

## 📂 Folder Structure

- **`KG-Driven Fake Information Generation/`**  
  Contains the code for generating synthetic misinformation samples from knowledge graph triples. This pipeline perturbs structured facts and uses LLMs to synthesize realistic fake news under controlled plausibility settings.

- **`KG-Consistent Evidence Detection/`**  
  Contains the code for the KG-consistent evidence pipeline used for fact verification. This includes candidate discovery, grounding into KG triples, and prompting-based evaluation for detecting factual inconsistencies.

---

## 🔄 Pipeline Overview

The codebase is organized into two main stages:

### 🔹 1. KG-Driven Fake Information Generation

This module generates synthetic misinformation by:
- extracting reference triples from the knowledge graph  
- perturbing the object entity to create controlled factual deviations  
- defining plausibility levels (e.g., high / low)  
- providing plausible fake triples to LLMs for the generation of fake information 

---

### 🔹 2. KG-Consistent Evidence Detection

This module evaluates factual correctness by:
- preprocessing and tokenizing input statements  
- identifying candidate entities using similarity matching    
- retrieving supporting or non-supporting evidence  
- prompting LLMs with structured KG evidence for verification  

---

## 🎯 Purpose

This code supports:
- reproducibility of the KG-FakeBench benchmark  
- generation of structured, KG-grounded misinformation  
- evaluation of LLMs under evidence-aware settings  
- analysis of factual inconsistencies 

---

## ⚠️ Notes

- Some components require access to a knowledge graph (e.g., WikiGraphs)  
- LLM-based modules may require API access or local model setup  
- File and folder names are preserved as defined for clarity with the paper  

---

## 🔗 Related Resources

- Dataset: see the `../data/` folder  
- Project Repository: https://github.com/sanianayab/KG-FakeBench  
