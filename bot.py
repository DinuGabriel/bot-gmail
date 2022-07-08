import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
import email
import re
import base64


# if modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']


def get_service():
    
    creds = None
    # the file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # if there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    
    return service


def search_messages_in_interval(service, user_id, search_string):

    try:
        label_id_one = 'INBOX'
        label_id_two = 'UNREAD'
        # getting all the unread messages from a time interval from Inbox
        # labelIds can be changed accordingly
        search_id = service.users().messages().list(
            userId = user_id, 
            q = search_string, 
            labelIds=[label_id_one, label_id_two]
        ).execute()

        number_results = search_id['resultSizeEstimate']

        unread_message_ids = []

        if number_results > 0:
            message_ids = search_id['messages']

            for ids in message_ids:
                unread_message_ids.append(ids['id'])
            return unread_message_ids
        
        else:
            print('There were 0 results for that search string, returning an empty string')
    
    except HttpError as error:
        print(f'An error occurred: {error}')


def get_message_content(service, user_id, message_ids):

    final_list = []
    for msg in message_ids:

        temp_dict = {}
        message_id = msg # get id of individual message
        message = service.users().messages().get(
            userId = user_id, 
            id = message_id
        ).execute() # fetch the message using API
        payld = message['payload'] # get payload of the message
        headr = payld['headers'] # get header of the payload

        for one in headr: # getting the Subject
            if one['name'] == 'Subject':
                message_subject = one['value']
                temp_dict['Subject'] = message_subject
            else:
                pass

        for two in headr: # getting the Sender
            if two['name'] == 'From':
                message_from = two['value']
                temp_dict['Sender'] = message_from
        
        if 'parts' in payld: # getting the attchment file name
            for fname in payld['parts']:
                temp_dict['file_name'] = fname['filename']

        try:
            #fetching and decode message body by getting the raw format
            message_body = service.users().messages().get(
                userId = user_id, 
                id = message_id, 
                format = 'raw'
            ).execute()
            msg_raw = base64.urlsafe_b64decode(message_body['raw'].encode('ASCII'))
            msg_str = email.message_from_bytes(msg_raw)
            content_types = msg_str.get_content_maintype()

            if content_types == 'multipart':
                parts = list(msg_str.get_payload())
                if isinstance(parts[0].get_payload(), str):
                    temp_dict['Message_body'] = parts[0].get_payload()
                else:
                    temp_dict['Message_body'] = None
            else:
                if isinstance(msg_str.get_payload(), str):
                    temp_dict['Message_body'] = msg_str.get_payload()
                else:
                    temp_dict['Message_body'] = None

        except HttpError as error:
            print(f'An error occurred: {error}')
        
        final_list.append(temp_dict) # this will create a dictonary item in the final list
    
    return final_list


def search_keywords(key_words, content_list, message_ids):

    # getting a list of keywords with no punctuation
    key_words = re.sub("[^\w\s]", "", key_words)
    key_words = key_words.split()

    count = 0
    lista_gasiri = []
    msg_ids = []

    # getting all the messages were keywords are found 
    for element in content_list:
        lista_elemente = list(element.values())
        for i in lista_elemente:
            for key in key_words:
                if i != None:
                    if key in i:
                        lista_gasiri.append(count)
        count += 1
    
    # if key words are found multiple times in the same message 
    # this will get rid of duplicate apparitions
    lista_gasiri = list(set(lista_gasiri))

    for i in lista_gasiri: # get the message ids where keywords were found
        msg_ids.append(message_ids[i])

    return msg_ids
        

def get_attachments(service, user_id, msg_id, save_location):

    try:
        message = service.users().messages().get(
            userId = user_id, 
            id = msg_id
        ).execute() # fetch the message using API
        # going through every message parts and look for attachments
        for part in message['payload']['parts']:
            newvar = part['body']
            if 'attachmentId' in newvar:
                attachment_id = newvar['attachmentId']
                attachment = service.users().messages().attachments().get(
                    userId = user_id,
                    messageId  =msg_id, 
                    id = attachment_id
                ).execute() # fetch the attachment using API
                data = attachment['data']
                # decode the attachment data
                file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
                print(part['filename'])
                filename = part['filename']
                # saving the attachment data in a specific directory
                path = os.path.join(save_location + '\\' + filename)
                f = open(path, 'wb')
                f.write(file_data)
                f.close()


    except HttpError as error:
        print(f'An error occurred: {error}')


service = get_service()
user_id = 'me'
before = input('Please enter the first date between which you want to download the attachments(please use / for the date input, Format:YYYY/MM/DD): ')
after = input('Please enter the second date between which you want to download the attachments(please use / for the date input, second, Format:YYYY/MM/DD): ')
search_string = f'after:{before} before:{after}'

m_ids = search_messages_in_interval(service, user_id, search_string)
#print(m_ids) 

content_list = get_message_content(service, user_id, m_ids)
#print(content_list)

key_words = input('Please enter the keyword pool that you want to search for: ')

lista_gasiri = search_keywords(key_words, content_list, m_ids)
#print(lista_gasiri)

save_location = input('Please enter the path for the directory that you want to save attachments in(make sure that you have two \\ betweeen directorys in path): ')
for msg_id in lista_gasiri:
    get_attachments(service, user_id, msg_id, save_location)