import os
import mlflow
import numpy as np

from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile, HTTPException

# Load the enviroment variables from the .ev file into the application
load_dotenv()

# Initialize the FastAPI application
app = FastAPI()

os.environ["MLFLOW_S3_ENDPOINT_URL"] = os.getenv("MLFLOW_S3_ENDPOINT_URL")


# Create a class to store the developed model & use it for prediction
class Model:
    def __init__(self, model_name, model_stage):
        """
        To initialize the model
        :param model_name: None of the model in registry
        :param model_stage: Stage of the model
        """
        # Load the model from Registry
        self.model = mlflow.pyfunc.load_model(f"models:/{model_name}/{model_stage}")

    def predict(self, data):
        """
        To use the loaded model to make predictions on the data
        :param data:
        :return:
        """
        predictions = self.model.predict(data)
        return predictions


# Create model
model = Model("real_estate_lgbm", "Staging")


@app.post("/invocations")
async def create_upload_file(file: UploadFile = File(...)):
    if file.filename.endswith(".npy"):
        # Create a temporary file with the same name as the uploaded
        # CSV File to load the data into a pandas Dataframe
        with open(file.filename, "wb") as f:
            f.write(file.file.read())
        data = np.load(file.filename)
        # print(data)
        os.remove(file.filename)
        return list(model.predict(data))

    else:
        # Raise a HTTP 400 Exception, indicating Bad Request
        raise HTTPException(
            status_code=400, detail="Invalid file format. Only NPY Files accepted"
        )


if os.getenv("AWS_ACCESS_KEY_ID") is None or os.getenv("AWS_SECRET_ACCESS_KEY") is None:
    exit(1)

# uvicorn inference:app --reload
