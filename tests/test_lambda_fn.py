"""
Exhaustive unit testing remains to be written for the application. As of now the lambda function
can be executed by calling the following api
 https://lexl6ptb3h.execute-api.us-west-2.amazonaws.com/default/steel_eye_data_extraction

The output file created in s3 can be accessed at:
https://s3-us-west-2.amazonaws.com/steel-eye-prepare-json/tmp/output.json
"""

import requests


def test():
    response = requests.get("https://lexl6ptb3h.execute-api.us-west-2.amazonaws.com/default/steel_eye_data_extraction")
    print(response.status_code)
    print(response.text)


def main():
    test()


if __name__ == '__main__':
    main()