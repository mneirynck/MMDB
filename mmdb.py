from googleapiclient.discovery import build
from google.oauth2 import service_account
import tmdbsimple as tmdb

scope = ['https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/spreadsheets']
sa_file = '../../Secrets/mmdb_secret.json'


def main():
    creds = service_account.Credentials.from_service_account_file(sa_file, scopes=scope)

    with open('../../Secrets/tmdb_secret') as f:
        tmdb_api_key = [line.strip() for line in list(f)]

    service = build('sheets', 'V4', credentials=creds)

    spreadsheet = '1ege7bvaIgUs7Y4OETbtdiQ_ISgwtGzH9zlZeBKYPXY8'
    range = 'A'
    result = service.spreadsheets().values().get(spreadsheetId=spreadsheet, range=range).execute()
    values = result.get('values', [])

    tmdb.API_KEY = tmdb_api_key

    tmdb_search = tmdb.Search()

    if not values:
        print('No data found')
    else:
        for row in values:
            tmdb_search.movie(query=row[0])
            result = tmdb_search.results[0]
            # lijst = itemgetter('title', 'id', 'vote_average', 'poster_path', 'overview', 'genre_ids')(result)
            print(result)
            movie_title = result.get('title')
            movie_id = result.get('id')
            movie_score = result.get('vote_average')
            movie_image = 'https://image.tmdb.org/t/p/original' + result.get('poster_path')
            movie_description = result.get('overview')
            movie_genres = result.get('genre_ids')
            # for genre_id in movie_genres:
            #     genre_request = tmdb.Genres(genre_id)
            #     movie_genre = genre_request.info()
            #     print(movie_genre)
            new_values = [[movie_id, movie_score, movie_image, movie_description]]
            # print(new_values)
            body = {'values': new_values}
            value_input_option = 'RAW'
            service.spreadsheets().values().update(spreadsheetId=spreadsheet, range=range,
                                                   valueInputOption=value_input_option, body=body).execute()


if __name__ == '__main__':
    main()
