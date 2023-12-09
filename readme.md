Docker Link : https://hub.docker.com/r/rb715715/cs643_prog_2


Apache Spark and Hadoop Installation on Windows

Step 1: Installing Apache Spark
Download Apache Spark: Obtain Apache Spark from Apache Spark Downloads.

Extract the Downloaded Files: Extract the contents to a chosen directory.

Set SPARK_HOME Environment Variable:

Open command prompt.
Execute the following command, replacing <SparkInstallationPath> with the Spark extraction path.
setx SPARK_HOME "<SparkInstallationPath>"

Close and reopen the command prompt.
Add Spark Bin Directory to PATH:

Append %SPARK_HOME%\bin to the PATH environment variable.
setx PATH "%PATH%;%SPARK_HOME%\bin"
Close and reopen the command prompt.


Step 2: Installing Hadoop
Download Hadoop for Windows: Get Hadoop from Apache Hadoop Releases.

Extract the Downloaded Files:

Extract the contents to a directory of your preference.
Set HADOOP_HOME Environment Variable:

Open a command prompt.
Execute the following command, replacing <HadoopInstallationPath> with the Hadoop extraction path.
setx HADOOP_HOME "<HadoopInstallationPath>"
Close and reopen the command prompt.


Step 3: AWS CLI Installation on Windows
Download AWS CLI Installer for Windows: Obtain the AWS CLI installer from AWS CLI Installer for Windows.

Run the Installer: Execute the installer and follow the provided instructions.

Verify Installation:

Open a new command prompt.
Run the following command:
aws --version
This should display the installed AWS CLI version.


Step 4: Configuring Prediction on EC2 Instance
Configuring EC2 Instance on AWS
Launch an EC2 Instance:

Navigate to the AWS Management Console.
Go to the EC2 service.
Click "Launch Instance."
Connect with SSH Command:

After creating the instance, use an SSH client like PuTTY for Windows to connect.
Install Java:

Install OpenJDK using the command prompt on Windows.
Add the Java installation path to the environment variables.
Install AWS CLI:

Install AWS CLI using a package manager like chocolatey on Windows.
Configure AWS CLI using the aws configure command.
Install Hadoop:

Download and Extract Hadoop.
Configure Hadoop and add the installation path to the environment variables.
Test Hadoop Installation.
Install Spark:

Download and Extract Spark.
Configure Spark and add the installation path to the environment variables.
Test Spark Installation.
Setup Python in AWS EC2 (Windows):

Download and install the latest version of Python from python.org.
Install virtualenv.
Create a virtual environment and activate it.
Install project dependencies from requirements.txt.
Execute the command using spark-submit.


Step 5: Configuring an AWS Cluster
Configuring EMR on AWS
Access EMR in AWS Console:

Navigate to the AWS Management Console.
Go to the Amazon EMR service.
Create a Cluster:

Click on "Create Cluster."
Provide a name for the cluster.
Select EMR Release:

Choose the appropriate Amazon EMR release (e.g., emr-6.15.0).
Configure Instances:

Click on "Cluster Configuration."
Add an instance group for cluster scaling.
Configure instance types and the number of instances.
Click "Add Instance Group" and then "Add."
Security Configuration:

Configure security settings and EC2 key pair.
Add an Amazon EC2 key pair for SSH access.
Select Roles:

Configure roles:
Amazon EMR service role: EMR_DefaultRole.
EC2 instance profile for Amazon EMR: EMR_DefaultRole.
Create Cluster:

Click on "Create Cluster."
After cluster creation, open port 22 for SSH in EC2 instance security settings.
Connect to EMR Instance (Windows):

Connect to the SSH Server using an SSH client like PuTTY.
Copy files to EMR Instance using scp.
Reconnect to the server using the SSH command.
Execute Commands in a Virtual Environment.






