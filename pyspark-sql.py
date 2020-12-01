# cevheri
# 2020

# NYC Open Data
# Fire Incident Dispatch Data
# The Fire Incident Dispatch Data file contains data that is generated by the
# Starfire Computer Aided Dispatch System. The data spans from the time
# the incident is created in the system to the time the incident is closed in the system.
# It covers information about the incident as it relates to the assignment
# of resources and the Fire Department’s response to the emergency.
# To protect personal identifying information in accordance with the Health Insurance Portability
# and Accountability Act (HIPAA), specific locations of incidents are not included
# and have been aggregated to a higher level of detail.
from pyspark.sql import SparkSession
from pyspark.sql import Row

import sys
import os

os.environ['SPARK_HOME'] = "/home/cevher/apps/spark-3.0.1-bin-hadoop2.7"
# os.environ['HADOOP_HOME'] = "/home/cevher/app/spark-3.0.1-bin-hadoop2.7/hadoop"
sys.path.append("/home/cevher/apps/spark-3.0.1-bin-hadoop2.7/python")
sys.path.append("/home/cevher/apps/spark-3.0.1-bin-hadoop2.7/python/lib")

if __name__ == '__main__':
    spark = SparkSession.builder.appName("sql").getOrCreate()


    def parse_line(lines):
        fields = lines.split(',')
        return Row(
            indate=fields[1][:10],
            incls=fields[15]
        )


    def remove_header(lines):
        header = lines.first()  # extract header
        return lines.filter(lambda row: row != header)  # filter out header


    lines = spark.sparkContext.textFile("Fire_Incident_Dispatch_Data.csv")  # all data
    data = remove_header(lines)
    rows = data.map(parse_line)

    schema = spark.createDataFrame(rows).cache()
    schema.createOrReplaceTempView("fires")
    schema.show(2)

    rows = spark.sql("SELECT incls, indate, count(*) "
                     "FROM fires "
                     "group by incls, indate"
                     )
    # date example
    spark.sql("""
    select from_unixtime(unix_timestamp('08/26/2016', 'MM/dd/yyyy'), 'yyyy:MM:dd') as new_format
    """).show()

    for row in rows:
        print(row)

    schema.groupBy("incls", "indate").count().show()
