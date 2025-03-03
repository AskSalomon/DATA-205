import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib_venn import venn3, venn3_circles
import numpy as np

# List definitions
transformed_list = [ 
    'Agency',
    'Place', 
    'Type Change',
    'match_status', 
    'hour',
    'month',
    'day',
    'year',
    'category'
]
merged_list = [ 
    'long', 'lat', 'PRA', 'ID',
    'Start_Time', 'Police_district_Number', 
    'category'
]
join_list = ['Incident_ID']
# original datasets: dispatch, crime, census
census_list = ['population','STATEFP', 'COUNTYFP', 'tract', 'GEOID', 'NAME', 'NAMELSAD', 'MTFCC',
   'FUNCSTAT', 'ALAND', 'AWATER', 'INTPTLAT', 'INTPTLON', 'geometry']
dispatch_list = ['Incident_ID', 'Crime Reports', 'Crash Reports', 'Start Time',
   'End Time', 'Priority', 'Initial Type', 'Close Type', 'Address', 'City',
   'State', 'Zip', 'Longitude', 'Latitude', 'Police District Number',
   'Beat', 'PRA', 'CallTime CallRoute', 'Calltime Dispatch',
   'Calltime Arrive', 'Calltime Cleared', 'CallRoute Dispatch',
   'Dispatch Arrive', 'Arrive Cleared', 'Disposition Desc', 'Location']
crime_list = ['Incident ID', 'Offence Code', 'CR Number', 'Dispatch Date / Time',
   'Start_Date_Time', 'End_Date_Time', 'NIBRS Code', 'Victims',
   'Crime Name1', 'Crime Name2', 'Crime Name3', 'Police District Name',
   'Block Address', 'City', 'State', 'Zip Code', 'Agency', 'Place',
   'Sector', 'Beat', 'PRA', 'Address Number', 'Street Prefix',
   'Street Name', 'Street Suffix', 'Street Type', 'Latitude', 'Longitude',
   'Police District Number', 'Location']
# created datasets: treemap, choropleth, line
joined_list = ['Offence Code',  'Victims', 'Crime Name1', 'Crime Name2',
   'Agency', 'Place',  'Priority', 'Type Change',
   'long', 'lat', 'PRA', 'Incident_ID', 'match_status',  
   'Start_Time', 'Police_district_Number', 'hour', 'month', 'day', 'category']
choropleth1_list = ['category','population', 'tract','GEOID', 'MTFCC', 'FUNCSTAT', 'ALAND',
   'AWATER', 'INTPTLAT', 'INTPTLON', 'geometry']
choropleth2_list = ['category','population', 'tract','GEOID', 'MTFCC', 'FUNCSTAT', 'ALAND',
   'AWATER', 'INTPTLAT', 'INTPTLON', 'geometry']
line_list = ['ID', 'Start_Time', 'Police_district_Number', 'category', 'match_status','year',
     'month','Crime Name1', 'Crime Name2', 'Victims','Agency']
treemap_list = ['Agency', 'Priority', 'match_status', 'Police_district_Number',
   'category']
# list of datasets
datasets_list = ['dispatch', 'crime', 'joined', 'treemap', 'choropleth1','choropleth2','line', 'census']


def data_loader():
    # Load the data
    treemap = pd.read_csv('/Users/gimle/DATA-205/capstone_streamlit_treemap_short.csv')
    joined = pd.read_csv('/Users/gimle/DATA-205/capstone_streamlit_joined_short.csv')
    choropleth1 = pd.read_csv('/Users/gimle/DATA-205/capstone_streamlit_choropleth1_short.csv')
    choropleth2 = pd.read_csv('/Users/gimle/DATA-205/capstone_streamlit_choropleth2_short.csv')
    census  = pd.read_csv('/Users/gimle/DATA-205/capstone_streamlit_census_short.csv')
    dispatch = pd.read_csv('/Users/gimle/DATA-205/capstone_streamlit_dispatch_short.csv')
    crime = pd.read_csv('/Users/gimle/DATA-205/capstone_streamlit_crime_short.csv')
    line = pd.read_csv('/Users/gimle/DATA-205/capstone_streamlit_linemap_short.csv')
    return dispatch, crime, census, joined, treemap, choropleth1, choropleth2, line 
    

def color_columns(df, transformed_list, merged_list, join_list, census_list, dispatch_list, crime_list):
    # Create a list of CSS properties for each column
    styles = []
    
    for col in df.columns:
        if col in transformed_list:
            styles.append({'selector': f'th.col{df.columns.get_loc(col)}', 
                           'props': [('background-color', 'purple'), ('color', 'white')]})
        elif col in merged_list:
            styles.append({'selector': f'th.col{df.columns.get_loc(col)}', 
                           'props': [('background-color', 'green'), ('color', 'white')]})
        elif col in join_list:
            styles.append({'selector': f'th.col{df.columns.get_loc(col)}', 
                           'props': [('background-color', 'orange'), ('color', 'black')]})
        elif col in census_list:
            styles.append({'selector': f'th.col{df.columns.get_loc(col)}', 
                           'props': [('background-color', 'red'), ('color', 'white')]})
        elif col in dispatch_list:
            styles.append({'selector': f'th.col{df.columns.get_loc(col)}', 
                           'props': [('background-color', 'yellow'), ('color', 'black')]})
        elif col in crime_list:
            styles.append({'selector': f'th.col{df.columns.get_loc(col)}', 
                           'props': [('background-color', 'blue'), ('color', 'white')]})
    
    # Apply styles
    return df.style.set_table_styles(styles)


def create_venn_diagram():
    # Create a figure
    fig, ax = plt.subplots(figsize=(10, 6))
    

    colors = {
        'dispatch': 'yellow',  
        'crime': 'blue',       
        'census': 'red',       
        'overlap': 'green'     
    }
    

    v = venn3(
        subsets=(1, 1, 1, 1, 1, 1, 1),
        set_labels=('Dispatch', 'Crime', 'Census'),
        ax=ax,
        set_colors=(colors['dispatch'], colors['crime'], colors['census'])
    )
    
    for text in v.set_labels:
        text.set_fontsize(14)
        text.set_fontweight('bold')
    
 
    # A: Dispatch only
    v.get_label_by_id('100').set_text('Priority\nClose Type')
    
    # B: Crime only  
    v.get_label_by_id('010').set_text('Agency\nPlace\nCrime Name')
    
    # C: Census only
    v.get_label_by_id('001').set_text('Population\nGeometry')
    
    # A&B: Dispatch & Crime
    v.get_label_by_id('110').set_text('Incident_ID')
    v.get_patch_by_id('110').set_color('orange')  # Join column color
    
    # A&C: Dispatch & Census
    v.get_label_by_id('101').set_text('')
    
    # B&C: Crime & Census
    v.get_label_by_id('011').set_text('Geometry Overlay')
    
    # A&B&C: All three
    v.get_label_by_id('111').set_text('Derived Data\nhour, month, day\ncategory')
    v.get_patch_by_id('111').set_color('purple')  # Transformed columns
    

    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='yellow', markersize=15, label='Dispatch Columns'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=15, label='Crime Columns'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=15, label='Census Columns'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='orange', markersize=15, label='Join Columns'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=15, label='Merged Columns'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='purple', markersize=15, label='Transformed Columns')
    ]
    
    ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=3)
    
    plt.tight_layout()
    
    return fig


def explainer(selected_dataset): 
    speech_dictionary = {
        'dispatch':
        """
        The dispatch dataset contains the following columns:
        - **Incident_ID**: Unique identifier for each incident 
        - **Crime Reports**: Another identifier connecting with crime reports
        - **Crash Reports**: Identifier for crash reports
        - **Start Time**: Time when the incident was reported
        - **End Time**: Time when the dispatch was resolved
        - **Priority**: Priority of the dispatch
        - **Initial Type**: Initial type of the dispatch
        - **Close Type**: Final type of the dispatch
        - **Address**: Location of the dispatch
        - **City**: City where the dispatch occurred
        - **State**: State where the dispatch occurred
        - **Zip**: Zip code of the dispatch
        - **Longitude**: Longitude of the dispatch
        - **Latitude**: Latitude of the dispatch
        - **Police District Number**: Identifier for the police district
        - **Beat**: Identifier for the beat
        - **PRA**: Identifier for the PRA  
        - **CallTime CallRoute**: Time when the call was routed
        - **Calltime Dispatch**: Time when the call was dispatched
        - **Calltime Arrive**: Time when the call arrived
        - **Calltime Cleared**: Time when the call was cleared
        - **CallRoute Dispatch**: Route of the call dispatch
        - **Dispatch Arrive**: Time when the dispatch arrived
        - **Arrive Cleared**: Time when the arrival was cleared
        - **Disposition Desc**: Description of the disposition
        - **Location**: Location of the dispatch
        """,
        'crime':
        """
        The crime dataset contains the following columns:
        - **Incident ID**: Unique identifier for each incident
        - **Offence Code**: Code for the offence, this is in NIBRS format
        - **CR Number**: Crime report number
        - **Dispatch Date / Time**: Time when the dispatch was made
        - **Start_Date_Time**: Time when the crime is reported to have started, this can be backdated in case of events that happend in the past
        - **End_Date_Time**: Time when the crime report was closed
        - **NIBRS Code**: Code for the offence in NIBRS format
        - **Victims**: Number of victims
        - **Crime Name1**: This first column, as one of four options, crime against society, crime against person, crime against property or not a crime
        - **Crime Name2**: This second column, has 55 options, describing the crime more closely 
        - **Crime Name3**: This third column, 
        - **Police District Name**: Name of the police district
        - **Block Address**: Address of the crime. This address has been block rounded, and the marker placed in the center of the block before the data is made available to the public
        - **City**: City where the crime occurred
        - **State**: State where the crime occurred. Usually maryland, but with some interesting exceptions not explored in this analysis
        - **Zip Code**: Zip code of the crime
        - **Agency**: Agency that was assigned to the crime report, either MCPD, Takoma Park PD, Rockville PD, or Gaithersburg PD
        - **Place**: A description of the place where the crime occurred. 
        - **Sector**: Sector of the police district
        - **Beat**: Beat of the police district
        - **PRA**: PRA of the police district
        - **Address Number**: Address number of the crime, block rounded
        - **Street Prefix**: Prefix of the street
        - **Street Name**: Name of the street
        - **Street Suffix**: Suffix of the street
        - **Street Type**: Type of the street, whether it is a road, street, avenue, etc.
        - **Latitude**: Latitude of the crime
        - **Longitude**: Longitude of the crime
        - **Police District Number**: The police district
        - **Location**: Location of the crime
        """,
        'joined':
        """
        The joined dataset contains the following columns:
        - **Offence Code**: Code for the offence, this is in NIBRS format
        - **Victims**: Number of victims
        - **Crime Name1**: This first column, as one of four options, crime against society, crime against person, crime against property or not a crime
        - **Crime Name2**: This second column, has 55 options, describing the crime more closely
        - **Agency**: Agency that was assigned to the crime report, either MCPD, Takoma Park PD, Rockville PD, or Gaithersburg PD
        - **Place**: A description of the place where the crime occurred
        - **Priority**: Priority of the dispatch
        - **Type Change**: Whether the type of the dispatch changed between the initial and closed type
        - **long**: Longitude of the dispatch or crime, with preference for crime location with NA's filled in by dispatch location
        - **lat**: Latitude of the dispatch or crime, with preference for crime location with NA's filled in by dispatch location
        - **PRA**: PRA of the police district
        - **Incident_ID**: Unique identifier for each incident that is shared between the dispatch and crime datasets
        - **match_status**: Whether the incident had a match in the crime dataset or not 
        - **Start_Time**: Time when the incident was reported, I wanted to focus on incidients that took place between 2019 and 2024, and choose this as the date 
        - **Police_district_Number**: Identifier for the police district, preference towards crime, NA's filled in by dispatch
        - **hour**: Hour of the incident, from Start_Time
        - **month**: Month of the incident, from Start_Time
        - **day**: Day of the incident, from Start_Time
        - **category**: Category of the crime, by using a dictionary to map the crime names and dispatch closed type to categories and then merging the two
        """,
        'treemap':
        """
        The treemap dataset contains the following columns:
        - **Agency**: Agency that was assigned to the crime report, either MCPD, Takoma Park PD, Rockville PD, or Gaithersburg PD
        - **Priority**: Priority of the dispatch
        - **match_status**: Whether the incident had a match in the crime dataset or not
        - **Police_district_Number**: Identifier for the police district
        - **category**: Category of the crime
        """,
        'choropleth1':
        """
        The choropleth1 dataset contains the following columns:
        - **category**: Category of the crime
        - **population**: Population of the census tract
        - **tract**: Tract number
        - **GEOID**: GEOID of the census tract
        - **MTFCC**: MTFCC of the census tract
        - **FUNCSTAT**: Functional status of the census tract
        - **ALAND**: Land area of the census tract
        - **AWATER**: Water area of the census tract
        - **INTPTLAT**: Latitude of the census tract
        - **INTPTLON**: Longitude of the census tract
        - **geometry**: Geometry of the census tract
        """,
        'choropleth2':
        """
        The choropleth2 dataset contains the following columns:
        - **category**: Category of the crime
        - **population**: Population of the census tract
        - **tract**: Tract number
        - **GEOID**: GEOID of the census tract
        - **MTFCC**: MTFCC of the census tract
        - **FUNCSTAT**: Functional status of the census tract
        - **ALAND**: Land area of the census tract
        - **AWATER**: Water area of the census tract
        - **INTPTLAT**: Latitude of the census tract
        - **INTPTLON**: Longitude of the census tract
        - **geometry**: Geometry of the census tract
        """,
        'line':
        """
        The line dataset contains the following columns:
        - **ID**: Unique identifier for each incident
        - **Start_Time**: Time when the incident was reported
        - **Police_district_Number**: Identifier for the police district
        - **category**: Category of the crime or dispatch
        - **match_status**: Whether the incident had a match in the crime dataset or not
        - **year**: Year of the incident from 'Start_Time'
        - **month**: Month of the incident from 'Start_Time'
        - **Crime Name1**: This first column, as one of four options, crime against society, crime against person, crime against property or not a crime
        - **Crime Name2**: This second column, has 55 options, describing the crime more closely
        - **Victims**: Number of victims
        - **Agency**: Agency that was assigned to the crime report, either MCPD, Takoma Park PD, Rockville PD, or Gaithersburg PD
        """,
        'census':  
        """
        The census dataset contains the following columns:
        - **population**: Population of the census tract
        - **STATEFP**: State FIPS code
        - **COUNTYFP**: County FIPS code
        - **tract**: Tract number
        - **GEOID**: GEOID of the census tract
        - **NAME**: Name of the census tract
        - **NAMELSAD**: Name and legal/statistical area description of the census tract
        - **MTFCC**: MTFCC of the census tract
        - **FUNCSTAT**: Functional status of the census tract
        - **ALAND**: Land area of the census tract
        - **AWATER**: Water area of the census tract
        - **INTPTLAT**: Latitude of the census tract
        - **INTPTLON**: Longitude of the census tract
        - **geometry**: Geometry of the census tract
        """
    }

    speech = speech_dictionary[selected_dataset]
    return speech


def main(): 
    st.title("Data Breakdown")
    
 
 

    
    st.sidebar.markdown(
    """
    This page shows which columns of the original datasets have been transformed, merged or carried over from the three parent datasets.
    The color coding is as follows:
    - :violet[**Purple**]: Transformed columns
    - :green[**Green**]: Merged columns, between dispatch and crime
    - :red[**Red**]: For Census columns
    - :blue[**Blue**]: For Crime columns  
    - :orange[**Orange**]: For Dispatch columns
    - :gray[**Gray**]: Is the colour of the join column 
    """
    )
    dispatch, crime, census, joined, treemap, choropleth1, choropleth2, line = data_loader()
    dataset_mapping = {
        'dispatch': dispatch,
        'crime': crime,
        'census': census,
        'joined': joined,
        'treemap': treemap,
        'choropleth1': choropleth1,
        'choropleth2': choropleth2,
        'line': line
    }

    st.sidebar.header("Select a dataset to explore")
    selected_dataset = st.sidebar.selectbox(
        "Select a subgroup to explore",
        options=datasets_list
    )

    current_df = dataset_mapping[selected_dataset]
    styled_df = color_columns(
        current_df, 
        transformed_list, 
        merged_list, 
        join_list, 
        census_list, 
        dispatch_list, 
        crime_list
    )
    st.pyplot(create_venn_diagram())
    st.dataframe(styled_df)
    
    st.markdown(explainer(selected_dataset))

if __name__ == "__main__":
    main()