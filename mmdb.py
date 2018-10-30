from googleapiclient.discovery import build
from google.oauth2 import service_account
import tmdbsimple as tmdb

scope = ['https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/spreadsheets']
sa_file = '../../Secrets/mmdb_secret.json'
spreadsheetID = '1ege7bvaIgUs7Y4OETbtdiQ_ISgwtGzH9zlZeBKYPXY8'

tmdb_api_key = '../../Secrets/tmdb_secret'


def connect_sheets_api(api_scope, api_sa_file):
    creds = service_account.Credentials.from_service_account_file(api_sa_file, scopes=api_scope)
    gsheets = build('sheets', 'V4', credentials=creds)
    return gsheets


def connect_tmdb(tmdb_key):
    with open(tmdb_key) as f:
        api_key = [line.strip() for line in list(f)]
    tmdb.API_KEY = api_key
    tmdb_search = tmdb.Search()
    return tmdb_search


def get_movies(sheet_connect, spreadsheet):
    gsheet_range = 'A:F'
    gsheet_data = sheet_connect.spreadsheets().values().get(spreadsheetId=spreadsheet, range=gsheet_range).execute()
    gsheet_values = gsheet_data.get('values', [])
    return gsheet_values


def get_genres(genre_ids,tmdb_key):
    with open(tmdb_key) as f:
        api_key = [line.strip() for line in list(f)]
    tmdb.API_KEY = api_key
    tmdb_genres = tmdb.Genres().movie_list()
    print(tmdb_genres)
    for genre_id in genre_ids:
        for genre in tmdb_genres:
            if genre.get('id') == genre_id:
                print(genre.get('name'))


def main():
    sheet_connect = connect_sheets_api(scope, sa_file)
    movies = get_movies(sheet_connect, spreadsheetID)

    tmdb_search = connect_tmdb(tmdb_api_key)

    if not movies:
        print('No data found')
    else:
        for movie in movies:
            tmdb_search.movie(query=movie[0])
            result = tmdb_search.results[0]
            # lijst = itemgetter('title', 'id', 'vote_average', 'poster_path', 'overview', 'genre_ids')(result)
            print(result)

            movie_title = result.get('title')
            movie_id = result.get('id')
            movie_score = result.get('vote_average')
            movie_image = 'https://image.tmdb.org/t/p/original' + result.get('poster_path')
            movie_description = result.get('overview')
            movie_genres = result.get('genre_ids')
            genres = get_genres(movie_genres, tmdb_api_key)
            # for genre_id in movie_genres:
            #     genre_request = tmdb.Genres(genre_id)
            #     movie_genre = genre_request.info()
            #     print(movie_genre)
            new_values = [[movie_id, movie_score, movie_image, movie_description]]
            # print(new_values)
            body = {'values': new_values}
            value_input_option = 'RAW'
            #service.spreadsheets().values().update(spreadsheetId=spreadsheet, range=range,
            #                                       valueInputOption=value_input_option, body=body).execute()


if __name__ == '__main__':
    main()
