from argparse import ArgumentParser
import mlflow
import mlflow.spark
from pyspark.sql import SparkSession
from common import *

print("MLflow Version:", mlflow.version.VERSION)
print("Tracking URI:", mlflow.tracking.get_tracking_uri())

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--run_id", dest="run_id", help="run_id", required=True)
    parser.add_argument("--data_path", dest="data_path", help="data_path", required=False)
    args = parser.parse_args()
    print("Arguments:")
    for arg in vars(args):
        print("  {}: {}".format(arg,getattr(args, arg)))

    spark = SparkSession.builder.appName("Predict").getOrCreate()
    data_path = args.data_path or default_data_path
    data = read_data(spark, data_path)

    # Predict with Spark ML
    model_uri = f"runs:/{args.run_id}/spark-model"
    print("model_uri:",model_uri)
    model = mlflow.spark.load_model(model_uri)
    predictions = model.transform(data)
    df = predictions.select(colPrediction, colLabel, colFeatures)
    print("Spark ML predictions")
    df.show(5,False)
