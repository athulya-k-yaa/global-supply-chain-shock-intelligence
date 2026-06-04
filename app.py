import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Global Supply Chain Shock Intelligence", layout="wide")

# Dark theme colors
bg = "#0E1117"
card = "#1E2A3A"
text = "#FFFFFF"
red = "#FF4B4B"
orange = "#FFA500"
yellow = "#FFD700"

st.title("🌍 Global Supply Chain Shock Intelligence")
st.markdown("Real-time risk monitoring for global trade disruptions")

# Scenario selector
scenario1 = st.selectbox("Select Disruption Scenario", 
                         ["Red Sea Crisis", "Taiwan Semiconductor Ban", "US-China Tariffs"])

# Risk data based on scenario
if scenario1 == "Red Sea Crisis":
    countries = ['China', 'India', 'Germany', 'United States', 'Japan', 'South Korea']
    risks = [9.2, 8.5, 7.8, 6.4, 7.1, 8.9]
    industries = ['Shipping', 'Electronics', 'Automotive', 'Textiles', 'Energy']
    ind_risks = [9.8, 8.2, 7.5, 8.9, 9.1]
    price = {'Container Freight': 280, 'Oil': 35, 'Electronics': 22}
    codes = ['CHN', 'IND', 'DEU', 'USA', 'JPN', 'KOR']
    
elif scenario1 == "Taiwan Semiconductor Ban":
    countries = ['Taiwan', 'China', 'United States', 'South Korea', 'Japan', 'Germany']
    risks = [9.8, 8.7, 8.1, 9.3, 8.5, 7.2]
    industries = ['Semiconductors', 'Electronics', 'Automotive', 'Mobile Phones', 'Cloud']
    ind_risks = [9.9, 9.2, 8.7, 8.8, 8.0]
    price = {'Chips': 150, 'Smartphones': 45, 'Laptops': 38}
    codes = ['TWN', 'CHN', 'USA', 'KOR', 'JPN', 'DEU']
    
else:  # US-China Tariffs
    countries = ['China', 'United States', 'Vietnam', 'Mexico', 'India', 'Germany']
    risks = [9.1, 7.8, 8.4, 7.9, 6.8, 6.2]
    industries = ['Manufacturing', 'Electronics', 'Textiles', 'Machinery', 'Chemicals']
    ind_risks = [9.0, 8.5, 8.8, 7.9, 7.2]
    price = {'Consumer Goods': 25, 'Industrial Parts': 32, 'Raw Materials': 18}
    codes = ['CHN', 'USA', 'VNM', 'MEX', 'IND', 'DEU']

df_country = pd.DataFrame({
    'Country': countries,
    'Risk': risks,
    'Code': codes
})

# Overall Risk Score
st.metric("Overall Risk Score", f"{max(risks)}/10", delta=f"+{max(risks)-5:.1f}")

# MAP SECTION - NEW
st.subheader("Country Risk Map")
fig_map = px.choropleth(df_country, 
                        locations='Code', 
                        color='Risk', 
                        hover_name='Country', 
                        color_continuous_scale='Reds',
                        range_color=(0, 10),
                        labels={'Risk': 'Risk Score'})
fig_map.update_layout(plot_bgcolor=bg, paper_bgcolor=bg, font=dict(color=text), height=500)
st.plotly_chart(fig_map, use_container_width=True)

# Country Table
st.subheader("Country Risk Table")
st.dataframe(df_country, use_container_width=True, hide_index=True)

# Columns for Industry + Price
colA, colB = st.columns([1.2, 0.8])

with colA:
    st.subheader("Industry Risk Matrix")
    df_ind = pd.DataFrame({
        'Industry': industries,
        'Risk': ind_risks
    })
    fig_bar = px.bar(df_ind, x='Industry', y='Risk', color='Risk', 
                     color_continuous_scale='Reds')
    fig_bar.update_layout(plot_bgcolor=bg, paper_bgcolor=bg, font=dict(color=text), height=400)
    st.plotly_chart(fig_bar, use_container_width=True)

with colB:
    st.subheader("Consumer Price Impact")
    st.markdown(f"<div style='background:{card};padding:1rem;border-radius:10px'>", unsafe_allow_html=True)
    
    for p, inc in price.items():
        st.markdown(f"{p}: <span style='color:{red};font-weight:bold'>{inc}% ↑</span>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Executive Summary
with st.expander("Executive Summary & Recommendations", expanded=True):
    top_country = countries[risks.index(max(risks))]
    top_industry = industries[ind_risks.index(max(ind_risks))]
    st.markdown(f"""
    **Scenario**: {scenario1}  
    **Key Impact**: {top_country} and {top_industry} sector face highest risk at {max(risks)}/10.  
    **Recommendation**: 
    1. Diversify suppliers away from high-risk regions
    2. Build 60-day inventory buffer for critical components  
    3. Hedge currency exposure for USD/CNY transactions
    4. Activate alternate shipping routes immediately
    """)

st.caption("Data simulated for demonstration. Updates every 5 minutes.")
   
