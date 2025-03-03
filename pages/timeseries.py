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

        df_age_cn1 = pd.read_csv('https://raw.githubusercontent.com/AskSalomon/DATA-205/refs/heads/main/capstone_streamlit_linemap_agecn1.csv')
        df_cn1_cn2 = pd.read_csv('https://raw.githubusercontent.com/AskSalomon/DATA-205/refs/heads/main/capstone_streamlit_linemap_cn1cn2.csv')
        df_match_cat = pd.read_csv('https://raw.githubusercontent.com/AskSalomon/DATA-205/refs/heads/main/capstone_streamlit_linemap_catsum.csv')
        df_cn2 = pd.read_csv("https://raw.githubusercontent.com/AskSalomon/DATA-205/refs/heads/main/capstone_streamlit_linemap_cn2.csv")

        return df_age_cn1, df_cn1_cn2, df_match_cat, df_cn2
    except Exception as e:
        logger.error(f'error in loading: {str(e)}')
        raise e


def linemap_function(filtered_linegraph_dataset, selected_linegraph_first_value, linegraph_y_values, color_linegraph, show_annotations=False, annotation_data=None):
    ''' Most of the code came originally from the example on Vega-ALtairs pages, which can be found here: 
    https://altair-viz.github.io/gallery/multiline_tooltip.html#gallery-multiline-tooltip
    https://altair-viz.github.io/gallery/multiline_tooltip_standard.html
    '''
    try:
        linegraph_x_values = 'Year and Month'
        linegraph_dataset = filtered_linegraph_dataset.groupby(['month_year', selected_linegraph_first_value])['count'].sum().reset_index()
        if pd.api.types.is_period_dtype(linegraph_dataset['month_year']):
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

        

        # Create main chart with all layers
        main_layers = [line, selectors, points, rules, text]
        
        # Add annotation layers to main chart if enabled
        if show_annotations and annotation_data is not None:
            vertical_lines = alt.Chart(annotation_data).mark_rule(
                color='blue',
                strokeWidth=1
            ).encode(
                x='month_year:T'
            )
            
            text_labels = alt.Chart(annotation_data).mark_text(
                align='center',
                baseline='top',
                fontSize=12,
                dy= 10,
                angle=0
            ).encode(
                x='month_year:T',
                text='note:N',
                color=alt.value('orange')
            )
            
            main_layers.extend([vertical_lines, text_labels])
        
        main_chart_linegraph = alt.layer(*main_layers).properties(
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


def get_annotation_data(linegraph_y_column):
    try:
        match_annotations = pd.DataFrame([
            {'month_year': pd.Timestamp('2018-12'), 'note': 'Year end'},
            {'month_year': pd.Timestamp('2019-12'), 'note': 'Year end'},
            {'month_year': pd.Timestamp('2020-12'), 'note': 'Year end'},
             {'month_year': pd.Timestamp('2021-12'), 'note': 'Year end'},
            {'month_year': pd.Timestamp('2022-12'), 'note': 'Year end'},
             {'month_year': pd.Timestamp('2023-12'), 'note': 'Year end'},
             {'month_year': pd.Timestamp('2024-9'), 'note': 'End of Data'}
        ])
        
        Crime_Name1_annotations = pd.DataFrame([
            {'month_year': pd.Timestamp('2023-05'), 'note': 'Data dip start'},
            {'month_year': pd.Timestamp('2024-04'), 'note': 'Data dip end'}
        ])
        
        Crime_Name2_annotations = pd.DataFrame([
            {'month_year': pd.Timestamp('2023-05'), 'note': 'Data dip start'},
            {'month_year': pd.Timestamp('2024-04'), 'note': 'Data dip end'}
        ])
        
        Agency_annotations = pd.DataFrame([
            {'month_year': pd.Timestamp('2021-02'), 'note': 'Covid dip 3'},
            {'month_year': pd.Timestamp('2020-04'), 'note': 'Covid dip 2'},
            {'month_year': pd.Timestamp('2019-02'), 'note': 'Covid dip 1'},
            {'month_year': pd.Timestamp('2019-02'), 'note': 'Covid dip 1'}
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
        
        return annotations_dict.get(linegraph_y_column)
        
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error('error in getting annotation data', exc_info=True)
        return None

def main():
    try:
        
        st.set_page_config(
            page_title="Graphing dispatches and crime reports over time",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        # DATASET LOADER 
        df_age_cn1, df_cn1_cn2, df_match_cat, df_cn2 = data_loader()
        
        # Dictionary because this got complicated 
        LINEGRAPH = {
            'Agency': df_age_cn1,
            'Crime Type 1': df_cn1_cn2, 
            'Match Status': df_match_cat,
            'Crime Name 2': df_cn2  # Added the new dataset
        }

        # SIDEBAR
        st.sidebar.markdown("""
        ## About this visualistion
        This timeseries displays the levels of the chosen columns over time                    
       
        Click the 'show annotations buttons to see aditional insights into the graphic'
        
        """
        )
        st.sidebar.header('First Select Data Set')
        selected_linegraph_key = st.sidebar.selectbox(
            "Select from one of these 4 options",  # Updated to reflect 4 options
            options=list(LINEGRAPH.keys()),
        )
      
        selected_linegraph_dataset = LINEGRAPH[selected_linegraph_key]
        
        if 'month_year' in selected_linegraph_dataset.columns and not pd.api.types.is_datetime64_any_dtype(selected_linegraph_dataset['month_year']):
            selected_linegraph_dataset['month_year'] = pd.to_datetime(selected_linegraph_dataset['month_year'])
        

        if selected_linegraph_key == 'Agency':
            selected_linegraph_first_value = 'Agency'
            linegraph_y_values = 'Crime Counts by Agency'
            color_linegraph = 'Agency'
        elif selected_linegraph_key == 'Crime Type 1':
            selected_linegraph_first_value = 'Crime Name1'
            linegraph_y_values = 'Crime Counts by Crime Type'
            color_linegraph = 'Crime Type'
        elif selected_linegraph_key == 'Crime Name 2':  # Added new condition for Crime Name 2
            selected_linegraph_first_value = 'Crime Name2'
            linegraph_y_values = 'Crime Counts by Crime Name 2'
            color_linegraph = 'Crime Name 2'
        else:  # 'Match Status'
            selected_linegraph_first_value = 'match_status'
            linegraph_y_values = 'Crime Counts by Match Status'
            color_linegraph = 'Match Status'

        st.sidebar.header(f'Filter by {selected_linegraph_first_value}')
        status_options_linegraph = selected_linegraph_dataset[selected_linegraph_first_value].unique()
        selected_statuses_linegraph = []

        st.sidebar.write(f"Select {selected_linegraph_first_value} values:")
        for status in status_options_linegraph:
            if st.sidebar.checkbox(str(status), value=True, key=f"status_{status}"):
                selected_statuses_linegraph.append(status)

        if selected_statuses_linegraph:
            filtered_linegraph_dataset = selected_linegraph_dataset[
                selected_linegraph_dataset[selected_linegraph_first_value].isin(selected_statuses_linegraph)
            ]
        else:
            filtered_linegraph_dataset = selected_linegraph_dataset
            st.warning(f"No {selected_linegraph_first_value} values selected. Showing all data.")

        show_annotations = st.sidebar.checkbox("Show annotations", value=False)
      

        annotation_data = None
        if show_annotations:
            annotation_data = get_annotation_data(selected_linegraph_first_value)

        final_chart_linegraph = linemap_function(
            filtered_linegraph_dataset, 
            selected_linegraph_first_value, 
            linegraph_y_values, 
            color_linegraph,
            show_annotations,
            annotation_data
        )
            
        st.altair_chart(final_chart_linegraph, use_container_width=True)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        logger.error(f"Application error: {str(e)}", exc_info=True)


if __name__ == "__main__":
    main()