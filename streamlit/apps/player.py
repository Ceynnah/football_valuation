import streamlit as st
import datetime
import requests
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib

st.set_page_config(
     page_title="Player Details",
     page_icon=":soccer:",
     layout="centered",
     initial_sidebar_state="collapsed",
     menu_items={'About': "Ask us about out project: contact details bla bla bla check our GitHub"}
 )

def app(input_name):

    # url to request
    url = "https://raw.githubusercontent.com/sixtine2/football_valuation/master/data/final_data_v1.csv"
    # pretty print JSON data
    df = pd.read_csv(url, sep = ';')
    dict_player = df.loc[df['pretty_name'] == input_name].to_dict(orient='records')[0]

    ###

    player_age = dict_player['age']
    position = dict_player['position']

    games_played = dict_player['Games']
    mean_games = np.mean(df['Games'][df['position'] == position])
    vs_average_games = int(((games_played - mean_games) / mean_games*100))

    goals = dict_player['Goals']
    mean_goals = np.mean(df['Goals'][df['position'] == position])
    vs_average_goals = int(((goals - mean_goals) / mean_goals*100))

    assists = dict_player['Assists']
    mean_assists = np.mean(df['Assists'][df['position'] == position])
    vs_average_assists = int(((assists - mean_assists) / mean_assists*100))

    spg = round(dict_player['SpG'],1)
    mean_spg = round(np.mean(df['SpG'][df['position'] == position]),1)
    vs_average_spg = int(((spg - mean_spg) / mean_spg*100))

    rating = round(dict_player['Rating'],1)
    mean_rating = round(np.mean(df['Rating'][df['position'] == position]),1)
    vs_average_rating = int(((rating - mean_rating) / mean_rating*100))

    tackles = round(dict_player['Tackles'],1)
    mean_tackles = round(np.mean(df['Tackles'][df['position'] == position]),1)
    vs_average_tackles = int(((tackles - mean_tackles) / mean_tackles*100))

    interceptions = round(dict_player['Interceptions'],1)
    mean_interceptions = round(np.mean(df['Interceptions'][df['position'] == position]),1)
    vs_average_interceptions = int(((interceptions - mean_interceptions) / mean_interceptions*100))

    fouls = round(dict_player['Fouls commited'],1)
    mean_fouls = round(np.mean(df['Fouls commited'][df['position'] == position]),1)
    vs_average_fouls = int(((fouls - mean_fouls) / mean_fouls*100))

    dribbled = round(dict_player['Dribbled past'],1)
    mean_dribbled = round(np.mean(df['Dribbled past'][df['position'] == position]),1)
    vs_average_dribbled = int(((dribbled - mean_dribbled) / mean_dribbled*100))

    key_passes = round(dict_player['Key Passes'],1)
    mean_key_passes = round(np.mean(df['Key Passes'][df['position'] == position]),1)
    vs_average_key_passes = int(((key_passes - mean_key_passes) / mean_key_passes*100))

    dribbles = round(dict_player['Dribbles'],1)
    mean_dribbles = round(np.mean(df['Dribbles'][df['position'] == position]),1)
    vs_average_dribbles = int(((dribbles - mean_dribbles) / mean_dribbles*100))

    fouled = round(dict_player['Fouled'],1)
    mean_fouled = round(np.mean(df['Fouled'][df['position'] == position]),1)
    vs_average_fouled = int(((fouled - mean_fouled) / mean_fouled*100))

    aearials_won = round(dict_player['Aearials Won'],1)
    mean_aearials_won = round(np.mean(df['Aearials Won'][df['position'] == position]),1)
    vs_average_aearials_won = int(((aearials_won - mean_aearials_won) / mean_aearials_won*100))

    clearances = round(dict_player['Clearances'],1)
    mean_clearances = round(np.mean(df['Clearances'][df['position'] == position]),1)
    vs_average_clearances = int(((clearances - mean_clearances) / mean_clearances*100))

    contract_expires = int(dict_player['club_contract_valid_until'])
    club_name = dict_player['club_name']
    country_name = dict_player['Nationality']

    market_value = dict_player['market_value_in_eur']
    mean_value = np.mean(df['market_value_in_eur'])
    vs_average_value = int(((market_value - mean_value) / mean_value*100))

    player_face = dict_player['player_face_url']
    club_logo = dict_player['club_logo_url']
    nation_logo = dict_player['nation_logo_url']

    #st.set_page_config(layout="wide")
    st.markdown("<h1 style='text-align: center; color: #0f4581;'>{}</h1>".format(input_name), unsafe_allow_html=True)

    col1, col2, col3 = st.columns([8, 5, 8])
    with col1:
        st.write("")
    with col2:
        st.image(player_face, use_column_width=True)
    with col3:
        st.write("")

    col1, col2, col3, col4, col5 = st.columns([5, 1, 4, 1, 5])
    with col1:
        st.write("")
    with col2:
        st.image(club_logo)
    with col3:
        st.markdown("<p style='text-align: center; color: #002448;'>{}</p>".format(club_name), unsafe_allow_html=True)
    with col4:
        st.image(club_logo)
    with col5:
        st.write("")


    #st.image(player_face)
    #st.image(club_logo)
    #st.markdown("<img src='https://cdn.sofifa.net/players/158/023/22_120.png'")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Position: ", str(position))
    col2.metric("Age: ", str(player_age))
    col3.metric("Transfermarkt value: ", "€" + str(round(market_value/1_000_000,1)).format('{:,.0f}') + "M", f'{vs_average_value}% vs. average')
    col4.metric("Our value: ", "€" + str(round(market_value/1_000_000,1)).format('{:,.0f}') + "M", f'{vs_average_value}% vs. average') # TO DO

    st.markdown("""<hr style="height:1px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

    st.subheader('Recent performance snapshot (2019-2022):')
    st.markdown(""" *The percentages of evolution are calculated in relation to the average of players playing the same position.*
                """)
    st.markdown("<h5 style='text-align: center; border:1px;'>Total statistics</h5>", unsafe_allow_html=True)

    if position != 'Goalkeeper' :
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🏟️ Games", int(games_played), f'{vs_average_games}%')
        col2.metric("⚽ Goals", int(goals), f'{vs_average_goals}%')
        col3.metric("🎯 Assists", int(assists), f'{vs_average_assists}%')
        col4.metric("🏅 Average Rating", rating, f'{vs_average_rating}%')
    else :
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🏟️ Games", int(games_played), f'{vs_average_games}%')
        col2.metric("🪁 Aearials Won p.G.", aearials_won, f'{vs_average_aearials_won}%')
        col3.metric("🎯 Clearances p.G.", clearances, f'{vs_average_clearances}%')
        col4.metric("🏅 Average Rating", rating, f'{vs_average_rating}%')


    if position == 'Attack':
        st.markdown("<h5 style='text-align: center; border:1px;'>Statistics per Game</h5>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("👟 Shots", spg, f'{vs_average_spg}%')
        col2.metric("🔁 Key Passes", key_passes, f'{vs_average_key_passes}%')
        col3.metric("🏃🏽 Dribbles", dribbles, f'{vs_average_dribbles}%')
        col4.metric("🤹‍♂️ Fouled", fouled, f'{vs_average_fouled}%')

    elif position == 'Midfield':
        st.markdown("<h5 style='text-align: center; border:1px;'>Statistics per Game</h5>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("👟 Shots", spg, f'{vs_average_spg}%')
        col2.metric("🔁 Key Passes", key_passes, f'{vs_average_key_passes}%')
        col3.metric("🏃🏽 Dribbles", dribbles, f'{vs_average_dribbles}%')
        col4.metric("🤹‍♂️ Fouled", fouled, f'{vs_average_fouled}%')

    elif position == 'Defender':
        st.markdown("<h5 style='text-align: center; border:1px;'>Statistics per Game</h5>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("✋ Interceptions", interceptions, f'{vs_average_interceptions}%')
        col2.metric("🤹‍♂️ Fouls committed", fouls, f'{vs_average_fouls}%')
        col3.metric("🏃🏽 Dribbled past", dribbled, f'{vs_average_dribbled}%')
        col4.metric("🥋 Tackles", tackles, f'{vs_average_tackles}%')


    else:
        pass

    st.markdown("""<hr style="height:1px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

    st.subheader('Market value bridge:')

    url_w = "https://raw.githubusercontent.com/sixtine2/football_valuation/master/data/Wagon%20-%20Waterfall.csv"
    df_waterfall = pd.read_csv(url_w)
    dict_player_w = df_waterfall.loc[df_waterfall['player_name'] == input_name].to_dict(orient='records')[0]
    game_stats = dict_player_w['game_stats']
    physical_factors = dict_player_w['physical_factors']
    contract_terms = dict_player_w['contract_terms']
    popularity = dict_player_w['popularity']
    bias = dict_player_w['bias']
    market_value_tfm = game_stats + physical_factors + contract_terms + popularity + bias
    fig = go.Figure(go.Waterfall(
		name = "20", orientation = "v",
		measure = ["relative", "relative", "relative", "relative", "relative", "total"],
		x = ["Game Stats", "Physical Factors", "Contract Terms", "Popularity", "Bias", "Market Value (TFM)"],
		textposition = "outside",
		text = [str(round(game_stats)) + "M", str(round(physical_factors)) + "M",str(round(contract_terms)) + "M", str(round(popularity)) + "M", str(round(bias)) + "M", str(round(market_value_tfm)) + "M"],
		y = [game_stats, physical_factors, contract_terms, popularity, bias, market_value_tfm],
		connector = {"line":{"color":"rgb(210, 210, 210)"}}
	))
    fig.update_layout(
			font_family="Helvetica",
		#  title = "Market Value Bridge",
			showlegend = False,
		plot_bgcolor='rgb(255,255,255)'
	)
    fig.update_layout(yaxis={'visible': False, 'showticklabels': False})
    fig.update_layout(xaxis={'visible': True, 'showticklabels': True}, xaxis_title=None)

    st.plotly_chart(fig)

    st.markdown("""<hr style="height:1px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

    st.subheader('Similar players:')

    model = joblib.load('streamlit/knn.pkl')
    scaler = joblib.load('streamlit/scaler.pkl')

    df_players = pd.read_csv('https://raw.githubusercontent.com/sixtine2/football_valuation/master/streamlit/players.csv', index_col=0, sep=';')

    list_players = df_players['pretty_name']
    list_players = pd.concat([pd.Series(['']), list_players])

    selected_player = st.selectbox('Select a player', list_players)

    if selected_player:

        X_players = df_players.drop(columns=['position', 'pretty_name', 'player_id',
		'Minutes played', 'MotM', 'Games', 'Rating', 'club_contract_valid_until',
		'release_clause_eur', 'market_value_in_eur', 'missed_games', 'wiki_views', 'insta_followers',
		'age', 'height_cm', 'club_name', 'weight_kg', 'foot', 'Nationality', 'Yellow cards', 'Red cards',
		'Play_in_CL', 'player_face_url','club_logo_url', 'club_flag_url', 'nation_logo_url', 'nation_flag_url',
		'player_positions', 'overall', 'potential', 'wage_eur'])

        idx = df_players[df_players['pretty_name'] == selected_player].index[0]

        df_player_selected = df_players.iloc[idx:idx+1]

        df_player_selected = df_player_selected.drop(columns=['position', 'pretty_name', 'player_id',
		'Minutes played', 'MotM', 'Games', 'Rating', 'club_contract_valid_until',
		'release_clause_eur', 'market_value_in_eur', 'missed_games', 'wiki_views', 'insta_followers',
		'age', 'height_cm', 'club_name', 'weight_kg', 'foot', 'Nationality', 'Yellow cards', 'Red cards',
		'Play_in_CL', 'player_face_url','club_logo_url', 'club_flag_url', 'nation_logo_url', 'nation_flag_url',
		'player_positions', 'overall', 'potential', 'wage_eur'])

        df_player_selected = scaler.transform(df_player_selected)

        neighbors = model.kneighbors(df_player_selected, n_neighbors=4)

        col_player1, col_player2, col_player3 = st.columns(3)
        with col_player1:
            st.image(df_players.iloc[neighbors[1][0][1]]['player_face_url'], width=200)
            st.markdown("<p style='text-align: center; color: #002448;'><b><font size='+4'>{}</font></b></p>".format(df_players.iloc[neighbors[1][0][1]]['pretty_name']), unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #002448;'><font size='+3.5'>{}</font></p>".format(df_players.iloc[neighbors[1][0][1]]['club_name']), unsafe_allow_html=True)
        with col_player2:
            st.image(df_players.iloc[neighbors[1][0][2]]['player_face_url'], width=200)
            st.markdown("<p style='text-align: center; color: #002448;'><b><font size='+4'>{}</font></b></p>".format(df_players.iloc[neighbors[1][0][2]]['pretty_name']), unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #002448;'><font size='+3.5'>{}</font></p>".format(df_players.iloc[neighbors[1][0][2]]['club_name']), unsafe_allow_html=True)
        with col_player3:
            st.image(df_players.iloc[neighbors[1][0][3]]['player_face_url'], width=200)
            st.markdown("<p style='text-align: center; color: #002448;'><b><font size='+4'>{}</font></b></p>".format(df_players.iloc[neighbors[1][0][3]]['pretty_name']), unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #002448;'><font size='+3.5'>{}</font></p>".format(df_players.iloc[neighbors[1][0][3]]['club_name']), unsafe_allow_html=True)

        col_comparison1,col_comparison2,col_comparison3, col_comparison4, col_comparison5, col_comparison6  = st.columns(6)
        with col_comparison1:
            st.markdown('Age: ' + str(df_players.iloc[neighbors[1][0][1]]['age']))
            st.markdown('Value: ' + str(df_players.iloc[neighbors[1][0][1]]['market_value_in_eur'] + 'M€'))
        with col_comparison2:
            st.markdown('Rating: ' + str(df_players.iloc[neighbors[1][0][1]]['Rating']))
            st.markdown('Wage: ' + str(df_players.iloc[neighbors[1][0][1]]['wage_eur']+ 'K€'))
        with col_comparison3:
            st.markdown('Age: ' + str(df_players.iloc[neighbors[1][0][2]]['age']))
            st.markdown('Value: ' + str(df_players.iloc[neighbors[1][0][2]]['market_value_in_eur'] + 'M€'))
        with col_comparison4:
            st.markdown('Rating: ' + str(df_players.iloc[neighbors[1][0][2]]['Rating']))
            st.markdown('Wage: ' + str(df_players.iloc[neighbors[1][0][2]]['wage_eur']+ 'K€'))
        with col_comparison5:
            st.markdown('Age: ' + str(df_players.iloc[neighbors[1][0][3]]['age']))
            st.markdown('Value: ' + str(df_players.iloc[neighbors[1][0][3]]['market_value_in_eur'] + 'M€'))
        with col_comparison6:
            st.markdown('Rating: ' + str(df_players.iloc[neighbors[1][0][3]]['Rating']))
            st.markdown('Wage: ' + str(df_players.iloc[neighbors[1][0][3]]['wage_eur']+ 'K€'))

        col_comparison4, col_comparison5, col_comparison6 = st.columns(3)
        col_comparison4.markdown('Position: ' + str(df_players.iloc[neighbors[1][0][1]]['player_positions']))
        col_comparison5.markdown('Position: ' + str(df_players.iloc[neighbors[1][0][2]]['player_positions']))
        col_comparison6.markdown('Position: ' + str(df_players.iloc[neighbors[1][0][3]]['player_positions']))


if __name__ == "__main__":
     app()
