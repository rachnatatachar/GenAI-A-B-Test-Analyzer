import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

st.set_page_config(page_title="GenAI A/B Test Analyzer", layout="centered")

st.title("📊 GenAI A/B Test Analyzer")
st.markdown("Upload your A/B test CSV file and get insights instantly.")

# Upload file
uploaded_file = st.file_uploader("📁 Upload CSV File", type=["csv"])

# Required columns
REQUIRED_COLUMNS = ['user_id', 'variant', 'conversion', 'platform', 'region', 'timestamp']

def validate_ab_test_data(df):
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        return False, f"Missing required columns: {', '.join(missing_cols)}"
    return True, "Data is valid"

def run_ab_test(df):
    group_a = df[df['variant'] == 'A']['conversion']
    group_b = df[df['variant'] == 'B']['conversion']

    t_stat, p_value = ttest_ind(group_a, group_b, equal_var=False)
    return {
        "variant_a_mean": round(group_a.mean() * 100, 2),
        "variant_b_mean": round(group_b.mean() * 100, 2),
        "p_value": round(p_value, 4),
        "significant": p_value < 0.05
    }

def generate_summary(result):
    if "error" in result:
        return result["error"]
    a_mean = result['variant_a_mean']
    b_mean = result['variant_b_mean']
    p_value = result['p_value']
    significant = result['significant']

    summary = (
        f"Variant A: **{a_mean}%**, Variant B: **{b_mean}%**\n\n"
    )
    if significant:
        summary += (
            f"✅ **Statistically significant** at 95% confidence (p = {p_value})\n\n"
        )
        summary += "🟢 **Recommendation:** Choose the better-performing variant."
    else:
        summary += (
            f"⚠️ Not statistically significant (p = {p_value})\n\n"
            "No clear winner. Consider collecting more data."
        )
    return summary

def plot_chart(a_mean, b_mean, p_value, significant):
    fig, ax = plt.subplots(figsize=(6, 4))
    variants = ['Variant A', 'Variant B']
    values = [a_mean, b_mean]
    bars = ax.bar(variants, values, color=['#4caf50', '#2196f3'])

    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}%', xy=(bar.get_x() + bar.get_width()/2, height),
                    xytext=(0, 5), textcoords='offset points', ha='center')

    ax.set_ylabel("Conversion Rate (%)")
    ax.set_title("Conversion Rate Comparison")

    subtitle = "Significant" if significant else "Not Significant"
    plt.suptitle(f"{subtitle} (p = {p_value})", fontsize=10, y=0.92)
    st.pyplot(fig)

# Run test if file uploaded
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    valid, message = validate_ab_test_data(df)
    st.info(f"🧪 Validation: {message}")

    if valid:
        result = run_ab_test(df)
        st.subheader("📊 Test Summary")
        st.markdown(generate_summary(result))
        st.subheader("📈 Conversion Chart")
        plot_chart(result['variant_a_mean'], result['variant_b_mean'], result['p_value'], result['significant'])
