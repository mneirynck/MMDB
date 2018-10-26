from googleapiclient.discovery import build
from google.oauth2 import service_account
from operator import itemgetter
import tmdbsimple as tmdb

scope = ['https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/spreadsheets']
sa_file = '../../Secrets/mmdb_secret.json'

def main():
    creds = service_account.Credentials.from_service_account_file(sa_file, scopes=scope)

    with open('../../Secrets/tmdb_secret') as f:
        tmdb_api_key = [ line.strip( ) for line in list(f) ]

    service = build('sheets', 'V4', credentials=creds)

    spreadsheet = '1ege7bvaIgUs7Y4OETbtdiQ_ISgwtGzH9zlZeBKYPXY8'
    range = 'A2:F'
    result = service.spreadsheets().values().get(spreadsheetId=spreadsheet,range=range).execute()
    values = result.get('values', [])

    tmdb.API_KEY = tmdb_api_key

    tmdb_search = tmdb.Search()

    if not values:
        print('No data found')
    else:
        for row in values:
            request = tmdb_search.movie(query=row[0])
            result = tmdb_search.results[0]
            #lijst = itemgetter('title', 'id', 'vote_average', 'poster_path', 'overview', 'genre_ids')(result)
            #print(lijst)
            movie_title = result.get('title')
            movie_id = result.get('id')
            new_values = [[movie_title, movie_id]]
            body = {'values': new_values}
            value_input_option = 'RAW'
            push = service.spreadsheets().values().update(spreadsheetId=spreadsheet,range=range,valueInputOption=value_input_option,body=body).execute()
            print('{0} cells updated.'.format(result.get('updatedCells')));

if __name__ == '__main__':
    main()
