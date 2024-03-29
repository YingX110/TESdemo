import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

mapdf = pd.read_csv('./data_inventory/mapdata.csv')
procloc = pd.read_csv('latlng.csv')



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

# fig2 = px.scatter_geo(procloc, locations="iso_alpha",
#                     size=2,
#                     color=df['Vk'].astype(float), 
#                     hover_name="Process", # column to add to hover information
#                     color_continuous_scale=px.colors.sequential.Plasma)

fig2 = px.scatter_geo(procloc, 
                    lat="lat", 
                    lon="lng", 
                    size='Scaled',
                    hover_name='Process')

# fig2 = px.scatter_mapbox(procloc, lat="lat", lon="lng", color="Vk", size='Scaled',
#                   color_continuous_scale=px.colors.cyclical.IceFire, size_max=15)




fig.add_trace(fig2.data[0])

for i, frame in enumerate(fig.frames):
    fig.frames[i].data += (fig2.frames[i].data[0],)

fig.show()



#############
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
#             size = ls[i]['Scaled'] * 30,
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