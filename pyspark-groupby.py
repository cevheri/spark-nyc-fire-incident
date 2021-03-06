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


from pyspark import SparkConf, SparkContext

import sys
import os
from operator import add

os.environ['SPARK_HOME'] = "/home/cevher/apps/spark-3.0.1-bin-hadoop2.7"
# os.environ['HADOOP_HOME'] = "/home/cevher/app/spark-3.0.1-bin-hadoop2.7/hadoop"
sys.path.append("/home/cevher/apps/spark-3.0.1-bin-hadoop2.7/python")
sys.path.append("/home/cevher/apps/spark-3.0.1-bin-hadoop2.7/python/lib")

if __name__ == '__main__':
    conf = SparkConf().setMaster("local").setAppName("groupByKey")
    sc = SparkContext(conf=conf)


    def parse_line(line):
        fields = line.split(',')
        in_class = str(fields[15])
        in_date = str(fields[1][:10])
        return in_date, in_class


    def remove_header(lines):
        header = lines.first()  # extract header
        return lines.filter(lambda row: row != header)  # filter out header


    lines = sc.textFile("Fire_Incident_Dispatch_Data.csv")  # all data
    data = remove_header(lines)
    rdd = data.map(parse_line)
    print(rdd)

    rdd1 = rdd.map(lambda x: (x, 1)).groupByKey().mapValues(len)
    result = rdd1.collect()
    for row in result:
        print(row)
