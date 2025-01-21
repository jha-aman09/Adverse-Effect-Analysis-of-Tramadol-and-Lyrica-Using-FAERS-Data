# 📊 Analysis and Visualization of Adverse Drug Reactions

---

A comparative study of Tramadol and Lyrica using FAERS data.


## 📝 Project Overview
This project analyzes adverse drug reactions for **Tramadol** and **Lyrica** using FAERS (FDA Adverse Event Reporting System) data. It involves data processing, analysis, and visualization of the most common adverse effects associated with these drugs.


## 👤 Author
**Aman Jha**  
*Data Analyst*

Feel free to connect with me on [LinkedIn](https://www.linkedin.com/in/aman--jha) or via email at [pjha78498@gmail.com](mailto:pjha78498@gmail.com).


## 📂 Project Structure
```
📁 Project Root
├── 📄 Analyse.py        # Main analysis script
├── 📂 Data              # Folder to store datasets (not included in the repository)
│   ├── DEMO19Q1.txt    # Example dataset file (to be downloaded separately)
│   ├── DRUG19Q1.txt
│   ├── THER19Q1.txt
│   └── REAC19Q1.txt
```


## 📦 Data Instructions
The FAERS dataset is too large to include in this repository. Please follow these steps to set up the required data:

1. **Download the datasets**:
   - Visit the official [FAERS data website](https://www.fda.gov/drugs/questions-and-answers-fda-adverse-event-reporting-system-faers).
   - Download the relevant quarterly data files for 2019.

2. **Extract and place the files**:
   - Extract the datasets.
   - Place the extracted files into the `Data` folder at the root of this project.

3. Ensure the following file naming conventions:
   - `DEMO19Q<quarter>.txt`
   - `DRUG19Q<quarter>.txt`
   - `THER19Q<quarter>.txt`
   - `REAC19Q<quarter>.txt`


## 🚀 How to Run
1. Clone this repository:
   ```bash
   git clone https://github.com/jha-aman09/Adverse-Effect-Analysis-of-Tramadol-and-Lyrica-Using-FAERS-Data.git
   ```

2. Navigate to the project directory:
   ```bash
   cd Adverse-Effect-Analysis-of-Tramadol-and-Lyrica-Using-FAERS-Data
   ```

3. Ensure you have Python installed along with the required libraries:
   ```bash
   pip install pandas matplotlib seaborn
   ```

4. Run the analysis script:
   ```bash
   python Analyse.py
   ```


## 📊 Output
- The script generates visualizations comparing the top 10 adverse effects for **Tramadol** and **Lyrica**.
- Example output file:
  - `adverse_effects_comparison.png`


## ✨ Features
- Data ingestion and preprocessing for FAERS datasets.
- Comparative analysis of adverse drug reactions.
- Visualizations for top reported adverse effects.


## 💡 Future Enhancements
- Extend the analysis to additional drugs.
- Incorporate machine learning to predict potential adverse effects.
- Automate dataset retrieval and processing.
