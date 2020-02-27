---
title: 使用 plotly 绘制 Choropleth 地图
date: 2020-02-25 16:28
tags:
  - Python
  - Data Science
---

本文将通过绘制中国省级 Choropleth 地图来解释如何使用 plotly 绘制 Choropleth 地图，主要有两种方法：底层 API `plotly.graph_objects.Choroplethmapbox` 和高层 API `plotly.express.choropleth_mapbox`，数据是 COVID-19 在某一天的疫情数据。

## 什么是 Choropleth 地图

> Choropleth map 即分级统计图。在整个制图区域的若干个小的区划单元内（行政区划或者其他区划单位），根据各分区资料的数量（相对）指标进行分级，并用相应色级或不同疏密的晕线，反映各区现象的集中程度或发展水平的分布差别。—— [Choropleth_百度百科](https://baike.baidu.com/item/Choropleth)

简单来说，具体到本文，就是在地图上为每个省上色，根据什么来确定上哪个颜色呢？在本文中就是该省的确诊人数，人数越多，颜色越亮。这样得到的地图就是 Choropleth 地图。

## 依赖

主要依赖为：

- [plotly](https://github.com/plotly/plotly.py)
- [pandas](https://github.com/pandas-dev/pandas)

均可以通过 `pip` 安装，然后导入：

```python
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import json
```

## 数据准备

- `data.csv`：某日 COVID-19 全国省级疫情数据，用于地图上色
- `china_province.geojson`：中国省级地图 geojson 文件，用于绘制地图轮廓

然后导入数据：

```python
with open("china_province.geojson") as f:
    provinces_map = json.load(f)
df = pd.read_csv('data.csv')
```

## plotly 的绘图逻辑

使用 plotly 绘图，其实就是两点：**data 和 layout**，即数据和布局。其实所有绘图都是这样，只不过在 plotly 里体现得尤为明显，尤其是底层 API。

data 决定绘图所使用的数据，比如绘制股票折线图用的股票历史数据，绘制疫情地图用的疫情数据。layout 决定图的布局，比如一幅折线图的宽高，一幅地图的风格和中心点。plotly 里一幅图是一个 `Figure` 对象，这个对象就有 `data` 和 `layout` 两个参数。

## 方法 1：底层 API `plotly.graph_objects`

`plotly.graph_objects.Choroplethmapbox`（以下简称 `go.Choroplethmapbox`）是 plotly 的底层 API，其全部参数可参考[其官方文档](https://plot.ly/python/reference/#choroplethmapbox)。不过这参数实在是太多了，下面我通过例子来介绍一下几个常用的。

先来看代码：

```python
fig = go.Figure(
    go.Choroplethmapbox(
        geojson=provinces_map,
        featureidkey="properties.NL_NAME_1",
        locations=df.地区,
        z=df.确诊,
        zauto=True,
        colorscale='viridis',
        marker_opacity=0.8,
        marker_line_width=0.8,
        showscale=True,
    )
)
fig.update_layout(
    mapbox_style="carto-darkmatter",
    mapbox_zoom=3,
    mapbox_center={"lat": 37.110573, "lon": 106.493924},
)
```

先看下 `go.Choroplethmapbox` 的参数：

- `geojson`：`dict` 类型，这个就是刚才说的用于绘制地图轮廓的数据，一般从相应的 geojson 文件中用 `json.load` 加载进来。
- `featureidkey`：`str` 类型，默认 为 `id`。函数会使用这个参数和 `locations` 匹配地图单元（比如省份）的名称，以此决定绘制哪些地图单元的轮廓。通常的形式为 `properties.name`，其中的 `name` 需要你自己根据 geojson 文件去指定，比如这里是 `properties.NL_NAME_1`，意思就是 `NL_NAME_1` 这一列是省份名称。这个很重要，设置不正确会导致地图轮廓显示不出来，**一定要保证和 `locations` 中的所有名称保持一致**。
- `locations`: 可以是以下类型：` list，numpy array，数字、字符串或者 datetime 构成的 Pandas series`。指定地图单元名称，决定绘制哪些地图单元的轮廓。同样需要注意**和 `featureidkey` 保持一致**。
- `z`：可以是以下类型：`list，numpy array，数字、字符串或者 datetime 构成的 Pandas series`。指定地图单元对应的数值，函数会将此值映射到 colorscale 中的某一颜色，然后将此颜色涂到相应的地图单元内。通常来说是一个 pandas dataframe 中的某一列，即一个 series。需要注意此参数中值的顺序需要和 `locations` 保持一致，一一对应，如河南在 `locations` 中的索引是 9，那么河南的确诊人数在 `z` 中的索引也必须是 9。
- `zauto`：`bool` 类型，默认为 `True`。是否让颜色自动适应 `z`，即自动计算 `zmin` 和 `zmax`，然后据此来映射 colorscale。
- `colorscale`：通常来说是 `str` 类型，也可以是 [`list` 类型](https://plot.ly/python/colorscales/#custom-discretized-heatmap-color-scale-with-graph-objects)。指定所使用的 colorscale，可使用的值参见[此处](https://plot.ly/python/builtin-colorscales/)。
- `marker_opacity`：`float` 类型，颜色透明度。
- `marker_line_width`：`float` 类型，地图轮廓宽度。
- `showscale`：`bool` 类型。是否显示 colorbar，就是地图旁边的颜色条。

`fig.update_layout` 的参数同样有很多，主要用来定义布局：

- `mapbox_style`：`str` 类型，指定 mapbox 风格。可用的 mapbox 风格列表可参见[这里](https://plot.ly/python/mapbox-layers/#base-maps-in-layoutmapboxstyle)。需要注意的是当你使用以下风格之一时，你就需要指定 `mapbox_token`（关于如何获取 token 详细可参见[这里](https://github.com/secsilm/2019-nCoV-dash#%E5%85%B3%E4%BA%8E-mapboxtoken)）：

  ```python
  ["basic", "streets", "outdoors", "light", "dark", "satellite", "satellite-streets"]
  ```

- `mapbox_zoom`：`int` 类型，指定地图的缩放级别。
- `mapbox_center`：`dict` 类型，key 为 `lat`（经度）和 `lon`（纬度），指定初始时地图的中心点。

最终的效果如图：

![go-choropleth-mapbox.gif](https://i.loli.net/2020/02/27/WYHqpbRixzUjI5d.gif)

## 方法 2：高层 API `plotly.express.choropleth_mapbox`

`plotly.express.choropleth_mapbox`（以下简称 `px.choropleth_mapbox`） 是 plotly 的高层 API，严格来说是 [`plotly_express`](https://github.com/plotly/plotly_express) 的接口，但是后来这个包被并入 `plotly`，可以直接用 `plotly.express` 来引入了，这个包主要就是简化了 plotly 的绘图方法。

详细参数可参考其[官方文档](https://plot.ly/python-api-reference/generated/plotly.express.choropleth_mapbox.html#plotly.express.choropleth_mapbox)。其实大部分参数是异曲同工的，下面我同样使用相同的数据来绘制地图，解释下。

老规矩，先来看代码：

```python
fig = px.choropleth_mapbox(
    data_frame=df,
    geojson=provinces_map,
    color='确诊',
    locations="地区",
    featureidkey="properties.NL_NAME_1",
    mapbox_style="carto-darkmatter",
    color_continuous_scale='viridis',
    center={"lat": 37.110573, "lon": 106.493924},
    zoom=3,
)
```

- `data_frame`：通常来说是 `pd.DataFrame` 格式。我们需要把绘图用到的数据都放到这个参数里面，后续很多参数都是基于此的，具体来说就是其中的列名。在 plot express 的各个绘图方法中，`DataFrame` 其实是最为方便的格式，也是官方推荐的格式，官方的大部分示例都是使用的这个格式。
- `geojson`：和 `go.Choroplethmapbox` 的同名参数对应。
- `color`：通常为 `str` 类型，`data_frame` 的列名。和 `go.Choroplethmapbox` 中的 `z` 对应。
- `locations`：通常为 `str` 类型，`data_frame` 的列名。和 `go.Choroplethmapbox` 中的同名参数对应。
- `featureidkey`：和 `go.Choroplethmapbox` 的同名参数对应。
- `mapbox_style`：和 `update_layout` 的同名参数对应。
- `color_continuous_scale`：和 `go.Choroplethmapbox` 中的 `colorscale` 对应。
- `center`：和 `update_layout` 中的 `mapbox_center` 对应。
- `zoom`：和 `update_layout` 中的 `mapbox_zoom` 对应。

最终的效果如图：

![这里记的放图](https://i.imgur.com/POkHX4t.gif)

## 一些没说到的

为了阅读体验，本文没有解释更多的参数，但我相信这已经能让你绘制一幅不错的 choropleth 地图了。有时间我会继续写一写如何在 dash 中融入这些地图，并实时更新。

其实本文所讲的是地图是一种 tile map，和这种地图对应的是一种轮廓地图，没有 mapbox 这种底图，只绘制 geojson 文件中定义的轮廓，如下面这幅图：

![中国地图](https://i.loli.net/2020/02/27/a6K4Sbj8IYzqrA1.png)

plotly 也可以绘制这种地图，只需要去掉本文所讲的函数中 `mapbox` 即可：`go.Choropleth` 和 `px.choropleth`，感兴趣可以参考[这里](https://plot.ly/python/choropleth-maps/)的示例。

## Reference

- [Mapbox Choropleth Maps | Python | Plotly](https://plot.ly/python/mapbox-county-choropleth/)
- [Choropleth Maps | Python | Plotly](https://plot.ly/python/choropleth-maps/#base-map-configuration)

## END