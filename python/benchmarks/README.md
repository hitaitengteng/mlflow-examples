# MLflow Benchmarks

Benchmarks for the MLflow scoring server.

## Overview
* Launch one of the variants of the MLflow scoring server. 
  * Web server - no container. See [Deploy MLflow models](https://www.mlflow.org/docs/latest/models.html#deploy-mlflow-models).
  * SageMaker docker container. See [mlflow.sagemaker](https://mlflow.org/docs/latest/python_api/mlflow.sagemaker.html#mlflow-sagemaker).
  * Plain docker container. See [mlflow CLI - build-docker](https://mlflow.org/docs/latest/cli.html#mlflow-models-build-docker).

The container servers support the same interface (POST a JSON-serialized pandas DataFrame or CSV) as the webserver (and I assume the same implementation).

However, there are some discrepancies in loading models.
Only the SageMaker container supports both SparkML and MLeap scoring. The other two do not support MLeap scoring and will return the following error.
```
Exception: No suitable flavor backend was found for the model.
```

Here's a breakdown of flavor support for the server variants.

| Server Type  | SparkML | MLeap  |
| ------------- |:------------- | -----:|
| webserver     | OK | Error |
| docker        | OK | Error |
| SageMaker     | OK | OK |


## Launch scoring server

Launch the scoring server on port 5001.
For examples, see PySpark [Real-time Predictions](../pyspark/README.md#real-time-predictions).

## Simple benchmark
```
python -u benchmark.py --host localhost --port 5001
```
```
Calls:
  0/4898: 0.087 - [5.470]
  100/4898: 0.083 - [5.474]
  .  . .
  400/4898: 0.065 - [6.626]

Results (seconds):
  mean:    0.126
  max:     0.413
  min:     0.081
  total:   2.529
  records: 4198
```

## Multi-threaded benchmark

Launches a number of threads that concurrently call the scoring server.
```
python -u threaded_benchmark.py --host localhost --port 5001 --num_threads 10
```
```
Summary
  Mean  Max   Min
  0.269 0.339 0.062
  0.272 0.351 0.116
  . . . 
  0.278 0.338 0.230
```
