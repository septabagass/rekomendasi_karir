import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# ==========================================
# KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(page_title="Dashboard MatchStep AI", layout="wide", page_icon="🎓")

# PALET WARNA PROFESIONAL
WARNA_UTAMA = "#2C3E50" # Biru gelap (Navy)
WARNA_AKSEN = "#18BC9C" # Hijau Teal

# ==========================================
# FUNGSI KARTU KUSTOM
# ==========================================
def buat_kartu_metrik(judul, nilai):
    return f"""
    <div style="background-color: #ffffff; padding: 20px 15px; border-radius: 8px; 
                box-shadow: 0 4px 6px rgba(0,0,0,0.05); text-align: center; 
                border-top: 4px solid {WARNA_AKSEN}; border-left: 1px solid #f0f0f0;
                border-right: 1px solid #f0f0f0; border-bottom: 1px solid #f0f0f0; margin-bottom: 20px;">
        <div style="color: {WARNA_UTAMA}; font-size: 14px; font-weight: 600; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px;">{judul}</div>
        <div style="color: #2b2b2b; font-size: 32px; font-weight: 800;">{nilai}</div>
    </div>
    """

# ==========================================
# LOAD DATA & MAPPING
# ==========================================
@st.cache_data
def load_data():
    # Pastikan nama file di dalam GitHub sama persis (huruf besar/kecilnya)
    df = pd.read_csv("dataset_bersih.csv", sep=";")
    
    # Standarisasi nama kolom ke huruf kecil dengan underscore
    df.columns = df.columns.str.strip().str.replace(" ", "_").str.lower()
    
    # Pengelompokan untuk Pertanyaan 3 (Manajerial/Analis vs Teknis)
    peran_analis_manajerial = [
        'Business Intelligence Analyst', 'Computer and Information Systems Manager', 
        'Computer Systems Analyst', 'Computer Systems Manager', 'Cybersecurity Analyst', 
        'Data Scientist', 'IT Consultant', 'IT Project Manager', 'IT Sales Professional', 
        'Systems Analyst', 'Research Scientist', 'Computer and Information Research Scientist'
    ]
    
    df['kategori_peran'] = df['career_goals'].apply(
        lambda x: 'Manajerial & Analis' if x in peran_analis_manajerial else 'Teknis Murni'
    )
    
    return df

df = load_data()

# ==========================================
# SIDEBAR (FILTERING)
# ==========================================
with st.sidebar:
    # Pengaman: Cek apakah file Logo.png ada di folder GitHub
    if os.path.exists("Logo.png"):
        st.image("Logo.png", width=250) 
    
    st.title("⚙️ Parameter Filter")
    
    # Sinkronisasi opsi selectbox dengan logika if di bawah
    magang = st.selectbox(
        "Pengalaman Kepemimpinan/Praktis:", 
        ["Semua", "Ada Pengalaman (Yes)", "Belum Ada (No)"]
    )
    
    st.divider()
    
    opsi_karir = sorted(df["career_goals"].dropna().unique())
    
    # Validasi nilai default
    default_pilihan = [k for k in ['Data Scientist', 'Software Engineer', 'IT Project Manager'] if k in opsi_karir]
    
    career = st.multiselect(
        "Pilih Target Karier:", 
        options=opsi_karir, 
        default=default_pilihan if default_pilihan else opsi_karir[:3]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.caption("© 2026 MatchStep AI | Dashboard Analitik")

# ==========================================
# LOGIKA FILTER
# ==========================================
filtered_df = df[df["career_goals"].isin(career)].copy()

if magang == "Ada Pengalaman (Yes)":
    filtered_df = filtered_df[filtered_df["leadership_experience"] == "Yes"]
elif magang == "Belum Ada (No)":
    filtered_df = filtered_df[filtered_df["leadership_experience"] == "No"]

# ==========================================
# MAIN DASHBOARD
# ==========================================
st.title("🎯 Dashboard Analitik MatchStep AI")
st.markdown("Menganalisis korelasi dan pola keterampilan mahasiswa terhadap target karier.")

# --- KPI METRICS ---
col1, col2, col3, col4 = st.columns(4)
prog_cols = ['python', 'java', 'c++', 'javascript', 'c#', 'php', 'ruby', 'swift', 'go', 'rust']
hard_skill_cols = ['software_development_experience', 'database_management', 'networking_skills', 'web_development_experience']
soft_skill_cols = ['communication_skills', 'problem_solving_abilities', 'teamwork_collaboration', 'time_management', 'adaptability']

if not filtered_df.empty:
    avg_prog = round(filtered_df[prog_cols].mean().mean(), 1)
    avg_soft = round(filtered_df[soft_skill_cols].mean().mean(), 1)
else:
    avg_prog, avg_soft = 0, 0

col1.markdown(buat_kartu_metrik("Data Terfilter", len(filtered_df)), unsafe_allow_html=True)
col2.markdown(buat_kartu_metrik("Karier Dipilih", len(career)), unsafe_allow_html=True)
col3.markdown(buat_kartu_metrik("Rata-rata Skor Coding", avg_prog), unsafe_allow_html=True)
col4.markdown(buat_kartu_metrik("Rata-rata Skor Soft Skill", avg_soft), unsafe_allow_html=True)

if not filtered_df.empty:
    
    st.markdown("---")
    
    # --- PERTANYAAN 1: BAHASA PEMROGRAMAN ---
    st.header("1. Profil Bahasa Pemrograman per Target Karier")
    c1, c2 = st.columns([1.2, 1])
    
    with c1:
        st.subheader("Heatmap Rata-rata Penguasaan")
        prog_df = filtered_df.groupby('career_goals')[prog_cols].mean().round(2)
        fig_heat = px.imshow(prog_df, 
                             labels=dict(x="Bahasa Pemrograman", y="Target Karier", color="Skor"),
                             color_continuous_scale="Teal",
                             text_auto=True, aspect="auto")
        st.plotly_chart(fig_heat, use_container_width=True)
        
    with c2:
        st.subheader("Pola Kombinasi Bahasa (Radar)")
        fig_radar = go.Figure()
        for c in career[:3]: 
            if c in prog_df.index:
                mean_scores = prog_df.loc[c].values.tolist()
                mean_scores.append(mean_scores[0]) 
                kategori_radar = prog_cols + [prog_cols[0]]
                
                fig_radar.add_trace(go.Scatterpolar(
                    r=mean_scores, theta=kategori_radar, fill='toself', name=c
                ))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 10])), showlegend=True,
                                legend=dict(orientation="h", y=-0.2))
        st.plotly_chart(fig_radar, use_container_width=True)

    st.markdown("---")

    # --- PERTANYAAN 2: HARD SKILL ---
    st.header("2. Pemetaan Hard Skill Utama terhadap Target Karier")
    hs_df = filtered_df.groupby('career_goals')[hard_skill_cols].mean().reset_index()
    hs_melted = hs_df.melt(id_vars='career_goals', var_name='Hard Skill', value_name='Skor Rata-rata')
    
    hs_melted['Hard Skill'] = hs_melted['Hard Skill'].str.replace('_', ' ').str.title()
    
    fig_bar = px.bar(hs_melted, x='career_goals', y='Skor Rata-rata', color='Hard Skill', 
                     barmode='group', color_discrete_sequence=px.colors.qualitative.Prism)
    fig_bar.update_layout(xaxis_title="Target Karier", yaxis_title="Skor Rata-rata (0-10)", legend_title="Jenis Hard Skill")
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")

    # --- PERTANYAAN 3: KEMAMPUAN INTERPERSONAL ---
    st.header("3. Distribusi Soft Skill: Peran Manajerial/Analis vs Teknis Murni")
    st.info("Visualisasi ini menggunakan data dari seluruh dataset (tanpa filter target karier di sidebar) untuk melihat perbandingan secara menyeluruh.")
    
    soft_df_melted = df.melt(id_vars=['kategori_peran'], value_vars=soft_skill_cols, 
                             var_name='Soft Skill', value_name='Skor')
    soft_df_melted['Soft Skill'] = soft_df_melted['Soft Skill'].str.replace('_', ' ').str.title()
    
    fig_box = px.box(soft_df_melted, x='Soft Skill', y='Skor', color='kategori_peran',
                     color_discrete_map={"Manajerial & Analis": WARNA_AKSEN, "Teknis Murni": WARNA_UTAMA})
    fig_box.update_layout(xaxis_title="Jenis Soft Skill", yaxis_title="Distribusi Skor (0-10)", 
                          legend_title="Kategori Peran", boxmode="group")
    st.plotly_chart(fig_box, use_container_width=True)

else:
    st.warning("⚠️ Data kosong. Silakan tambah opsi Karier atau ubah parameter Pengalaman di panel kiri.")
