import streamlit as st
import pandas as pd
from plotly import express as px
from PIL import Image

container = st.container()
col1,col2 = st.columns(2)


@st.cache_data
def load_data(file):
    return pd.read_csv(file)


# Functions for Filtering section ...........
# to print top N rows  
def top_n_rows(df):
    st.sidebar.header('data filtering'.upper())
    nrows = st.sidebar.number_input("Top N Rows", min_value=5, max_value=df.shape[0])
    return nrows
    
# to choose only selected columns 
def display_columns(df):
    columns = st.sidebar.multiselect("Choose Columns:", df.columns)
    return columns
       
# sorting data by user's choice 
def sort_data(df):
    cols = [None]
    for colns in df.columns:
        cols.append(colns)

    sort_column = st.sidebar.selectbox("Sort by", cols)
    order = st.sidebar.selectbox('Order', ['Ascending', 'Descending'])
    return sort_column, order


# Functions for Grouping Section ..........
aggregate_functions = ['count', 'sum', 'mean', 'median', 'min', 'max', 'std', 'var']

def group_by(df):
    st.sidebar.header('data grouping'.upper())
    grouped_column = st.sidebar.selectbox("Column to Group by ", df.columns)
    aggregate = st.sidebar.multiselect('Aggregate By ', aggregate_functions)
    return grouped_column, aggregate

def sel_colns(df):
    colns = st.sidebar.multiselect('Choose Columns: ', df.columns)
    return colns

def top_n_grps(grp_data):
    ngrps= st.sidebar.number_input("Top N Groups", min_value=5, max_value=grp_data.ngroups)
    return ngrps

def get_grps(grp_data):
    grps = [None]
    for name, info in grp_data:
        grps.append(name)

    grps = st.sidebar.selectbox("Choose Group ", grps)
    return grps


def analyze_data(data):
    # Perform basic data analysis
    container.markdown("# DATA ANALYSIS .....")
    container.markdown('## ')
      
    with col1:
       st.write("### Number of rows:", data.shape[0])

    with col2:   
       st.write("### Number of columns:", data.shape[1])
    
    st.empty()   
    with col1:
       st.write("Columns Names ", data.columns)

    with col1: 
       st.write("Columns Data Types ", data.dtypes)

    with col2:
       st.write("Missing Values ", data.isnull().sum())
   
    with col2:
       st.write("Unique Values ", data.nunique())


    try:     
        # Code for Filtering section
        container.markdown('### Basic Analysis of your Data 🕵️')
        nrows = top_n_rows(data)
        columns = display_columns(data)
        sorted_coln, order = sort_data(data)

        if len(columns) > 0:
            if sorted_coln is not None:
                if order == 'Ascending':
                    data2 = data.sort_values(by=sorted_coln)
                    container.write(data2[columns].head(nrows))
                else:
                    data2 = data.sort_values(by=sorted_coln, ascending=False)
                    container.write(data2[columns].head(nrows))

            else:
                container.write(data[columns].head(nrows))
        else:
            if sorted_coln is not None:
                if order == 'Ascending':
                    data1 = data.sort_values(by=sorted_coln)
                    container.write(data1.head(nrows))
                else:
                    data1 = data.sort_values(by=sorted_coln, ascending=False)
                    container.write(data1.head(nrows))
            else:
                container.write(data.head(nrows))
        
       
        # Code for Grouping section
        container.markdown('### Analyze your Data by grouping 🕵️')
        grp_col, agg_fns = group_by(data)
        grp_data = data.groupby(grp_col)
    
        colns = sel_colns(data)
        get_grp = get_grps(grp_data)
        ngrps = top_n_grps(grp_data=grp_data)

        if len(colns) > 0:
            if get_grp is not None:
                grp_df = grp_data.get_group(get_grp) 
                container.write(grp_df[colns].agg(agg_fns))
            else:
                container.write(grp_data[colns].agg(agg_fns).head(ngrps))
        else:
            if get_grp is not None:
                grp_df = grp_data.get_group(get_grp) 
                container.write(grp_df.agg(agg_fns))
            else:
                container.write(grp_data.agg(agg_fns).head(ngrps))


        # Descriptive Analysis 
        container.write('### Descriptive Analysis')
        container.write('Description')
        container.write(data.describe())

        container.write('Correletion')
        container.write(data.corr())

    except Exception as error:
        container.write(error)
    
    # code for this function completes here 



# FUNCTIONS FOR DATA VISUALIZATION SECTION
def top_n_sections(data):
    st.sidebar.header('data filtering'.upper())
    nsections= st.sidebar.number_input("Top N Sections", min_value=5, max_value=data.shape[0])
    return nsections


def sort_by2(data):
    cols = [None]
    for colns in data.columns:
        cols.append(colns)

    sort_column = st.sidebar.selectbox("Sort by", cols)
    order = st.sidebar.selectbox('Order', ['Ascending', 'Descending'])
    return sort_column, order


def display_chart(data, chart, x_axis, y_axis, xlbl, ylbl):
    # creating charts
    if chart == 'Bar':
        fig = px.bar(data, x=x_axis, y=y_axis, title=f'{xlbl} by {ylbl}', text=y_axis,
                      labels={'x': xlbl, 'y': ylbl})
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig)

    elif chart == 'Line':
        fig = px.line(data, x_axis, y_axis, title=f'{xlbl} by {ylbl}', labels={'x': xlbl, 'y': ylbl}) 
        st.plotly_chart(fig)

    elif chart == 'Scatter':
        fig = px.scatter(data, x_axis, y_axis, title=f'{xlbl} by {ylbl}', labels={'x': xlbl, 'y': ylbl},
                          color=y_axis, size=y_axis)
        st.plotly_chart(fig)

    elif chart == 'Histogram':
        fig = px.histogram(data, x_axis, y_axis, title=f'{xlbl} by {ylbl}', log_x=False, log_y=False,
                            labels={'x': xlbl, 'y': ylbl})
        st.plotly_chart(fig)

    elif chart == 'Pie':
        fig = px.pie(data, names=x_axis, values=y_axis, color=x_axis, title=f'{xlbl} by {ylbl}',
                     color_discrete_sequence=px.colors.sequential.deep)
        st.plotly_chart(fig)


def visualize_data(data):
    # Doing Visualization on data
    container.markdown("# DATA VISUALIZATION 📈 📊")
    top_n_sect = top_n_sections(data)
    sorted_coln, order = sort_by2(data)

    st.sidebar.header('Data Visualization')

    chart_type = st.sidebar.selectbox("Chart Type", ["Bar", "Line", "Scatter", "Histogram","Pie"])

    x_column = st.sidebar.selectbox("Label", data.columns)

    y_column = st.sidebar.selectbox("Values", data.columns)
            
    try:
        if sorted_coln is not None:
            if order == 'Ascending':
                data2 = data.sort_values(by=sorted_coln)
            else:
                data2 = data.sort_values(by=sorted_coln, ascending=False)
        else:
            data2 = data
        
        x_axis = data2[x_column].head(top_n_sect)
        y_axis = data2[y_column].head(top_n_sect)



        display_chart(data2, chart_type, x_axis, y_axis, x_column, y_column)

    except Exception as error:
        print(error)

    

def main():
    image = Image.open("banner.png")

    # container.image(image,width = 800)
    
    st.sidebar.image(image,width = 300)
    file = st.sidebar.file_uploader("Upload a file (CSV Only)", type=['csv'])

    options = st.sidebar.radio('pages'.upper(), options = ['Data Analysis','Data visualization'])

    if file is not None:
        data = load_data(file)

        if options == 'Data Analysis':
           analyze_data(data)

        if options =='Data visualization':
            visualize_data(data)


        
if __name__ == "__main__":
    main()
