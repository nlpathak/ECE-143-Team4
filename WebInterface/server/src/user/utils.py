import pandas as pd
import plotly.express as px
import chart_studio.plotly as py
import chart_studio.tools as tls
import os

# Global Settings
cdm = {"Positive": "Blue", "Negative": "Red"}
co ={"sentiment": ["Positive", "Negative"]}


def plotly_url(data,user, freq='H'):
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
        print(f'PLOTLY | USER: {user_plotly}, API: {api}')

        # Make dataframe and group by month
        df = pd.DataFrame(data)
        df['created_at'] = pd.to_datetime(df['created_at'])
        if 'user_id' in df.columns: 
            df.rename(columns={'user_id':'user'})
            df['user'] = user

        # Changes sentiment to +1 and -1
        df['sentiment'] = df['sentiment'].apply(lambda x: 1 if x=="Positive" else -1)

        # Set's up series for plotting by grouping datetime
        df_u = df.groupby(['user',pd.Grouper(key='created_at',freq='H')])['sentiment'].sum().reset_index(name='net')
        df_u['sentiment'] = df_u['net'].apply(lambda x: "Negative" if x < 0 else "Positive")
        
        # Plotly
        tls.set_credentials_file(username=user_plotly,api_key=api)
        user_bar = px.bar(df_u, x="created_at", y="net", color="sentiment", category_orders=co, title=f'{user}: Tweets',hover_data=df_u.columns)
        url = py.plot(user_bar, filename=f'{user}_tweets_{freq}',auto_open=False)

        return tls.get_embed(url)
    except Exception as e:
        print(f'plotly_url error: {e}')
