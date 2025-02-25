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
        #df_match_age=pd.read_csv('/Users/gimle/DATA-205/capstone_streamlit_linemap_agesum.csv') # might not need this one, assume unnecessary
        #df_match_victims=pd.read_csv('/Users/gimle/DATA-205/capstone_streamlit_linemap_victims.csv')

        return df_age_cn1,df_cn1_cn2,df_match_cat, # df_match_victims,df_match_age,
    except Exception as e:
        logger.error(f'error in loading: {str(e)}')
        raise e


def linemap_function(filtered_linegraph_dataset, selected_linegraph_first_value, linegraph_y_values, color_linegraph):
    try:
        linegraph_x_values = 'Year and Month'
        linegraph_dataset = filtered_linegraph_dataset.groupby(['month_year', selected_linegraph_first_value])['count'].sum().reset_index()
        linegraph_dataset['month_year'] = linegraph_dataset['month_year'].dt.to_timestamp()
        # Create a selection that chooses the nearest point & selects based on x-value


        nearest = alt.selection_point(nearest=True, on="mouseover", 
                                fields=["month_year"], empty=False)

        brush = alt.selection_interval(encodings=['x'])
        # The basic line
        line = alt.Chart(linegraph_dataset).mark_line(interpolate="basis").encode(
            x= alt.X('month_year:T', timeUnit='yearmonth', title= linegraph_x_values),
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


def annotations_linegraph(final_chart_linegraph, linegraph_y_column):
    try:

        match_annotations = pd.DataFrame([
            {'month_year': pd.Timestamp('2023-05'), 'note': 'Low'},
            {'month_year': pd.Timestamp('2023-06'), 'note': 'Peak'}
        ])
        
        Crime_Name1_annotations = pd.DataFrame([
            {'month_year': pd.Timestamp('2023-07'), 'note': 'Low'},
            {'month_year': pd.Timestamp('2023-09'), 'note': 'Peak'}
        ])
        
        Crime_Name2_annotations = pd.DataFrame([
            {'month_year': pd.Timestamp('2023-01'), 'note': 'Peak'},
            {'month_year': pd.Timestamp('2023-02'), 'note': 'Low'}
        ])
        
        Agency_annotations = pd.DataFrame([
            {'month_year': pd.Timestamp('2021-02'), 'note': 'Peak'},
            {'month_year': pd.Timestamp('2022-02'), 'note': 'Low'}
        ])
        
        Category_annotations = pd.DataFrame([
            {'month_year': pd.Timestamp('2020-07'), 'note': 'Low'},
            {'month_year': pd.Timestamp('2020-08'), 'note': 'Peak'}
        ])
        
        annotations_dict = {
            'match_status': match_annotations,
            'Crime Name1': Crime_Name1_annotations,
            'Crime Name2': Crime_Name2_annotations,
            'Agency': Agency_annotations,
            'category': Category_annotations,
        }
        
        annotation_data = annotations_dict.get(linegraph_y_column)
        
        if annotation_data is None:
            return final_chart_linegraph
        
        vertical_lines = alt.Chart(annotation_data).mark_rule(
            color='red',
            strokeWidth=1
        ).encode(
            x='month_year:T'
        )
        
        text_labels = alt.Chart(annotation_data).mark_text(
            align='center',
            baseline='bottom',
            fontSize=12,
            dy=-10,
            angle=0
        ).encode(
            x='month_year:T',
            text='note:N',
            color=alt.value('red')
        )
        
        return alt.layer(final_chart_linegraph, vertical_lines, text_labels)
        
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error('error in annotations linegraph', exc_info=True)
        raise

def main():
    try:
        

        LINEGRAPH = {
            'Agency and Crime Type 1': df_age_cn1,
            'Crime Type 1 & 2': df_cn1_cn2, 
            'Match and Category': df_match_cat
        }

        selected_linegraph_key, selected_lingraph_dataset = get_selected_linegraph(LINEGRAPH)
        filter_linegraph_columns = get_filter_column_options(selected_linegraph_dataset)
        selected_filter_column = select_filter_column(selected_dataset, filter_linegraph_columns)

        st.sidebar.header('First Select Data Set')
        selected_linegraph_dataset = st.sidebar.selectbox(
            "Select from one of these 3 options",
            options=list(LINEGRAPH.keys()),
            format_func_linegraph=lambda x: LINEGRAPH[x]
        )

        status_options_linegraph = selected_linegraph_dataset[selected_linegraph_first_value].unique()
        selected_statuses_linegraph = []

        st.write("Select Data:")
        for status in status_options_linegraph:
            if st.checkbox(status_linegraph, value=True):
                selected_statuses_linegraph.append(status)

        filter_option = st.selectbox(
        'Select Match Status:',
        options=['All'] + list(selected_linegraph_dataset['match_status'].unique()),
        index=0
        )

        # Annotations selector here: I want on or off swtich
        show_annotations = toggle_annotations()

        if filter_option == 'All':
            filtered_linegraph_dataset = selected_linegraph_dataset
        else:
            filtered_linegraph_dataset = selected_linegraph_dataset[selected_linegraph_dataset[values_selected_from_select] == filter_option]

        



        st.set_page_config(
            page_title="Graphing dispatches and crime reports over time",
            layout="wide",
            initial_sidebar_state="expanded"
        )

        

        # Sidebar text
        st.sidebar.markdown("""
        ## About this visualistion

        """)

        # Body text
        st.markdown(
        """
        
        """
        )
        



    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        logger.error(f"Application error: {str(e)}")

if __name__ == "__main__":
    main()