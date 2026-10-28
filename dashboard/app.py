from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="NEXUS | Job Market Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_FILE = PROJECT_ROOT / "data" / "raw" / "jobs.csv"
SKILLS_FILE = PROJECT_ROOT / "data" / "processed" / "skills_analysis.csv"
CLASSIFIED_FILE = PROJECT_ROOT / "data" / "processed" / "classified_jobs.csv"


# ============================================================
# STYLE
# ============================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,500;12..96,600;12..96,700&family=IBM+Plex+Sans:wght@400;500;600&display=swap');

    :root {
        --background: #0f0d1a;
        --sidebar: #141127;
        --panel: #181530;
        --panel-light: #201c3f;
        --border: #322d58;
        --text: #f2eefc;
        --muted: #a49cc4;
        --accent: #f2b544;
        --violet: #9d8cff;
    }

    .stApp {
        background: var(--background);
        color: var(--text);
        font-family: 'IBM Plex Sans', sans-serif;
    }

    [data-testid="stHeader"] {
        background: rgba(15, 13, 26, 0.92);
    }

    [data-testid="stSidebar"] {
        background: var(--sidebar);
        border-right: 1px solid var(--border);
    }

    [data-testid="stSidebar"] * {
        color: var(--text);
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1600px;
    }

    h1, h2, h3 {
        font-family: 'Bricolage Grotesque', sans-serif !important;
        color: var(--text) !important;
        letter-spacing: -0.01em;
    }

    hr {
        border-color: var(--border) !important;
    }

    /* ---------- Marque ---------- */

    .brand {
        font-family: 'Bricolage Grotesque', sans-serif;
        font-size: 1.7rem;
        font-weight: 700;
        letter-spacing: 3px;
        color: var(--text);
        margin-bottom: 0;
    }

    .brand span {
        color: var(--accent);
    }

    .brand-subtitle {
        color: var(--muted);
        font-size: 0.74rem;
        letter-spacing: 1px;
        margin-top: 4px;
        margin-bottom: 24px;
    }

    /* ---------- En-tête ---------- */

    .eyebrow {
        display: inline-block;
        color: var(--accent);
        font-size: 0.85rem;
        font-weight: 500;
        letter-spacing: 0.5px;
        padding-left: 14px;
        border-left: 3px solid var(--accent);
        margin-bottom: 14px;
    }

    .hero-title {
        font-family: 'Bricolage Grotesque', sans-serif;
        font-size: clamp(2.1rem, 3.8vw, 3.3rem);
        font-weight: 700;
        line-height: 1.05;
        letter-spacing: -0.03em;
        margin-bottom: 12px;
        color: var(--text);
    }

    .hero-description {
        color: var(--muted);
        font-size: 1rem;
        line-height: 1.6;
        max-width: 70ch;
        margin-bottom: 25px;
    }

    .section-heading {
        font-family: 'Bricolage Grotesque', sans-serif;
        font-size: 1.3rem;
        font-weight: 600;
        letter-spacing: -0.01em;
        color: var(--text);
        margin-top: 22px;
        margin-bottom: 4px;
    }

    .section-sub {
        font-size: 0.85rem;
        color: var(--muted);
        margin-bottom: 15px;
    }

    /* ---------- Cartes ---------- */

    .metric-card {
        background: var(--panel);
        border: 1px solid var(--border);
        border-left: 4px solid var(--accent);
        border-radius: 6px;
        padding: 19px 20px;
        min-height: 126px;
    }

    .metric-label {
        font-size: 0.74rem;
        font-weight: 500;
        letter-spacing: 1px;
        color: var(--muted);
        margin-bottom: 12px;
    }

    .metric-value {
        font-family: 'Bricolage Grotesque', sans-serif;
        font-size: 2.2rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        color: var(--text);
        line-height: 1.1;
    }

    .metric-caption {
        font-size: 0.78rem;
        color: var(--violet);
        margin-top: 9px;
    }

    .info-panel {
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 18px;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid var(--border);
        border-radius: 10px;
        overflow: hidden;
    }

    div[data-testid="stPlotlyChart"] {
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 10px;
    }

    /* ---------- Widgets ---------- */

    [data-testid="stSidebar"] [data-baseweb="input"],
    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        background: var(--panel-light);
        border-color: var(--border);
        border-radius: 8px;
    }

    [data-testid="stSidebar"] [data-baseweb="tag"] {
        background: var(--violet);
        border-radius: 6px;
    }

    [data-testid="stSidebar"] [data-baseweb="tag"] * {
        color: #14102b;
    }

    [data-testid="stSidebar"] [role="radiogroup"] label {
        padding: 6px 10px;
        border-radius: 8px;
    }

    [data-testid="stSidebar"] [role="radiogroup"] label:hover {
        background: var(--panel-light);
    }

    .stButton > button {
        background: var(--panel-light);
        border-radius: 8px;
        border: 1px solid var(--border);
        color: var(--text);
    }

    .stButton > button:hover {
        border-color: var(--accent);
        color: var(--accent);
    }

    .stDownloadButton > button {
        background: var(--accent);
        color: #1a1405;
        font-weight: 600;
        border: none;
        border-radius: 8px;
    }

    .stDownloadButton > button:hover {
        background: #ffc95f;
        color: #1a1405;
    }

    .footer {
        color: #7f77a3;
        font-size: 0.78rem;
        border-top: 1px solid var(--border);
        padding-top: 18px;
        margin-top: 35px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# CHARGEMENT DES DONNÉES
# ============================================================

if not RAW_FILE.exists():
    st.error(
        "Le fichier jobs.csv est introuvable. "
        "Lance d'abord la collecte des offres."
    )
    st.code("python src/data/fetch_jobs.py")
    st.stop()

df = pd.read_csv(RAW_FILE)

EXPECTED_COLUMNS = [
    "job_title",
    "company",
    "location",
    "country",
    "job_type",
    "salary",
    "experience",
    "skills",
    "date_posted",
    "source",
    "job_url",
]

for column in EXPECTED_COLUMNS:
    if column not in df.columns:
        df[column] = ""

df = df.fillna("")

for column in EXPECTED_COLUMNS:
    df[column] = df[column].astype(str).replace("nan", "")

df["date_posted"] = pd.to_datetime(
    df["date_posted"],
    errors="coerce",
    utc=True,
).dt.tz_localize(None)

# Retirer les doublons éventuels
df = df.drop_duplicates(
    subset=["job_title", "company", "job_url"],
    keep="first",
).reset_index(drop=True)


# ============================================================
# INTÉGRATION DU CLASSIFICATEUR
# ============================================================

df["domain"] = "Non classé"

if CLASSIFIED_FILE.exists():
    try:
        classified_df = pd.read_csv(CLASSIFIED_FILE)

        if {"job_title", "domain"}.issubset(classified_df.columns):
            classified_df = classified_df.drop_duplicates(
                subset=["job_title"],
                keep="first",
            )

            domain_mapping = classified_df.set_index(
                "job_title"
            )["domain"].to_dict()

            mapped_domains = df["job_title"].map(domain_mapping)

            df["domain"] = mapped_domains.fillna("Non classé")

    except (pd.errors.ParserError, OSError, ValueError) as error:
        st.warning(
            f"Les classifications n'ont pas pu être chargées : {error}"
        )


# ============================================================
# FONCTIONS UTILITAIRES
# ============================================================

def metric_card(label, value, caption):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-caption">{caption}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def style_chart(fig, height=350):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="IBM Plex Sans, sans-serif",
            color="#e4def7",
            size=12,
        ),
        margin=dict(l=15, r=15, t=30, b=15),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="#b9b1d8"),
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(164,156,196,0.14)",
            zeroline=False,
            title_font=dict(color="#a49cc4"),
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            title_font=dict(color="#a49cc4"),
        ),
    )
    return fig


def clean_counts(series, limit=10):
    values = series.astype(str).str.strip()
    values = values[values.ne("") & values.ne("nan")]
    return values.value_counts().head(limit)


def parse_skills(series):
    all_skills = []

    for value in series.dropna().astype(str):
        for skill in value.split(","):
            skill = skill.strip()

            if skill and skill.lower() != "nan":
                all_skills.append(skill)

    return pd.Series(all_skills, dtype="object")


# ============================================================
# SIDEBAR ET FILTRES
# ============================================================

with st.sidebar:
    st.markdown(
        """
        <div class="brand">NE<span>X</span>US</div>
        <div class="brand-subtitle">JOB MARKET INTELLIGENCE</div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Navigation")

    page = st.radio(
        "Choisir une page",
        [
            "Vue d'ensemble",
            "Explorer les offres",
            "Compétences",
            "Classification",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("### Filtres globaux")

    search_query = st.text_input(
        "Recherche",
        placeholder="Métier, entreprise, mot-clé...",
    )

    available_locations = sorted(
        value
        for value in df["location"].unique()
        if value.strip()
    )

    selected_locations = st.multiselect(
        "Localisation",
        options=available_locations,
        placeholder="Toutes les localisations",
    )

    available_companies = sorted(
        value
        for value in df["company"].unique()
        if value.strip()
    )

    selected_companies = st.multiselect(
        "Entreprise",
        options=available_companies,
        placeholder="Toutes les entreprises",
    )

    available_domains = sorted(
        value
        for value in df["domain"].unique()
        if value.strip()
    )

    selected_domains = st.multiselect(
        "Domaine professionnel",
        options=available_domains,
        placeholder="Tous les domaines",
    )

    st.markdown("---")

    st.caption(f"{len(df):,} offres dans la base".replace(",", " "))

    if st.button("Réinitialiser les filtres", use_container_width=True):
        st.rerun()


# ============================================================
# APPLICATION DES FILTRES
# ============================================================

filtered = df.copy()

if search_query.strip():
    searchable_columns = [
        "job_title",
        "company",
        "location",
        "country",
        "skills",
        "domain",
    ]

    mask = pd.Series(False, index=filtered.index)

    for column in searchable_columns:
        mask |= filtered[column].astype(str).str.contains(
            search_query.strip(),
            case=False,
            regex=False,
            na=False,
        )

    filtered = filtered[mask]

if selected_locations:
    filtered = filtered[filtered["location"].isin(selected_locations)]

if selected_companies:
    filtered = filtered[filtered["company"].isin(selected_companies)]

if selected_domains:
    filtered = filtered[filtered["domain"].isin(selected_domains)]


# ============================================================
# EN-TÊTE
# ============================================================

st.markdown(
    '<div class="eyebrow">Market intelligence / 01</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="hero-title">Comprendre le marché de l’emploi.</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero-description">
        Explore les offres, identifie les compétences recherchées
        et observe les tendances du marché à partir des données collectées.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="section-sub">
        Données affichées : {len(filtered):,} offre(s) sur {len(df):,}
        dans la base.
    </div>
    """.replace(",", " "),
    unsafe_allow_html=True,
)


# ============================================================
# PAGE 1 — VUE D'ENSEMBLE
# ============================================================

if page == "Vue d'ensemble":

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric_card(
            "OFFRES D'EMPLOI",
            f"{len(filtered):,}".replace(",", " "),
            "Après application des filtres",
        )

    with col2:
        company_count = filtered["company"].replace("", pd.NA).nunique()
        metric_card(
            "ENTREPRISES",
            f"{company_count:,}".replace(",", " "),
            "Entreprises distinctes",
        )

    with col3:
        location_count = filtered["location"].replace("", pd.NA).nunique()
        metric_card(
            "LOCALISATIONS",
            f"{location_count:,}".replace(",", " "),
            "Zones géographiques détectées",
        )

    with col4:
        skills = parse_skills(filtered["skills"])
        skill_count = skills.nunique() if not skills.empty else 0
        metric_card(
            "COMPÉTENCES",
            f"{skill_count:,}".replace(",", " "),
            "Compétences distinctes détectées",
        )

    st.markdown(
        '<div class="section-heading">Domaines professionnels</div>'
        '<div class="section-sub">'
        "Répartition selon le classificateur actuel."
        "</div>",
        unsafe_allow_html=True,
    )

    domain_counts = clean_counts(filtered["domain"], limit=15)

    if not domain_counts.empty:
        domain_plot = domain_counts.rename_axis("domain").reset_index(
            name="count"
        )

        fig = px.bar(
            domain_plot,
            x="count",
            y="domain",
            orientation="h",
            labels={
                "count": "Nombre d'offres",
                "domain": "Domaine",
            },
            color="count",
            color_continuous_scale=["#3a2f7a", "#f2b544"],
        )

        fig.update_layout(
            coloraxis_showscale=False,
            yaxis=dict(categoryorder="total ascending"),
        )

        st.plotly_chart(
            style_chart(fig, max(260, len(domain_plot) * 42)),
            use_container_width=True,
        )
    else:
        st.info("Aucune classification disponible pour ces filtres.")

    left, right = st.columns(2)

    with left:
        st.markdown(
            '<div class="section-heading">Entreprises qui recrutent</div>'
            '<div class="section-sub">Top entreprises selon les offres visibles.</div>',
            unsafe_allow_html=True,
        )

        company_counts = clean_counts(filtered["company"], 10)

        if not company_counts.empty:
            company_plot = company_counts.rename_axis(
                "company"
            ).reset_index(name="offers")

            fig = px.bar(
                company_plot,
                x="offers",
                y="company",
                orientation="h",
                labels={
                    "offers": "Nombre d'offres",
                    "company": "Entreprise",
                },
                color_discrete_sequence=["#9d8cff"],
            )

            fig.update_layout(yaxis=dict(categoryorder="total ascending"))

            st.plotly_chart(
                style_chart(fig, 360),
                use_container_width=True,
            )
        else:
            st.info("Aucune entreprise disponible.")

    with right:
        st.markdown(
            '<div class="section-heading">Répartition géographique</div>'
            '<div class="section-sub">Localisations les plus fréquentes.</div>',
            unsafe_allow_html=True,
        )

        location_counts = clean_counts(filtered["location"], 10)

        if not location_counts.empty:
            location_plot = location_counts.rename_axis(
                "location"
            ).reset_index(name="offers")

            fig = px.pie(
                location_plot,
                names="location",
                values="offers",
                hole=0.62,
                color_discrete_sequence=[
                    "#f2b544",
                    "#9d8cff",
                    "#ff7a6b",
                    "#4fd1c5",
                    "#6cb6ff",
                    "#f472b6",
                    "#c4b5fd",
                    "#fbd38d",
                ],
            )

            fig.update_traces(
                textposition="inside",
                textinfo="percent",
                marker=dict(line=dict(color="#181530", width=2)),
            )

            st.plotly_chart(
                style_chart(fig, 360),
                use_container_width=True,
            )
        else:
            st.info("Aucune localisation disponible.")

    st.markdown(
        '<div class="section-heading">Dernières offres collectées</div>'
        '<div class="section-sub">Aperçu des offres disponibles dans la base.</div>',
        unsafe_allow_html=True,
    )

    recent = filtered.copy()

    if recent["date_posted"].notna().any():
        recent = recent.sort_values(
            "date_posted",
            ascending=False,
            na_position="last",
        )

    display_columns = [
        "job_title",
        "company",
        "location",
        "domain",
        "skills",
    ]

    st.dataframe(
        recent[display_columns].head(10),
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# PAGE 2 — EXPLORER LES OFFRES
# ============================================================

elif page == "Explorer les offres":

    st.markdown(
        '<div class="section-heading">Explorer les opportunités</div>'
        '<div class="section-sub">'
        "Filtre les offres et consulte leurs informations principales."
        "</div>",
        unsafe_allow_html=True,
    )

    if filtered.empty:
        st.warning("Aucune offre ne correspond aux filtres sélectionnés.")
    else:
        display_columns = [
            "job_title",
            "company",
            "location",
            "country",
            "job_type",
            "salary",
            "experience",
            "domain",
            "skills",
            "source",
            "job_url",
        ]

        display_columns = [
            column for column in display_columns
            if column in filtered.columns
        ]

        st.dataframe(
            filtered[display_columns],
            use_container_width=True,
            hide_index=True,
            column_config={
                "job_url": st.column_config.LinkColumn(
                    "Lien vers l'offre",
                    display_text="Ouvrir l'offre",
                )
            },
        )

        csv_data = filtered.to_csv(index=False).encode("utf-8-sig")

        st.download_button(
            "Télécharger les offres filtrées en CSV",
            data=csv_data,
            file_name="nexus_offres_filtrees.csv",
            mime="text/csv",
        )

        st.caption(
            "Les informations de salaire ou d'expérience peuvent être "
            "absentes si la source ne les fournit pas."
        )


# ============================================================
# PAGE 3 — COMPÉTENCES
# ============================================================

elif page == "Compétences":

    st.markdown(
        '<div class="section-heading">Compétences recherchées</div>'
        '<div class="section-sub">'
        "Compétences extraites des descriptions des offres collectées."
        "</div>",
        unsafe_allow_html=True,
    )

    skills_series = parse_skills(filtered["skills"])

    if skills_series.empty:
        st.warning(
            "Aucune compétence détectée. Vérifie la collecte et "
            "l'extraction des compétences."
        )
    else:
        skill_counts = skills_series.value_counts()

        total_mentions = int(skill_counts.sum())
        unique_skills = int(skill_counts.nunique() * 0 + len(skill_counts))

        c1, c2, c3 = st.columns(3)

        with c1:
            metric_card(
                "MENTIONS DE COMPÉTENCES",
                f"{total_mentions:,}".replace(",", " "),
                "Total des occurrences",
            )

        with c2:
            metric_card(
                "COMPÉTENCES DISTINCTES",
                f"{unique_skills:,}".replace(",", " "),
                "Éléments détectés",
            )

        with c3:
            metric_card(
                "OFFRES AVEC COMPÉTENCES",
                f"{filtered['skills'].astype(str).str.strip().ne('').sum():,}".replace(",", " "),
                "Dans la sélection actuelle",
            )

        skill_plot_data = skill_counts.head(20).rename_axis(
            "skill"
        ).reset_index(name="mentions")

        fig = px.bar(
            skill_plot_data.sort_values("mentions"),
            x="mentions",
            y="skill",
            orientation="h",
            labels={
                "mentions": "Nombre de mentions",
                "skill": "Compétence",
            },
            color="mentions",
            color_continuous_scale=["#3a2f7a", "#f2b544"],
        )

        fig.update_layout(
            coloraxis_showscale=False,
            yaxis=dict(categoryorder="total ascending"),
        )

        st.plotly_chart(
            style_chart(fig, max(400, len(skill_plot_data) * 28)),
            use_container_width=True,
        )

        st.markdown(
            '<div class="section-heading">Tableau des compétences</div>',
            unsafe_allow_html=True,
        )

        skill_table = skill_counts.rename(
            "mentions"
        ).reset_index(names="compétence")

        skill_table["part des mentions (%)"] = (
            skill_table["mentions"] / total_mentions * 100
        ).round(1)

        st.dataframe(
            skill_table,
            use_container_width=True,
            hide_index=True,
        )

        st.download_button(
            "Télécharger l'analyse des compétences",
            data=skill_table.to_csv(index=False).encode("utf-8-sig"),
            file_name="nexus_analyse_competences.csv",
            mime="text/csv",
        )

        st.info(
            "Les compétences proviennent d'une extraction par mots-clés. "
            "Elles peuvent être manquantes ou mal détectées ; les résultats "
            "représentent cet échantillon et non l'ensemble du marché."
        )


# ============================================================
# PAGE 4 — CLASSIFICATION
# ============================================================

elif page == "Classification":

    st.markdown(
        '<div class="section-heading">Classification des métiers</div>'
        '<div class="section-sub">'
        "Résultats issus du modèle expérimental de classification des offres."
        "</div>",
        unsafe_allow_html=True,
    )

    if not CLASSIFIED_FILE.exists():
        st.warning(
            "Le fichier de classification n'existe pas encore. "
            "Lance d'abord le script du modèle."
        )
        st.code("python src/models/job_classifier.py")

    else:
        try:
            classified = pd.read_csv(CLASSIFIED_FILE)

            if "job_title" not in classified.columns:
                st.error("Le fichier ne contient pas la colonne job_title.")
            elif "domain" not in classified.columns:
                st.error("Le fichier ne contient pas la colonne domain.")
            else:
                classified = classified.drop_duplicates(
                    subset=["job_title"],
                    keep="first",
                )

                class_counts = classified["domain"].value_counts()

                c1, c2 = st.columns(2)

                with c1:
                    metric_card(
                        "OFFRES CLASSÉES",
                        f"{len(classified):,}".replace(",", " "),
                        "Dans le fichier du modèle",
                    )

                with c2:
                    metric_card(
                        "CATÉGORIES IDENTIFIÉES",
                        f"{classified['domain'].nunique():,}".replace(",", " "),
                        "Domaines distincts",
                    )

                if not class_counts.empty:
                    class_plot = class_counts.rename_axis(
                        "domain"
                    ).reset_index(name="offers")

                    fig = px.bar(
                        class_plot.sort_values("offers"),
                        x="offers",
                        y="domain",
                        orientation="h",
                        labels={
                            "offers": "Nombre d'offres",
                            "domain": "Domaine",
                        },
                        color="offers",
                        color_continuous_scale=["#3a2f7a", "#f2b544"],
                    )

                    fig.update_layout(
                        coloraxis_showscale=False,
                        yaxis=dict(categoryorder="total ascending"),
                    )

                    st.plotly_chart(
                        style_chart(fig, max(300, len(class_plot) * 55)),
                        use_container_width=True,
                    )

                st.markdown(
                    '<div class="section-heading">Offres classées</div>',
                    unsafe_allow_html=True,
                )

                display_class_columns = [
                    column for column in [
                        "job_title",
                        "company",
                        "location",
                        "domain",
                    ]
                    if column in classified.columns
                ]

                st.dataframe(
                    classified[display_class_columns],
                    use_container_width=True,
                    hide_index=True,
                )

                st.warning(
                    "Limite méthodologique : les catégories d'entraînement "
                    "sont générées par des règles sur les titres. Le modèle "
                    "apprend donc à reproduire ces étiquettes sur un très "
                    "petit échantillon ; ce résultat ne constitue pas encore "
                    "une classification validée du marché de l'emploi."
                )

        except (pd.errors.ParserError, OSError, ValueError) as error:
            st.error(f"Impossible de lire le fichier de classification : {error}")


# ============================================================
# PIED DE PAGE
# ============================================================

st.markdown(
    """
    <div class="footer">
        NEXUS · Job Market Intelligence Platform
        <br>
        Analyse exploratoire des offres d'emploi · Projet Data
    </div>
    """,
    unsafe_allow_html=True,
)