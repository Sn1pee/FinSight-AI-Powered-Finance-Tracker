import streamlit as st
import pandas as pd
import tempfile, uuid
import os

from logic.PDFtoCSV import convert_pdf_to_csv
from logic.categorizer import categorize
from logic.analyzer   import analyze
from logic.insights   import generate_insights
from utils.plotter    import plot_finance_dashboard
from logic.ai_categorizer import categorize_with_ai

st.set_page_config(page_title="FinSight - Personal Finance AI", page_icon="💸", layout="centered")


st.sidebar.title("💸 FinSight")
st.sidebar.markdown(
    "Upload your bank-statement CSV or PDF and let FinSight break down "
    "your spending, visualise habits, and serve AI-driven tips.\n\n"
    "*Made by Monish Ⓜ️.*"
)

uploaded_file = st.sidebar.file_uploader("Upload Account Statement", type=["pdf", "csv"], label_visibility="collapsed")
api_ok = st.sidebar.checkbox("🔑 I have set my `API_KEY` env-var", value=False)

use_ai_cat = st.sidebar.checkbox("Use AI for Categorization", value=True)

def load_and_prepare(file) -> pd.DataFrame:
    df = pd.read_csv(file)
    df.columns = [c.strip().title() for c in df.columns]
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    df.dropna(subset=["Amount"], inplace=True)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    if use_ai_cat:
        with st.spinner("Letting AI categorise your transactions…"):
            try:
                df = categorize_with_ai(df)
            except Exception as e:
                st.error("❌ Failed to categorize using AI.")
                st.exception(e)
                st.stop()
    else:
        df["Category"] = df["Description"].apply(categorize)
    return df

def extract_text_from_pdf(file) -> str:
    import pdfplumber
    with pdfplumber.open(file) as pdf:
        text = "\n".join(page.extract_text() or "" for page in pdf.pages)
    return text

if uploaded_file:
    filetype = os.path.splitext(uploaded_file.name)[1].lower()
    if filetype == ".csv":
        df = load_and_prepare(uploaded_file)
        
    elif filetype == ".pdf":
        if not api_ok:
            st.warning("Please enable the API checkbox to process PDFs.")
            st.stop()
        with st.spinner("Extracting text from PDF..."):
            tmp_dir = tempfile.mkdtemp()
            safe_filename = f"{uuid.uuid4().hex}.pdf"
            tmp_path = os.path.join(tmp_dir, safe_filename)

            with open(tmp_path, "wb") as f:
                f.write(uploaded_file.read())

            try:
                statement_text = extract_text_from_pdf(tmp_path)
                csv_data = convert_pdf_to_csv({"text": statement_text})
                # Show preview and allow download
                st.subheader("📄 Extracted Transactions (AI-generated CSV)")
                st.download_button("Download CSV", csv_data, file_name="statement.csv", mime="text/csv")
                st.text_area("CSV Preview", csv_data, height=200)
                # Load into DataFrame for further analysis
                from io import StringIO
                df = load_and_prepare(StringIO(csv_data))
            except Exception as e:
                st.error("⚠️ Something went wrong while processing the PDF with AI.")
                st.exception(e)  # ⬅️ This logs the full traceback in Streamlit for debugging
                st.stop()

            finally:
                os.unlink(tmp_path)
                os.rmdir(tmp_dir)

    else:
        st.error("Unsupported file type.")
        st.stop()

    st.subheader("📄 Raw Transactions")
    st.dataframe(df.head(), use_container_width=True)

    summary = analyze(df)

    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Income",   f"₹{summary['income']:,.0f}")
    col2.metric("💸 Expense",  f"₹{summary['expense']:,.0f}")
    col3.metric("🟢 Savings",  f"₹{summary['savings']:,.0f}")

    st.subheader("🧩 Expense Split by Category")
    dashboard_fig = plot_finance_dashboard(df, summary)
    st.pyplot(dashboard_fig)

    if api_ok:
        with st.spinner("Generating AI insights…"):
            try:
                ai_text = generate_insights(summary)
                st.subheader("🤖 AI Money Coach Says:")
                st.markdown(ai_text)
            except RuntimeError as err:
                st.error(str(err))
    else:
        st.info("Enable the checkbox once your `API_KEY` env-var is set to fetch AI advice.")

else:
    st.title("Welcome to FinSight 💸✨")
    st.markdown(
        """
        **How to use**

        1. Export your bank or UPI statement to CSV or PDF  
        2. Ensure columns: `Date`, `Description`, `Amount`, `Type` (`Debit`/`Credit`)  
        3. Upload here and watch the magic happen ⚡  
        """
    )