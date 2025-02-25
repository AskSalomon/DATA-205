from pathlib import Path
import streamlit as st
import pandas as pd
import geopandas as gpd
import altair as alt
import numpy as np
import logging
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

def load_and_prepare_data(selected_crime):
    try:
        file_path = 'https://raw.githubusercontent.com/AskSalomon/DATA-205/refs/heads/main/capstone_streamlit_scattermap_topo.json'
        
        gdf = gpd.read_file(file_path, driver='TopoJSON')
        geo = alt.topo_feature(file_path, feature='data')
        
        if selected_crime not in gdf.columns:
            logger.error(f"Column '{selected_crime}' not found in data")
            raise ValueError(f"Crime type '{selected_crime}' not found in dataset")
        
        # Define column names
        crime_col = f'crime_{selected_crime}'
        dispatch_col = f'dispatch_{selected_crime}'
        
        return gdf, crime_col, dispatch_col, geo
    
    except Exception as e:
        logger.error(f"Error in data preparation: {str(e)}")
        raise

def create_linked_visualization(gdf, selected_crime, crime_col, dispatch_col, geo):
    try:
        
        brush = alt.selection_interval(
            encodings=['x', 'y'],
            name='brush' 
            )
        
        lookup_data = alt.LookupData(
            data=gdf,
            key='tract',
            fields=[crime_col, dispatch_col, selected_crime, 'population'])

        scatter = alt.Chart(gdf).mark_point(
            filled=True,
            size=100 
        ).encode(
            x=alt.X(dispatch_col,
                   title=f"Dispatches - {selected_crime.title()}",
                   scale=alt.Scale(zero=True)),  # Force include zero
            y=alt.Y(crime_col,
                   title=f"Crime Reports - {selected_crime.title()}",
                   scale=alt.Scale(zero=True)),  # Force include zero
            opacity=alt.condition(brush, alt.value(1), alt.value(0.2)),
            color=alt.Color(f'{selected_crime}:Q', 
                scale=alt.Scale(
                    domain=[-1, 0, 1], 
                    range=['rgba(255,0,0,0.8)', 'rgba(255,255,255,0.8)', 'rgba(0,0,255,0.8)']
                ),
                title="Dispatch vs Crime Ratio"),
            #size=alt.Size('population:Q', 
            #   scale=alt.Scale(range=[50, 300]),
            #    title="Population"),
            tooltip=[
                alt.Tooltip('tract:N', title='Census Tract'),
                alt.Tooltip(crime_col, title='Crime Reports', format=','),
                alt.Tooltip(dispatch_col, title='Dispatch Reports', format=','),
                alt.Tooltip('population:Q', title='Population', format=','),
                alt.Tooltip(f'{selected_crime}:Q', title='Normalized Ratio', format='.2f')
            ]
        ).properties(
            width=400,  
            height=300,
            title=f"Crime Reports vs Dispatches: {selected_crime.title()}"
        ).add_selection(brush)
        
        # Regression analysis
        X = gdf[[dispatch_col]]
        y = gdf[crime_col]
        lr = LinearRegression()
        lr.fit(X, y)
        r2 = r2_score(y, lr.predict(X))
        
        # Create regression line
        x_range = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
        y_pred = lr.predict(x_range)
        regression_df = pd.DataFrame({'x': x_range.flatten(), 'y': y_pred})
        
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
            fontSize=16,
            dx=5,
            dy=5  
        ).encode(
            x=alt.value(50),
            y=alt.value(25),
            text='text:N'
        )
        
        # Map with improved linking
        map_chart = alt.Chart(geo).mark_geoshape(
            stroke='white', 
            strokeWidth=1
        ).transform_lookup(
            lookup='properties.tract',
            from_=lookup_data
        ).encode(
            opacity=alt.condition(brush, alt.value(1), alt.value(0.2)),
            color=alt.Color(f'properties.{selected_crime}:Q', 
                scale=alt.Scale(
                    domain=[-1, 0, 1],
                    range=['rgb(255,0,0)', 'rgb(255,255,255)', 'rgb(0,0,255)']
                ),
                title="Dispatch vs Crime Ratio"),
            tooltip=[
                alt.Tooltip('properties.tract:N', title='Census Tract'),
                alt.Tooltip(f'{crime_col}:Q', title='Crime Reports', format=','),
                alt.Tooltip(f'{dispatch_col}:Q', title='Dispatches', format=','),
                alt.Tooltip(f'properties.{selected_crime}:Q', title='Normalized Ratio', format='.2f')
            ]
        ).properties(
            width=400,
            height=400,
            title="Geographic Distribution"
        )
        
       
        top_chart = alt.layer(scatter, regression, r_2_annotation)
        bottom_chart = map_chart
        final_viz = alt.vconcat(
            bottom_chart,
            top_chart
        ).configure_view(
            stroke=None 
        ).configure_title(
            fontSize=16,
            anchor='middle'
        )

        return final_viz
        
    except Exception as e:
        logger.error(f"Error creating visualization: {str(e)}")
        raise

def main():
    try:
        st.set_page_config(
            page_title="Geographic Comparison of Crime vs Dispatch Data",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        st.title("Geographic Comparison of Crime vs Dispatch Data")
        
        CRIME_TYPES = {
            'theft': 'Theft Reports',
            'drug': 'Drug-Related Incidents',
            'sexassult': 'Sexual Assault Reports',
            'parts': 'Auto Parts Theft',
            'violent': 'Violent Crime',
            'property': 'Property Crime',
            'person': 'Crimes Against Persons'
        }
        
        # Improved sidebar with descriptions
        st.sidebar.header("Data Selection")
        selected_crime = st.sidebar.selectbox(
            "Select Crime Type",
            options=list(CRIME_TYPES.keys()),
            format_func=lambda x: CRIME_TYPES[x]
        )
        
        st.sidebar.markdown("""
        ### About this Visualization
        This tool compares crime reports with police dispatches across census tracts.
        - :blue[**Blue areas**]: More crime reports than dispatches
        - **White areas**: Balanced ratio
        - :red[**Red areas**]: More dispatches than crime reports
        
        Use the brush tool to select areas in either view to highlight corresponding regions.
        
        :rainbow[***To do list***]

        **Short Explainer** 
        To give give an account of each type 

        **Annotations** 
        For map indicating location on scatter and map of
        - westfield shopping centre 
        - The village 
        - Police stations

        **Map edits** 
        - Carto b underlay
        - Zoom function 
        
    
        """)
        
        gdf, crime_col, dispatch_col, geo = load_and_prepare_data(selected_crime)
        viz = create_linked_visualization(gdf, selected_crime, crime_col, dispatch_col, geo)
        
        st.altair_chart(viz, use_container_width=True)
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        logger.error(f"Application error: {str(e)}")

if __name__ == "__main__":
    main()