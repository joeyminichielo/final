import csv
import pprint as pp
import streamlit as st
import pydeck as pdk
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = "Fast_Food_Restaurants_8000_sample (1).csv"
ff = pd.read_csv(data)

ff_nll = ff.drop(
    ['id', 'dateAdded', 'dateUpdated', 'address', 'categories', 'city', 'country', 'keys', 'postalCode',
     'sourceURLs', 'websites'], inplace=False, axis=1)

ff_nec = ff.drop(
    ['id', 'dateAdded', 'dateUpdated', 'address', 'latitude', 'longitude', 'categories', 'country', 'keys',
     'postalCode', 'sourceURLs', 'websites'], inplace=False, axis=1)

ff_type = ff.drop(
    ['id', 'dateAdded', 'dateUpdated', 'address', 'city', 'country', 'keys',
     'postalCode', 'sourceURLs', 'websites'], inplace=False, axis=1)


def filter_data(sel_state, sel_rest):
    df = ff
    df = df.loc[df['province'].isin(sel_state)]
    df = df.loc[df['categories'].isin(sel_rest)]
    return df


def rest_in_st(st, df):
    result = df[df['province'] == st]
    return result


def type_of_rest(df):
    lst = []
    for x in df['categories']:
        if x not in lst:
            lst.append(x)
    return lst


def name_st_city(df):
    namelst = []
    stlst = []
    citylst = []
    for name in df['name']:
        namelst.append(name)
    for st in df['province']:
        stlst.append(st)
    for city in df['city']:
        citylst.append(city)
    result = tuple(zip(namelst, citylst, stlst))
    short_tup = result[0:20]
    return short_tup


def state_name(st, name):
    query = ff_nec[(ff_nec['province'] == st) & (ff_nec['name'] == name)]
    return query


def panda():
    print(ff_nll[['province', 'name']].groupby('province').count())
    print(ff[["name", "province"]].sort_values('province'))
    print(ff[["name", "latitude", "longitude", "province"]].sort_values('name'))


def get_data(df, state, restaurant):
    p1 = df[ff_type['province'] == state]
    result = p1[p1["categories"] == restaurant]
    return result


def makemap(df):
    view_state = pdk.ViewState(
        latitude=df["latitude"].mean(),
        longitude=df["longitude"].mean(),
        zoom=4,
        pitch=0)

    layer1 = pdk.Layer('ScatterplotLayer',
                       data=df,
                       get_position='[longitude, latitude]',
                       get_radius=1000,
                       get_color=[0, 0, 255],  # big red circle
                       pickable=True
                       )

    layer2 = pdk.Layer('ScatterplotLayer',
                       data=df,
                       get_position='[longitude, latitude]',
                       get_radius=100,
                       get_color=[255, 0, 255],  # purple circle
                       pickable=True
                       )

    tool_tip = {"html": "Fast Food:<br/> <b>{name}</b> ",
                "style": {"backgroundColor": "steelblue",
                          "color": "white"}
                }

    map = pdk.Deck(
        map_style='mapbox://styles/mapbox/outdoors-v11',
        initial_view_state=view_state,
        layers=[layer1, layer2],
        tooltip=tool_tip
    )

    st.pydeck_chart(map)


def pie_chart(df):
    names = []
    for x in df['name']:
        if x not in names:
            names.append(x)
    lst = [df.loc[df['name'].isin([name])].shape[0] for name in names]

    plt.figure()

    explodes = [0 for i in range(len(lst))]
    maximum = lst.index(np.max(lst))
    explodes[maximum] = 0.25

    plt.pie(lst, labels=names, explode=explodes, autopct="%.2f")
    plt.title("Percent of Restaurants in Selected State:")
    plt.show()
    return plt


topten = ["McDonald's", "Burger King", "Dairy Queen", "Chick-fil-A", "Taco Bell", "Arby's", "Pizza Hut", "Subway",
          "Wendy's", "Jack in the Box"]


def bar_count(df):
    return [df.loc[df['name'].isin([name])].shape[0] for name in topten]

def main():
    state = input("Enter a State Abbreviation: ")
    print(rest_in_st(state, ff_nec))
    input("Continue:")
    st_choice = input("Enter a State Abbreviation: ")
    name_choice = input("Enter a Name of a Restaurant: ")
    print(state_name(st_choice, name_choice))
    input("Continue:")
    pp.pprint(type_of_rest(ff))
    input("Continue:")
    print(name_st_city(ff_nec))
    input("Continue:")
    print(panda())
    input("Continue:")

main()


def slit():
    st.header("Map of Restaurants")

    st.sidebar.header("User Inputs")
    province = []
    for x in ff['province']:
        if x not in province:
            province.append(x)
    type = []
    for x in ff['categories']:
        if x not in type:
            type.append(x)
    visual = ["Map", "Pie Chart", "Bar Graph"]
    state = st.sidebar.multiselect("Select State: ", province)
    restaurant = st.sidebar.multiselect("Select type: ", type)
    button = st.sidebar.selectbox("Select type: ", visual)
    fdata = filter_data(state, restaurant)
    makemap(ff_type)
    st.dataframe(fdata)
    st.pyplot(pie_chart(fdata))
    x = topten
    y = bar_count(fdata)
    plt.figure()
    plt.bar(x, y)
    plt.show()
    plt.title("Top Ten Restaurants in Selected State:")
    plt.xticks(x, x, rotation='vertical')
    st.pyplot(plt)


slit()



