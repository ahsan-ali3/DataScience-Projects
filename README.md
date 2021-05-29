# DataScience-Projects
Code can be excuted direcly by using .ipynb file in colab with TPU configurations. 
Model File is too big to be uploaded here (475 MB)
FAST API is built on Colab because of no support of torch_xla packages on local cpu. Fast API can be run easily with just uploading model file on path colab path and loading it through this.
Tweet Data Pipeline file is used to update pipeline on AWS RDS mysql server which is live just for dspd project. It has three tables, training_data, test_Data and training full data. 
This pipeline process data using chunk of files and update the pipeline in mysql. 
Once data is processed through pipeline, code can be executed in the same file to upload training data into AWS S3 bucket. 
AWS S3 bucket is used to store files for trainng data and that file is consumed directly in .ipynb file. AWS rds mysql has some limitation for accessing it through colab.
