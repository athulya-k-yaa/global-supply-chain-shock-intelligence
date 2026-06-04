import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Global Supply Chain Risk Intelligence", page_icon="🌍", layout="wide", initial_sidebar_state="collapsed")

# THEME TOGGLE - FIXED ICONS
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

col_t1, col_t2, col_t3 = st.columns([8, 1, 1])
with col_t3:
    if st.button("🌙" if st.session_state.theme == 'dark' else "☀️"):
        st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
        st.rerun()

# COLORS
if st.session_state.theme == 'dark':
    bg = '#0a0a0a'
    card = '#141414'
    text = '#ffffff'
    text2 = '#a0a0a0'
    border = '#2a2a2a'
    map_land = '#1e3a8a'
    map_bg = '#000'
else:
    bg = '#f8fafc'
    card = '#ffffff'
    text = '#0f172a'
    text2 = '#64748b'
    border = '#e2e8f0'
    map_land = '#e2e8f0'
    map_bg = '#f8fafc'

red = '#ff4444'
green = '#22c55e'
orange = '#f97316'

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, .stApp {{background-color: {bg}!important;}}
* {{font-family: Inter, sans-serif; color: {text}!important;}}
h1 {{font-size: 2.8rem; font-weight: 700; margin-bottom: 0.3rem;}}
.subtitle {{color: {text2}; font-size: 1.1rem; margin-bottom: 2rem;}}
div[data-testid="metric-container"] {{background: transparent; border: none; padding: 0; margin-bottom: 40px;}}
[data-testid="stMetricLabel"] {{color: {text2}!important; font-size: 12px!important; text-transform: uppercase; letter-spacing: 0.1em; font-weight: 500;}}
[data-testid="stMetricValue"] {{font-size: 36px!important; font-weight: 700; color: {text}!important;}}
</style>
""", unsafe_allow_html=True)

st.markdown('<h1>Global Supply Chain Risk Intelligence</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Impact Analysis for Businesses, Consumers & Investors</p>', unsafe_allow_html=True)

# SCENARIO + COMPARE MODE
col_s1, col_s2 = st.columns([4, 1])
with col_s1:
    scenario1 = st.selectbox("Select Shock Scenario", 
        ["Semiconductor Shock - Taiwan 40%", "Oil Shock - Middle East +35%", "Port Closure - Shipping Crisis", "China Rare Earth Restriction"],
        key="scenario1")
with col_s2:
    compare_mode = st.toggle("Compare Mode", key="compare_toggle")

scenario2 = None
if compare_mode:
    scenario2 = st.selectbox("Compare with", 
        ["Oil Shock - Middle East +35%", "Semiconductor Shock - Taiwan 40%", "Port Closure - Shipping Crisis", "China Rare Earth Restriction"],
        index=0, key="scenario2")

def get_data(s):
    countries = ['Taiwan','China','USA','Germany','India','Japan','Vietnam','Mexico']
    industries = ['Electronics','Automotive','Pharma','Textile','Banking']
    if "Semiconductor" in s:
        risks = [9, 10, 7, 6, 5, 8, 4, 5]; ind_risks = [9, 4, 6, 7, 10]
        revenue = "$420B"; c_risk = 18; r_score = 9.1; r_delta = "Critical"
        price = {"Laptops": "+35%", "Smartphones": "+40%", "Cars": "+18%", "Gaming Consoles": "+45%"}
        timeline = "2-4 months"; conf = 87
    elif "Oil" in s:
        risks = [8, 7, 6, 7, 6, 5, 3, 4]; ind_risks = [9, 5, 7, 8, 7]
        revenue = "$180B"; c_risk = 12; r_score = 7.2; r_delta = "High"
        price = {"Petrol": "+35%", "Flights": "+25%", "Plastics": "+20%", "Food": "+12%"}
        timeline = "1-2 months"; conf = 82
    elif "Port" in s:
        risks = [7, 8, 8, 7, 6, 7, 5, 6]; ind_risks = [6, 7, 8, 7, 6]
        revenue = "$95B"; c_risk = 14; r_score = 6.8; r_delta = "High"
        price = {"Electronics": "+15%", "Clothes": "+20%", "Medicines": "+18%", "Toys": "+22%"}
        timeline = "3-6 weeks"; conf = 79
    else:
        risks = [8, 9, 9, 6, 7, 7, 6, 5]; ind_risks = [7, 5, 9, 8, 10]
        revenue = "$310B"; c_risk = 16; r_score = 8.4; r_delta = "Critical"
        price = {"EV Batteries": "+50%", "Wind Turbines": "+40%", "Smartphones": "+25%", "Military Tech": "+35%"}
        timeline = "4-6 months"; conf = 85
    return countries, industries, risks, ind_risks, revenue, c_risk, r_score, r_delta, price, timeline, conf

data1 = get_data(scenario1)
countries, industries, risks, ind_risks, revenue, c_risk, r_score, r_delta, price, timeline, conf = data1

if compare_mode and scenario2:
    data2 = get_data(scenario2)
    countries2, industries2, risks2, ind_risks2, revenue2, c_risk2, r_score2, r_delta2, price2, timeline2, conf2 = data2

tab1, tab2 = st.tabs(["Supply Chain Risk", "Investment Intelligence"])

with tab1:
    # KPIs WITH COMPARISON
    col1, col2, col3, col4 = st.columns(4)

    ind_impact1 = len([r for r in ind_risks if r >= 7])
    ind_impact2 = len([r for r in ind_risks2 if r >= 7]) if compare_mode and scenario2 else 0

    with col1: 
        if compare_mode and scenario2:
            delta = ind_impact2 - ind_impact1
            st.metric("INDUSTRIES IMPACTED", f"{ind_impact1}/5", f"vs {ind_impact2}/5 {delta:+d}")
        else:
            st.metric("INDUSTRIES IMPACTED", f"{ind_impact1}/5", "↑ 0% from baseline", delta_color="off")

    with col2: 
        if compare_mode and scenario2:
            st.metric("REVENUE AT RISK", revenue, f"vs {revenue2}")
        else:
            st.metric("REVENUE AT RISK", revenue)

    with col3: 
        if compare_mode and scenario2:
            delta = c_risk2 - c_risk
            st.metric("COUNTRIES AFFECTED", c_risk, f"vs {c_risk2} {delta:+d}")
        else:
            st.metric("COUNTRIES AFFECTED", c_risk)

    with col4: 
        if compare_mode and scenario2:
            delta_score = r_score2 - r_score
            st.metric("RISK SCORE", f"{r_score}/10", f"vs {r_score2}/10 {delta_score:+.1f}", delta_color="inverse")
        else:
            st.metric("RISK SCORE", f"{r_score}/10", f"↑ {r_delta}", delta_color="inverse")

import plotly.express as px
import pandas as pd

st.subheader("Supply Chain Risk Map")

# Dummy data - same bubbles as your laptop screenshot
df = pd.DataFrame({
    'country': ['USA', 'Canada', 'Mexico', 'Germany', 'France', 'UK', 'China', 'Japan', 'India', 'Brazil'],
    'lat': [37.09, 56.13, 23.63, 51.16, 46.22, 55.37, 35.86, 36.20, 20.59, -14.23],
    'lon': [-95.71, -106.34, -102.55, 10.45, 2.21, -3.43, 104.19, 138.25, 78.96, -51.92],
    'risk_score': [8.5, 6.9, 7.3, 6.8, 6.5, 7.5, 9.1, 8.2, 7.2, 7.9],
    'revenue': [120, 22, 18, 45, 15, 28, 95, 32, 60, 38]
})

fig = px.scatter_geo(df,
                     lat='lat',
                     lon='lon',
                     size='risk_score',
                     color='risk_score',
                     hover_name='country',
                     hover_data=['revenue'],
                     color_continuous_scale="Reds",
                     range_color=[0, 10],
                     projection="natural earth",
                     title="Supply Chain Risk Map")

fig.update_geos(showocean=True, oceancolor="rgb(10,10,30)", showland=True, landcolor="rgb(20,20,20)")
fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0}, height=450, paper_bgcolor="black")
st.plotly_chart(fig, use_container_width=True)


# COUNTRY TABLE
st.subheader("Country Risk Breakdown")
df_country = pd.DataFrame({
'Country': countries,
'Risk Score': risks,
'Risk Level': ['Critical' if r>=9 else 'High' if r>=7 else 'Medium' if r>=5 else 'Low' for r in risks]
})
csv = df_country.to_csv(index=False).encode('utf-8')
col_t1, col_t2 = st.columns([5, 1])
with col_t2: 
     st.download_button("Download CSV", csv, f'risk_data.csv', 'text/csv', use_container_width=True)
st.dataframe(df_country, use_container_width=True, hide_index=True, height=280)

    # INDUSTRY + CONSUMER - NO METHODOLOGY HERE
    colA, colB = st.columns([1.2, 0.8])
    with colA:
        st.subheader("Industry Risk Score")
        df_ind = pd.DataFrame({'Industry': industries, 'Risk': ind_risks})
        fig_bar = px.bar(df_ind, x='Risk', y='Industry', color='Risk', orientation='h',
                         color_continuous_scale='Reds', range_color=[0, 10])
        fig_bar.update_layout(
            height=350,
            yaxis={'categoryorder':'total ascending', 'gridcolor': border},
            plot_bgcolor=bg,
            paper_bgcolor=bg,
            font=dict(color=text, size=12),
            xaxis=dict(gridcolor=border)
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with colB:
        st.subheader("Consumer Price Impact")
        st.markdown(f"<div style='background:{card}; padding:24px; border-radius:8px; border:1px solid {border}; margin-top:28px;'>", unsafe_allow_html=True)
        for p, inc in price.items():
            st.markdown(f"{p}: <span style='color:{red}; font-weight:600'>{inc}</span>", unsafe_allow_html=True)
        st.markdown(f"<div style='background:#1e3a8a; padding:12px; border-radius:6px; margin-top:16px; color:#93c5fd; font-size:13px;'>Timeline: Price changes expected in {timeline}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # EXECUTIVE SUMMARY
    with st.expander("Executive Summary & Recommendations", expanded=True):
        top_country = countries[risks.index(max(risks))]
        top_industry = industries[ind_risks.index(max(ind_risks))]
        st.markdown(f"""
**Scenario**: {scenario1}

**Key Impact**: {top_country} and {top_industry} sector face highest risk at {max(risks)}/10 and {max(ind_risks)}/10 respectively.

**Financial Impact**: Estimated {revenue} revenue at risk across {c_risk} countries.

**Recommendations**:
1. Diversify supplier base away from high-risk regions
2. Increase inventory buffer for critical components
3. Implement dynamic pricing strategies
4. Monitor secondary supplier markets
        """)

with tab2:
    st.subheader("Investment Intelligence")
    st.caption(f"Analysis for: {scenario1}")
    
    df_invest = pd.DataFrame({'Industry': industries, 'Risk Score': ind_risks})
    df_invest['Opportunity Score'] = 10 - df_invest['Risk Score']
    
    buy_df = df_invest[df_invest['Opportunity Score'] >= 6]
    hold_df = df_invest[(df_invest['Opportunity Score'] >= 4) & (df_invest['Opportunity Score'] < 6)]
    risk_df = df_invest[df_invest['Risk Score'] >= 8]

    # 3 CARDS
    colI1, colI2, colI3 = st.columns(3)
    with colI1:
        st.markdown(f"<div style='background:{card}; border:1px solid {green}; padding:20px; border-radius:8px;'>", unsafe_allow_html=True)
        st.markdown("**Buy Opportunities**")
        for _, row in buy_df.iterrows():
            st.markdown(f"{row['Industry']} → {row['Opportunity Score']:.0f}/10")
        st.markdown("</div>", unsafe_allow_html=True)

    with colI2:
        st.markdown(f"<div style='background:{card}; border:1px solid {orange}; padding:20px; border-radius:8px;'>", unsafe_allow_html=True)
        st.markdown("**Hold**")
        for _, row in hold_df.iterrows():
            st.markdown(f"{row['Industry']} → {row['Opportunity Score']:.0f}/10")
        st.markdown("</div>", unsafe_allow_html=True)

    with colI3:
        st.markdown(f"<div style='background:{card}; border:1px solid {red}; padding:20px; border-radius:8px;'>", unsafe_allow_html=True)
        st.markdown("**Avoid - High Risk**")
        for _, row in risk_df.iterrows():
            st.markdown(f"{row['Industry']} → {row['Risk Score']:.0f}/10")
        st.markdown("</div>", unsafe_allow_html=True)

    # RISK VS OPPORTUNITY MATRIX
    colS1, colS2 = st.columns([1.3, 0.7])
    with colS1:
        st.subheader("Risk vs Opportunity Matrix")
        fig_scatter = px.scatter(df_invest, x='Risk Score', y='Opportunity Score', color='Industry', 
                                 size='Risk Score', size_max=30, range_x=[0,10], range_y=[0,10])
        fig_scatter.update_layout(
            height=400,
            plot_bgcolor=bg,
            paper_bgcolor=bg,
            font=dict(color=text),
            xaxis=dict(gridcolor=border, title="Risk Score"),
            yaxis=dict(gridcolor=border, title="Opportunity Score"),
            legend=dict(bgcolor=card, bordercolor=border, borderwidth=1)
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

        # METHODOLOGY & ASSUMPTIONS - MOVED UNDER MATRIX
        with st.expander("Methodology & Assumptions", expanded=False):
            st.markdown(f"""
**Risk Scoring**: 0.4×Manufacturing + 0.3×Logistics + 0.3×Market Concentration | Scale 0-10

**Revenue Impact**: Sector GDP × Regional Exposure % × Risk Score / 10

**Opportunity Score**: 10 - Risk Score. Higher = Better buy opportunity

**Confidence Level**: {conf}% based on historical data accuracy
            """)

    with colS2:
        st.subheader("Investment Guidance")
        st.markdown(f"<div style='background:{card}; padding:20px; border-radius:8px; border:1px solid {border};'>", unsafe_allow_html=True)
        st.markdown(f"**Reduce exposure**: {', '.join(risk_df['Industry'].tolist()) if len(risk_df)>0 else 'None'}")
        buy_list = ', '.join(buy_df['Industry'].tolist()) if len(buy_df)>0 else 'None'
        st.markdown(f"**Consider increasing**: {buy_list}")
        st.markdown(f"<div style='background:#854d0e; padding:12px; border-radius:6px; margin-top:16px; color:#fde047; font-size:13px; font-weight:500;'>For demonstration purposes only. Not financial advice.</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
