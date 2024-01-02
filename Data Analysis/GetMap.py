import branca.colormap
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import geopandas
import folium
import folium.plugins as plugins
import os
from collections import defaultdict, OrderedDict
from branca.element import Template, MacroElement

df = pd.read_csv('finalDataset.csv', header=0)
df = df.dropna(thresh=10)

df = df.astype(dtype= {"HDI":"float64", "DALYs":"float64",
            "GDP":"float64","Year":"int32", "Net Migration Rate": "float64",
            "Life Expectancy":"float64", 'Mortality':"float64",
            "Inflation":"float64", "Healthcare expenditure":"float64"})
            
world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))

world.columns=['Pop_est', 'Continent', 'name', 'Country Code', 'gdp_md_est', 'geometry']
# world = world.drop(columns='Country Name')
# print(list(set(world['name'])))
world.loc[world["name"] == "Norway", "Country Code"] = 'NOR'
world.loc[world["name"] == "France", "Country Code"] = 'FRA'
world.loc[world["name"] == "United States of America", "name"] = 'United States'
world.loc[world["Country Code"]=='COD', "name"] = 'Democratic Republic of Congo'
world.loc[world["Country Code"]=='CAF', "name"] = "Central African Republic"
print(world.loc[world["Country Code"]=='CAF'])
merge=pd.merge(world,df,on='Country Code')

def generateJpeg():
    # counter for the for loop
    i = 0
    output_path = 'Milestone 2/Maps'
    # list of years (which are the column names at the moment)
    list_of_years = range(1955,2021)
    vmin, vmax = -10, 10# start the for loop to create one map per year
    for year in list_of_years:
        
        # create map, UDPATE: added plt.Normalize to keep the legend range the same for all maps
        fig = merge.plot(column=str(year), 
                        cmap='OrRd', 
                        figsize=(8,4), 
                        linewidth=0.3, 
                        edgecolor='0.8', 
                        vmin=vmin, 
                        vmax=vmax,
                        legend=True, 
                        norm=plt.Normalize(vmin=vmin, vmax=vmax))
        
        # remove axis of chart
        fig.axis('off')
        
        # add a title
        fig.set_title(f'Net Migrant Rate: {year}', \
                fontdict={'fontsize': '14',
                            'fontweight' : '4'})
        # this will save the figure as a high-res png in the output path. you can also save as svg if you prefer.
        filepath = os.path.join(output_path, str(year)+'_migrant.jpeg')
        chart = fig.get_figure()
        chart.savefig(filepath, dpi=500)
        print(year)

def getPlots():
    for year in range(1955,2021):
        ax = merge.plot(column=str(year),
                    cmap='OrRd', 
                    legend = True,
                    legend_kwds={'label': "Net Migration Rate",
                                'orientation': "horizontal"},
                    missing_kwds={"color": "lightgrey",
                                "label": "Missing values"})
        print(type(ax))
        #removing axis ticks
        ax.axis('off')#Add the title
        ax.set_title(f"Net Migration Rate per Country in {year}")
        # plt.show()
        plt.savefig(f'Milestone 2/MatplotlibMap/{year}.png', dpi=500)
        ax.cla()

def getHTML():
    # merge=pd.merge(world,df,on='Country Code')


    # macro = MacroElement()
    # macro._template = Template(template)
    merge = prepForHeatMap()
    # merge=pd.merge(world,df,on='Country Code')
    merge = merge.replace('Unknown', np.nan)
    merge = merge.drop(columns=['Center_point', 'long', 'lat', 'Pop_est', 'Continent', 'Country Code', 'gdp_md_est'],errors='ignore')
    print(merge)
    for year in range(2020,1989,-1):
        print(year)
        my_map = folium.Map([0,0], zoom_start=2)
        # Add the data
        data = merge[merge['Year']==year]
        # print(data)
        # data.dropna()
        # my_map.get_root().add_child(macro)
        folium.Choropleth(
                geo_data=data,
                data=data,
                columns=['name', 'migRate'],
                key_on="feature.properties.name",
                fill_color='YlOrRd',
                fill_opacity=0.8,
                line_opacity=0.1,
                legend_name="Net Migration Rate",
                smooth_factor=0,
                Highlight= True,
                line_color = "#0000",
                name = "Net Migration Rate",
                show=True,
                overlay=True,
                nan_fill_color = "White"
                ).add_to(my_map)
        
        folium.Choropleth(
            geo_data=data,
            data=data,
            columns=['name', 'DALYs'],
            key_on="feature.properties.name",
            fill_color='BuPu',
            fill_opacity=0.8,
            line_opacity=0.1,
            legend_name="DALYs",
            smooth_factor=0,
            Highlight= True,
            line_color = "#0000",
            name = "DALYs",
            show=True,
            overlay=True,
            nan_fill_color = "White"
            ).add_to(my_map)  
        
        folium.Choropleth(
            geo_data=data,
            data=data,
            columns=['name', 'GDP'],
            key_on="feature.properties.name",
            fill_color='BuGn',
            fill_opacity=0.8,
            line_opacity=0.1,
            legend_name="GDP",
            smooth_factor=0,
            Highlight= True,
            line_color = "#0000",
            name = "GDP",
            show=True,
            overlay=True,
            nan_fill_color = "White"
            ).add_to(my_map)
        
        folium.Choropleth(
            geo_data=data,
            data=data,
            columns=['name', 'Inflation'],
            key_on="feature.properties.name",
            fill_color='PuRd',
            fill_opacity=0.8,
            line_opacity=0.1,
            legend_name="Inflation",
            smooth_factor=0,
            Highlight= True,
            line_color = "#0000",
            name = "Inflation",
            show=True,
            overlay=True,
            nan_fill_color = "White"
            ).add_to(my_map)  
        
        folium.Choropleth(
            geo_data=data,
            data=data,
            columns=['name', 'HDI'],
            key_on="feature.properties.name",
            fill_color='YlGnBu',
            fill_opacity=0.8,
            line_opacity=0.1,
            legend_name="HDI",
            smooth_factor=0,
            Highlight= True,
            line_color = "#0000",
            name = "HDI",
            show=True,
            overlay=True,
            nan_fill_color = "White"
            ).add_to(my_map)
        
        folium.Choropleth(
            geo_data=data,
            data=data,
            columns=['name', 'mortality'],
            key_on="feature.properties.name",
            fill_color='BuPu',
            fill_opacity=0.8,
            line_opacity=0.1,
            legend_name="Mortality",
            smooth_factor=0,
            Highlight= True,
            line_color = "#0000",
            name = "mortality",
            show=True,
            overlay=True,
            nan_fill_color = "White"
            ).add_to(my_map)
        
        folium.Choropleth(
            geo_data=data,
            data=data,
            columns=['name', 'lifeExp'],
            key_on="feature.properties.name",
            fill_color='YlGnBu',
            fill_opacity=0.8,
            line_opacity=0.1,
            legend_name="Life Expectancy",
            smooth_factor=0,
            Highlight= True,
            line_color = "#0000",
            name = "Life Expectancy",
            show=True,
            overlay=True,
            nan_fill_color = "White"
            ).add_to(my_map)
        folium.Choropleth(
            geo_data=data,
            data=data,
            columns=['name', 'Out-of-pocket'],
            key_on="feature.properties.name",
            fill_color='YlOrBr',
            fill_opacity=0.8,
            line_opacity=0.1,
            legend_name="Out-of-pocket",
            smooth_factor=0,
            Highlight= True,
            line_color = "#0000",
            name = "Out-of-pocket",
            show=True,
            overlay=True,
            nan_fill_color = "White"
            ).add_to(my_map)
        # (filter(lambda x: print(x) if x else None, data['HDI'].isnull()))
        # Here we add cross-hatching (crossing lines) to display the Null values.
        # nans = data[data["HDI"].isnull()]['name'].values
        # gdf_nans = data[data['name'].isin(nans)]
        # sp = plugins.StripePattern(angle=45, color='grey', space_color='white', opacity=0.3)
        # sp.add_to(my_map)
        # folium.features.GeoJson(name="Click for NaN values",data=gdf_nans, style_function=lambda x :{'fillPattern': sp},show=True).add_to(my_map)
        # Add hover functionality.
        style_function = lambda x: {'fillColor': '#ffffff', 
                                    'color':'#000000', 
                                    'fillOpacity': 0.1, 
                                    'weight': 0.1}
        highlight_function = lambda x: {'fillColor': '#000000', 
                                        'color':'#000000', 
                                        'fillOpacity': 0.50, 
                                        'weight': 0.1}
        NIL = folium.features.GeoJson(
            data = data,
            style_function=style_function, 
            control=False,
            highlight_function=highlight_function, 
            tooltip=folium.features.GeoJsonTooltip(
                fields=['name','Migration Rate'],
                aliases=['Country','Migration Rate'],
                style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
            )
        )
        my_map.add_child(NIL)
        my_map.keep_in_front(NIL)
        # We add a layer controller. 
        folium.LayerControl(collapsed=False, autoZIndex=False).add_to(my_map)
        my_map.save(f'MapsHTML/{year}.html')

def prepForHeatMap():
    merge=pd.merge(world,df,on='Country Code')
    merge = merge.rename(columns={'Net Migration Rate':'migRate',
                            'Life Expectancy':'lifeExp', 'Mortality':'mortality'})
    merge = merge.drop(columns='Country Name')
    merge.insert(8,'Migration Rate', round(merge['migRate'],3))
    print(merge.columns)
    for col in merge.columns[9:]:
        # print(col)
        # print(merge.describe()[col])
        
        for year in range(1955,2020):
            df_sub = (merge[merge['Year']==year]).loc[:, col]
            lim1 = (df_sub - df_sub.mean()) / df_sub.std(ddof=0) < 3
            merge.loc[merge.Year==year, col] = df_sub.where(lim1, df_sub.max())

            df_sub = merge.loc[:, col]
            lim2 = (df_sub - df_sub.mean()) / df_sub.std(ddof=0) > -3
            merge.loc[merge.Year==year, col] = df_sub.where(lim2, df_sub.min())
            temp = merge.dropna(subset=[col])
            # print(merge.describe()[col])
            merge.loc[merge.Year==year, col] = round((temp.loc[temp.Year==year, col] - temp.loc[temp.Year==year, col].min()) / (temp.loc[temp.Year==year, col].max() - temp.loc[temp.Year==year, col].min()), 3)    
    merge.insert(1,'Center_point', ['']*len(merge))
    merge.insert(2,'long', ['']*len(merge))
    merge.insert(3,'lat', ['']*len(merge))
    merge['Center_point'] = merge['geometry'].to_crs('+proj=cea').centroid.to_crs(merge['geometry'].crs)
    #Extract lat and lon from the centerpoint
    merge["long"] = merge.Center_point.map(lambda p: p.x)
    merge["lat"] = merge.Center_point.map(lambda p: p.y)
    merge.to_csv('finalHeatMap.csv', index=False)
    return merge
    
def heatMap(col, m, grad):
    merge = pd.read_csv('finalHeatMap.csv', header=0)
    # print(merge[merge['name']=='Syria'][['migRatio','Year']])
    data = defaultdict(list)
    for r in merge.iterrows():
        r = r[1]
        if r[col]==0: r[col]=0.001
        data[r['Year']].append([r['lat'], r['long'], r[col]])
        
    data = OrderedDict(sorted(data.items(), key=lambda t: t[0]))

    steps=10
    if grad=='OrRd':
        colormap = branca.colormap.LinearColormap(['#ffffcc', '#ffffcc', '#ffefa5', '#febf5a', '#febf5a', '#fe9e43', '#f43c25', '#db141e', '#db141e', '#b60026'],
                  index=[x/steps for x in range(0,steps)]).to_step(steps)
    elif grad=='BlPu':
        colormap = branca.colormap.LinearColormap(['#80cebc', '#48b4c1', '#3789bd', '#3845a0', 'purple'],
                  index=[x/5 for x in range(0,5)]).to_step(steps)
    elif grad=='RdBl':
        colormap = branca.colormap.LinearColormap(['purple', 'red', 'orange', 'yellow', 'green'],
                  index=[0,0.25,0.5,0.7,0.9]).to_step(steps)
                  
    gradient_map=defaultdict(dict)
    for i in range(steps):
        gradient_map[str(round(1/steps*i, 3))] = colormap.rgb_hex_str(1/steps*i)
    colormap.add_to(m)
    print(gradient_map)
    hm = plugins.HeatMapWithTime(data=list(data.values()),
                        index=list(data.keys()),
                        index_steps=1,
                        radius=30,
                        auto_play=True,
                        max_opacity=0.5, 
                        min_opacity=0.2,
                        gradient=dict(gradient_map),
                        use_local_extrema=True)
    return hm
    hm.add_to(m)
    m.save(f'HeatMaps/{col}.html')
def heatMap1(col):
    m = folium.Map([0,0], zoom_start=2)
    merge = prepForHeatMap()
    data = defaultdict(list)
    for r in merge.iterrows():
        r = r[1]
        if r[col]==0: r[col]=0.001
        data[r['Year']].append([r['lat'], r['long'], r[col]])
        
    data = OrderedDict(sorted(data.items(), key=lambda t: t[0]))
    steps=10
    colormap = branca.colormap.LinearColormap(['purple', 'red', 'orange', 'yellow', 'green'],
                  index=[0,0.25,0.5,0.7,0.9]).to_step(steps)
                  
    gradient_map=defaultdict(dict)
    for i in range(steps):
        gradient_map[str(round(1/steps*i, 3))] = colormap.rgb_hex_str(1/steps*i)
    colormap.add_to(m)

    hm = plugins.HeatMapWithTime(data=list(data.values()),
                        index=list(data.keys()),
                        index_steps=1,
                        radius=30,
                        auto_play=True,
                        max_opacity=0.5, 
                        min_opacity=0.2,
                        gradient=dict(gradient_map))
    hm.add_to(m)
    m.save('heatMap.html')
    return m
if __name__ == '__main__':
    # prepForHeatMap()

    # m = folium.Map([0,0], zoom_start=2)
    hm1 = heatMap1('migRate')
    # # hm2 = heatMap('DALYs', m, 'BlPu')
    # hm1.add_to(m)
    # # hm2.add_to(m)
    # m.save('HeatMaps/migRatio.html')

    # getHTML()