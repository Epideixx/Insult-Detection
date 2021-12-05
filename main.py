import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from tweepy.error import TweepError
from datetime import timedelta
from math import floor

from twitter_collect import *
from tweet_analyze import average_hate
from wave_prevention import best_approximation, linear_approximation

app = dash.Dash(external_stylesheets=[dbc.themes.FLATLY])
valid_user_name = False
while not valid_user_name:
    screen_name = input("Which user profile do you want to analyse ? ")
    max_queries = input("How many replies do you want to gather (Warning: over 500 replies may take long to gather) ? ")
    try:
        dataframe = get_dataframe(screen_name,max_queries = int(max_queries))
        valid_user_name = True
    except TweepError as err:
        print("Invalid user")

fig_analyse_1 = px.scatter(average_hate(dataframe),x="date",y="avrg_hate",marginal_x='histogram', marginal_y='histogram',color="insult",labels={"avrg_hate":"Niveau de toxicité"})
fig_analyse_2 = px.scatter(dataframe,x="avrg_hate",y="retweets",color="insult",labels={"avrg_hate":"Niveau de toxicité"})

# Create a dataframe discretize by time to create a model
dataframe_discreet = dataframe.copy()
dataframe_discreet["date"] = dataframe_discreet["date"].apply(lambda date:date.replace(second = floor(date.second/30)*30,microsecond = 0))
dataframe_discreet["hate"] = dataframe_discreet["avrg_hate"].apply(lambda rate:int(rate>0.5))
dataframe_discreet = dataframe_discreet.groupby(by=["date"]).sum().reset_index()

fig_analyse_3 = px.scatter(dataframe_discreet,x="date",y="hate",labels={"hate":"Nombre d'insultes"})
linear_approximation = linear_approximation(dataframe_discreet["date"].apply(lambda date:date.timestamp()).to_list(),dataframe_discreet["hate"].to_list())
hate_approximation = best_approximation(dataframe_discreet["date"].apply(lambda date:date.timestamp()).to_list(),dataframe_discreet["hate"].to_list())
delta = timedelta(seconds=30)
X = [dataframe["date"].min()+(delta * i) for i in range(int((dataframe["date"].max()-dataframe["date"].min()).total_seconds()//30*1.1))]
Y = [linear_approximation(x.timestamp()) for x in X]
Y_croissance = [hate_approximation(x.timestamp()) for x in X]
fig_analyse_3.add_trace(go.Scatter(x=X,y=Y,mode="lines",line=go.scatter.Line(color="crimson"),name="Tendance des insultes"))
fig_analyse_3.add_trace(go.Scatter(x=X,y=Y_croissance,mode="lines",line=go.scatter.Line(color="blue"),name="Croissance des insultes en cas de vagues d'harcèlement"))

app.layout = html.Div([
        html.Div(style={"height":"50px","background-color":"#2c3e50","width":"100%"}),
        dbc.Container([
        dcc.Location(id="url"),
        html.H1("Résultats de l'analyse du compte de @"+screen_name,style={"margin-top":"25px","margin-bottom":"40px"}),
        dbc.Card([
            dbc.CardHeader("Détection récentes d'insultes"),
            dbc.CardBody([dcc.Graph(id= 'graph1', figure=fig_analyse_1),
            dbc.FormGroup(
                [
                dbc.Checklist(
                options=[
                    {"label": "Mettre en valeur les utilisateurs influents", "value": 1},
                ],
                value=[],
                id="switches-input",
                switch=True,
        ),
    ]
)
        ])],
            className="card border-primary mb-3"),
        dbc.Card([
            dbc.CardHeader("Détection d'insultes populaires"),
            dbc.CardBody(dcc.Graph(id= 'graph2', figure=fig_analyse_2))],
            className="card border-primary mb-3"),
        dbc.Card([
            dbc.CardHeader("Détection de tendances d'insultes"),
            dbc.CardBody(dcc.Graph(id= 'graph3', figure=fig_analyse_3))],
            className="card border-primary mb-3"),
    ],style={"padding":"0.5em"}
)],style={"width":"100%"},id="page-content")

@app.callback(
    Output("graph1", "figure"),
    [
        Input("switches-input", "value"),
    ],
)
def on_form_change(switches_value):
    if 1 in switches_value:
        return px.scatter(dataframe,x="date",y="avrg_hate",marginal_x='histogram', marginal_y='histogram',color="insult",size="followers")
    return px.scatter(dataframe,x="date",y="avrg_hate",marginal_x='histogram', marginal_y='histogram',color="insult")


if __name__ == "__main__":
    app.run_server(port=8888)