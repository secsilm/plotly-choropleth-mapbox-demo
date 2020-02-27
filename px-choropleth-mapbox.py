import pandas as pd
# import geopandas
import plotly.express as px
import numpy as np
import json

with open("china_province.geojson") as f:
    provinces_map = json.load(f)

df = pd.read_csv('data.csv')
df.确诊 = df.确诊.map(np.log)

fig = px.choropleth_mapbox(
    df,
    geojson=provinces_map,
    # color=f"{selected_radio}区间",
    color='确诊',
    locations="地区",
    featureidkey="properties.NL_NAME_1",
    mapbox_style="carto-darkmatter",
    # color_discrete_map={
    #     "0": colorscales[selected_radio][0],
    #     "1-9": colorscales[selected_radio][1],
    #     "10-99": colorscales[selected_radio][2],
    #     "100-499": colorscales[selected_radio][3],
    #     "500-999": colorscales[selected_radio][4],
    #     "1000-9999": colorscales[selected_radio][5],
    #     "10000+": colorscales[selected_radio][6],
    # },
    # category_orders={f"{selected_radio}区间": labels},
    color_continuous_scale='viridis',
    center={"lat": 37.110573, "lon": 106.493924},
    zoom=3,
    # hover_name="地区",
    # hover_data=["确诊", "疑似", "治愈", "死亡"],
)
# fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig.show()