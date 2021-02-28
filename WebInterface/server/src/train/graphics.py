import pandas as pd
import plotly.express as px
import chart_studio.plotly as py
import chart_studio.tools as tls
import os


def plotly_creds():
    if ('PLOTLY_USER','PLOTLY_API') in os.environ:
        username = os.environ.get('PLOTLY_USER')
        api_key = os.environ.get('PLOTLY_API')
        return {'username':username,'api_key':api_key}
    else:
        return {}

def plotly_url(data,user):
    """
    Takes list of dicts from django model.objects.values iterable and
    turns it into a dataframe for use with plotly plotting.
    """
    creds = plotly_creds()
    if creds:
        # Make dataframe and group by month
        df = pd.DataFrame(data)
        df.index = pd.to_datetime(df['created_at'],format='%m/%d/%y %I:%M%p')
        # todo: confirm how to get the freq of tweets in the best way...
        df['sentiment'] = df['sentiment'].apply(lambda x: -1 if x == 'Negative' else 1)
        gf = df.groupby(by=pd.Grouper(freq='M')).sum()
        tls.set_credentials_file(username=creds['username'],api_key=creds['api_key'])
        fig = px.bar(data=df,x='created_at',y='
        url = py.plot(fig, filename=f'{user}_tweets',auto_open=False)
