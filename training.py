# Import necessary libraries
from pyspark.sql.functions import col, isnan
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.ml.classification import LogisticRegression, RandomForestClassifier, DecisionTreeClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder
from pyspark.ml import Pipeline

# Create a Spark session
spark = SparkSession.builder \
    .master("local") \
    .appName("Wine_Quality_Predictions_Project") \
    .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.2.2") \
    .getOrCreate()

# Configure Spark to work with AWS S3
# (Replace access and secret keys with your actual AWS credentials)
spark.sparkContext._jsc.hadoopConfiguration().set("com.amazonaws.services.s3.enableV4", "true")
spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.aws.credentials.provider", "com.amazonaws.auth.InstanceProfileCredentialsProvider,com.amazonaws.auth.DefaultAWSCredentialsProviderChain")
spark.sparkContext._jsc.hadoopConfiguration().set("fs.AbstractFileSystem.s3a.impl", "org.apache.hadoop.fs.s3a.S3A")
spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.access.key", "YOUR_ACCESS_KEY")
spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.secret.key", "YOUR_SECRET_KEY")
spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.endpoint", "s3.us-east-1.amazonaws.com")

# Load training and validation datasets from S3
df = spark.read.format("csv") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .option("sep", ";") \
    .load("s3a://cldassign2/TrainingDataset.csv")

validation_df = spark.read.format("csv") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .option("sep", ";") \
    .load("s3a://cldassign2/ValidationDataset.csv")

# Check if data is loaded successfully
if df.count() > 0 and validation_df.count() > 0:
    print("Data loaded successfully")
else:
    print("Something unexpected happened during data load")

# Rename columns for consistency
column_name_mapping = {
    '"""""fixed acidity""""': 'fixed_acidity',
    '"""fixed acidity""""': 'fixed_acidity',
    '""""volatile acidity""""': 'volatile_acidity',
    '""""citric acid""""': 'citric_acid',
    '""""residual sugar""""': 'residual_sugar',
    '""""chlorides""""': 'chlorides',
    '""""free sulfur dioxide""""': 'free_sulfur_dioxide',
    '""""total sulfur dioxide""""': 'total_sulfur_dioxide',
    '""""density""""': 'density',
    '""""pH""""': 'pH',
    '""""sulphates""""': 'sulphates',
    '""""alcohol""""': 'alcohol',
    '""""quality"""""': 'label'
}

for old_name, new_name in column_name_mapping.items():
    df = df.withColumnRenamed(old_name, new_name)
    validation_df = validation_df.withColumnRenamed(old_name, new_name)

# Display column names
print(df.columns)
print(validation_df.columns)

# Check for null or NaN values in columns
null_counts = [(col_name, df.filter(col(col_name).isNull() | isnan(col(col_name))).count()) for col_name in df.columns]

for col_name, null_count in null_counts:
    print(f"Column '{col_name}' has {null_count} null or NaN values.")

# Split the dataset into training and testing sets
df, test_df = df.randomSplit([0.7, 0.3], seed=42)

# Define data preprocessing and modeling pipeline
feature_assembler = VectorAssembler(inputCols=['fixed_acidity', 'volatile_acidity', 'citric_acid', 'residual_sugar',
                                               'chlorides', 'free_sulfur_dioxide', 'total_sulfur_dioxide', 'density',
                                               'pH', 'sulphates', 'alcohol'], outputCol="inputFeatures")

feature_scaler = StandardScaler(inputCol="inputFeatures", outputCol="features")

# Initialize classification models
logistic_regression = LogisticRegression()
random_forest = RandomForestClassifier()
decision_tree = DecisionTreeClassifier(labelCol="label", featuresCol="features", seed=0)

# Create pipelines with different classifiers
pipeline_lr = Pipeline(stages=[feature_assembler, feature_scaler, logistic_regression])
pipeline_rf = Pipeline(stages=[feature_assembler, feature_scaler, random_forest])
pipeline_dt = Pipeline(stages=[feature_assembler, feature_scaler, decision_tree])

# Build a parameter grid for hyperparameter tuning
param_grid = ParamGridBuilder().build()

# Initialize evaluator for model performance evaluation
model_evaluator = MulticlassClassificationEvaluator(metricName="f1")

# Cross-validate each pipeline using the specified classifiers
cross_validator_lr = CrossValidator(estimator=pipeline_lr, estimatorParamMaps=param_grid, evaluator=model_evaluator, numFolds=10)
cv_model_lr = cross_validator_lr.fit(df)
print("F1 Score for LogisticRegression Model: ", model_evaluator.evaluate(cv_model_lr.transform(test_df)))

cross_validator_rf = CrossValidator(estimator=pipeline_rf, estimatorParamMaps=param_grid, evaluator=model_evaluator, numFolds=10)
cv_model_rf = cross_validator_rf.fit(df)
print("F1 Score for RandomForestClassifier Model: ", model_evaluator.evaluate(cv_model_rf.transform(test_df)))

cross_validator_dt = CrossValidator(estimator=pipeline_dt, estimatorParamMaps=param_grid, evaluator=model_evaluator, numFolds=10)
cv_model_dt = cross_validator_dt.fit(df)
print("F1 Score for DecisionTreeClassifier Model: ", model_evaluator.evaluate(cv_model_dt.transform(test_df)))

# Save models to S3
model_path_lr = "s3a://cldassign2/LogisticRegression"
cv_model_lr.save(model_path_lr)

model_path_rf = "s3a://cldassign2/RandomForestClassifier"
cv_model_rf.save(model_path_rf)

model_path_dt = "s3a://cldassign2/DecisionTreeClassifier"
cv_model_dt.save(model_path_dt)

# Stop the Spark session
spark.stop()
