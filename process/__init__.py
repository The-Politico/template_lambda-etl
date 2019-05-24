import os
import pandas as pd
from .errors import MismatchedDataSchema

# REQUIRED!
ALLOWED_FILE_TYPES = ["XLSX", "XLS"]


class Process:
    def __init__(self, file_path):
        self.file_path = file_path

    def validateSchema(self):
        """Validate uploaded data's structure before cleaning or loading."""
        # Replace a test file
        test_file = os.path.join(os.path.dirname(__file__), "test.xlsx")
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
            # Do something in LAMBDA
            print(data)
        else:
            # Do something in test
            print(data)

    def etl(self):
        """This method is called by the server."""
        self.extract()
        self.transform()
        self.load()
