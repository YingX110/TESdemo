import plotly.express as px
import pandas as pd
import plotly.graph_objects as go



def mapplot(mapdf, procloc, SPM, SCALE):
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
        


    #############
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
    fig.show()
    # return fig


if __name__ == '__main__':
    
    SPM = "Area" 
    SCALE = "Local, National"
    mapdf = pd.read_csv('mapdata.csv')
    procloc = pd.read_csv('latlng.csv')
    mapplot(mapdf, procloc, SPM, SCALE)


