from googleapiclient.discovery import build
from google.oauth2 import service_account
from oauth2client import file, client, tools
import tmdbsimple as tmdb

scope = ['https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/spreadsheets']
sa_file = '/home/matthew/Secrets/mmdb_secret.json'
tmdb.API_KEY = '2b9e09520a4454a1e2922fb9dde72137'

def main():
    creds = service_account.Credentials.from_service_account_file(sa_file, scopes=scope)
    tmdb_search = tmdb.Search()
    #if not creds or cred.invalid:
    #    flow = client.flow_from_clientsecrets('client_secret.json', scope)
    #    creds = tools.run_flow(flow, store)
    service = build('sheets', 'V4', credentials=creds)

    spreadsheet = '1ege7bvaIgUs7Y4OETbtdiQ_ISgwtGzH9zlZeBKYPXY8'
    range = 'A2:D'
    result = service.spreadsheets().values().get(spreadsheetId=spreadsheet,range=range).execute()

    values = result.get('values', [])

    if not values:
        print('No data found')
    else:
        print(values)
        for row in values:
            response = tmdb_search.movie(query=row[0])
            print(response)
            #print('%s, %s' % (row[0], row[3]))

if __name__ == '__main__':
    main()
