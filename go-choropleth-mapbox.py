import pandas as pd
import plotly.graph_objs as go
import numpy as np
import json

with open("china_province.geojson") as f:
    provinces_map = json.load(f)

df = pd.read_csv('data.csv')
df['确诊_log'] = df.确诊.map(np.log)
fig = go.Figure(
    go.Choroplethmapbox(
        featureidkey="properties.NL_NAME_1",
        geojson=provinces_map,
        locations=df.地区,
        z=df.确诊_log,
        zauto=True,
        colorscale='viridis',
        reversescale=False,
        marker_opacity=0.8,
        marker_line_width=0.8,
        customdata=np.vstack((df.地区, df.确诊, df.疑似, df.治愈, df.死亡)).T,
        hovertemplate="<b>%{customdata[0]}</b><br><br>"
        + "确诊：%{customdata[1]}<br>"
        + "疑似：%{customdata[2]}<br>"
        + "治愈：%{customdata[3]}<br>"
        + "死亡：%{customdata[4]}<br>"
        + "<extra></extra>",
        showscale=True,
    )
)
fig.update_layout(
    mapbox_style="carto-darkmatter",
    mapbox_zoom=3,
    mapbox_center={"lat": 37.110573, "lon": 106.493924},
)
fig.show()