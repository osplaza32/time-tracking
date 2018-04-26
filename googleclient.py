from __future__ import print_function
import httplib2
import os
import json
import datetime


from apiclient import discovery
from apiclient import errors
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from dateutil.parser import parse



try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'
# fin calendar
# to google drive
SCOPES2 = 'https://www.googleapis.com/auth/drive.metadata.readonly'
CLIENT_SECRET_FILE2 = 'client_secret.json'
APPLICATION_NAME2 = 'Drive API Python Quickstart'
# fin google drive
# to google sheets
SCOPES3 = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE3 = 'client_secret.json'
APPLICATION_NAME3 = 'Google Sheets API Python Quickstart'
# fin google sheets



def pp_json(json_thing, sort=True, indents=4):
    '''
    print nice json way
    '''
    if type(json_thing) is str:
        print(json.dumps(json.loads(json_thing), sort_keys=sort, indent=indents))
    else:
        print(json.dumps(json_thing, sort_keys=sort, indent=indents))
    return None
def get_credentials3():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE3, SCOPES3)
        flow.user_agent = APPLICATION_NAME3
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def get_credentials2():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE2, SCOPES2)
        flow.user_agent = APPLICATION_NAME2
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """

    credentials2 = get_credentials2()
    http2 = credentials2.authorize(httplib2.Http())
    #Mover
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    #page_token = None
    #calendar_list = service.calendarList().list(pageToken=page_token).execute()
    # getEvets4User(json.dumps(calendar_list),service)
    #fin de mover
    service2 = discovery.build('drive', 'v2', http=http2)
    getIdDoc(service2, '1G5R6x9ibu7ksycWJCR2nHkFD_5ZUy1Ui')



def getIdDoc(service, folder_id):
  """GET id file to a folder.

  Args:
    service: Drive API service instance.
    folder_id: ID of the folder to print files from.
  """
  credentials = get_credentials3()
  http = credentials.authorize(httplib2.Http())

  service2 = discovery.build('sheets', 'v4', http=http)
  page_token = None
  while True:
    try:
      param = {}
      if page_token:
        param['pageToken'] = page_token
      children = service.children().list(
          folderId=folder_id, **param).execute()

      for child in children.get('items', []):
          opendfile(child['id'],service2)
      page_token = children.get('nextPageToken')
      if not page_token:
        break
    except errors.HttpError:
      #print('An error occurred')
      break
def opendfile(id,service):
    """open file when have id file in a folder.

    Args:
      service: Drive API service instance.
      id: ID of the file
    """
    rangeName = 'Hoja 1!A1:J44'
    result = service.spreadsheets().get(
        spreadsheetId=id, ranges=rangeName,includeGridData=False).execute()
    nameequipo = result['properties']['title']
    result = service.spreadsheets().values().get(spreadsheetId=id, range=rangeName).execute()
    mails = getMail(result["values"][0])
    result["values"].pop(0)
    initapicalendar(result["values"],mails,nameequipo)

def getMail(entrada):
    """

    :param entrada: list of mail no depurada
    :return: list of mail depurada
    """
    entrada.pop(0)
    return entrada
def initapicalendar(hashcolletion,mails,names):
    '''

    :param hash: collection of hashes
    :param mails: colletion of username whithout @techo.org
    :param names: colletion of names
    :return: ?
    '''
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    print('***********************************************************************+*************************+')

    print(names)
    getEvets4UserHash(service,mails,hashcolletion)


def DiffCalendar(nombreactividad,calculo,hashscollettion):
    #print(nombreactividad.find(hashscollettion))
    if nombreactividad.find(hashscollettion) != -1:
        return calculo.total_seconds()
    else:
        return 0


def  getEvets4UserHash(service,mails,hashcolletion):
    print(hashcolletion)
    i = 0
    while i < len(hashcolletion):
        #print(i)
        getEvets4User(service,mails,hashcolletion[i][0])
        i+=1


def getEvets4User(service, mails, hashcolle, page_token=None):

    i = 0
    total = 0
    while i < len(mails):
        print('==================================================================================')

        print(mails[i])
        valur = mails[i]+'@techo.org'

        now = datetime.datetime.now()
        start = now - datetime.timedelta(days=now.weekday())
        end = start + datetime.timedelta(days=6)
        events = service.events().list(calendarId=valur,
                                         pageToken=page_token,
                                         timeMin=start.strftime('%Y-%m-%dT%H:%M:%S-00:00'),
                                         timeMax=end.strftime('%Y-%m-%dT%H:%M:%S-00:00')
                                         ).execute()


        items = events.get('items', [])

        for item in items:
            summary = item.get('summary', '')  # Event summary exists!! Yea!!
            start = item.get('start', '')  # Event start exists!! Yea!!
            end = item.get('end', '')  # Event start exists!! Yea!!

            if len(summary)>= 1:
                if type(start) == dict:
                    try:
                        calculo = parse(end['dateTime'])-parse(start['dateTime'])
                        total += DiffCalendar(summary, calculo, hashcolle)

                    except:
                        calculo = parse(end['date'])-parse(start['date'])
                        total += DiffCalendar(summary, calculo, hashcolle)

                else:
                    calculo = parse(end)-parse(start)
                    total += DiffCalendar(summary, calculo, hashcolle)
        page_token = events.get('nextPageToken')
        usercount4hash(total,hashcolle)
        total= 0
        

        i+=1
def usercount4hash(total,hashcolle):
    total_hash = datetime.timedelta(seconds=total)
    print("en "+hashcolle+" Se uso")
    print(total_hash)

if __name__ == '__main__':
    main()
