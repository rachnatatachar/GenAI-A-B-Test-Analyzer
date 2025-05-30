# GenAI A/B Test Analyzer

A GenAI-powered A/B test analyzer that enables product managers, data analysts, and marketers to evaluate A/B test results in a simple and effective way.

Built using **Python**, **Streamlit**, and **statistical testing**, this tool helps you:
- Upload A/B test results (CSV)
- Validate the dataset
- Visualize and compare variant performance
- Get a recommendation based on statistical significance (t-test @ 95% confidence)

---

## Project Structure

| File | Description |
|------|-------------|
| `app.py` | Streamlit app – upload CSV and view results |
| `Run_AB_Test_Tool.ipynb` | Jupyter Notebook with complete backend engine + visualization + run demo |
| `data/sample_ab_test.csv` | Sample A/B test dataset |

---

## How to Run Locally

### Install Dependencies
```bash
pip install -r requirements.txt
