import streamlit as st
import pandas as pd
import great_expectations as ge
import matplotlib.pyplot as plt

st.set_page_config(page_title="CSV Validator with GE", layout="wide")

st.title("📊 CSV Data Validator using Great Expectations")

uploaded_file = st.file_uploader("🗂️ Upload CSV file", type="csv")

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("✅ File uploaded!")
        st.write("📋 Preview:", df.head())

        # แปลงเป็น GE DataFrame
        ge_df = ge.from_pandas(df)

        # เลือกคอลัมน์
        column = st.selectbox("🧩 Select column to test", df.columns)

        # เลือก Expectation
        expectation = st.selectbox(
            "📌 Select Great Expectations check",
            [
                "expect_column_values_to_not_be_null",
                "expect_column_values_to_be_unique"
            ]
        )

        # รัน Expectation
        if st.button("✅ Run Test"):
            if expectation == "expect_column_values_to_not_be_null":
                result = ge_df.expect_column_values_to_not_be_null(column)
            elif expectation == "expect_column_values_to_be_unique":
                result = ge_df.expect_column_values_to_be_unique(column)

            # แสดงผลลัพธ์
            st.subheader("✅ Test Result:")
            st.json(result)

            # แสดง Pie Chart
            labels = ['Passed', 'Failed']
            total = result['result']['element_count']
            failed = result['result']['unexpected_count']
            passed = total - failed

            fig, ax = plt.subplots()
            ax.pie([passed, failed], labels=labels, autopct='%1.1f%%', colors=['green', 'red'])
            st.pyplot(fig)

    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
else:
    st.info("👆 Please upload a CSV file to validate.")
