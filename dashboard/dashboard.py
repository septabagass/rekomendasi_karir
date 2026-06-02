import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ==========================================
# KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(page_title="Dashboard MatchStep AI", layout="wide", page_icon="🎓")

# ==========================================
# PALET WARNA PROFESIONAL
# ==========================================
WARNA_UTAMA = "#2C3E50"     # Biru gelap (Navy)
WARNA_AKSEN = "#18BC9C"     # Hijau Teal
WARNA_SEKUNDER = "#3498DB"  # Biru Terang 
WARNA_NETRAL = "#95A5A6"    # Abu-abu 
WARNA_KATEGORIKAL = [WARNA_UTAMA, WARNA_AKSEN, WARNA_SEKUNDER, WARNA_NETRAL]
SKALA_GRADASI = "Teal"      

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
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(BASE_DIR, "dataset_bersih.csv")
    
    try:
        df = pd.read_csv(file_path, sep=";")
    except FileNotFoundError:
        df = pd.read_csv("dataset_bersih.csv", sep=";") 
        
    df.columns = df.columns.str.strip().str.replace(" ", "_").str.lower()
    
    if 'leadership_experience' in df.columns:
        df['leadership_experience'] = df['leadership_experience'].astype(str).str.strip().str.title()
        
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
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(BASE_DIR, "Logo.png")
    
    if os.path.exists(logo_path):
        st.image(logo_path, width=250) 
    elif os.path.exists("Logo.png"):
        st.image("Logo.png", width=250)
        
    st.title("⚙️ Parameter Filter")
    
    opsi_karir = sorted(df["career_goals"].dropna().unique())
    default_pilihan = [k for k in ['Data Scientist', 'Software Engineer', 'IT Project Manager'] if k in opsi_karir]
    
    career = st.multiselect(
        "Pilih Target Karier:", 
        options=opsi_karir, 
        default=default_pilihan if default_pilihan else opsi_karir[:3]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.caption("© 2026 MatchStep AI | Pendidikan Teknik Informatika - UNY")

# ==========================================
# LOGIKA FILTER
# ==========================================
filtered_df = df[df["career_goals"].isin(career)].copy()

# ==========================================
# MAIN DASHBOARD
# ==========================================
st.title("🎯 Dashboard Analitik MatchStep AI")
st.markdown("Menganalisis korelasi dan pola keterampilan mahasiswa terhadap target karier.")

# --- KPI METRICS ---
col1, col2, col3, col4 = st.columns(4)
prog_cols = ['python', 'java', 'c++', 'javascript', 'c#', 'php', 'ruby', 'swift', 'go', 'rust']
hard_skill_cols = ['software_development_experience', 'database_management', 'networking_skills', 'web_development_experience']
soft_skill_fokus = ['communication_skills', 'problem_solving_abilities', 'teamwork_collaboration']

if not filtered_df.empty:
    avg_prog = round(filtered_df[prog_cols].stack().mean(), 2)
    avg_soft = round(filtered_df[soft_skill_fokus].stack().mean(), 2)
else:
    avg_prog, avg_soft = 0, 0

col1.markdown(buat_kartu_metrik("Data Terfilter", len(filtered_df)), unsafe_allow_html=True)
col2.markdown(buat_kartu_metrik("Karier Dipilih", len(career)), unsafe_allow_html=True)
col3.markdown(buat_kartu_metrik("Rata-rata Skor Coding", avg_prog), unsafe_allow_html=True)
col4.markdown(buat_kartu_metrik("Rata-rata Skor Soft Skill", avg_soft), unsafe_allow_html=True)

tinggi_dinamis = max(450, len(career) * 45)

if not filtered_df.empty:
    
    st.markdown("---")
    
    # --- BAGIAN 1: OVERVIEW DEMOGRAFI & KEPEMIMPINAN ---
    st.header("1. Overview Demografi Mahasiswa")
    col_demo1, col_demo2 = st.columns([2, 1]) 
    
    with col_demo1:
        st.subheader("Distribusi Target Karier")
        career_counts = filtered_df['career_goals'].value_counts().reset_index()
        career_counts.columns = ['Target Karier', 'Jumlah Mahasiswa']
        
        # PERBAIKAN: Memaksa teks angka muncul di luar (outside) grafik batang
        fig_career = px.bar(career_counts, x='Jumlah Mahasiswa', y='Target Karier', orientation='h', text='Jumlah Mahasiswa')
        fig_career.update_traces(marker_color=WARNA_SEKUNDER, textposition='outside', textfont_size=13) 
        fig_career.update_layout(height=tinggi_dinamis, yaxis={'categoryorder':'total ascending'}, xaxis_title="", yaxis_title="")
        st.plotly_chart(fig_career, use_container_width=True)

    with col_demo2:
        st.subheader("Pengalaman Kepemimpinan")
        lead_counts = filtered_df['leadership_experience'].value_counts().reset_index()
        lead_counts.columns = ['Status', 'Jumlah']
        
        fig_pie = px.pie(lead_counts, values='Jumlah', names='Status', hole=0.4,
                         color='Status', color_discrete_map={"Yes": WARNA_AKSEN, "No": WARNA_UTAMA})
        
        # PERBAIKAN: Memperjelas persentase dengan font warna putih yang tebal
        fig_pie.update_traces(textposition='inside', textinfo='percent+label', 
                              textfont=dict(color='white', size=15, weight='bold'))
        fig_pie.update_layout(height=450, showlegend=False) 
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")
    
    # --- BAGIAN 2: BAHASA PEMROGRAMAN ---
    st.header("2. Profil Bahasa Pemrograman per Target Karier")
    st.subheader("Heatmap Rata-rata Penguasaan")
    prog_df = filtered_df.groupby('career_goals')[prog_cols].mean().round(2)
    
    fig_heat = px.imshow(prog_df, 
                         labels=dict(x="Bahasa Pemrograman", y="Target Karier", color="Skor"),
                         color_continuous_scale=SKALA_GRADASI,
                         text_auto=True, aspect="auto")
    
    fig_heat.update_layout(height=tinggi_dinamis, xaxis_title="", yaxis_title="")
    st.plotly_chart(fig_heat, use_container_width=True)

    st.markdown("---")

    # --- BAGIAN 3: HARD SKILL (MENGGUNAKAN TABS) ---
    st.header("3. Pemetaan Hard Skill Utama terhadap Target Karier")
    
    hs_df = filtered_df.groupby('career_goals')[hard_skill_cols].mean().round(2)
    hs_df_display = hs_df.copy()
    hs_df_display.columns = [col.replace('_', ' ').title() for col in hs_df_display.columns]
    
    tab1, tab2 = st.tabs(["🔥 Heatmap Skor Hard Skill", "📊 Bar Chart Distribusi"])
    
    with tab1:
        fig_heat_hs = px.imshow(hs_df_display, 
                             labels=dict(x="Jenis Hard Skill", y="Target Karier", color="Skor"),
                             color_continuous_scale=SKALA_GRADASI,
                             text_auto=True, aspect="auto")
                             
        fig_heat_hs.update_layout(height=tinggi_dinamis, xaxis_title="", yaxis_title="")
        st.plotly_chart(fig_heat_hs, use_container_width=True)

    with tab2:
        hs_melted = hs_df.reset_index().melt(id_vars='career_goals', var_name='Hard Skill', value_name='Skor Rata-rata')
        hs_melted['Hard Skill'] = hs_melted['Hard Skill'].str.replace('_', ' ').str.title()
        
        fig_bar = px.bar(hs_melted, x='career_goals', y='Skor Rata-rata', color='Hard Skill', 
                         barmode='group', color_discrete_sequence=WARNA_KATEGORIKAL)
                         
        fig_bar.update_layout(height=tinggi_dinamis, xaxis_title="", yaxis_title="Skor Rata-rata (0-10)", legend_title="Jenis Hard Skill")
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")

    # --- BAGIAN 4: KEMAMPUAN INTERPERSONAL ---
    st.header("4. Distribusi Soft Skill Utama: Peran Manajerial/Analis vs Teknis Murni")
    st.info("Visualisasi membandingkan 3 *Soft Skill* kunci (Communication, Problem Solving, Teamwork) menggunakan data seluruh populasi dataset.")
    
    df_q3 = df[df['kategori_peran'] != 'Lainnya'].copy()
    
    soft_df_melted = df_q3.melt(id_vars=['kategori_peran'], value_vars=soft_skill_fokus, 
                             var_name='Soft Skill', value_name='Skor')
    
    soft_df_melted['Soft Skill'] = soft_df_melted['Soft Skill'].str.replace('_', ' ').str.title()
    soft_df_melted['Soft Skill'] = soft_df_melted['Soft Skill'].str.replace('Abilities', '').str.replace('Collaboration', '').str.strip()
    
    fig_box = px.box(soft_df_melted, x='Soft Skill', y='Skor', color='kategori_peran',
                     color_discrete_map={"Manajerial & Analis": WARNA_AKSEN, "Teknis Murni": WARNA_UTAMA})
    fig_box.update_layout(xaxis_title="Jenis Soft Skill", yaxis_title="Distribusi Skor (0-10)", 
                          legend_title="Kategori Peran", boxmode="group")
    st.plotly_chart(fig_box, use_container_width=True)

else:
    st.warning("⚠️ Data kosong. Silakan tambah opsi Karier di panel kiri.")
