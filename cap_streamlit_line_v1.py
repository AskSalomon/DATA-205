from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np
import logging
import altair as alt


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

def data_loader():
    try:
#'https://raw.githubusercontent.com/AskSalomon/DATA-205/refs/heads/main/capstone_streamlit_scattermap_topo.json'

        df_age_cn1=pd.read_csv('/Users/gimle/DATA-205/capstone_streamlit_linemap_agecn1.csv')
        df_cn1_cn2=pd.read_csv('/Users/gimle/DATA-205/capstone_streamlit_linemap_cn1cn2.csv')
        df_match_cat=pd.read_csv('/Users/gimle/DATA-205/capstone_streamlit_linemap_catsum.csv')
        df_match_age=pd.read_csv('/Users/gimle/DATA-205/capstone_streamlit_linemap_agesum.csv')
        df_match_victims=pd.read_csv('/Users/gimle/DATA-205/capstone_streamlit_linemap_victims.csv')

        return df_age_cn1,df_cn1_cn2,df_match_age,df_match_cat,df_match_victims
    except Exception as e:
        logger.error(f'error in loading: {str(e)}')
        raise e


def linemap_function(selected_linegraph_dataset, selected_linegraph_first_value, linegraph_x_values, linegraph_y_values, color_linegraph):
    try:

        linegraph_dataset = selected_linegraph_dataset.groupby(['month_year', selected_linegraph_first_value])['count'].sum().reset_index()
        linegraph_dataset['month_year'] = linegraph_dataset['month_year'].dt.to_timestamp()
        # Create a selection that chooses the nearest point & selects based on x-value


        nearest = alt.selection_point(nearest=True, on="mouseover", 
                                fields=["month_year"], empty=False)

        brush = alt.selection_interval(encodings=['x'])
        # The basic line
        line = alt.Chart(linegraph_dataset).mark_line(interpolate="basis").encode(
            x= alt.X('month_year:T', timeUnit='yearmonth', title= lingegraph_x_values),
            y= "count:Q",
            color= alt.Color(f'{selected_linegraph_first_value}:N').title(color_linegraph)
        )

        # Transparent selectors across the chart. This is what tells us  x value of the cursor
        selectors = alt.Chart(linegraph_dataset).mark_point().encode(
            x= alt.X('month_year:T', timeUnit='yearmonth'),
            opacity= alt.value(0),
        ).add_selection(nearest)

        # Draw points on the line, and highlight based on selection
        points = line.mark_point().encode(
            opacity=alt.condition(nearest, alt.value(1), alt.value(0))
        )

        # Draw text labels near the points, and highlight based on selection
        text = line.mark_text(align="left", dx=5, dy=-5).encode(
            text=alt.condition(nearest,"count:Q", alt.value(" "))
        )

        # Draw a rule at the location of the selection
        rules = alt.Chart(linegraph_dataset).mark_rule(color="gray").encode(
            x= alt.X('month_year:T', timeUnit='yearmonth'),
        ).transform_filter(
            nearest
        )

        main_chart_linegraph = alt.layer(
            line, selectors, points, rules, text,
        ).properties(
            width=600, height=300
        ).transform_filter(
            brush
        )

        time_selector = alt.Chart(linegraph_dataset).mark_area().encode(
            x=alt.X('month_year:T', timeUnit='yearmonth', title = linegraph_x_values),
            y=alt.Y('count:Q', aggregate='sum', title = linegraph_y_values),
            color=f'{selected_linegraph_first_value}:N'
        ).properties(
            height=60
        ).add_params(
            brush
        )

        final_chart_linegraph = alt.vconcat(
            main_chart_linegraph,
            time_selector.properties(width=600)
        )


        return final_chart_linegraph
    except Exception as e: 
        logger.error('error in line function', exc_info=True)
        raise


def annotations_linegraph()
    try:

                # Very unfinished
        lingegraph_large_title = 'Linegraph schminegraph' # this should change 
        linegraph_small_title = 'use the brush tool to select points in time' 
        color_linegraph = 'Match'
        lingegraph_y_values = 'Number of entries'
        linegraph_x_values = 'Year & Month'


        annotations_df = pd.DataFrame([
            {'month_year': pd.Timestamp('2023-05-01'), 'count': 150, 'note': 'Peak activity'},
            {'month_year': pd.Timestamp('2023-01-01'), 'count': 50, 'note': 'New year drop'}
        ])



        return annotations_linegraph
    except Exception as e:
        logger.error('error in annotations linegraph', exc_info = True)
        raise

def filter_linegraph():
    try:




        return
    except Exception as e: 
        logger.error('error in filtering', exc_info = True)
        raise
    
def main():
    try:
        data_loader()

        # For multiple selection with checkboxes
        status_options = match_cat_graph['match_status'].unique()
        selected_statuses = []

        st.write("Select Match Statuses to Display:")
        for status in status_options:
            if st.checkbox(status, value=True):
                selected_statuses.append(status)

        # Filter based on multiple selections
        filtered_data = match_cat_graph[match_cat_graph['match_status'].isin(selected_statuses)]

        filter_option = st.selectbox(
        'Select Match Status:',
        options=['All'] + list(match_cat_graph['match_status'].unique()),
        index=0
        )

        if filter_option == 'All':
            filtered_data = match_cat_graph
        else:
            filtered_data = match_cat_graph[match_cat_graph['match_status'] == filter_option]


        # match_cat_graph is an example, insert selectbox here
        selected_linegraph_dataset = cn1_cn2_sum
        selected_linegraph_first_value = 'Crime Name2'

        st.set_page_config(
            page_title="Graphing dispatches and crime reports over time",
            layout="wide",
            initial_sidebar_state="expanded"
        )

        st.title("Graphing Crime Reports and Dispatches over time")
        

        # Sidebar text
        st.sidebar.markdown("""
        ## About this visualistion

        """)

        # Body text
        st.markdown(
        """
        
        """
        )
        
        crime_linemap_function(), dispatch_linemap_function(), 


    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        logger.error(f"Application error: {str(e)}")

if __name__ == "__main__":
    main()