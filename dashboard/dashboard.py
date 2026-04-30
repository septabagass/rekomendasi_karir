import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Dashboard Karier Mahasiswa", layout="wide")
sns.set(style="darkgrid")

# ==========================================
# LOAD DATA
# ==========================================
@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/all_data_bersih.csv", sep=None, engine='python')
    return df

df = load_data()

# ==========================================
# CLEANING KOLOM (WAJIB)
# ==========================================
df.columns = df.columns.str.strip()
df.columns = df.columns.str.replace(" ", "_")
df.columns = df.columns.str.lower()

# DEBUG (hapus nanti kalau sudah aman)
# st.write(df.columns.tolist())

# ==========================================
# SIDEBAR
# ==========================================
with st.sidebar:
    st.sidebar.image("dashboard/Logo.png", width=250)

    st.title("Filter Dashboard")
    
    career = st.multiselect(
        "Pilih Target Karier",
        options=df["career_goals"].unique(),
        default=df["career_goals"].unique()
    )
    
    internship = st.selectbox(
        "Pengalaman Magang",
        options=["All", "Yes", "No"]
    )

# ==========================================
# FILTER DATA
# ==========================================
filtered_df = df[df["career_goals"].isin(career)]

if internship != "All":
    filtered_df = filtered_df[
        filtered_df["internship_experience"] == internship
    ]

# ==========================================
# KPI
# ==========================================
st.title("Dashboard Analisis Karier Mahasiswa")

col1, col2, col3 = st.columns(3)

adapt_col = [col for col in df.columns if "adapt" in col][0]
comm_col = [col for col in df.columns if "comm" in col][0]

col2.metric(
    "Rata-rata Adaptability",
    round(filtered_df[adapt_col].mean(), 2)
)

col3.metric(
    "Rata-rata Communication",
    round(filtered_df[comm_col].mean(), 2)
)

# ==========================================
# 1. DISTRIBUSI KARIER
# ==========================================
st.subheader("Distribusi Target Karier")

fig1, ax1 = plt.subplots(figsize=(12, 10))
filtered_df["career_goals"].value_counts().plot(kind="barh", ax=ax1)
st.pyplot(fig1)

# ==========================================
# 2. HEATMAP SKILL
# ==========================================
st.subheader("Korelasi Skill Teknis")

tech_cols = [
    "python","java","c++","javascript","c#","php",
    "database_management","networking_skills"
]

# pastikan kolom ada
tech_cols = [col for col in tech_cols if col in filtered_df.columns]

fig2, ax2 = plt.subplots(figsize=(10, 15))
sns.heatmap(filtered_df[tech_cols].corr(), annot=True, cmap="coolwarm", ax=ax2)
st.pyplot(fig2)

# ==========================================
# 3. SOFT SKILL ANALYSIS
# ==========================================
st.subheader("Perbandingan Soft Skill")

soft_cols = [
    "communication_skills",
    "problem_solving",
    "teamwork"
]

soft_cols = [col for col in soft_cols if col in filtered_df.columns]

soft_df = filtered_df.groupby("career_goals")[soft_cols].mean().reset_index()

soft_melt = soft_df.melt(
    id_vars="career_goals",
    var_name="Skill",
    value_name="Score"
)

fig3, ax3 = plt.subplots(figsize=(12, 6))
sns.barplot(data=soft_melt, x="career_goals", y="Score", hue="Skill", ax=ax3)
plt.xticks(rotation=45)
st.pyplot(fig3)

# ==========================================
# 4. INTERNSHIP VS ADAPTABILITY
# ==========================================
st.subheader("Pengaruh Magang terhadap Adaptability")

intern_col = [col for col in df.columns if "intern" in col][0]

fig4, ax4 = plt.subplots()
sns.boxplot(
    data=filtered_df,
    x=intern_col,
    y=adapt_col,
    ax=ax4
)
st.pyplot(fig4)

# ==========================================
# 5. FEATURE ENGINEERING
# ==========================================
st.subheader("Feature Engineering Insights")

prog_cols = ["python","java","c++","javascript","c#","php"]
prog_cols = [col for col in prog_cols if col in filtered_df.columns]

soft_cols = ["communication_skills","problem_solving","teamwork"]
soft_cols = [col for col in soft_cols if col in filtered_df.columns]

filtered_df["total_programming"] = filtered_df[prog_cols].sum(axis=1)
filtered_df["total_softskill"] = filtered_df[soft_cols].sum(axis=1)

fig5, ax5 = plt.subplots()
sns.scatterplot(
    data=filtered_df,
    x="total_programming",
    y="total_softskill",
    hue="career_goals",
    ax=ax5
)
st.pyplot(fig5)

# ==========================================
# TABLE DATA
# ==========================================
st.subheader("Data Mahasiswa")
st.dataframe(filtered_df)

# ==========================================
# FOOTER
# ==========================================
st.caption("© 2026 Dashboard Sistem Rekomendasi Karier")
