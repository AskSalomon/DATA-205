
from pathlib import Path
import streamlit as st
import pandas as pd
import geopandas as gpd
import altair as alt
import numpy as np
import logging
import altair_tiles as til
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression



MC_CENTER = [39.1547, -77.2405]
#file_path = Path('/Users/gimle/DATA-205-SETS/capstone_streamlit_scattermap.json')
file_path = "https://raw.githubusercontent.com/AskSalomon/DATA-205/refs/heads/main/capstone_streamlit_scattermap.json"
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)



def load_and_prepare_data(file_path, selected_crime):

    try:
     
        # DATA
        gdf = gpd.read_file(file_path)

        crime_col = f'crime_{selected_crime}'
        dispatch_col = f'dispatch_{selected_crime}'


        return gdf, crime_col, dispatch_col
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        raise

def create_linked_visualization(gdf, selected_crime, crime_col, dispatch_col):

    try:
    
        # altair brush 
        brush = alt.selection_interval(name='brush')
        
        # Scatterplot with brush 
        scatter = alt.Chart(gdf).mark_circle(size=60).encode(
            x=alt.X(dispatch_col,
                   title=f"Dispatches - {selected_crime.title()}",
                   scale=alt.Scale(zero=True)),
            y=alt.Y(crime_col,
                   title=f"Crime Reports - {selected_crime.title()}",
                   scale=alt.Scale(zero=True)),
            color=alt.condition(
                brush,
                alt.Color(f'{selected_crime}:Q', scale=alt.Scale(
                    domain=[gdf[selected_crime].min(), 0, gdf[selected_crime].max()],
                    range=['rgba(255,0,0,0.6)', 'rgba(0,0,255,0.6)']
                )),
                alt.value('lightgray')
            ),
            tooltip=[
                alt.Tooltip('tract', title='Census Tract'),
                alt.Tooltip(crime_col, title='Crime Reports', format=','),
                alt.Tooltip(dispatch_col, title='Dispatch Reports', format=','),
                #alt.Tooltip('crime_prop', title='Crime %', format='.1%'),
                #alt.Tooltip('dispatch_prop', title='Dispatch %', format='.1%')
            ]
        ).properties(
            width=500,
            height=300,
            title=f"Crime vs Dispatch Reports - {selected_crime.title()}"
        ).add_selection(brush)

        # Line of Regression
        X = gdf[[dispatch_col]]
        y = gdf[crime_col]
        lr = LinearRegression()
        lr.fit(X,y)
        lr.score(X,y)
        y_pred=lr.predict(X)
        r2 = r2_score(y, y_pred)
        x_range = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
        y_pred = lr.predict(x_range)
        
        regression_df = pd.DataFrame({
            'x': x_range.flatten(),
            'y': y_pred
        })

        regression = alt.Chart(regression_df).mark_line(
            color='red',
            strokeWidth=2,
            strokeDash=[4, 4]
        ).encode(
            x='x',
            y='y'
        )

        
        # R² 
        r_2_annotation = alt.Chart(pd.DataFrame([{
                'x': gdf[dispatch_col].min(), 
                'y': gdf[crime_col].max(),     
                'text': f'R² = {r2:.3f}'
        }])).mark_text(
            color='red',
            align='left',
            baseline='top',
            fontSize=17
        ).encode(
            x=alt.value(20), 
            y=alt.value(20),
            text='text:N'
        )
        
        
        # Map

        # Base Layer
        base = alt.Chart(gdf).mark_geoshape(
            stroke='white',
            strokeWidth=1
        ).encode(
        ).properties(
            width=500,
            height=300
        ).project(
            type='albersUsa' 
        )

        map_chart = alt.Chart(gdf).mark_geoshape(
            strokeWidth=1.5
        ).encode(
            alt.Color(selected_crime, 
                scale=alt.Scale(scheme='redblue'), title = 'scale'),
            tooltip=[
            selected_crime,'tract'
            ] 
        )
        
        # Combine charts
        top_chart = alt.layer(scatter, regression, r_2_annotation)
        bottom_chart = alt.layer(base + map_chart) 
        final_viz = alt.vconcat(bottom_chart, top_chart)

        return final_viz   
    except Exception as e:
        logger.error(f"Error creating visualization: {str(e)}")
        raise

def main():
    st.set_page_config(
        page_title="Geographic Comparison of Crime vs Dispatch Data",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.title("Crime vs Dispatch Reports Analysis")
    
    # Configurations
    CRIME_TYPES = ['theft', 'drug', 'sexassult', 'parts', 'violent', 'property', 'person']
    
    # Sidebar controls
    selected_crime = st.sidebar.selectbox(
        "Select reports related to ",
        options=CRIME_TYPES,
        format_func=lambda x: x.title()
    )
    
    try:
        # Load and prepare data
        gdf, crime_col, dispatch_col = load_and_prepare_data(file_path, selected_crime)
        viz = create_linked_visualization(gdf, selected_crime, crime_col, dispatch_col)

        st.altair_chart(viz, use_container_width=True)
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()