import plotly.express as px
import pandas as pd
import plotly.graph_objects as go


def mapplot(mapdf, procloc):
    SPM = "Population" 
    SCALE = "Local, Worldwide"

    if SCALE != "Direct downscaling (PB)":
        df = mapdf[(mapdf.Scale == SCALE) & (mapdf.Method == 'TES') & (mapdf.SP == SPM)]
    else:
        df = mapdf[(mapdf.Method == 'PB') & (mapdf.SP == SPM)]


    df = df.T
    df = df.iloc[3:, :]
    df = df.reset_index()
    df = df.set_axis(['code', 'supply'], axis=1, inplace=False)

    up = max(df['supply'])
    low = min(df['supply'])

    fig = px.choropleth(locations=df['code'], 
                        locationmode="USA-states", 
                        color=df['supply'].astype(float), 
                        range_color=(low,up),
                        color_continuous_scale="Blugrn",
                        scope="usa")

    colors = ["lightseagreen", "crimson"]
    sus = procloc.loc[procloc['Vk'] >= 0]
    unsus = procloc.loc[procloc['Vk'] < 0]
    ls = [sus, unsus]

    fig2 = go.Figure()

    for i in range(len(ls)):
        fig2.add_trace(go.Scattergeo(
            locationmode = 'USA-states',
            lon = ls[i]['lng'],
            lat = ls[i]['lat'],
            marker = dict(
                size = ls[i]['Scaled'] * 110,
                color = colors[i],
                line_color='rgb(40,40,40)',
                line_width=0.5,
                sizemode = 'area'
            )))
        



    #####
    fig.add_trace(fig2.data[0])
    fig.add_trace(fig2.data[1])

    for i, frame in enumerate(fig.frames):
        fig.frames[i].data += (fig2.frames[i].data[0],)


    #############
    fig.update_layout(
            title_text = 'Transgression Level for Each Process',
            showlegend = False,
            geo = dict(
                scope = 'usa',
                landcolor = 'rgb(217, 217, 217)'
            )
        )

    return fig
    # fig.show()

if __name__ == '__main__':

    mapdf = pd.read_csv('./data_inventory/mapdata.csv')
    procloc = pd.read_csv('latlng.csv')
    mapplot(mapdf, procloc)

# colors = ["lightseagreen", "crimson"]

# fig = go.Figure()
# sus = procloc.loc[procloc['Vk'] >= 0]
# unsus = procloc.loc[procloc['Vk'] < 0]
# ls = [sus, unsus]

# for i in range(len(ls)):
#     fig.add_trace(go.Scattergeo(
#         locationmode = 'USA-states',
#         lon = ls[i]['lng'],
#         lat = ls[i]['lat'],
#         marker = dict(
#             size = ls[i]['Scaled'] * 40,
#             color = colors[i],
#             line_color='rgb(40,40,40)',
#             line_width=0.5,
#             sizemode = 'area'
#         )))

# fig.update_layout(
#         title_text = 'absolute sustainability metric',
#         showlegend = True,
#         geo = dict(
#             scope = 'usa',
#             landcolor = 'rgb(217, 217, 217)',
#         )
#     )

# fig.show()


###
# import plotly.express as px
# import pandas as pd

# mapdf = pd.read_csv('./data_inventory/mapdata.csv')
# procloc = pd.read_csv('latlng.csv')



# df = px.data.gapminder()
# fig = px.choropleth(df, locations="iso_alpha",
#                     color="lifeExp", # lifeExp is a column of gapminder
#                     hover_name="country", # column to add to hover information
#                     color_continuous_scale=px.colors.sequential.Plasma,
#                     animation_frame='year')
# fig2 = px.scatter_geo(df, locations="iso_alpha",
#                     size="lifeExp", # lifeExp is a column of gapminder
#                     hover_name="country", # column to add to hover information
#                     color_continuous_scale=px.colors.sequential.Plasma,
#                     animation_frame='year')
# fig.add_trace(fig2.data[0])
# for i, frame in enumerate(fig.frames):
#     fig.frames[i].data += (fig2.frames[i].data[0],)
# fig.show()


###############################################
# 'Basic plot (one color for all bubbles):'
# fig = px.choropleth(locations=df['code'], 
#                     locationmode="USA-states", 
#                     color=df['supply'].astype(float), 
#                     range_color=(low,up),
#                     color_continuous_scale="Blugrn",
#                     scope="usa")

# fig2 = px.scatter_geo(procloc, 
#                     lat="lat", 
#                     lon="lng", 
#                     size='Scaled',
#                     hover_name='Process')


# 'Use openstreet map (require mapbox token):'
# px.set_mapbox_access_token(open("carbon.mapbox_token").read())
# fig = px.scatter_mapbox(procloc, 
#                         lat="lat", lon="lng", 
#                         color="Vk", size="Scaled",
#                         color_continuous_scale=px.colors.cyclical.IceFire, 
#                         size_max=15, zoom=2)
# fig.show()

