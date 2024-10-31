# Amino Acid Pattern Prediction in High-Temperature Daqu Fermentation

This repository contains the R and Python scripts for analyzing amino acid patterns in high-temperature Daqu (HTD) fermentation. It includes microbial community analysis, correlation analysis, and machine learning-based modeling to predict amino acid patterns from microbial features.

## Project Overview

Amino acids are vital nitrogen sources in HTD and are closely linked to HTD quality. This study examines amino acid patterns by measuring fermentation parameters, microbial community dynamics, and amino acid concentrations throughout the HTD fermentation process. Through correlation analysis and feature selection using machine learning, we identified critical amplicon sequence variants (ASVs) and built predictive models for amino acid patterns.

## Contents

- `data/raw`: Example datasets (fermentation parameters, microbial data, amino acid concentrations)
- `data/result`: The intermediate data files
- `src/R/`: R scripts for microbial community analysis, RDA, and visualizations
- `src/Python`: Python scripts for co-linearity network, machine learning model construction

## Methods

### Microbial Community Analysis

The R scripts in this repository analyze the microbial community's role in amino acid metabolism using correlation analysis, redundancy analysis (RDA), and visualization. Key packages include `vegan` for RDA.

### Machine Learning Model

Using Python, we implemented three machine learning algorithms—XGBoost, Random Forest (RF), and Partial Least Squares Regression (PLSR)—for feature selection and predictive modeling. Feature importance is assessed using SHAP values, feature importance metrics, and VIP scores respectively.

- Feature Selection:

   Three methods were employed to select key ASVs:

  - XGBoost with SHAP
  - RF with Feature Importance
  - PLSR with VIP

- **Model Construction:** The selected ASVs were used to construct high-accuracy models for amino acid pattern prediction.

## Installation and Setup

1. Clone the repository:

   ```
   bash
   
   
   复制代码
   git clone https://github.com/yourusername/htd-amino-acid-pattern-prediction.git
   ```

2. Install required R packages:

   ```
   R
   
   
   复制代码
   install.packages(c("vegan", ...))  # You need install all necessary packages
   ```

3. Install required Python packages:

   ```
   bash
   
   
   复制代码
   pip install pandas    # You need install all necessary packages
   ```

## Usage

- **Microbial Community Analysis:** Run R scripts in `src/R` to perform microbial community analysis, RDA.
- **Machine Learning Model Construction:** Execute Python scripts in `src/python` to conduct feature selection and build predictive models.

## Results

Key findings indicate that five ASVs—two from *Saccharopolyspora*, two from *Bacillus*, and one from *Lactobacillus*—are critical predictors of amino acid patterns in HTD fermentation.