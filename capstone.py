import streamlit as st


# Set page configuration
st.set_page_config(
    page_title= "Cross-Referencing Dispatched Incidents, Crime",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to style the app
def local_css():
    st.markdown("""
    <style>
        .main-header {
        font-size: 2.5rem;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 700;
        }
        .sub-header {
        font-size: 1.5rem;
        margin-bottom: 1rem;
        }
        .card {
        border-radius: 10px;
        margin-bottom: 1rem;
        background-color: rgba(37, 99, 235, 0.08);  /* Pale translucent blue based on #2563EB */
        border: 1px solid rgba(37, 99, 235, 0.15);
        padding: 1.2rem;
        box-shadow: 0 4px 6px rgba(37, 99, 235, 0.05);
        transition: all 0.3s ease;
        }
        .card:hover {
        transition: all 0.3s ease;
        background-color: rgba(37, 99, 235, 0.12);
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(37, 99, 235, 0.08);
        }
        .card-title {
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: #1D4ED8;  /* Slightly darker blue for card titles */
        }
        .highlight {
        font-weight: 600;
        }
        .footer {
        text-align: center;
        margin-top: 3rem;
        font-size: 0.8rem;
        }
        .nav-button {
        background-color: #2563EB;
        color: white;
        padding: 0.5rem 1rem;
        font-size: 1rem;
        font-weight: 500;
        border-radius: 5px;
        margin-right: 0.5rem;
        margin-top: 0.5rem;
        display: inline-block;
        text-align: center;
        text-decoration: none;
        transition: all 0.3s ease;
        border: none;
        cursor: pointer;
        }
        .nav-button:hover {
        background-color: #1D4ED8;
        transform: translateY(-2px);
        }
    </style>
    """, unsafe_allow_html=True)

local_css()

# Function to create a card component
def create_card(title, description ):
    st.markdown(f"""
    <div class="card">
        <div class="card-title">{title}</div>
        <div class="card-text">{description}</div>
    </div>
    """, unsafe_allow_html=True)

# Main header
st.markdown('<div class="main-header"> Crime Reports & Police Dispatch Analysis</div>', unsafe_allow_html=True)

# Introduction
st.markdown("""
<div class="sub-header">Introduction </div>
""", unsafe_allow_html=True)

# Brief app description
st.markdown("""
This dashboard aims to provide analytical insights into crime reports and police dispatched incidents. It does not investigate the relationship crime reports or police dispatch incidents might have to actual criminal activity. 
The data spans from November 2018 to November 2024, covering a wide range of incident types and locations.
            

""")

# Navigation Section
st.markdown('<div class="sub-header">Navigation</div>', unsafe_allow_html=True)

# Layout for navigation cards
col1, col2 = st.columns(2)

with col1:
    create_card("Dataframe Walkthrough", "Exploration of the datasets, their content and the data quality.")
    if st.button("Go to Data Walkthrough", key="data_walkthrough"):
        # You can replace these with your actual page paths
        st.switch_page("pages/data_breakdown.py")

    create_card("Treemap Analysis", "Visualizes patterns in crime categories and dispatch priorties with a treemap.")
    if st.button("Go to Treemap Analysis", key="treemap"):
        st.switch_page("pages/treemap.py")
        
with col2:
    create_card("Time Series Analysis", "Analyzes trends and patterns in crime and dispatch data over time.")
    if st.button("Go to Time Series Analysis", key="time_series"):
        st.switch_page("pages/timeseries.py")
        
    create_card("Geographic Analysis", "Explores spatial distribution of crime reports vs dispatch incidents.")
    if st.button("Go to Geographic Analysis", key="geographic"):
        st.switch_page("pages/geographic_distribution.py")



# About section with disclaimer
st.markdown('<div class="sub-header"> About This Dashboard</div>', unsafe_allow_html=True)
st.markdown("""
This app serves is the result of my capstone project and internship project through Montgomery College and dataMontgomery respectively. 
Montgomery County has exercised a first rate open data policy and as a result made publicly available a large amount of data collected on its operations. 
The access to these data are easy and a few key manipulaties/modes of analysis are avialable through dataMontgomery's own website. 
The purpose of this project was to make use of this fantastic public service and to put together two such datasets. 

**Note**: All data is publically available on dataMontgomery's website: https://data.montgomerycountymd.gov

**My Thanks and Appriciation**:
I would very much like to give my deepest thanks to Professor Jane Valentine, and to Darren Dobkin for their help and support with this project. 
It was a real pleasure to get to work with dataMontgomery. 
""")

# Footer
st.markdown('<div class="footer">steal away</div>', unsafe_allow_html=True)
