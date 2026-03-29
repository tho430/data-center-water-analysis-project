# Data Center Water Usage Analysis

## Overview

This project analyzes water consumption and sustainability efforts associated with data center operations. As demand for cloud computing and artificial intelligence continues to grow, data centers require increasing amounts of water for cooling systems. This analysis focuses on identifying trends in water usage and evaluating whether water replenishment efforts are improving over time.

---

## Objectives

The primary goals of this project are:

- Analyze trends in data center water consumption over time  
- Evaluate changes in water replenishment efforts  
- Understand how sustainability initiatives compare to operational growth  

---

## Dataset

The dataset was compiled from publicly available corporate sustainability reports. It includes annual data from 2019 to 2024.

### Variables:

- `year` – Reporting year  
- `water_consumption` – Total water usage (billions of gallons)  
- `replenishment_percent` – Percentage of water replenished  
- `notes` – Additional context  

---

## Tools & Technologies

- Python  
- Pandas  
- Matplotlib   

---

## Analysis

Two descriptive analysis questions guided this project:

1. How has water consumption changed over time?  
2. Has the percentage of water replenished increased as water consumption has grown?  

---

## Visualizations

- **Line Chart**: Water consumption trends over time  
- **Bar Chart**: Water replenishment percentages by year  

These visualizations help illustrate both operational growth and sustainability improvements.

---

## Key Findings

- Water consumption increased steadily from 2019 to 2023, with a slight decrease in 2024  
- Water replenishment percentages improved significantly, especially in 2024  
- Sustainability efforts appear to be accelerating alongside increased resource demand  

---

## Limitations

- Dataset is limited to recent years (2019–2024)  
- Data is aggregated and does not reflect regional differences  
- Lack of standardized reporting across companies limits broader comparison  

---

## How to Run

1. Clone this repository  
2. Open the notebook in Google Colab or Jupyter  
3. Ensure required libraries are installed:

```bash
pip install pandas matplotlib
