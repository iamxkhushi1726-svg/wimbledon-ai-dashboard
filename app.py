import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

load_dotenv()

# ── Page Configuration ──────────────────────────────────────────
st.set_page_config(
    page_title="Wimbledon Advanced Analytics Platform",
    page_icon="🎾",
    layout="wide",
)

# ── Native Streamlit Variable Integration CSS ───────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;1,400&family=EB+Garamond:ital,wght@0,400;0,600;0,700;1,400&family=Inter:wght@400;500;600&family=Roboto+Mono:wght@400;500&display=swap');

    /* Bind main typography to native Streamlit text variable */
    h1, .championship-title {
        font-family: 'Playfair Display', Georgia, serif !important;
        font-weight: 700 !important;
        color: var(--text-color) !important;
        letter-spacing: -0.01em !important;
    }
    
    h2, h3, h4, h5, h6, .metric-label, .player-name, .framework-subtitle {
        font-family: 'EB Garamond', Georgia, serif !important;
        color: var(--text-color) !important;
        font-weight: 600 !important;
        letter-spacing: 0.01em !important;
    }

    /* Force all text paragraphs, spans, and headings inside markdown to use native text color */
    div[data-testid="stMarkdownContainer"] p, 
    div[data-testid="stMarkdownContainer"] span,
    div[data-testid="stMarkdownContainer"] li,
    div[data-testid="stMarkdownContainer"] h1,
    div[data-testid="stMarkdownContainer"] h2,
    div[data-testid="stMarkdownContainer"] h3,
    div[data-testid="stMarkdownContainer"] h4,
    div[data-testid="stMarkdownContainer"] h5,
    div[data-testid="stMarkdownContainer"] h6 {
        color: var(--text-color) !important;
    }

    /* Cards adapt to secondary background and primary text colors */
    .profile-card {
        background-color: var(--secondary-background-color) !important;
        border: 1px solid rgba(128, 128, 128, 0.2) !important;
        border-top: 4px solid #006633 !important; 
        padding: 24px;
        border-radius: 6px;
        text-align: left;
        margin-bottom: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    
    .player-name {
        font-size: 26px;
        font-weight: 700;
        margin-bottom: 2px;
        color: var(--text-color) !important;
    }
    
    .player-meta {
        font-family: 'Inter', sans-serif !important;
        font-size: 11px;
        color: var(--text-color) !important;
        opacity: 0.7;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 600;
        margin-bottom: 18px;
    }
    
    .metric-value {
        font-family: 'Roboto Mono', monospace;
        font-size: 30px;
        font-weight: 500;
        color: #006633 !important;
        margin-bottom: 2px;
    }
    
    .data-grid {
        margin-top: 18px;
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
        border-top: 1px solid rgba(128, 128, 128, 0.2);
        padding-top: 14px;
    }
    
    .data-item {
        color: var(--text-color) !important;
        opacity: 0.8;
        font-size: 14px;
    }
    
    .data-item strong {
        color: var(--text-color) !important;
        opacity: 1;
        font-family: 'Roboto Mono', monospace;
    }
    
    .analysis-box {
        background-color: var(--secondary-background-color) !important;
        border-left: 4px solid #006633 !important;
        border-top: 1px solid rgba(128, 128, 128, 0.2) !important;
        border-right: 1px solid rgba(128, 128, 128, 0.2) !important;
        border-bottom: 1px solid rgba(128, 128, 128, 0.2) !important;
        padding: 24px;
        border-radius: 6px;
        color: var(--text-color) !important;
        font-size: 16px;
        line-height: 1.65;
        font-family: 'EB Garamond', Georgia, serif;
    }

    /* Navigation Tabs */
    div[data-testid="stTabs"] button {
        background-color: transparent !important;
        border-bottom: 2px solid transparent !important;
    }
    div[data-testid="stTabs"] button p {
        color: var(--text-color) !important;
        opacity: 0.7;
        font-family: 'EB Garamond', Georgia, serif !important;
        font-size: 18px !important;
    }
    div[data-testid="stTabs"] button[aria-selected="true"] {
        border-bottom-color: #006633 !important;
    }
    div[data-testid="stTabs"] button[aria-selected="true"] p {
        color: #006633 !important;
        opacity: 1 !important;
        font-weight: bold !important;
    }

    /* Radio Buttons & Inputs */
    div[data-testid="stRadio"] label p, div[data-testid="stWidgetLabel"] p {
        font-family: 'Inter', sans-serif !important;
        color: var(--text-color) !important;
        font-size: 14px !important;
    }

    /* Action Buttons */
    div.stButton > button:first-child {
        background-color: #006633 !important;
        color: #FFFFFF !important;
        border: 1px solid #006633 !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        border-radius: 4px !important;
        padding: 8px 20px !important;
    }

    /* Head-to-Head Table */
    .h2h-table {
        width: 100%;
        border-collapse: collapse;
        font-family: 'Inter', sans-serif;
        margin-top: 10px;
    }
    .h2h-table th {
        padding: 16px 20px;
        background-color: var(--secondary-background-color) !important;
        color: var(--text-color) !important;
        font-family: 'EB Garamond', Georgia, serif;
        font-size: 18px;
        font-weight: 600;
        border-bottom: 2px solid rgba(128, 128, 128, 0.3) !important;
    }
    .h2h-table td {
        padding: 14px 20px;
        font-size: 14px;
        vertical-align: middle;
        border-bottom: 1px solid rgba(128, 128, 128, 0.2) !important;
        background-color: var(--background-color) !important;
    }
    .h2h-dim-cell {
        font-family: 'EB Garamond', Georgia, serif;
        font-weight: 600;
        font-size: 16px !important;
        color: var(--text-color) !important;
        width: 40%;
    }
    .h2h-stat-cell {
        font-family: 'Roboto Mono', monospace;
        font-size: 14px;
        font-weight: 500;
        text-align: center;
        width: 30%;
    }
</style>
""", unsafe_allow_html=True)

# ── Data Matrices ───────────────────────────────────────────────
PLAYERS = {
    "Novak Djokovic": {
        "country": "SRB", "rank": 2, "age": 38, "grand_slams": 24, "wimbledon_titles": 7,
        "win_rate_2025": 78, "grass_win_rate": 85, "serve_speed_kmh": 215, "aces_per_match": 9.2,
        "first_serve_pct": 63, "style": "All-court baseline master", "odds_to_win": 18,
    },
    "Carlos Alcaraz": {
        "country": "ESP", "rank": 3, "age": 22, "grand_slams": 4, "wimbledon_titles": 2,
        "win_rate_2025": 82, "grass_win_rate": 80, "serve_speed_kmh": 220, "aces_per_match": 8.1,
        "first_serve_pct": 65, "style": "Aggressive all-court attacking", "odds_to_win": 22,
    },
    "Jannik Sinner": {
        "country": "ITA", "rank": 1, "age": 23, "grand_slams": 3, "wimbledon_titles": 0,
        "win_rate_2025": 86, "grass_win_rate": 72, "serve_speed_kmh": 218, "aces_per_match": 7.8,
        "first_serve_pct": 67, "style": "Powerful baseline grinder", "odds_to_win": 25,
    },
    "Daniil Medvedev": {
        "country": "RUM", "rank": 4, "age": 29, "grand_slams": 1, "wimbledon_titles": 0,
        "win_rate_2025": 74, "grass_win_rate": 68, "serve_speed_kmh": 210, "aces_per_match": 10.1,
        "first_serve_pct": 62, "style": "Unorthodox defensive counter-puncher", "odds_to_win": 12,
    },
}

WOMEN_PLAYERS = {
    "Iga Swiatek": {
        "country": "POL", "rank": 1, "age": 24, "grand_slams": 5, "wimbledon_titles": 0,
        "win_rate_2025": 88, "grass_win_rate": 70, "serve_speed_kmh": 185, "aces_per_match": 3.2,
        "first_serve_pct": 65, "style": "Topspin baseline dominance", "odds_to_win": 20,
    },
    "Aryna Sabalenka": {
        "country": "BLR", "rank": 2, "age": 27, "grand_slams": 3, "wimbledon_titles": 0,
        "win_rate_2025": 80, "grass_win_rate": 75, "serve_speed_kmh": 195, "aces_per_match": 5.8,
        "first_serve_pct": 62, "style": "Powerful aggressive baseline", "odds_to_win": 25,
    },
    "Elena Rybakina": {
        "country": "KAZ", "rank": 6, "age": 26, "grand_slams": 1, "wimbledon_titles": 1,
        "win_rate_2025": 74, "grass_win_rate": 82, "serve_speed_kmh": 192, "aces_per_match": 6.1,
        "first_serve_pct": 63, "style": "Serve and volley power", "odds_to_win": 30,
    },
    "Coco Gauff": {
        "country": "USA", "rank": 3, "age": 21, "grand_slams": 1, "wimbledon_titles": 0,
        "win_rate_2025": 76, "grass_win_rate": 70, "serve_speed_kmh": 182, "aces_per_match": 3.8,
        "first_serve_pct": 66, "style": "Athletic all-court defensive game", "odds_to_win": 18,
    },
}

def get_llm():
    key = os.getenv("GROQ_API_KEY")
    if not key:
        return None
    return ChatGroq(
        groq_api_key=key,
        model_name="llama-3.3-70b-versatile",
        temperature=0.4,
    )

def generate_match_preview(p1: str, p2: str, tour: str) -> str:
    llm = get_llm()
    if not llm:
        return "Configure GROQ_API_KEY within environment variables to populate data."
    players_dict = PLAYERS if tour == "Men's" else WOMEN_PLAYERS
    d1, d2 = players_dict[p1], players_dict[p2]
    prompt = f"""You are an elite tennis performance analyst for BBC Sport covering The Championships.
Write a precise, strategic 150-word pre-match brief for the 2025 Championship draw:

{p1} vs {p2}

Statistical Parameters:
- {p1}: {d1['grass_win_rate']}% grass efficiency, technical style: {d1['style']}
- {p2}: {d2['grass_win_rate']}% grass efficiency, technical style: {d2['style']}

Maintain a neutral, highly professional, broadcast-ready tone. Conclude with a clear strategic winning projection."""
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        return response.content
    except Exception as e:
        return f"Analytical compilation failure: {str(e)}"

def generate_tournament_prediction(tour: str) -> str:
    llm = get_llm()
    if not llm:
        return "Configure GROQ_API_KEY within environment variables to populate data."
    player_list = "\n".join([
        f"- {name}: Rank #{d['rank']}, Grass Win Pct: {d['grass_win_rate']}%, Style: {d['style']}"
        for name, d in (PLAYERS if tour == "Men's" else WOMEN_PLAYERS).items()
    ])
    prompt = f"""You are a professional predictive sports data scientist forecasting the 2025 Wimbledon Draw.
Evaluate the field strengths using these technical parameters:
{player_list}

Structure the output strictly using these parameters:
Expected Winner: [Name]
Expected Runner-up: [Name]
Analytical Justification: [Provide technical rationale under 100 words]"""
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        return response.content
    except Exception as e:
        return f"Analytical compilation failure: {str(e)}"

# ── App Header ──────────────────────────────────────────────────
st.title("The Championships, Wimbledon 2025")
st.markdown("##### Advanced Performance Architecture · Bilateral Modeling · Predictive Analytics")
st.markdown("<p class='framework-subtitle'>Enterprise Inference Engine Integration Framework</p>", unsafe_allow_html=True)
st.markdown("---")

# ── Bracket Focus Selector ───────────────────────────────────────
tour = st.radio(
    "Isolate Bracket Focus",
    ["Men's", "Women's"],
    horizontal=True,
    label_visibility="collapsed",
)
current_players = PLAYERS if tour == "Men's" else WOMEN_PLAYERS

# ── Navigation Architecture ──────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "Profile Distributions",
    "Head-to-Head Matrix",
    "Match Play Projections",
    "Draw Probability Models",
])

# ── TAB 1: Profile Distributions ─────────────────────────────────
with tab1:
    st.subheader("Contender Performance Architecture")
    cols = st.columns(len(current_players))
    for i, (name, data) in enumerate(current_players.items()):
        with cols[i]:
            st.markdown(f"""
            <div class="profile-card">
                <div class="player-name">{name}</div>
                <div class="player-meta">{data['country']} · RANK {data['rank']}</div>
                <div class="metric-value">{data['win_rate_2025']}%</div>
                <div class="metric-label">2025 Season Efficiency</div>
                <div class="data-grid">
                    <div class="data-item">Grass Win: <strong>{data['grass_win_rate']}%</strong></div>
                    <div class="data-item">SW19 Titles: <strong>{data['wimbledon_titles']}</strong></div>
                    <div class="data-item">Majors: <strong>{data['grand_slams']}</strong></div>
                    <div class="data-item">Aces/Match: <strong>{data['aces_per_match']}</strong></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Data Parameter Segmentation")
    metric = st.selectbox(
        "Select Isolation Parameter:",
        ["grass_win_rate", "win_rate_2025", "grand_slams",
         "wimbledon_titles", "aces_per_match", "first_serve_pct"],
        format_func=lambda x: x.replace("_", " ").title()
    )
    df = pd.DataFrame([
        {"Player": name, "Value": data[metric]}
        for name, data in current_players.items()
    ]).sort_values("Value", ascending=True)

    fig = px.bar(
        df, x="Value", y="Player", orientation="h",
        color="Value",
        color_continuous_scale=["#E2E0D8", "#006633"], 
        title=f"Field Weighting: {metric.replace('_', ' ').title()}",
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False,
        height=260,
    )
    st.plotly_chart(fig, use_container_width=True)

# ── TAB 2: Head-to-Head Matrix ──────────────────────────────────
with tab2:
    st.subheader("Bilateral Technical Mapping")
    player_names = list(current_players.keys())
    c1, c2 = st.columns(2)
    with c1:
        p1 = st.selectbox("Baseline Profile:", player_names, index=0)
    with c2:
        p2 = st.selectbox("Target Benchmark Profile:", player_names, index=1)

    if p1 == p2:
        st.warning("Please isolate two unique profiles to compare structural output.")
    else:
        d1, d2 = current_players[p1], current_players[p2]

        metrics = [
            ("Current World Ranking", f"#{d1['rank']}", f"#{d2['rank']}", d1['rank'] < d2['rank']),
            ("Biometric Age Profile", str(d1['age']), str(d2['age']), d1['age'] < d2['age']),
            ("Historic Major Titles", str(d1['grand_slams']), str(d2['grand_slams']), d1['grand_slams'] > d2['grand_slams']),
            ("Wimbledon Championship Crowns", str(d1['wimbledon_titles']), str(d2['wimbledon_titles']), d1['wimbledon_titles'] > d2['wimbledon_titles']),
            ("2025 Tour Win Efficiency", f"{d1['win_rate_2025']}%", f"{d2['win_rate_2025']}%", d1['win_rate_2025'] > d2['win_rate_2025']),
            ("Surface Specific Grass Rating", f"{d1['grass_win_rate']}%", f"{d2['grass_win_rate']}%", d1['grass_win_rate'] > d2['grass_win_rate']),
            ("Mean First Serve Velocity (km/h)", f"{d1['serve_speed_kmh']}", f"{d2['serve_speed_kmh']}", d1['serve_speed_kmh'] > d2['serve_speed_kmh']),
            ("Calculated Ace Delivery Ratio", str(d1['aces_per_match']), str(d2['aces_per_match']), d1['aces_per_match'] > d2['aces_per_match']),
            ("First Serve In-Play Conversion", f"{d1['first_serve_pct']}%", f"{d2['first_serve_pct']}%", d1['first_serve_pct'] > d2['first_serve_pct']),
        ]

        table_body = ""
        for m in metrics:
            bg_p1 = "rgba(0, 102, 51, 0.15)" if m[3] else "transparent"
            bg_p2 = "rgba(0, 102, 51, 0.15)" if not m[3] else "transparent"
            color_p1 = "#006633" if m[3] else "var(--text-color)"
            color_p2 = "#006633" if not m[3] else "var(--text-color)"
            
            table_body += f"""<tr>
                <td class='h2h-dim-cell'>{m[0]}</td>
                <td class='h2h-stat-cell' style='background-color: {bg_p1}; color: {color_p1};'>{m[1]}</td>
                <td class='h2h-stat-cell' style='background-color: {bg_p2}; color: {color_p2};'>{m[2]}</td>
            </tr>"""

        table_html = f"""
        <table class='h2h-table'>
            <thead>
                <tr>
                    <th style='text-align: left;'>Analytical Dimension</th>
                    <th style='text-align: center;'>{p1}</th>
                    <th style='text-align: center;'>{p2}</th>
                </tr>
            </thead>
            <tbody>
                {table_body}
            </tbody>
        </table>
        """
        
        st.markdown(table_html, unsafe_allow_html=True)

        st.markdown("---")
        categories = ["Grass Win %", "2025 Win %", "Grand Slams", "Wimbledon Titles", "Serve Speed", "First Serve %"]

        def norm(val, mn, mx):
            return round((val - mn) / max(mx - mn, 1) * 100, 1)

        v1 = [d1['grass_win_rate'], d1['win_rate_2025'], norm(d1['grand_slams'], 0, 24), norm(d1['wimbledon_titles'], 0, 7), norm(d1['serve_speed_kmh'], 180, 230), d1['first_serve_pct']]
        v2 = [d2['grass_win_rate'], d2['win_rate_2025'], norm(d2['grand_slams'], 0, 24), norm(d2['wimbledon_titles'], 0, 7), norm(d2['serve_speed_kmh'], 180, 230), d2['first_serve_pct']]

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=v1 + [v1[0]], theta=categories + [categories[0]], fill='toself', name=p1, line_color='#006633', fillcolor='rgba(0,102,51,0.08)'))
        fig.add_trace(go.Scatterpolar(r=v2 + [v2[0]], theta=categories + [categories[0]], fill='toself', name=p2, line_color='#6B7A72', fillcolor='rgba(107,122,114,0.08)'))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True, 
                    range=[0, 100], 
                    tickfont=dict(family="Roboto Mono")
                ),
                angularaxis=dict(
                    tickfont=dict(family="Inter")
                ),
                bgcolor="rgba(0,0,0,0)",
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            title="Biometric Index Radial Dispersion",
            height=380,
        )
        st.plotly_chart(fig, use_container_width=True)

# ── TAB 3: Match Play Projections ───────────────────────────────
with tab3:
    st.subheader("Predictive Text Narrative Engine")
    st.caption("Transforms structured core stats into situational tactical intelligence briefings.")

    player_names = list(current_players.keys())
    mc1, mc2 = st.columns(2)
    with mc1:
        mp1 = st.selectbox("Isolate Profile Alpha:", player_names, index=0, key="mp1")
    with mc2:
        mp2 = st.selectbox("Isolate Profile Beta:", player_names, index=1, key="mp2")

    if st.button("Execute Technical Match Interpretation", type="secondary"):
        if mp1 == mp2:
            st.error("Select two discrete profiles to test cross-distribution arrays.")
        else:
            with st.spinner("Compiling tactical performance briefing..."):
                preview = generate_match_preview(mp1, mp2, tour)
            st.markdown("---")
            st.markdown(f"""
            <div class="analysis-box">
                {preview}
            </div>
            """, unsafe_allow_html=True)

# ── TAB 4: Draw Probability Models ──────────────────────────────
with tab4:
    st.subheader("Tournament Distribution Probability Models")
    st.caption("Aggregates historic 2025 performance coefficients to yield future surface trajectory boundaries.")

    if st.button("Generate Bracket Success Horizon Models", type="secondary"):
        with st.spinner("Processing deep database array variables..."):
            prediction = generate_tournament_prediction(tour)
        st.markdown("---")
        st.markdown(f"""
        <div class="analysis-box" style="border-left-color: #006633;">
            {prediction}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("Calculated Bracket Power Index Coefficient")
        odds_df = pd.DataFrame([
            {"Player": name, "Index": data["odds_to_win"]}
            for name, data in current_players.items()
        ]).sort_values("Index", ascending=False)

        fig = px.bar(
            odds_df, x="Player", y="Index",
            color="Index",
            color_continuous_scale=["#E2E0D8", "#006633"],
            title="Aggregated Target Variable Weighting Coefficients",
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            coloraxis_showscale=False,
            yaxis_title="Probability Density Over Time",
        )
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.caption("Data Platform Model Systems Framework Architecture Description Log")