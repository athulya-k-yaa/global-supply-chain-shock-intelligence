import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Global Supply Chain Risk Intelligence", layout="wide")

# Dark/White mode toggle
theme_mode = st.toggle("🌙 Dark Mode", value=True)

if theme_mode:
    bg = "#0E1117"
    text = "white"
    card = "#1E2A3A"
else:
    bg = "#FFFFFF"
    text = "black"
    card = "#F0F2F6"

st.markdown(f"""
<style>
.stApp {{background-color: {bg}; color: {text};}}
[data-testid="stMetricValue"] {{font-size: 2rem; font-weight: bold; color: {text};}}
</style>
""", unsafe_allow_html=True)

st.title("Global Supply Chain Risk Intelligence")
st.markdown("Impact Analysis for Businesses, Consumers & Investors")

col1, col2 = st.columns([4, 1])
with col1:
    scenario = st.selectbox("Select Shock Scenario", ["Semiconductor Shock - Taiwan 40%"])
with col2:
    compare_mode = st.toggle("Compare Mode")

tab1, tab2 = st.tabs(["Supply Chain Risk", "Investment Intelligence"])

with tab1:
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("INDUSTRIES IMPACTED", "3/5", "↑ 0% from baseline")
    m2.metric("REVENUE AT RISK", "$420B")
    m3.metric("COUNTRIES AFFECTED", "18")
    m4.metric("RISK SCORE", "9.1/10", "↑ Critical", delta_color="inverse")
    
    # MAP - CHOROPLETH FIXED - WILL SHOW FOR SURE
    st.subheader("Supply Chain Risk Map")
    df_map = pd.DataFrame({
        'Country': ['United States', 'Germany', 'China', 'Taiwan', 'India', 'Japan', 'Vietnam'],
        'Code': ['USA', 'DEU', 'CHN', 'TWN', 'IND', 'JPN', 'VNM'], # ISO-3 codes required
        'Risk': [7, 6, 10, 9, 5, 8, 4]
    })
    
    fig_map = px.choropleth(df_map, 
                            locations='Code',
                            color='Risk',
                            hover_name='Country',
                            color_continuous_scale=['#FFD700', '#FFA500', '#FF4B4B'],
                            range_color=(0, 10),
                            labels={'Risk': 'Risk Score'})
    
    fig_map.update_geos(showcountries=True, countrycolor=text, showcoastlines=True, coastlinecolor=text)
    fig_map.update_layout(height=500, margin=dict(l=0,r=0,t=0,b=0), 
                          paper_bgcolor=bg, plot_bgcolor=bg, font=dict(color=text))
    st.plotly_chart(fig_map, use_container_width=True)
    
    st.subheader("Country Risk Breakdown")
    st.dataframe(df_map[['Country', 'Risk']].rename(columns={'Risk': 'Risk Score'}), 
                 use_container_width=True, hide_index=True)
    
    colA, colB = st.columns([1.5, 1])
    with colA:
        st.subheader("Industry Risk Score")
        df_ind = pd.DataFrame({
            'Industry': ['Banking', 'Electronics', 'Textile', 'Pharma', 'Automotive'],
            'Risk': [10, 9, 7, 6, 4]
        })
        fig_bar = px.bar(df_ind, x='Risk', y='Industry', orientation='h', 
                         color='Risk', color_continuous_scale='Reds')
        fig_bar.update_layout(height=350, paper_bgcolor=bg, plot_bgcolor=bg, 
                              font=dict(color=text), xaxis=dict(range=[0,10]))
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with colB:
        st.subheader("Consumer Price Impact")
        st.markdown(f"<div style='background:{card};padding:1rem;border-radius:10px;color:{text}'>", unsafe_allow_html=True)
        st.markdown("Laptops: **+35%**")
        st.markdown("Smartphones: **+40%**")
        st.markdown("Cars: **+18%**")
        st.markdown("Gaming Consoles: **+45%**")
        st.markdown("</div>", unsafe_allow_html=True)
        st.button("Timeline: Price changes expected in 2 weeks")
    
    with st.expander("Executive Summary & Recommendations", expanded=True):
        st.markdown("**Scenario:** Semiconductor Shock - Taiwan 40%")
        st.markdown("**Key Impact:** China and Banking sector face highest risk at 10/10 and 10/10 respectively.")
        st.markdown("**Financial Impact:** Estimated $420B revenue at risk across 18 countries.")
        st.markdown("**Recommendations:**")
        st.markdown("1. Diversify supplier base away from high-risk regions")
        st.markdown("2. Increase inventory buffer for critical components")
        st.markdown("3. Implement dynamic pricing strategies")
        st.markdown("4. Monitor secondary supplier markets")

with tab2:
    st.subheader("Investment Intelligence")
    st.markdown(f"Analysis for: {scenario}")
    
    b1, b2, b3 = st.columns(3)
    with b1:
        st.markdown(f"<div style='border:2px solid green;padding:1rem;border-radius:5px;color:{text}'>Buy Opportunities<br>Automotive → 6/10</div>", unsafe_allow_html=True)
    with b2:
        st.markdown(f"<div style='border:2px solid orange;padding:1rem;border-radius:5px;color:{text}'>Hold<br>Pharma → 4/10</div>", unsafe_allow_html=True)
    with b3:
        st.markdown(f"<div style='border:2px solid red;padding:1rem;border-radius:5px;color:{text}'>Avoid - High Risk<br>Electronics → 9/10<br>Banking → 10/10</div>", unsafe_allow_html=True)
    
    colX, colY = st.columns([2, 1])
    with colX:
        st.subheader("Risk vs Opportunity Matrix")
        df_scatter = pd.DataFrame({
            'Industry': ['Electronics', 'Automotive', 'Pharma', 'Textile', 'Banking'],
            'Risk': [9, 4, 6, 7, 10],
            'Opportunity': [1, 6, 4, 3, 0]
        })
        fig_scatter = px.scatter(df_scatter, x='Risk', y='Opportunity', color='Industry', size=[20]*5)
        fig_scatter.update_layout(height=400, paper_bgcolor=bg, plot_bgcolor=bg, font=dict(color=text))
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with colY:
        st.subheader("Investment Guidance")
        st.markdown("Reduce exposure: Electronics, Banking")
        st.markdown("Consider increasing: Automotive")
        st.warning("For demonstration purposes only. Not financial advice")
    
    with st.expander("Methodology & Assumptions"):
        st.markdown("Risk scores based on supplier concentration, geopolitical stability, and trade dependency.")
