# helper functions
def get_country_alpha(country):
    ''' Simple function to return iso alpha code of a country '''
    from iso3166 import countries
    c = countries.get(country)
    return c[2]

def get_country_name(alpha):
    ''' Simple function to return name of a country based on iso alpha'''
    from iso3166 import countries
    c = countries.get(alpha)
    return c[0]

def split_game_type(df, game_type):
    ''' Splits the df for a certain game_type
        - Summer or Winter
    '''
    if game_type == "Summer" or game_type == "Winter":
        df = df.loc[df['games_type'] == game_type]
    return df

def split_by_years(df, selected_years):
    ''' Splits a DataFrame in the year column based on a list
        of years and returns it
        - selected_years[start_year, end_year]
    '''
    df = df[~(df['year'] < selected_years[0])]
    df = df[~(df['year'] > selected_years[1])]
    return df

def format_trace(df, column):
        ''' Groups a column by years and and DataFrame column, sets new headers for easy trace ploting
            - column: "athletes", "teams", "competitions"
        '''
        df = df.groupby(["year"], as_index=False)[column].max().T
        new_header = df.iloc[0]
        df = df[1:]
        df.columns = new_header
        return df

def adjust_country_name(country):
    ''' A match (Python swith) case for Olympic data to ISO country
        Assumes the appropriate ISO name of a country as names have changed over time.
        - This function is in no way politically correct
    '''

    match country:
        case "People's Republic of China" | "ROC" | "Chinese Taipei":
            return "Taiwan"
        case "Hong Kong, China":
            return "Hong Kong"
        case "Republic of Korea" | "Democratic People's Republic of Korea":
            return "Korea, Republic of"
        case "Islamic Republic of Iran":
            return "Iran, Islamic Republic of"
        case "Moldova":
            return "Moldova, Republic of"
        case "Turkey":
            return "Türkiye"
        case "Venezuela":
            return "Venezuela, Bolivarian Republic of"
        case "Vietnam":
            return "Viet Nam"
        case "Serbia and Montenegro" | "Yugoslavia": # https://en.wikipedia.org/wiki/Yugoslavia
            return "Serbia"
        case "Czechoslovakia":
            return "Czechia"
        case "Unified Team" | "USSR": # https://en.wikipedia.org/wiki/Unified_Team_at_the_Olympics
            return "Russian Federation"
        case "Federal Republic of Germany" | "German Democratic Republic (Germany)":
            return "Germany"
        case "Virgin Islands, US":
            return "Virgin Islands, U.S."
        case "United Kingdom" | "Great Britain":
            return "United Kingdom of Great Britain and Northern Ireland"
        case "Netherlands Antilles":
            return "Netherlands"
        case "United Republic of Tanzania":
            return "Tanzania, United Republic of"
        case _ :
            return country

def set_country_names(df):
    df["country"] = df["country"].apply(lambda x: adjust_country_name(x))
    return df

def set_countries_alpha(df, column):
    ''' Gets all the alpha codes from select country column'''
    df["iso_alpha"] = df[column].apply(lambda x: get_country_alpha(x))
    return df

def set_olympic_medals(df):
    ''' Rudementariy aggergation of gold, silver, bronze medals to new column'''
    df.eval('olympic_medals = gold + silver + bronze', inplace=True)
    return df

# Compressed cleaning function
def clean_olympics(df):
    ''' Tailored function to clean the Olympics DataFrame
        See notebook for reasoning
    '''
    df = df.drop(df.loc[df['country'] == "Mixed team"].index)
    df.loc[186, "country"] = "Kuwait"
    df.loc[816, "country"] = "Serbia"
    return df     

# Plots
def summer_winter_games(df):
    ''' Static simple composition showing summer vs winter games '''
    import plotly.express as px
    df = df["games_type"].value_counts(dropna=False)
    fig = px.pie(
        df,
        values=df.values,
        color=df.keys(),
        color_discrete_map={'Summer':'darkgreen',
                            'Winter': 'lightcyan'}
        )
    fig.update_layout(title=dict(text="Summer vs Winter games"))
    fig.update_layout(showlegend=False)
    return fig

def host_by_country(df):
    ''' Takes a DataFrame and returns a bar chart for comparision of times counties have been host '''
    import plotly.express as px
    df = df.groupby(["year"], as_index=False)["host_country"].max()
    fig = px.bar(
        x=df["host_country"].unique(),
        y=df["host_country"].value_counts(dropna=False),
        color=df["host_country"].unique()
        )
    fig.update_layout(title=dict(text="Times Hosted by Country"), legend={"title":None})
    fig.update_xaxes(showticklabels=False)
    fig.update_layout(xaxis={"title":None},yaxis={"title": "Times Hosted"},)
    return fig

def pie_plot_medals(df, country=None, year=None):
    ''' Takes a DataFrame and returns a pie chart on medal distributions
        - Can be adjusted with a country. Ex: "Sweden"
        - Can be adjusted with a year. Ex: 2016
    '''
    import plotly_express as px
    medals = ["gold", "silver", "bronze"]
    if country != None and year != None:  
        _df = df.loc[(df['country'] == country) & (df['year'] == year)][medals].sum()
    elif country != None:
        _df = df.loc[df['country'] == country][medals].sum()
    elif year != None:
        _df = df.loc[df['year'] == year][medals].sum()
    else:
        _df = df[medals].sum()
    
    fig = px.pie(_df, values=_df.array, color=_df.keys(),
                 color_discrete_map={
                     'gold':'rgb(255, 215, 0)',
                     'silver':'rgb(	192, 192, 192)',
                     'bronze':'rgb(	205, 127, 50)',
                     })
    fig.update_layout(title=dict(text=f"{country}'s medals"), legend={"title":"Medals"})
    return fig

def bar_distribution_maker(df, selected_years, game_type):
    ''' Takes a DataFrame and returns a column chart on "athletes", "teams", "competitions" distributions by year
         - Can be adjusted with a range (list of years) Ex: [1896, 2022]
         - Can be adjusted with a game_type "Summer", "Winter"
    '''
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    df = split_game_type(df, game_type)
    columns = ["athletes", "teams", "competitions"]
    secondary = [0,1,1] # Custom array for which Yaxis to apply
    fig = make_subplots(specs=[[{"secondary_y": True}]])     # Create figure with secondary y-axis
    df = split_by_years(df, selected_years)
    for i, c in enumerate(columns): # Loop to make trace (line) for each column and apply it to Y axis from secondary[]
        _df = format_trace(df, c)
        fig.add_trace(go.Scatter(x=_df.T.index, y=_df.T[c], name=str(c)),secondary_y=secondary[i])

    fig.update_layout(title=dict(text="Atheletes, Teams and Compisitions"),
                      legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01, title=None),
                      xaxis={"title":"Year"}, yaxis1={"title": "Athelets"},yaxis2={"title": "Teams & Competitions"},
                      )
    return fig

# geographical plot
def geo_map_conditions(x):
    ''' Multicondition apply function for geo maps, built using:
        - We want relevant medals data to plot on a scatter geo map
        - https://stackoverflow.com/a/47103408; pd.DataFrame.agg workaround
    '''
    import pandas as pd
    d = {}
    d['country'] = x['country'].max()
    d['iso_alpha'] = x['iso_alpha'].max()
    d['golds'] = x['gold'].sum()
    d['silvers'] = x['silver'].sum()
    d['bronzes'] = x['bronze'].sum()
    d['total'] = x['olympic_medals'].sum()
    d['mean'] = x['olympic_medals'].mean()
    return pd.Series(d, index=['country','iso_alpha','golds', 'silvers', 'bronzes', 'total', 'mean'])

def geo_groupby(df, column='country', game_type=None):
    ''' Uses standard groupby with preset conditions for geo_maps
        User can specify season Winter/Summer. Default: None
    '''
    df = split_game_type(df, game_type)
    new_df = df.groupby(column, as_index=False).apply(geo_map_conditions)
    return new_df

def make_geo_map(df, selected_years, game_type=None):
    ''' Creates a plotly scatter geo plot based on a DataFrame on Olympic data
         - Can be adjusted with a range (list of years) Ex: [1896, 2022]
         - Can be adjusted with a game_type "Summer", "Winter"
    '''
    import plotly.express as px
    df = split_by_years(df, selected_years)
    df = geo_groupby(df, game_type=game_type)
    fig = px.choropleth(df, locations="iso_alpha",
                        hover_name="country",
                        hover_data=["golds", "silvers","bronzes"],
                        color="total",
                        color_continuous_scale=px.colors.sequential.deep,
                        )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}) # Zooms the map by default
    fig.update_geos(showland=True,showocean=True, showcountries=True, oceancolor="LightBlue")

    return fig