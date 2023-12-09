# Import necessary libraries
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.tuning import CrossValidatorModel
from pyspark.sql.session import SparkSession

# Initialize Spark session
spark = SparkSession.builder\
          .appName("Wine_Quality_Predictions_Project")\
          .getOrCreate()

# Configure Spark to work with AWS S3
spark.sparkContext._jsc.hadoopConfiguration().set("com.amazonaws.services.s3.enableV4", "true")
spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.aws.credentials.provider", "com.amazonaws.auth.InstanceProfileCredentialsProvider,com.amazonaws.auth.DefaultAWSCredentialsProviderChain")
spark.sparkContext._jsc.hadoopConfiguration().set("fs.AbstractFileSystem.s3a.impl", "org.apache.hadoop.fs.s3a.S3A")
spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.endpoint", "s3.us-east-1.amazonaws.com")

# Load validation dataset from S3
validation_df = spark.read.format("csv")\
                    .option("header", "true")\
                    .option("inferSchema", "true")\
                    .option("sep", ";")\
                    .load("s3a://cldassign2/ValidationDataset.csv")

# Check if data loaded successfully
if validation_df.count() > 0:
    print("Data loaded successfully")
else:
    print("Something unexpected happened during data load")

# Rename columns for better readability
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

# Rename columns in the DataFrame
for old_name, new_name in column_name_mapping.items():
    validation_df = validation_df.withColumnRenamed(old_name, new_name)

# Load and evaluate Logistic Regression model
model_lr = CrossValidatorModel.load('s3a://cldassign2/LogisticRegression')
evaluator_lr = MulticlassClassificationEvaluator(metricName="f1")
print("F1 Score for LogisticRegression Model: ", evaluator_lr.evaluate(model_lr.transform(validation_df)))

# Load and evaluate Random Forest Classifier model
model_rf = CrossValidatorModel.load('s3a://cldassign2/RandomForestClassifier')
evaluator_rf = MulticlassClassificationEvaluator(metricName="f1")
print("F1 Score for RandomForestClassifier Model: ", evaluator_rf.evaluate(model_rf.transform(validation_df)))

# Load and evaluate Decision Tree Classifier model
model_dt = CrossValidatorModel.load('s3a://cldassign2/DecisionTreeClassifier')
evaluator_dt = MulticlassClassificationEvaluator(metricName="f1")
print("F1 Score for DecisionTreeClassifier Model: ", evaluator_dt.evaluate(model_dt.transform(validation_df)))
