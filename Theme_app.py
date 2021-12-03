import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(layout="wide", page_icon=":art:", page_title="Custom Theming")

blank, title_col, blank = st.columns([2,3.5,2])
title_col.title("Custom Themes :art:")
st.header("Lets change it up!")

#st.write("this is a bit of `code` in markdown")
#st.code("an st.code() block")

st.sidebar.write("Use the widgets to alter the graphs:")
chck = st.sidebar.checkbox("Use your theme colours on graphs", value=True) # get colours for graphs

# get colors from theme config file, or set the colours to altair standards
if chck:
    primary_clr = st.get_option("theme.primaryColor")
    txt_clr = st.get_option("theme.textColor")
    # I want 3 colours to graph, so this is a red that matches the theme:
    second_clr = "#d87c7c"
else:
    primary_clr = '#4c78a8'
    second_clr = '#f58517'
    txt_clr = '#e45756'


select = st.sidebar.multiselect("Lines to display on charts", ["a", "b", "c"],["a", "b", "c"]) # select one or more of lines a,b,c

slide = st.sidebar.slider("Change the domain (x-axis) on the graphs",0,20,(0,20)) # interact with x-axis

button = st.sidebar.button("New set of random numbers") #generate new set of random numbers

#get data or make new data
if button:
    chart_data = pd.DataFrame({
        'index': 3 * list(range(20)),
        'data': np.random.randn(3 * 20, 1)[:,0],
        'label': ['a'] * 20 + ['b'] * 20 + ['c'] * 20,
    })

    chart_data.to_pickle("data/dataframe.pkl")
else:
    chart_data = pd.read_pickle("data/dataframe.pkl")


# filter data based on multiselect button
a = set(['a','b','c']).symmetric_difference(select) # get removed value
for x in a:
    chart_data = chart_data[chart_data.label != x]

line_graph = (
    alt.Chart(chart_data.reset_index())
        .mark_line(tooltip=True)
        .encode(
            x=alt.X('index', title='Datapoint index'),
            y=alt.Y('data', title='Value'),
            color=alt.Color('label'), #'color', scale=None ,scale=alt.Scale(scheme='My_custom')
        )
        .configure_range(
            category=[primary_clr,second_clr,txt_clr]
        )
        .transform_filter(
            (alt.datum.index >= slide[0]) & (alt.datum.index <= slide[1])
        )
        .interactive()
)

area = (
    alt.Chart(chart_data.reset_index())
        .mark_area(tooltip=True)
        .encode(
            x=alt.X('index', title='Datapoint index'),
            y=alt.Y('data', title='Value'),
            color=alt.Color('label'), #'color', scale=None ,scale=alt.Scale(scheme='My_custom')
        )
        .configure_range(
            category=[primary_clr,second_clr,txt_clr]
        )
        .transform_filter(
            (alt.datum.index >= slide[0]) & (alt.datum.index <= slide[1])
        )
        .interactive()
)

body1, sep, body2 = st.columns([8,0.2,8])

with body1:

    st.altair_chart(line_graph, use_container_width=True)

with body2:

    st.altair_chart(area, use_container_width=True)

if not chck:
    st.write("""When the checkbox is not selected, the altair graphs go back to
    using the altair defined standard colours.""")
else:
    st.write("""Having the checkbox selected, the script pulls the colours from the
    config.toml file located in your CWD.

This overrides the basic altair defined colours.""")
