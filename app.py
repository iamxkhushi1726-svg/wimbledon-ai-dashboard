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

# ── Theme Toggle State Engine ───────────────────────────────────
with st.sidebar:
    st.markdown("### Platform Controls")
    theme_selection = st.radio(
        "Application Interface Theme",
        ["Luxury Light", "Premium Dark"],
        index=0
    )

# Dynamic Variable Mappings based on Selector State
if theme_selection == "Luxury Light":
    bg_app = "#FDFDFB"
    bg_card = "#F5F4F0"
    border_card = "#E2E0D8"
    text_main = "#1A2421"
    text_muted = "#5C6A62"
    plotly_template = "plotly_white"
    
    # Premium Light H2H Table Variables
    h2h_winner_bg = "rgba(0, 102, 51, 0.08)"
    h2h_winner_text = "#006633"
    h2h_loser_bg = "transparent"
    h2h_loser_text = "#1A2421"
    table_header_bg = "#1A2421"
    table_header_text = "#FDFDFB"
else:
    bg_app = "#0A0E0C"
    bg_card = "#121815"
    border_card = "#1F2925"
    text_main = "#F8FAFC"
    text_muted = "#8CA396"
    plotly_template = "plotly_dark"
    
    # Premium Dark H2H Table Variables
    h2h_winner_bg = "rgba(0, 102, 51, 0.2)"
    h2h_winner_text = "#10B981"
    h2h_loser_bg = "transparent"
    h2h_loser_text = "#8CA396"
    table_header_bg = "#121815"
    table_header_text = "#F8FAFC"

# ── Typography & Dynamic Theme Responsive Style Injection ───────
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;1,400&family=EB+Garamond:ital,wght@0,400;0,600;0,700;1,400&family=Inter:wght@400;500;600&family=Roboto+Mono:wght@400;500&display=swap');
    
    .stApp {{
        background-color: {bg_app} !important;
        color: {text_main} !important;
    }}
    
    h1, .championship-title {{
        font-family: 'Playfair Display', Georgia, serif !important;
        font-weight: 700 !important;
        color: {text_main} !important;
        letter-spacing: -0.01em !important;
    }}
    
    h2, h3, h4, h5, h6, .metric-label, .player-name, .framework-subtitle, div[data-testid="stMarkdownContainer"] p {{
        font-family: 'EB Garamond', Georgia, serif !important;
        color: {text_main} !important;
    }}
    
    h2, h3, h4, h5, h6 {{
        font-weight: 600 !important;
        letter-spacing: 0.01em !important;
    }}
    
    .profile-card {{
        background-color: {bg_card};
        border: 1px solid {border_card};
        border-top: 4px solid #006633; 
        padding: 24px;
        border-radius: 4px;
        text-align: left;
        margin-bottom: 16px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }}
    
    .player-name {{
        font-size: 26px;
        font-weight: 700;
        margin-bottom: 2px;
    }}
    
    .player-meta {{
        font-family: 'Inter', sans-serif !important;
        font-size: 11px;
        color: {text_muted};
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 600;
        margin-bottom: 18px;
    }}
    
    .metric-value {{
        font-family: 'Roboto Mono', monospace;
        font-size: 30px;
        font-weight: 500;
        color: #006633;
        margin-bottom: 2px;
    }}
    
    .data-grid {{
        margin-top: 18px;
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
        border-top: 1px solid {border_card};
        padding-top: 14px;
    }}
    
    .data-item {{
        color: {text_muted};
        font-size: 14px;
    }}
    
    .data-item strong {{
        color: {text_main};
        font-family: 'Roboto Mono', monospace;
    }}
    
    .analysis-box {{
        background-color: {bg_card};
        border-left: 4px solid #006633;
        padding: 24px;
        border-radius: 4px;
        color: {text_main};
        font-size: 16px;
        line-height: 1.65;
        font-family: 'EB Garamond', Georgia, serif;
    }}

    div[data-testid="stTabs"] button {{
        font-family: 'EB Garamond', Georgia, serif !important;
        font-size: 18px !important;
        color: {text_muted} !important;
    }}
    div[data-testid="stTabs"] button[aria-selected="true"] {{
        color: #006633 !important;
        border-bottom-color: #006633 !important;
        font-weight: bold !important;
    }}
    div[data-testid="stTabs"] button:hover {{
        color: {text_main} !important;
    }}

    div[data-testid="stRadio"] label, div[data-baseweb="select"] * {{
        font-family: 'Inter', sans-serif !important;
        color: {text_main} !important;
    }}
    div[data-testid="stRadio"] label {{
        font-size: 14px !important;
    }}
    div[data-baseweb="radio"] div[aria-checked="true"] > div {{
        background-color: #006633 !important;
    }}
    div[data-baseweb="radio"] div[aria-checked="true"] {{
        border-color: #006633 !important;
    }}

    div.stButton > button:first-child {{
        background-color: #006633 !important;
        color: #FFFFFF !important;
        border: 1px solid #006633 !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        border-radius: 4px !important;
        padding: 8px 20px !important;
    }}
    div.stButton > button:first-child:hover {{
        background-color: #004D26 !important;
        border-color: #004D26 !important;
    }}

    /* Elegant Editorial Matrix Borders & Alignment */
    .h2h-table {{
        width: 100%;
        border-collapse: collapse;
        font-family: 'Inter', sans-serif;
        margin-top: 10px;
    }}
    .h2h-table th {{
        padding: 16px 20px;
        background-color: {table_header_bg};
        color: {table_header_text};
        font-family: 'EB Garamond', Georgia, serif;
        font-size: 18px;
        font-weight: 600;
        letter-spacing: 0.01em;
        border: none;
    }}
    .h2h-table td {{
        padding: 14px 20px;
        font-size: 14px;
        vertical-align: middle;
        border-bottom: 1px solid {border_card};
    }}
    .h2h-dim-cell {{
        font-family: 'EB Garamond', Georgia, serif;
        font-weight: 600;
        font-size: 16px !important;
        color: {text_main};
        width: 40%;
    }}
    .h2h-stat-cell {{
        font-family: 'Roboto Mono', monospace;
        font-size: 14px;
        font-weight: 500;
        text-align: center;
        width: 30%;
    }}
</style>
""", unsafe_allow_html=True)

# ── 2025 Player Matrices ────────────────────────────────────────
PLAYERS = {
    "Novak Djokovic": {
        "country": "SRB",
        "rank": 2,
        "age": 38,
        "grand_slams": 24,
        "wimbledon_titles": 7,
        "win_rate_2025": 78,
        "grass_win_rate": 85,
        "serve_speed_kmh": 215,
        "aces_per_match": 9.2,
        "first_serve_pct": 63,
        "style": "All-court baseline master",
        "strength": "Return depth, mental resilience",
        "weakness": "Age-related fatigue in deep 5-setters",
        "odds_to_win": 18,
    },
    "Carlos Alcaraz": {
        "country": "ESP",
        "rank": 3,
        "age": 22,
        "grand_slams": 4,
        "wimbledon_titles": 2,
        "win_rate_2025": 82,
        "grass_win_rate": 80,
        "serve_speed_kmh": 220,
        "aces_per_match": 8.1,
        "first_serve_pct": 65,
        "style": "Aggressive all-court attacking",
        "strength": "Drop shot variation, linear athleticism",
        "weakness": "Unforced error inconsistency under pressure",
        "odds_to_win": 22,
    },
    "Jannik Sinner": {
        "country": "ITA",
        "rank": 1,
        "age": 23,
        "grand_slams": 3,
        "wimbledon_titles": 0,
        "win_rate_2025": 86,
        "grass_win_rate": 72,
        "serve_speed_kmh": 218,
        "aces_per_match": 7.8,
        "first_serve_pct": 67,
        "style": "Powerful baseline grinder",
        "strength": "Groundstroke depth, topspin consistency",
        "weakness": "Lateral transition limits on grass",
        "odds_to_win": 25,
    },
    "Daniil Medvedev": {
        "country": "RUM",
        "rank": 4,
        "age": 29,
        "grand_slams": 1,
        "wimbledon_titles": 0,
        "win_rate_2025": 74,
        "grass_win_rate": 68,
        "serve_speed_kmh": 210,
        "aces_per_match": 10.1,
        "first_serve_pct": 62,
        "style": "Unorthodox defensive counter-puncher",
        "strength": "First serve velocity, deep baseline coverage",
        "weakness": "Low-bounce mechanical movement issues",
        "odds_to_win": 12,
    },
}

WOMEN_PLAYERS = {
    "Iga Swiatek": {
        "country": "POL",
        "rank": 1,
        "age": 24,
        "grand_slams": 5,
        "wimbledon_titles": 0,
        "win_rate_2025": 88,
        "grass_win_rate": 70,
        "serve_speed_kmh": 185,
        "aces_per_match": 3.2,
        "first_serve_pct": 65,
        "style": "Topspin baseline dominance",
        "strength": "Forehand heavy rotation, lateral speed",
        "weakness": "Low slice variations on fast grass",
        "odds_to_win": 20,
    },
    "Aryna Sabalenka": {
        "country": "BLR",
        "rank": 2,
        "age": 27,
        "grand_slams": 3,
        "wimbledon_titles": 0,
        "win_rate_2025": 80,
        "grass_win_rate": 75,
        "serve_speed_kmh": 195,
        "aces_per_match": 5.8,
        "first_serve_pct": 62,
        "style": "Powerful aggressive baseline",
        "strength": "Serve execution, flat groundstroke power",
        "weakness": "Double fault lapses during critical breaks",
        "odds_to_win": 25,
    },
    "Elena Rybakina": {
        "country": "KAZ",
        "rank": 6,
        "age": 26,
        "grand_slams": 1,
        "wimbledon_titles": 1,
        "win_rate_2025": 74,
        "grass_win_rate": 82,
        "serve_speed_kmh": 192,
        "aces_per_match": 6.1,
        "first_serve_pct": 63,
        "style": "Serve and volley power",
        "strength": "Flat baseline depth, quiet composure",
        "weakness": "Physical strain in extended point durations",
        "odds_to_win": 30,
    },
    "Coco Gauff": {
        "country": "USA",
        "rank": 3,
        "age": 21,
        "grand_slams": 1,
        "wimbledon_titles": 0,
        "win_rate_2025": 76,
        "grass_win_rate": 70,
        "serve_speed_kmh": 182,
        "aces_per_match": 3.8,
        "first_serve_pct": 66,
        "style": "Athletic all-court defensive game",
        "strength": "Backhand drive, fast perimeter defense",
        "weakness": "Forehand wing structural errors under pressure",
        "odds_to_win": 18,
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
        color_continuous_scale=["#E2E0D8" if theme_selection == "Luxury Light" else "#1A2420", "#006633", "#1A2421"], 
        title=f"Field Weighting: {metric.replace('_', ' ').title()}",
        template=plotly_template,
    )
    fig.update_layout(
        paper_bgcolor=bg_app,
        plot_bgcolor=bg_app,
        coloraxis_showscale=False,
        font=dict(family="Inter", color=text_main),
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

        # FIXED & CLEANED: Compiled rows seamlessly into an absolute continuous HTML string block
        # to ensure that Streamlit processes it natively without falling back to pre-formatted text mode.
        table_body = ""
        for m in metrics:
            bg_p1 = h2h_winner_bg if m[3] else h2h_loser_bg
            bg_p2 = h2h_winner_bg if not m[3] else h2h_loser_bg
            color_p1 = h2h_winner_text if m[3] else h2h_loser_text
            color_p2 = h2h_winner_text if not m[3] else h2h_loser_text
            
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
        fig.add_trace(go.Scatterpolar(r=v1 + [v1[0]], theta=categories + [categories[0]], fill='toself', name=p1, line_color='#006633', fillcolor='rgba(0,102,51,0.04)'))
        fig.add_trace(go.Scatterpolar(r=v2 + [v2[0]], theta=categories + [categories[0]], fill='toself', name=p2, line_color='#6B7A72', fillcolor='rgba(107,122,114,0.04)'))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True, 
                    range=[0, 100], 
                    gridcolor=border_card, 
                    color=text_muted,
                    tickfont=dict(family="Roboto Mono")
                ),
                angularaxis=dict(
                    gridcolor=border_card, 
                    color=text_muted,
                    tickfont=dict(family="Inter")
                ),
                bgcolor=bg_app,
            ),
            paper_bgcolor=bg_app,
            font=dict(color=text_main, family="Inter"),
            legend=dict(bgcolor=bg_card, bordercolor=border_card),
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
            color_continuous_scale=["#E2E0D8" if theme_selection == "Luxury Light" else "#1A2420", "#006633", "#1A2421"],
            title="Aggregated Target Variable Weighting Coefficients",
            template=plotly_template,
        )
        fig.update_layout(
            paper_bgcolor=bg_app,
            plot_bgcolor=bg_app,
            coloraxis_showscale=False,
            font=dict(family="Inter", color=text_main),
            yaxis_title="Probability Density Over Time",
        )
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.caption(
    "Data Platform Model Systems Framework Architecture Description Log"
)