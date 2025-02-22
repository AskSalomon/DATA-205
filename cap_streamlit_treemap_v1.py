from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np
import logging
import plotly.graph_objects as go


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
def data_loader():
    try:
        file_path = '/Users/gimle/DATA-205/capstone_streamlit_treemap.csv'
        df_treemap = pd.read_csv(file_path)
        reverse_match_dict = {1 :'Dispatch', 2: 'Crime', 3:'Match'}
        df_treemap['match_status'] = df_treemap['match_status'].map(reverse_match_dict)
    
        return df_treemap
    except Exception as e:
        logger.error(f'error in loading: {str(e)}')
        raise e

def treemap(df_treemap, selection):
    try:
# I need df_treemap, selection
# Group data by match_status and my selection
        grouped_data = df_treemap.groupby(['match_status', selection ]).size().reset_index(name='count')

        labels = []
        parents = []
        values = []

        for parent in grouped_data['match_status'].unique():
            labels.append(parent)
            parents.append('Montgomery County')
            values.append(grouped_data[grouped_data['match_status'] == parent]['count'].sum())
    
            children = grouped_data[grouped_data['match_status'] == parent]
            for _, row in children.iterrows():
                labels.append(f"{row[selection]}")
                parents.append(parent)
                values.append(row['count'])


        treemap = go.Figure(go.Treemap(
            labels=labels,
            parents=parents,
            values=values,
            textinfo="label+value",
            branchvalues="total"
        ))

        treemap.update_layout(
            title='Treemap of the number of Dispatches and Crime Reports with Matching ID`s by ',
            width=900,
            height=700,
            treemapcolorway=["#636efa","#EF553B", "#00cc96"], # fix colour palette
            margin=dict(t=50, l=25, r=25, b=25)
        )

        return treemap
    except Exception as e: 
        logger.error('error in treemap function', exc_info=True)
        raise



def main():
    try:
        st.set_page_config(
            page_title="Exploring the combined dataset",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        types = {'category':'Crime Type', 'Police_district_Number' :'Police District', 'Priority':'Priority', 'Agency':'Police Agency'}

        st.title("Treemap of the combined dataset of Crime Reports and Dispatches")
        
        # Improved sidebar with descriptions
        st.sidebar.header("Data Selection")
        selection = st.sidebar.selectbox(
            "Select a subgroup to explore",
            options=list(types.keys()),
            format_func=lambda x: types[x]
        )
        
        st.sidebar.markdown("""
        ## About this Treemap
        This Treemap compares how the selected subgroup is present in the combined dataset of Crime Reports and Dispatches.
        ### How the Datasets were joined 
        When a dispatch is created, a unique identifier is carried over to the crime report. 
        It is this identifier that was used to join the two datasets. 
        Ideally, each crime report should have a corresponding dispatch. However, this is not always the case.
        It is therefore useful to explore the data to understand the ways in which they are and are not related. 
        ### What to look for 
        - **Police Districts**: Takoma PD, does not share dispatch data, and therefore only appears in the crime reports dataset. 
        - **Crime Type**: 
        - **Priority**: Is only present in the dispatch dataset. Therefore will not appear in the crime reports dataset. 
        - **Police Agency**:
        """)

        st.plotly_chart(treemap(data_loader(), selection))


    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        logger.error(f"Application error: {str(e)}")

if __name__ == "__main__":
    main()