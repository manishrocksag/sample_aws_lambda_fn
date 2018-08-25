import json
import os
import logging
import uuid

import xlrd
import urllib.request, urllib.error
import boto
from boto.s3.key import Key

import settings

logger = logging.getLogger()
logger.setLevel(logging.INFO)

"""
This the main handler file which executes the lambda function in the aws. Here we have some utilities 
classes like S3 Client which helps in uploading file to s3/

"""


class S3Client(object):
    """
        Creates a s3 connection object and provides us with the interface to upload files to s3.
        Other utilities functions can be added on demand.
    """
    def __init__(self, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, bucket_name, dest_file):
        self.AWS_ACCESS_KEY_ID = AWS_ACCESS_KEY_ID
        self.AWS_SECRET_ACCESS_KEY = AWS_SECRET_ACCESS_KEY
        self.bucket_name = bucket_name
        self.conn = boto.connect_s3()
        self.dest_file = dest_file

    def upload(self):
        """
            Uploads the file to s3 and returns the url of the uploaded path which
            can be accessed later.
        """
        s3 = boto.connect_s3()
        bucket = s3.get_bucket(self.bucket_name, validate=False)
        k = Key(bucket)
        k.key = self.dest_file
        k.set_contents_from_filename(self.dest_file)
        url = k.generate_url(expires_in=0, query_auth=False)

        return url

    def download(self):
        raise NotImplemented


class PrepareJSON(object):
    """
        The main utility. It downloads the xls file from the given source url. It parses the file
        and generates the appropriate json format for it. It then writes the json to a file
        which is later uploaded to s3.

        This is the main function which executes in the aws lambda.
    """
    def __init__(self, source_file_path, source_file_url):
        self.source_file_path = source_file_path
        self.source_file_url = source_file_url
        self.dest_file_path = ''

    def download_file(self):
        try:
            urllib.request.urlretrieve(self.source_file_url, self.source_file_path)
        except urllib.error.HTTPError as e:
            # write code to notify the user in the failed execution of the lambda function.
            logger.error(e)
            return
        except urllib.error.URLError:
            # write code to notify the user in the failed execution of the lambda function.
            logger.error(e)
            return

    def prepare_dict(self, row, keys):
        """"
            Takes a row and returns a dict with the keys as the header of the row.
        """
        if len(keys) != len(row):
            return {}

        return dict(zip(keys, row))

    def clean_up(self):
        """
            UTILITY func to clean up files once they are downloaded and uploaded to s3.
        """
        try:
            os.remove(self.source_file_path)
        except OSError:
            pass

        try:
            os.remove(self.dest_file_path)
        except OSError:
            pass

    def read_xlsx_file(self, sheet_name):
        """
            The parse function which reads the xls file and prepares json from the read content.
        """
        output = []
        # load the workbook
        workbook = xlrd.open_workbook(self.source_file_path)
        sheet_names = workbook.sheet_names()
        if sheet_name in sheet_names:
            working_sheet = workbook.sheet_by_name(sheet_name)

            # Get all the keys from the file
            keys = [working_sheet.cell(0, col_index).value for col_index in range(working_sheet.ncols)]

            # Iterate over the sheet starting from the first row.
            for row_idx in range(1, working_sheet.nrows):
                output.append(self.prepare_dict(working_sheet.row_values(row_idx), keys))

        return output

    def prepare_output_file(self, filepath, content):
        """
            Takes the output content and writes it to a file.
        """
        with open(filepath, 'w') as _file:
            _file.writelines(json.dumps(content, indent=4))


def handler(event, context):
    """
        The main function which executes in aws lambda. Here the event can be defined which
        can be used to trigger the lambda function. In this case the event is null since
        we will be executing this lambda function manually.
    """

    # get the file
    prepare_json_instance = PrepareJSON("/tmp/data.xls", settings.FILE_URL)
    prepare_json_instance.download_file()

    # parse the file, extract and prepare the output.
    content = prepare_json_instance.read_xlsx_file("MICs List by CC")

    file_name = '.'.join([str(uuid.uuid4()), "json"])
    lambda_path = "/tmp/" + file_name

    # write the file
    prepare_json_instance.prepare_output_file(lambda_path, content)
    bucket_name = "steel-eye-prepare-json"

    # upload the file to s3.
    s3_connection = S3Client(settings.AWS_ACCESS_KEY_ID,  settings.AWS_SECRET_ACCESS_KEY, bucket_name, lambda_path)
    uploaded_url = s3_connection.upload()

    logger.info(s3_connection)
    return uploaded_url
