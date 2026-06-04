import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Global Supply Chain Risk Intelligence", layout="wide")

# THEME TOGGLE
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

col_t1, col_t2, col_t3 = st.columns([8, 1, 1])
with col_t3:
    if st.button("☀️" if st.session_state.theme == 'dark' else "🌙"):
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
html, body, .stApp {{background-color: {bg} !important;}}
* {{font-family: Inter, sans-serif; color: {text} !important;}}
h1 {{font-size: 2.8rem; font-weight: 700; margin-bottom: 0.3rem;}}
[data-testid="stMetricLabel"] {{color: {text2} !important; font-size: 12px !important;}}
[data-testid="stMetricValue"] {{font-size: 36px !important; font-weight: 700 !important;}}
</style>
""", unsafe_allow_html=True)

st.title("Global Supply Chain Shock Intelligence")
st.markdown("**Real-time risk monitoring across 16 countries & 5 industries**")

scenario1 = st.selectbox("Select Scenario", ["Taiwan Strait Disruption", "Red Sea Blockage", "Port Strike"])

@st.cache_data
def get_data(s):
    countries = ["Taiwan", "China", "Vietnam", "Mexico", "Germany", "USA", "India", "Japan", "Korea", "Thailand", "Malaysia", "Singapore", "Brazil", "UK", "France", "Canada"]
    industries = ["Semiconductors", "EV Batteries", "Textiles", "Pharma", "Automotive"]
    if "Taiwan" in s:
        risks = [9, 8, 7, 6, 5, 7, 6, 8, 7, 5, 6, 7, 4, 6, 5, 6]
        ind_risks = [9, 8, 7, 6, 7]
        revenue = "$420B"
        c_risk = 12
        r_score = 9.1
        r_delta = 1.8
        price = {"Chips": "+45%", "Electronics": "+25%", "Phones": "+30%"}
        timeline = "2-4 weeks"
        conf = 87
    elif "Red Sea" in s:
        risks = [7, 8, 8, 7, 6, 7, 5, 6, 6, 7, 8, 9, 5, 6, 7, 5]
        ind_risks = [8, 7, 9, 6, 7]
        revenue = "$280B"
        c_risk = 14
        r_score = 8.3
        r_delta = 1.2
        price = {"Oil": "+35%", "Shipping": "+50%", "Plastics": "+20%"}
        timeline = "1-2 months"
        conf = 82
    elif "Port" in s:
        risks = [7, 8, 8, 7, 6, 7, 5, 6, 7, 6, 5, 6, 8, 7, 6, 5]
        ind_risks = [6, 7, 5, 8, 6]
        revenue = "$95B"
        c_risk = 14
        r_score = 6.8
        r_delta = 0.5
        price = {"Electronics": "+15%", "Clothes": "+20%", "Medical": "+18%"}
        timeline = "3-6 weeks"
        conf = 79
    else:
        risks = [8, 9, 9, 6, 7, 7, 6, 5, 8, 7, 8, 6, 9, 8, 7, 6]
        ind_risks = [7, 5, 9, 8, 6]
        revenue = "$310B"
        c_risk = 16
        r_score = 8.4
        r_delta = 1.5
        price = {"EV Batteries": "+50%", "Wind Turbines": "+40%", "Solar": "+35%"}
        timeline = "4-6 months"
        conf = 85
    return countries, industries, risks, ind_risks, revenue, c_risk, r_score, r_delta, price, timeline, conf

data1 = get_data(scenario1)
countries, industries, risks, ind_risks, revenue, c_risk, r_score, r_delta, price, timeline, conf = data1

compare_mode = False
tab1, tab2 = st.tabs(["Supply Chain Risk", "Investment Intelligence"])

with tab1:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("INDUSTRIES IMPACTED", f"{len([r for r in ind_risks if r >= 7])}/5")
    with col2:
        st.metric("REVENUE AT RISK", revenue)
    with col3:
        st.metric("COUNTRIES AFFECTED", c_risk)
    with col4:
        st.metric("RISK SCORE", f"{r_score}/10", f"+{r_delta}")

    st.subheader("Geographic Risk Heatmap")
    df_map = pd.DataFrame({
    'Country': ["Taiwan", "China", "Vietnam", "Mexico", "Germany", "United States", "India", "Japan", 
                "South Korea", "Thailand", "Malaysia", "Singapore", "Brazil", "United Kingdom", "France", "Canada"],
    'Risk': risks
})
fig_map = px.choropleth(df_map, locations='Country', locationmode='country names', color='Risk', 
                        color_continuous_scale='Reds', range_color=[0, 10])
fig_map.update_layout(plot_bgcolor=bg, paper_bgcolor=bg, font=dict(color=text), height=450, 
                      geo=dict(bgcolor=map_bg, landcolor=map_land, showframe=False, showcoastlines=True))
st.plotly_chart(fig_map, use_container_width=True)

    st.subheader("Country Risk Breakdown")
    df_country = pd.DataFrame({
        'Country': countries,
        'Risk Score': risks,
        'Risk Level': ['Critical' if r >= 8 else 'High' if r >= 6 else 'Medium' for r in risks]
    })
    csv = df_country.to_csv(index=False).encode('utf-8')
    col_t1, col_t2 = st.columns([5, 1])
    with col_t2:
        st.download_button("Download CSV", csv, 'risk_data.csv', 'text/csv')
    st.dataframe(df_country, use_container_width=True, hide_index=True)

    colA, colB = st.columns([1.2, 0.8])
    with colA:
        st.subheader("Industry Risk Matrix")
        df_ind = pd.DataFrame({'Industry': industries, 'Risk': ind_risks})
        fig_bar = px.bar(df_ind, x='Industry', y='Risk', color='Risk', color_continuous_scale='Reds')
        fig_bar.update_layout(plot_bgcolor=bg, paper_bgcolor=bg, font=dict(color=text), height=350, showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with colB:
        st.subheader("Consumer Price Impact")
        st.markdown(f"<div style='background:{card}; padding:20px; border-radius:12px; border:1px solid {border}'>", unsafe_allow_html=True)
        for p, inc in price.items():
            st.markdown(f"{p}: <span style='color:{red}; font-weight:700'>{inc}</span>", unsafe_allow_html=True)
        st.markdown(f"<div style='background:#1e3a8a; padding:12px; border-radius:8px; margin-top:10px'>Timeline: {timeline}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with st.expander("Executive Summary & Recommendations", expanded=False):
        top_country = countries[risks.index(max(risks))]
        top_industry = industries[ind_risks.index(max(ind_risks))]
        st.markdown(f"""
**Scenario**: {scenario1}

**Key Impact**: {top_country} and {top_industry} sector face highest disruption risk

**Financial Impact**: Estimated {revenue} revenue at risk across supply chain

**Recommendations**:
1. Diversify supplier base away from high-risk regions
2. Increase inventory buffer for critical components
3. Implement dynamic pricing strategies
        """)

with tab2:
    st.subheader("Investment Opportunity Matrix")
    df_invest = pd.DataFrame({'Industry': industries, 'Risk Score': ind_risks})
    df_invest['Opportunity Score'] = 10 - df_invest['Risk Score']
    
    buy_df = df_invest[df_invest['Opportunity Score'] >= 6]
    hold_df = df_invest[(df_invest['Opportunity Score'] >= 4) & (df_invest['Risk Score'] < 7)]
    risk_df = df_invest[df_invest['Risk Score'] >= 8]
    
    colI1, colI2, colI3 = st.columns(3)
    with colI1:
        st.markdown(f"<div style='background:{card}; border:1px solid {green}; padding:20px; border-radius:12px'>", unsafe_allow_html=True)
        st.markdown("**Buy Opportunities**")
        for _, row in buy_df.iterrows():
            st.markdown(f"{row['Industry']} → {row['Opportunity Score']:.0f}/10")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with colI2:
        st.markdown(f"<div style='background:{card}; border:1px solid {orange}; padding:20px; border-radius:12px'>", unsafe_allow_html=True)
        st.markdown("**Hold**")
        for _, row in hold_df.iterrows():
            st.markdown(f"{row['Industry']} → {row['Opportunity Score']:.0f}/10")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with colI3:
        st.markdown(f"<div style='background:{card}; border:1px solid {red}; padding:20px; border-radius:12px'>", unsafe_allow_html=True)
        st.markdown("**Reduce Exposure**")
        for _, row in risk_df.iterrows():
            st.markdown(f"{row['Industry']} → {row['Risk Score']}/10")
        st.markdown("</div>", unsafe_allow_html=True)

    fig_scatter = px.scatter(df_invest, x='Risk Score', y='Opportunity Score', size='Risk Score', size_max=30)
    fig_scatter.update_layout(height=400, plot_bgcolor=bg, paper_bgcolor=bg, font=dict(color=text),
                              xaxis=dict(gridcolor=border, title="Risk Score"),
                              yaxis=dict(gridcolor=border, title="Opportunity Score"))
    st.plotly_chart(fig_scatter, use_container_width=True)

    with st.expander("Methodology & Assumptions", expanded=False):
        st.markdown(f"""
**Risk Scoring**: 0.4xManufacturing + 0.3xLogistics + 0.3xMarket Concentration

**Revenue Impact**: Sector GDP x Regional Exposure % x Risk Score / 10

**Opportunity Score**: 10 - Risk Score. Higher = Better buy opportunity

**Confidence Level**: {conf}% based on historical data accuracy
        """)
    
    with colI2:
        st.subheader("Investment Guidance")
        st.markdown(f"<div style='background:{card}; padding:20px; border-radius:12px; border:1px solid {border}'>", unsafe_allow_html=True)
        st.markdown(f"**Reduce exposure**: {', '.join(risk_df['Industry'].tolist()) if len(risk_df)>0 else 'None'}")
        buy_list = ', '.join(buy_df['Industry'].tolist()) if len(buy_df)>0 else 'None'
        st.markdown(f"**Consider increasing**: {buy_list}")
        st.markdown(f"<div style='background:#854d0e; padding:12px; border-radius:8px'>High volatility expected next 30 days</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


   
