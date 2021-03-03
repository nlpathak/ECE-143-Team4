import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import chart_studio.plotly as py
import chart_studio.tools as tls
import os

# Global Settings
cdm = {"Positive": "Blue", "Negative": "Red"}
co ={"sentiment": ["Positive", "Negative"]}


def plotly_url(data,user, freq='D'):
    """
    Takes list of dicts from django model.objects.values iterable and
    turns it into a dataframe for use with plotly plotting.
    :param data: list containing all values
    :param freq: timeperiod, default H:hour
    :type data: list
    :type freq: str
    """
    try:
        user_plotly = os.environ.get('PLOTLY_USER')
        api = os.environ.get('PLOTLY_API')

        # Make dataframe and group by month
        df = pd.DataFrame(data)
        df['created_at'] = pd.to_datetime(df['created_at'])
        if 'user_id' in df.columns: 
            df.rename(columns={'user_id':'user'})
            df['user'] = user

        # Set's up series for plotting by grouping datetime
        df_u = df.groupby(['user','sentiment',pd.Grouper(key='created_at',freq=freq)])['sentiment'].count().reset_index(name='total')
        
        # Get rolling avgs
        df_u['nroll_7'] = df_u[df_u['sentiment']=='Negative'].total.rolling(7,win_type='triang').mean()
        df_u['proll_7'] = df_u[df_u['sentiment']=='Positive'].total.rolling(7,win_type='triang').mean()

        df_u['nroll_7'] = df_u['nroll_7'].fillna(0)
        df_u['proll_7'] = df_u['proll_7'].fillna(0)

        # Plotly
        tls.set_credentials_file(username=user_plotly,api_key=api)
        user_bar = px.bar(df_u, x="created_at", y="total", color="sentiment",barmode="group", category_orders=co,labels={'created_at':'Date','total':'Total'}, title=f'{user}: Tweets',hover_data=df_u.columns)

        # Plot rolling averages
        user_bar.add_trace(go.Scatter(x=df_u[df_u['sentiment']=='Negative']['created_at'],y=df_u[df_u['sentiment']=='Negative']['nroll_7'], name='nroll_7'))
        user_bar.add_trace(go.Scatter(x=df_u[df_u['sentiment']=='Positive']['created_at'],y=df_u[df_u['sentiment']=='Positive']['proll_7'], name='proll_7'))

        url = py.plot(user_bar, filename=f'{user}_tweets_{freq}',auto_open=False)

        return tls.get_embed(url)
    except Exception as e:
        print(f'plotly_url error: {e}')
