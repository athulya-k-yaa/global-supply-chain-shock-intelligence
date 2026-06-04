import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Global Supply Chain Risk Intelligence", layout="wide")

# Theme
dark = st.toggle("🌙 Dark Mode", value=True, key="theme_toggle")
bg = "#0E1117" if dark else "#FFFFFF"
text = "#FFFFFF" if dark else "#000"
card = "#1E2A3A" if dark else "#F0F2F6"

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

# 4 Scenarios
col1, col2 = st.columns([3, 1])
with col1:
    scenario1 = st.selectbox("Select Shock Scenario", 
                             ["Taiwan Semiconductor Ban", "China Rare Earth Ban", "Oil Price Shock $150", "US-China Tariffs 25%"], 
                             key="s1")
with col2:
    compare_mode = st.toggle("Compare Mode", key="cmp")

if compare_mode:
    scenario2 = st.selectbox("Compare With", 
                             ["China Rare Earth Ban", "Oil Price Shock $150", "US-China Tariffs 25%", "Taiwan Semiconductor Ban"], 
                             index=1, key="s2")

# Clean data - no duplicates, all commas present
data = {
    "Taiwan Semiconductor Ban": {
        'countries': ['Taiwan', 'China', 'United States of America', 'Germany', 'Japan', 'India', 'Vietnam'],
        'codes': ['TWN', 'CHN', 'USA', 'DEU', 'JPN', 'IND', 'VNM'],
        'c_risks': [9, 10, 7, 6, 8, 5, 4],
        'revenue': '$420B', 
        'countries_count': 18, 
        'industries_count': 3, 
        'risk_score': 9.1,
        'industries': ['Banking', 'Electronics', 'Automotive', 'Pharma', 'Textile'],
        'i_risks': [10, 9, 7, 6, 4],
        'prices': {'Laptops': '+35%', 'Smartphones': '+40%', 'Cars': '+18%', 'Gaming Consoles': '+45%'},
        'summary': '60% global chip supply disrupted. Electronics and Automotive hit hardest.',
        'recommendations': ['Diversify chip sourcing to Samsung/Intel', 'Increase 90-day inventory', 'Redesign products for mature nodes']
    },
    "China Rare Earth Ban": {
        'countries': ['China', 'United States of America', 'Japan', 'Germany', 'India'],
        'codes': ['CHN', 'USA', 'JPN', 'DEU', 'IND'],
        'c_risks': [10, 8, 9, 7, 6],
        'revenue': '$380B', 
        'countries_count': 15, 
        'industries_count': 4, 
        'risk_score': 8.9,
        'industries': ['Automotive', 'Electronics', 'Defense', 'Renewable Energy', 'Pharma'],
        'i_risks': [9, 8, 9, 7, 5],
        'prices': {'EV Batteries': '+50%', 'Wind Turbines': '+30%', 'Smartphones': '+20%', 'Fighter Jets': '+25%'},
        'summary': '90% rare earth supply controlled by China. EV and Defense industries critical.',
        'recommendations': ['Source from Australia/Africa mines', 'Invest in recycling tech', 'Stockpile 6-month reserves']
    },
    "Oil Price Shock $150": {
        'countries': ['Saudi Arabia', 'Russia', 'United States of America', 'China', 'India'],
        'codes': ['SAU', 'RUS', 'USA', 'CHN', 'IND'],
        'c_risks': [9, 8, 7, 6, 8],
        'revenue': '$520B', 
        'countries_count': 22, 
        'industries_count': 5, 
        'risk_score': 8.5,
        'industries': ['Transportation', 'Chemicals', 'Aviation', 'Plastics', 'Agriculture'],
        'i_risks': [9, 8, 9, 7, 6],
        'prices': {'Fuel': '+60%', 'Air Tickets': '+40%', 'Plastics': '+35%', 'Fertilizer': '+30%'},
        'summary': 'Oil at $150/barrel increases logistics cost globally. Aviation and Shipping worst hit.',
        'recommendations': ['Switch to rail/sea freight', 'Hedge fuel costs', 'Optimize routes to reduce mileage']
    },
    "US-China Tariffs 25%": {
        'countries': ['China', 'United States of America', 'Vietnam', 'Mexico', 'India'],
        'codes': ['CHN', 'USA', 'VNM', 'MEX', 'IND'],
        'c_risks': [9, 7, 8, 7, 6],
        'revenue': '$350B', 
        'countries_count': 12, 
        'industries_count': 5, 
        'risk_score': 8.2,
        'industries': ['Electronics', 'Automotive', 'Textile', 'Pharma', 'Banking'],
        'i_risks': [9, 7, 8, 5, 6],
        'prices': {'Electronics': '+30%', 'Cars': '+15%', 'Clothing': '+22%', 'Appliances': '+18%'},
        'summary': '25% tariffs shift production to Vietnam/Mexico. Supply chains re-routing.',
        'recommendations': ['Shift manufacturing to Vietnam', 'Apply for tariff exemptions', 'Renegotiate supplier contracts']
    }
}

def show_all_sections(scenario_name, suffix=""):
    d = data[scenario_name]
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("INDUSTRIES IMPACTED", f"{d['industries_count']}/5")
    m2.metric("REVENUE AT RISK", d['revenue'])
    m3.metric("COUNTRIES AFFECTED", d['countries_count'])
    m4.metric("RISK SCORE", f"{d['risk_score']}/10", "↑ Critical", delta_color="inverse")
    
    st.subheader(f"Supply Chain Risk Map {suffix}")
    df_map = pd.DataFrame({'Country': d['countries'], 'Code': d['codes'], 'Risk': d['c_risks']})
    fig_map = px.choropleth(df_map, locations='Code', color='Risk', hover_name='Country',
                            locationmode='ISO-3', scope='world',
                            color_continuous_scale=['#FFFF00', '#FF8C00', '#FF0000'], range_color=(0,10))
    fig_map.update_geos(showcountries=True, countrycolor=text, showcoastlines=True, coastlinecolor=text)
    fig_map.update_layout(height=500, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor=bg, plot_bgcolor=bg, font=dict(color=text, size=16))
    st.plotly_chart(fig_map, use_container_width=True, key=f"map{suffix}")
    
    st.subheader(f"Country Risk Breakdown {suffix}")
    df_country = pd.DataFrame({
        'Country': d['countries'],
        'Risk Score': d['c_risks'],
        'Risk Level': ['Critical' if r>=9 else 'High' if r>=7 else 'Medium' if r>=4 else 'Low' for r in d['c_risks']]
    })
    st.dataframe(df_country, use_container_width=True, hide_index=True, key=f"table{suffix}")
    
    colA, colB = st.columns([1.5, 1])
    with colA:
        st.subheader(f"Industry Risk Score {suffix}")
        df_ind = pd.DataFrame({'Industry': d['industries'], 'Risk': d['i_risks']})
        fig_bar = px.bar(df_ind, x='Risk', y='Industry', orientation='h', color='Risk', color_continuous_scale='Reds')
        fig_bar.update_layout(height=350, paper_bgcolor=bg, plot_bgcolor=bg, font=dict(color=text, size=16), xaxis=dict(range=[0,10]))
        st.plotly_chart(fig_bar, use_container_width=True, key=f"bar{suffix}")
    
    with colB:
        st.subheader(f"Consumer Price Impact {suffix}")
        st.markdown(f"<div style='background:{card};padding:1.5rem;border-radius:10px'>", unsafe_allow_html=True)
        for item, price in d['prices'].items():
            st.markdown(f"<p style='color:{text};font-size:18px;margin:10px 0'>{item}: <b>{price}</b></p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with st.expander(f"Executive Summary & Recommendations {suffix}", expanded=True):
        st.markdown(f"<p style='color:{text};font-size:16px'><b>Scenario:</b> {scenario_name}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:{text};font-size:16px'><b>Key Impact:</b> {d['summary']}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:{text};font-size:16px'><b>Recommendations:</b></p>", unsafe_allow_html=True)
        for i, rec in enumerate(d['recommendations'], 1):
            st.markdown(f"<p style='color:{text};font-size:16px'>{i}. {rec}</p>", unsafe_allow_html=True)

def show_investment(scenario_name, suffix=""):
    d = data[scenario_name]
    st.subheader(f"Investment Intelligence - {scenario_name} {suffix}")
    
    b1, b2, b3 = st.columns(3)
    with b1:
        st.markdown(f"<div style='border:2px solid #00FF00;padding:1rem;border-radius:8px'><p style='color:{text};font-size:16px'>Buy Opportunities<br><b>Rare Earth Mining → 8/10</b></p></div>", unsafe_allow_html=True)
    with b2:
        st.markdown(f"<div style='border:2px solid orange;padding:1rem;border-radius:8px'><p style='color:{text};font-size:16px'>Hold<br><b>Pharma → 5/10</b></p></div>", unsafe_allow_html=True)
    with b3:
        st.markdown(f"<div style='border:2px solid red;padding:1rem;border-radius:8px'><p style='color:{text};font-size:16px'>Avoid - High Risk<br><b>Electronics → 9/10<br>Automotive → 9/10</b></p></div>", unsafe_allow_html=True)
    
    colX, colY = st.columns([2, 1])
    with colX:
        st.subheader(f"Risk vs Opportunity Matrix {suffix}")
        df_scatter = pd.DataFrame({
            'Industry': d['industries'],
            'Risk': d['i_risks'],
            'Opportunity': [6, 3, 1, 4, 2]
        })
        fig_scatter = px.scatter(df_scatter, x='Risk', y='Opportunity', color='Industry', size=[25]*5)
        fig_scatter.update_layout(height=400, paper_bgcolor=bg, plot_bgcolor=bg, font=dict(color=text, size=16))
        st.plotly_chart(fig_scatter, use_container_width=True, key=f"scatter{suffix}")
    
    with colY:
        st.subheader(f"Investment Guidance {suffix}")
        st.markdown(f"<p style='color:{text};font-size:16px'>Reduce exposure: Electronics, Automotive</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:{text};font-size:16px'>Consider increasing: Rare Earth Mining</p>", unsafe_allow_html=True)
        st.warning("For demonstration purposes only. Not financial advice")

tab1, tab2 = st.tabs(["Supply Chain Risk", "Investment Intelligence"])

with tab1:
    if compare_mode:
        c1, c2 = st.columns(2)
        with c1:
            show_all_sections(scenario1, suffix="_A")
        with c2:
            show_all_sections(scenario2, suffix="_B")
    else:
        show_all_sections(scenario1)

with tab2:
    if compare_mode:
        c1, c2 = st.columns(2)
        with c1:
            show_investment(scenario1, suffix="_A")
        with c2:
            show_investment(scenario2, suffix="_B")
    else:
        show_investment(scenario1)

with st.expander("Methodology & Assumptions", expanded=False):
    st.markdown(f"<p style='color:{text};font-size:16px'><b>Risk Formula:</b> Risk = 0.4×Supplier Concentration + 0.3×Geopolitical Stability + 0.2×Trade Dependency + 0.1×Logistics</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:{text};font-size:16px'><b>Data Sources:</b> UN Comtrade, USGS Mineral Data, EIA Oil Data</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:{text};font-size:16px'><b>Assumptions:</b> >40% supply from 1 country = +3 Risk | Oil $150 = +2 Logistics Risk</p>", unsafe_allow_html=True)
