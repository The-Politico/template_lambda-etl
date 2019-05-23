import os
from os import path
import pandas as pd

# import requests
from .errors import MismatchedDataSchema


class Process:
    def __init__(self, file_path):
        self.file_path = file_path

    def validateSchema(self):
        """Validate uploaded data's structure before cleaning or loading."""
        # Replace a test file
        test_file = path.join(path.dirname(__file__), "test.xlsx")
        testDf = pd.read_excel(open(test_file, "rb"), sheet_name="Sheet1")
        if not testDf.dtypes.equals(self.df.dtypes):
            raise MismatchedDataSchema("Data schema does not match test")

    def extract(self):
        """Read in and validate your data."""
        self.df = pd.read_excel(
            open(self.file_path, "rb"), sheet_name="Sheet1"
        )
        self.validateSchema()

    def transform(self):
        """Transform your data."""
        # Do some data-cleaning stuff...
        pass

    def load(self):
        """Load your clean data into an API or upload a static file."""
        data = self.df.to_json(orient="records")
        if os.getenv("LAMBDA"):
            print("SUCCESSFULLY PROCESSED")
            print(data)
            # Do something here
            return
            # requests.post(
            #     "http://localhost:3000/mock-api/",
            #     headers={
            #         "Access-Control-Allow-Origin": "*",
            #         "Content-Type": "application/json",
            #         "Authorization": "Token {}".format(
            #             os.getenv("API_AUTH_TOKEN")
            #         ),
            #     },
            #     data=data,
            # )
        else:
            print(data)

    def etl(self):
        print("PROCESSING")
        self.extract()
        self.transform()
        self.load()
