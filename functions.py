def adjust_country_name(country):
    ''' Match (Python swith) case
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

def geo_map_conditions(x):
    ''' Multicondition apply function for geo maps, built using:
        https://stackoverflow.com/a/47103408
        - We want relevant medals data to plot on a scatter geo map
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
        User can specify season Winter/Summer. Default both
    '''
    df = split_game_type(df, game_type)
    new_df = df.groupby(column, as_index=False).apply(geo_map_conditions)
    return new_df



def make_geo_map(df, selected_years, game_type=None):
    ''' Creates a plotly scatter geo plot based on a DataFrame on Olympic data
        Can specify season: Summer or Winter
    '''
    import plotly.express as px
    df = split_by_years(df, selected_years)
    df = geo_groupby(df, game_type=game_type)
    fig = px.scatter_geo(df, locations="iso_alpha",
                        hover_name="country",
                        hover_data=["golds", "silvers","bronzes"],
                        size="total",
                        color="mean",
                        #range_color=(0,3000),
                        projection="natural earth"
                        )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}) # Zooms the map by default
    fig.update_traces(dict(marker_line_width=0)) # Removes faded marker around bubbles (I didn't like them)
    fig.update_geos(showland=True, landcolor="Green",showocean=True, oceancolor="LightBlue") # Changed colors for increased contrast

    return fig
        
def set_country_names(df):
    df["country"] = df["country"].apply(lambda x: adjust_country_name(x))
    return df

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

def clean_olympics(df):
    ''' Tailored function to clean DataFrame
        See notebook for reasoning
    '''
    # Drop Mixed teams
    df = df.drop(df.loc[df['country'] == "Mixed team"].index)
    # Fix Serbia & Kuwait
    df.loc[186, "country"] = "Kuwait"
    df.loc[816, "country"] = "Serbia"
    return df

def summer_winter_games(df):
    ''' Static simple composition showing summer vs winter games '''
    import plotly.express as px
    df = df["games_type"].value_counts(dropna=False)
    fig = px.pie(
        df,
        values=df.values,
        names=df.keys()
        )
    return fig

def host_by_country(df):
    ''' Static bar chart showing host by country comparision'''
    ## Host by country
    import plotly.express as px
    df = df.groupby(["year"], as_index=False)["host_country"].max()
    fig = px.bar(
        x=df["host_country"].unique(),
        y=df["host_country"].value_counts(dropna=False),
        color=df["host_country"].unique()
        )
    return fig


def set_countries_alpha(df, column):
    ''' Gets all the alpha codes from select country column'''
    df["iso_alpha"] = df[column].apply(lambda x: get_country_alpha(x))
    return df

def set_olympic_medals(df):
    ''' Rudementariy aggergation of gold, silver, bronze medals to new column'''
    df.eval('olympic_medals = gold + silver + bronze', inplace=True)
    return df

def pie_plot_medals(df, country=None, year=None):
    ''' Takes a DataFrame and returns a pie chart on medal distributions
        Optinal: country and/or year for more specific charts
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
    
    fig = px.pie(_df, values=_df.array, names=_df.keys())
    fig.update_layout(legend={"title":"Medals"})
    return fig

def bar_distribution_maker(df, selected_years, game_type):
    ''' Takes a DataFrame and returns a column chart on distributions
         - Can be specified to 
        Columns: athletes, teams or	competitions
    '''
    import pandas as pd
    import plotly_express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    df = split_game_type(df, game_type)
    columns = ["athletes", "teams", "competitions"]
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    df = split_by_years(df, selected_years)
    secondary = [0,1,1]
    for i, c in enumerate(columns):
        __df = df.groupby(["year"], as_index=False)[c].max().T
        # make first row header
        new_header = __df.iloc[0]
        __df = __df[1:]
        __df.columns = new_header
        fig.add_trace(go.Scatter(x=__df.T.index, y=__df.T[c], name=str(c)),secondary_y=secondary[i])
    
    fig.update_layout(legend={"title":None})
    fig.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
    fig.update_layout(yaxis1={"title": "Athelets"},yaxis2={"title": "Teams & Competitions"},)
    return fig