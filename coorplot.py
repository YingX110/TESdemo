import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def quadrant_plot(df, xax, yax, col):

    xrange = [min(df[xax])-5, max(df[xax])+5]
    yrange = [min(df[yax])-5, max(df[yax])+5]

    fig = px.scatter(df, x=xax, y=yax, color=col)
    fig.update_xaxes(range=xrange)
    fig.update_yaxes(range=yrange)
    fig.update_traces(marker=dict(size=12, line=dict(width=2,color='DarkSlateGrey')), 
                      selector=dict(mode='markers'))

    fig.add_vline(x=0, line_width=1, line_dash="dash", line_color="black")
    fig.add_hline(y=0, line_width=1, line_dash="dash", line_color="black")
    
    block = {
        'Q1': [0, 0, xrange[1], yrange[1], 'limegreen'],
        'Q2': [0, 0, xrange[0], yrange[1], 'LightSkyBlue'],
        'Q3': [0, 0, xrange[0], yrange[0], 'maroon'],
        'Q4': [0, 0, xrange[1], yrange[0], 'goldenrod']
    }

    for v in block.values():
        fig.add_shape(
            type='rect',
            x0=v[0], y0=v[1], x1=v[2], y1=v[3],
            line=dict(color='black', width=0),
            fillcolor=v[4],
            opacity=0.4
        )
    return fig
    # fig.show()

if __name__ == '__main__':
    '''To test, need change self.coordinateplot(es) function -> return df'''
    from main2 import *
    df_s1 = pd.read_csv('ES1_info1.csv', index_col=0)
    ls_df1 = [df_s1]
    
    dfA = pd.read_csv('./user_input_data/tech_matrix1.csv', index_col=0) 
    dfD1 = pd.read_csv('./user_input_data/intv_matrix1.csv', index_col=0) 
    wt = pd.read_csv('./user_input_data/weighting_vec.csv', index_col=0)
    
    toy1 = format_process(ls_df1)
    obj1 = LcaSystem(toy1, dfA, dfD1, wt)
    obj1.add_process(SP_info)
    res1 = obj1.tes_cal()
    es = 'carbon sequestration'
    df = obj1.coordinateplot(es)
    xax = 'Vk loc'
    yax = 'Vk svc'
    col = 'Process'
    
    quadrant_plot(df, xax, yax, col)

