import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Global Supply Chain Risk Intelligence", layout="wide")

# Dark theme
st.markdown("""
<style>
.stApp {background-color: #0E1117; color: white;}
[data-testid="stMetricValue"] {font-size: 2rem; font-weight: bold;}
[data-testid="stMetricLabel"] {color: #A0A0A0; text-transform: uppercase; font-size: 0.8rem;}
</style>
""", unsafe_allow_html=True)

# Header
st.title("Global Supply Chain Risk Intelligence")
st.markdown("Impact Analysis for Businesses, Consumers & Investors")

# Scenario + Compare Mode
col1, col2 = st.columns([4, 1])
with col1:
    scenario = st.selectbox("Select Shock Scenario", ["Semiconductor Shock - Taiwan 40%"])
with col2:
    compare_mode = st.toggle("Compare Mode")

# Tabs
tab1, tab2 = st.tabs(["Supply Chain Risk", "Investment Intelligence"])

with tab1:
    # 4 Metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("INDUSTRIES IMPACTED", "3/5", "↑ 0% from baseline")
    m2.metric("REVENUE AT RISK", "$420B")
    m3.metric("COUNTRIES AFFECTED", "18")
    m4.metric("RISK SCORE", "9.1/10", "↑ Critical", delta_color="inverse")
    
    # MAP - Scatter geo with bubbles like your screenshot
    st.subheader("Supply Chain Risk Map")
    df_map = pd.DataFrame({
        'Country': ['USA', 'Germany', 'China', 'Taiwan', 'India', 'Japan', 'Vietnam'],
        'Risk': [7, 6, 10, 9, 5, 8, 4],
        'Lat': [37.09, 51.16, 35.86, 23.69, 20.59, 36.20, 14.05],
        'Lon': [-95.71, 10.45, 104.19, 120.96, 78.96, 138.25, 108.28]
    })
    
    fig_map = px.scatter_geo(df_map, lat='Lat', lon='Lon', size='Risk', color='Risk',
                             hover_name='Country', size_max=40,
                             color_continuous_scale=['#FFD700', '#FFA500', '#FF4B4B'])
    fig_map.update_geos(projection_type="orthographic", showland=True, landcolor="#0E1117",
                        showocean=True, oceancolor="#000", showcountries=True, countrycolor="#FFFFFF")
    fig_map.update_layout(height=500, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor="#0E1117")
    st.plotly_chart(fig_map, use_container_width=True)
    
    # Country Risk Breakdown Table
    st.subheader("Country Risk Breakdown")
    df_country = pd.DataFrame({
        'Country': ['Taiwan', 'China', 'USA', 'Germany', 'India', 'Japan', 'Vietnam'],
        'Risk Score': [9, 10, 7, 6, 5, 8, 4],
        'Risk Level': ['Critical', 'Critical', 'High', 'Medium', 'Medium', 'High', 'Low']
    })
    st.dataframe(df_country, use_container_width=True, hide_index=True)
    
    # Industry + Price columns
    colA, colB = st.columns([1.5, 1])
    with colA:
        st.subheader("Industry Risk Score")
        df_ind = pd.DataFrame({
            'Industry': ['Banking', 'Electronics', 'Textile', 'Pharma', 'Automotive'],
            'Risk': [10, 9, 7, 6, 4]
        })
        fig_bar = px.bar(df_ind, x='Risk', y='Industry', orientation='h', 
                         color='Risk', color_continuous_scale='Reds')
        fig_bar.update_layout(height=350, paper_bgcolor="#0E1117", plot_bgcolor="#0E1117", 
                              font=dict(color="white"), xaxis=dict(range=[0,10]))
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with colB:
        st.subheader("Consumer Price Impact")
        st.markdown("Laptops: **+35%**")
        st.markdown("Smartphones: **+40%**")
        st.markdown("Cars: **+18%**")
        st.markdown("Gaming Consoles: **+45%**")
        st.button("Timeline: Price changes expected in 2 weeks")
    
    # Executive Summary
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
    
    # 3 boxes
    b1, b2, b3 = st.columns(3)
    with b1:
        st.markdown("<div style='border:2px solid green;padding:1rem;border-radius:5px'>Buy Opportunities<br>Automotive → 6/10</div>", unsafe_allow_html=True)
    with b2:
        st.markdown("<div style='border:2px solid orange;padding:1rem;border-radius:5px'>Hold<br>Pharma → 4/10</div>", unsafe_allow_html=True)
    with b3:
        st.markdown("<div style='border:2px solid red;padding:1rem;border-radius:5px'>Avoid - High Risk<br>Electronics → 9/10<br>Banking → 10/10</div>", unsafe_allow_html=True)
    
    # Risk vs Opportunity Matrix
    colX, colY = st.columns([2, 1])
    with colX:
        st.subheader("Risk vs Opportunity Matrix")
        df_scatter = pd.DataFrame({
            'Industry': ['Electronics', 'Automotive', 'Pharma', 'Textile', 'Banking'],
            'Risk': [9, 4, 6, 7, 10],
            'Opportunity': [1, 6, 4, 3, 0]
        })
        fig_scatter = px.scatter(df_scatter, x='Risk', y='Opportunity', color='Industry', size=[20]*5)
        fig_scatter.update_layout(height=400, paper_bgcolor="#0E1117", plot_bgcolor="#0E1117", font=dict(color="white"))
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with colY:
        st.subheader("Investment Guidance")
        st.markdown("Reduce exposure: Electronics, Banking")
        st.markdown("Consider increasing: Automotive")
        st.warning("For demonstration purposes only. Not financial advice")
    
    with st.expander("Methodology & Assumptions"):
        st.markdown("Risk scores based on supplier concentration, geopolitical stability, and trade dependency.")
