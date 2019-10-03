from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from httplib2 import Http
from googleapiclient.discovery import build
from oauth2client import file, client, tools

import base64
import mimetypes
import os

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


class Mail(object):
    def __init__(self, credentials_path, token_path):
        self._credentials_path = credentials_path
        self._token_path = token_path

    def _get_service(self):
        store = file.Storage(self._token_path)
        token = store.get()
        if not token or token.invalid:
            flow = client.flow_from_clientsecrets(
                self._credentials_path, SCOPES)
            token = tools.run_flow(flow, store)
        service = build("gmail", "v1", http=token.authorize(Http()))

        return service

    @staticmethod
    def create_message(to, subject, body):
        message = MIMEText(body)
        message["to"] = to
        message["from"] = "me"
        message["subject"] = subject

        byte_msg = message.as_string().encode()
        return {"raw": base64.urlsafe_b64encode(byte_msg).decode()}

    @staticmethod
    def create_message_with_image(to, subject, body, file_path):
        message = MIMEMultipart()
        message["to"] = to
        message["from"] = "me"
        message["subject"] = subject

        msg = MIMEText(body)
        message.attach(msg)

        content_type, encoding = mimetypes.guess_type(file_path)
        if content_type is None or encoding is not None:
            content_type = "application/octet-stream"
        main_type, sub_type = content_type.split("/", 1)
        assert main_type == "image", "type is not image"

        with open(file_path, "rb") as fp:
            msg = MIMEImage(fp.read(), _subtype=sub_type)

        msg.add_header(
            "Content-Disposition", "attachment", filename=os.path.basename(file_path)
        )
        message.attach(msg)

        byte_msg = message.as_string().encode()
        return {"raw": base64.urlsafe_b64encode(byte_msg).decode()}

    def send_message(self, body):
        service = self._get_service()

        try:
            message = service.users().messages().send(userId="me", body=body).execute()
            return message
        except Exception as e:
            print(e)
            pass
