message = service.users().messages().get(
                userId = user_id, 
                id = message_id
            ).execute()
            parts = message['payload']
            while parts:
                part = parts.pop()
                if part.get('parts'):
                    parts.extend(part['parts'])
                if part.get('filename'):
                    if 'data' in part['body']:
                        file_data = base64.urlsafe_b64decode(part['body']['data'].encode('UTF-8'))
                    elif 'attachmentId' in part['body']:
                        attachment = service.user().messages().attachments().get(
                            userId = user_id,
                            messageId = message_id,
                            id = part['body']['attachemntId']
                        ).execute()
                        file_data = base64.urlsafe_b64decode(attachment['data'].encode('UTF-8'))
                    else:
                        file_data = None
                    
                    if file_data:
                        path = ''.join([save_location, part['filename']])
                        with open(path, 'w') as f:
                            f.write(file_data)