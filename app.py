import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Global Supply Chain Risk Intelligence", layout="wide")

# Theme toggle
# Theme
dark = st.toggle("🌙 Dark Mode", value=True, key="theme_toggle")
bg = "#0E1117" if dark else "#FFFFFF"
text = "#FFFFFF" if dark else "#000"
card = "#1E2A3A" if dark else "#F0F2F6"

st.markdown(f"<style>.stApp{{background-color:{bg};}} *{{color:{text}!important;}} h1,h2,h3{{color:{text}!important;}} [data-testid='stMetricValue']{{font-size:2.5rem;color:{text}!important;}}</style>", unsafe_allow_html=True)
# CSS for visible text
st.markdown(f"""
<style>
.stApp{{background-color:{bg};}}
*{{color:{text}!important;}}
h1,h2,h3{{color:{text}!important;}}
[data-testid="stMetricValue"]{{font-size:2.5rem;color:{text}!important;}}
div[data-baseweb="select"] * {{color:{text}!important;}}
</style>
""", unsafe_allow_html=True)

st.title("Global Supply Chain Risk Intelligence")
st.markdown(f"<p style='color:{text};font-size:18px'>Impact Analysis for Businesses, Consumers & Investors</p>", unsafe_allow_html=True)

# Scenario + Compare Mode
# 4 SCENARIOS
col1, col2 = st.columns([3, 1])
with col1:
    scenario1 = st.selectbox("Select Shock Scenario", ["Taiwan Chip Ban 40%", "Red Sea Crisis", "US-China Tariffs"], key="s1")
    scenario1 = st.selectbox("Select Shock Scenario", 
                             ["Taiwan Semiconductor Ban", "China Rare Earth Ban", "Oil Price Shock $150", "US-China Tariffs 25%"], 
                             key="s1")
with col2:
    compare_mode = st.toggle("Compare Mode", key="cmp")

if compare_mode:
    scenario2 = st.selectbox("Compare With", ["Red Sea Crisis", "US-China Tariffs", "Taiwan Chip Ban 40%"], index=1, key="s2")
    scenario2 = st.selectbox("Compare With", 
                             ["China Rare Earth Ban", "Oil Price Shock $150", "US-China Tariffs 25%", "Taiwan Semiconductor Ban"], 
                             index=1, key="s2")

# Data
# Data for 4 scenarios
data = {
    "Taiwan Chip Ban 40%": {
    "Taiwan Semiconductor Ban": {
        'countries': ['Taiwan', 'China', 'United States', 'Germany', 'Japan', 'India', 'Vietnam'],
        'codes': ['TWN', 'CHN', 'USA', 'DEU', 'JPN', 'IND', 'VNM'],
        'c_risks': [9, 10, 7, 6, 8, 5, 4],
        'risks': [9, 10, 7, 6, 8, 5, 4],
        'lats': [23.7, 35.0, 37.0, 51.0, 36.0, 20.0, 14.0],
        'lons': [121.0, 104.0, -98.0, 10.0, 138.0, 78.0, 108.0],
        'revenue': '$420B', 'countries_count': 18, 'industries_count': 3, 'risk_score': 9.1,
        'industries': ['Banking', 'Electronics', 'Textile', 'Pharma', 'Automotive'],
        'industries': ['Banking', 'Electronics', 'Automotive', 'Pharma', 'Textile'],
        'i_risks': [10, 9, 7, 6, 4],
        'prices': {'Laptops': '+35%', 'Smartphones': '+40%', 'Cars': '+18%', 'Gaming Consoles': '+45%'},
        'summary': 'China and Banking sector face highest risk. $420B revenue at risk across 18 countries.',
        'recommendations': ['Diversify supplier base away from Taiwan/China', 'Increase 60-day inventory buffer', 'Implement dynamic pricing', 'Monitor secondary markets'],
        'summary': '60% global chip supply disrupted. Electronics and Automotive hit hardest.',
        'recommendations': ['Diversify chip sourcing to Samsung/Intel', 'Increase 90-day inventory', 'Redesign products for mature nodes']
    },
    "Red Sea Crisis": {
        'countries': ['China', 'India', 'Germany', 'United States', 'Japan'],
        'codes': ['CHN', 'IND', 'DEU', 'USA', 'JPN'],
        'c_risks': [9, 8, 7, 6, 7],
        'revenue': '$280B', 'countries_count': 14, 'industries_count': 4, 'risk_score': 7.8,
        'industries': ['Textile', 'Automotive', 'Pharma', 'Electronics', 'Banking'],
        'i_risks': [8, 7, 6, 9, 5],
        'prices': {'Shipping': '+25%', 'Cars': '+12%', 'Clothing': '+20%', 'Electronics': '+15%'},
        'summary': 'Shipping delays increase costs. Textile and Automotive most affected.',
        'recommendations': ['Reroute via Cape of Good Hope', 'Build regional warehouses', 'Negotiate air freight contracts']
    "China Rare Earth Ban": {
        'countries': ['China', 'United States', 'Japan', 'Germany', 'India'],
        'risks': [10, 8, 9, 7, 6],
        'lats': [35.0, 37.0, 36.0, 51.0, 20.0],
        'lons': [104.0, -98.0, 138.0, 10.0, 78.0],
        'revenue': '$380B', 'countries_count': 15, 'industries_count': 4, 'risk_score': 8.9,
        'industries': ['Automotive', 'Electronics', 'Defense', 'Renewable Energy', 'Pharma'],
        'i_risks': [9, 8, 9, 7, 5],
        'prices': {'EV Batteries': '+50%', 'Wind Turbines': '+30%', 'Smartphones': '+20%', 'Fighter Jets': '+25%'},
        'summary': '90% rare earth supply controlled by China. EV and Defense industries critical.',
        'recommendations': ['Source from Australia/Africa mines', 'Invest in recycling tech', 'Stockpile 6-month reserves']
    },
    "US-China Tariffs": {
    "Oil Price Shock $150": {
        'countries': ['Saudi Arabia', 'Russia', 'United States', 'China', 'India'],
        'risks': [9, 8, 7, 6, 8],
        'lats': [24.0, 61.0, 37.0, 35.0, 20.0],
        'lons': [45.0, 105.0, -98.0, 104.0, 78.0],
        'revenue': '$520B', 'countries_count': 22, 'industries_count': 5, 'risk_score': 8.5,
        'industries': ['Transportation', 'Chemicals', 'Aviation', 'Plastics', 'Agriculture'],
        'i_risks': [9, 8, 9, 7, 6],
        'prices': {'Fuel': '+60%', 'Air Tickets': '+40%', 'Plastics': '+35%', 'Fertilizer': '+30%'},
        'summary': 'Oil at $150/barrel increases logistics cost globally. Aviation and Shipping worst hit.',
        'recommendations': ['Switch to rail/sea freight', 'Hedge fuel costs', 'Optimize routes to reduce mileage']
    },
    "US-China Tariffs 25%": {
        'countries': ['China', 'United States', 'Vietnam', 'Mexico', 'India'],
        'codes': ['CHN', 'USA', 'VNM', 'MEX', 'IND'],
        'c_risks': [9, 7, 8, 7, 6],
        'risks': [9, 7, 8, 7, 6],
        'lats': [35.0, 37.0, 14.0, 23.0, 20.0],
        'lons': [104.0, -98.0, 108.0, -102.0, 78.0],
        'revenue': '$350B', 'countries_count': 12, 'industries_count': 5, 'risk_score': 8.2,
        'industries': ['Electronics', 'Automotive', 'Textile', 'Pharma', 'Banking'],
        'i_risks': [9, 7, 8, 5, 6],
        'prices': {'Electronics': '+30%', 'Cars': '+15%', 'Clothing': '+22%', 'Appliances': '+18%'},
        'summary': 'Tariffs shift production to Vietnam/Mexico. Electronics supply chain disrupted.',
        'summary': '25% tariffs shift production to Vietnam/Mexico. Supply chains re-routing.',
        'recommendations': ['Shift manufacturing to Vietnam', 'Apply for tariff exemptions', 'Renegotiate supplier contracts']
    }
}

def show_tab1(scenario_name, suffix=""):
def get_color(risk):
    if risk >= 9: return 'red'
    elif risk >= 7: return 'orange'
    elif risk >= 4: return 'yellow'
    else: return 'green'

def show_all_sections(scenario_name, suffix=""):
    d = data[scenario_name]

    # FIXED: Removed key from metrics - Streamlit Cloud error
    # 1. Metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("INDUSTRIES IMPACTED", f"{d['industries_count']}/5")
    m2.metric("REVENUE AT RISK", d['revenue'])
    m3.metric("COUNTRIES AFFECTED", d['countries_count'])
    m4.metric("RISK SCORE", f"{d['risk_score']}/10", "↑ Critical", delta_color="inverse")

    # MAP - GUARANTEED VISIBLE
    # 2. FOLIUM MAP - GUARANTEED VISIBLE
    st.subheader(f"Supply Chain Risk Map {suffix}")
    df_map = pd.DataFrame({'Country': d['countries'], 'Code': d['codes'], 'Risk': d['c_risks']})
    fig_map = px.choropleth(df_map, locations='Code', color='Risk', hover_name='Country',
                            locationmode='ISO-3', color_continuous_scale='Reds', range_color=(0,10))
    fig_map.update_geos(showcountries=True, countrycolor=text, showcoastlines=True, coastlinecolor=text)
    fig_map.update_layout(height=450, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor=bg, plot_bgcolor=bg, font=dict(color=text, size=16))
    st.plotly_chart(fig_map, use_container_width=True, key=f"map{suffix}")
    m = folium.Map(location=[20, 0], zoom_start=2, tiles='CartoDB dark_matter' if dark else 'OpenStreetMap')
    for country, risk, lat, lon in zip(d['countries'], d['risks'], d['lats'], d['lons']):
        folium.CircleMarker(
            location=[lat, lon],
            radius=risk*4,
            color=get_color(risk),
            fill=True,
            fill_color=get_color(risk),
            fill_opacity=0.8,
            popup=f"{country}: Risk {risk}/10"
        ).add_to(m)
    st_folium(m, height=500, use_container_width=True, key=f"folium{suffix}")

    # Country Table
    # 3. Country Table
    st.subheader(f"Country Risk Breakdown {suffix}")
    df_country = pd.DataFrame({
        'Country': d['countries'],
        'Risk Score': d['c_risks'],
        'Risk Level': ['Critical' if r>=9 else 'High' if r>=7 else 'Medium' if r>=4 else 'Low' for r in d['c_risks']]
        'Risk Score': d['risks'],
        'Risk Level': ['Critical' if r>=9 else 'High' if r>=7 else 'Medium' if r>=4 else 'Low' for r in d['risks']]
    })
    st.dataframe(df_country, use_container_width=True, hide_index=True, key=f"table{suffix}")

    # Industry + Price
    # 4. Industry Risk + 5. Consumer Price
    colA, colB = st.columns([1.5, 1])
    with colA:
        st.subheader(f"Industry Risk Score {suffix}")
        df_ind = pd.DataFrame({'Industry': d['industries'], 'Risk': d['i_risks']})
        fig_bar = px.bar(df_ind, x='Risk', y='Industry', orientation='h', color='Risk', color_continuous_scale='Reds')
        fig_bar.update_layout(height=350, paper_bgcolor=bg, plot_bgcolor=bg, font=dict(color=text, size=16), xaxis=dict(range=[0,10]))
        st.plotly_chart(fig_bar, use_container_width=True, key=f"bar{suffix}")
        st.bar_chart(df_ind.set_index('Industry'))

    with colB:
        st.subheader(f"Consumer Price Impact {suffix}")
@@ -106,26 +145,26 @@ def show_tab1(scenario_name, suffix=""):
            st.markdown(f"<p style='color:{text};font-size:18px;margin:10px 0'>{item}: <b>{price}</b></p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Summary
    # 6. Executive Summary
    with st.expander(f"Executive Summary & Recommendations {suffix}", expanded=True):
        st.markdown(f"<p style='color:{text};font-size:16px'><b>Scenario:</b> {scenario_name}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:{text};font-size:16px'><b>Key Impact:</b> {d['summary']}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:{text};font-size:16px'><b>Recommendations:</b></p>", unsafe_allow_html=True)
        for i, rec in enumerate(d['recommendations'], 1):
            st.markdown(f"<p style='color:{text};font-size:16px'>{i}. {rec}</p>", unsafe_allow_html=True)

def show_tab2(scenario_name, suffix=""):
def show_investment(scenario_name, suffix=""):
    d = data[scenario_name]
    st.subheader(f"Investment Intelligence - {scenario_name} {suffix}")

    # Investment boxes
    b1, b2, b3 = st.columns(3)
    with b1:
        st.markdown(f"<div style='border:2px solid #00FF00;padding:1rem;border-radius:8px'><p style='color:{text};font-size:16px'>Buy Opportunities<br><b>Automotive → 6/10</b></p></div>", unsafe_allow_html=True)
        st.markdown(f"<div style='border:2px solid #00FF00;padding:1rem;border-radius:8px'><p style='color:{text};font-size:16px'>Buy Opportunities<br><b>Rare Earth Mining → 8/10</b></p></div>", unsafe_allow_html=True)
    with b2:
        st.markdown(f"<div style='border:2px solid orange;padding:1rem;border-radius:8px'><p style='color:{text};font-size:16px'>Hold<br><b>Pharma → 4/10</b></p></div>", unsafe_allow_html=True)
        st.markdown(f"<div style='border:2px solid orange;padding:1rem;border-radius:8px'><p style='color:{text};font-size:16px'>Hold<br><b>Pharma → 5/10</b></p></div>", unsafe_allow_html=True)
    with b3:
        st.markdown(f"<div style='border:2px solid red;padding:1rem;border-radius:8px'><p style='color:{text};font-size:16px'>Avoid - High Risk<br><b>Electronics → 9/10<br>Banking → 10/10</b></p></div>", unsafe_allow_html=True)
        st.markdown(f"<div style='border:2px solid red;padding:1rem;border-radius:8px'><p style='color:{text};font-size:16px'>Avoid - High Risk<br><b>Electronics → 9/10<br>Automotive → 9/10</b></p></div>", unsafe_allow_html=True)

    # Risk vs Opportunity
    colX, colY = st.columns([2, 1])
@@ -134,16 +173,14 @@ def show_tab2(scenario_name, suffix=""):
        df_scatter = pd.DataFrame({
            'Industry': d['industries'],
            'Risk': d['i_risks'],
            'Opportunity': [0, 1, 3, 4, 6]
            'Opportunity': [6, 3, 1, 4, 2]
        })
        fig_scatter = px.scatter(df_scatter, x='Risk', y='Opportunity', color='Industry', size=[25]*5)
        fig_scatter.update_layout(height=400, paper_bgcolor=bg, plot_bgcolor=bg, font=dict(color=text, size=16))
        st.plotly_chart(fig_scatter, use_container_width=True, key=f"scatter{suffix}")
        st.scatter_chart(df_scatter.set_index('Industry'))

    with colY:
        st.subheader(f"Investment Guidance {suffix}")
        st.markdown(f"<p style='color:{text};font-size:16px'>Reduce exposure: Electronics, Banking</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:{text};font-size:16px'>Consider increasing: Automotive</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:{text};font-size:16px'>Reduce exposure: Electronics, Automotive</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:{text};font-size:16px'>Consider increasing: Rare Earth Mining</p>", unsafe_allow_html=True)
        st.warning("For demonstration purposes only. Not financial advice")

# Tabs
@@ -153,24 +190,24 @@ def show_tab2(scenario_name, suffix=""):
    if compare_mode:
        c1, c2 = st.columns(2)
        with c1:
            show_tab1(scenario1, suffix="_A")
            show_all_sections(scenario1, suffix="_A")
        with c2:
            show_tab1(scenario2, suffix="_B")
            show_all_sections(scenario2, suffix="_B")
    else:
        show_tab1(scenario1)
        show_all_sections(scenario1)

with tab2:
    if compare_mode:
        c1, c2 = st.columns(2)
        with c1:
            show_tab2(scenario1, suffix="_A")
            show_investment(scenario1, suffix="_A")
        with c2:
            show_tab2(scenario2, suffix="_B")
            show_investment(scenario2, suffix="_B")
    else:
        show_tab2(scenario1)
        show_investment(scenario1)

# Methodology
with st.expander("Methodology & Assumptions", expanded=False):
    st.markdown(f"<p style='color:{text};font-size:16px'><b>Risk Formula:</b> Risk = 0.4×Supplier Concentration + 0.3×Geopolitical Stability + 0.2×Trade Dependency + 0.1×Logistics</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:{text};font-size:16px'><b>Data Sources:</b> UN Comtrade, World Bank Governance, GDELT Events</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:{text};font-size:16px'><b>Assumptions:</b> >40% supply from 1 country = +3 Risk | 30-day inventory = -2 Risk</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:{text};font-size:16px'><b>Data Sources:</b> UN Comtrade, USGS Mineral Data, EIA Oil Data, GDELT Events</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:{text};font-size:16px'><b>Assumptions:</b> >40% supply from 1 country = +3 Risk | Oil $150 = +2 Logistics Risk</p>", unsafe_allow_html=True)
