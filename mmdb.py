from googleapiclient.discovery import build
from google.oauth2 import service_account
from oauth2client import file, client, tools

scope = ['https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/spreadsheets']
sa_file = '/home/matthew/Secrets/mmdb_secret.json'

def main():
    #store = file.Storage('token.json')
    #creds = store.get()
    creds = service_account.Credentials.from_service_account_file(sa_file, scopes=scope)

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
        print('Movie, Description')
        for row in values:
            print('%s, %s' % (row[0], row[3]))

if __name__ == '__main__':
    main()
