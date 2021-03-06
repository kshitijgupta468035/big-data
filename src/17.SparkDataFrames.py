# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,../src//py
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.4'
#       jupytext_version: 1.2.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # Spark DataFrames
#
# - Enable wider audiences beyond “Big Data” engineers to leverage the power of distributed processing
# - Inspired by data frames in R and Python (Pandas)
# - Designed from the ground-up to support modern big
# data and data science applications
# - Extension to the existing RDD API
#
# ## References
# - [Spark SQL, DataFrames and Datasets Guide](https://spark.apache.org/docs/latest/sql-programming-guide.html)
# - [Introduction to DataFrames - Python](https://docs.databricks.com/spark/latest/dataframes-datasets/introduction-to-dataframes-python.html)
# - [PySpark Cheat Sheet: Spark DataFrames in Python](https://www.datacamp.com/community/blog/pyspark-sql-cheat-sheet)

# ### DataFrames are :
# - The preferred abstraction in Spark
# - Strongly typed collection of distributed elements 
# - Built on Resilient Distributed Datasets (RDD)
# - Immutable once constructed

# ### With Dataframes you can :
# - Track lineage information to efficiently recompute lost data 
# - Enable operations on collection of elements in parallel

# ### You construct DataFrames
# - by parallelizing existing collections (e.g., Pandas DataFrames) 
# - by transforming an existing DataFrames
# - from files in HDFS or any other storage system (e.g., Parquet)

# ### Features
# - Ability to scale from kilobytes of data on a single laptop to petabytes on a large cluster
# - Support for a wide array of data formats and storage systems
# - Seamless integration with all big data tooling and infrastructure via Spark
# - APIs for Python, Java, Scala, and R

# ### DataFrames versus RDDs
# - Nice API for new users familiar with data frames in other programming languages.
# - For existing Spark users, the API will make Spark easier to program than using RDDs
# - For both sets of users, DataFrames will improve performance through intelligent optimizations and code-generation

# ## PySpark Shell

# **Run the Spark shell:**
#
# ~~~ bash
# pyspark
# ~~~
#
# Output similar to the following will be displayed, followed by a `>>>` REPL prompt:
#
# ~~~
# Python 3.6.5 |Anaconda, Inc.| (default, Apr 29 2018, 16:14:56)
# [GCC 7.2.0] on linux
# Type "help", "copyright", "credits" or "license" for more information.
# 2018-09-18 17:13:13 WARN  NativeCodeLoader:62 - Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
# Setting default log level to "WARN".
# To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
# Welcome to
#       ____              __
#      / __/__  ___ _____/ /__
#     _\ \/ _ \/ _ `/ __/  '_/
#    /__ / .__/\_,_/_/ /_/\_\   version 2.3.1
#       /_/
#
# Using Python version 3.6.5 (default, Apr 29 2018 16:14:56)
# SparkSession available as 'spark'.
# >>>
# ~~~
#
# Read data and convert to Dataset
#
# ~~~ py
# df = sqlContext.read.csv("/tmp/irmar.csv", sep=';', header=True)
# ~~~
#
# ~~~
# >>> df2.show()
# +---+--------------------+------------+------+------------+--------+-----+---------+--------+
# |_c0|                name|       phone|office|organization|position|  hdr|    team1|   team2|
# +---+--------------------+------------+------+------------+--------+-----+---------+--------+
# |  0|      Alphonse Paul |+33223235223|   214|          R1|     DOC|False|      EDP|      NA|
# |  1|        Ammari Zied |+33223235811|   209|          R1|      MC| True|      EDP|      NA|
# .
# .
# .
# | 18|    Bernier Joachim |+33223237558|   214|          R1|     DOC|False|   ANANUM|      NA|
# | 19|   Berthelot Pierre |+33223236043|   601|          R1|      PE| True|       GA|      NA|
# +---+--------------------+------------+------+------------+--------+-----+---------+--------+
# only showing top 20 rows
# ~~~

# ## Transformations, Actions, Laziness
#
# Like RDDs, DataFrames are lazy. Transformations contribute to the query plan, but they don't execute anything.
# Actions cause the execution of the query.
#
# ### Transformation examples
# - filter
# - select
# - drop
# - intersect 
# - join
# ### Action examples
# - count 
# - collect 
# - show 
# - head
# - take

# ## Creating a DataFrame in Python

# +
import os
import findspark

os.environ["JAVA_HOME"]="/Library/Java/JavaVirtualMachines/jdk1.8.0_202.jdk/Contents/Home"
os.environ["SPARK_HOME"]="/usr/local/opt/apache-spark/libexec"
os.environ["PYSPARK_PYTHON"]="/usr/local/bin/python3"

findspark.init()
# -

# # For macosx 
# - Install java-8 (https://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html)
# - Install spark with homebrew `brew install apache-spark`
# - Install pyspark with pip `pip3 install pyspark`
# ```py
# import os
# import findspark
# os.environ["JAVA_HOME"]="/Library/Java/JavaVirtualMachines/jdk1.8.0_152.jdk/Contents/Home"
# os.environ["SPARK_HOME"]="/usr/local/opt/apache-spark/libexec"
# os.environ["PYSPARK_PYTHON"]="/usr/local/bin/python3"
# findspark.init()
# ```

from pyspark import SparkContext, SparkConf, SQLContext
# The following three lines are not necessary
# in the pyspark shell
conf = SparkConf().setAppName("people").setMaster("local[*]") 
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)

# +
df = sqlContext.read.json("../data/people.json") # get a dataframe from json file

df.show(24)
# -

# ## Schema Inference
#
# In this exercise, let's explore schema inference. We're going to be using a file called `irmar.txt`. The data is structured, but it has no self-describing schema. And, it's not JSON, so Spark can't infer the schema automatically. Let's create an RDD and look at the first few rows of the file.

rdd = sc.textFile("../data/irmar.csv")
for line in rdd.take(10):
  print(line)

# ## Hands-on Exercises
#
# You can look at the <a href="http://spark.apache.org/docs/2.3.1/api/python/index.html" target="_blank">DataFrames API documentation</a> 
#
# Let's take a look to file "/tmp/irmar.csv". Each line consists 
# of the same information about a person:
#
# * name
# * phone
# * office
# * organization
# * position 
# * hdr
# * team1
# * team2

# +
from collections import namedtuple

rdd = sc.textFile("../data/irmar.csv")

Person = namedtuple('Person', ['name', 'phone', 'office', 'organization', 
                               'position', 'hdr', 'team1', 'team2'])
def str_to_bool(s):
    if s == 'True': return True
    return False

def map_to_person(line):
    cols = line.split(";")
    return Person(name         = cols[0],
                  phone        = cols[1],
                  office       = cols[2],
                  organization = cols[3],
                  position     = cols[4], 
                  hdr          = str_to_bool(cols[5]),
                  team1        = cols[6],
                  team2        = cols[7])
    
people_rdd = rdd.map(map_to_person)
df = people_rdd.toDF()
# -

df.show()

# ### Schema

df.printSchema()

# ### display

display(df)

# ### select

df.select(df["name"], df["position"], df["organization"])

df.select(df["name"], df["position"], df["organization"]).show()

# ### filter

df.filter(df["organization"] == "R2").show()

# ### filter + select

df2 = df.filter(df["organization"] == "R2").select(df['name'],df['team1'])

df2.show()

# ### orderBy

(df.filter(df["organization"] == "R2")
   .select(df["name"],df["position"])
   .orderBy("position")).show()

# ### groupBy

df.groupby(df["hdr"])

df.groupby(df["hdr"]).count().show()

# WARNING: Don't confuse GroupedData.count() with DataFrame.count(). GroupedData.count() is not an action. DataFrame.count() is an action.

df.filter(df["hdr"]).count()

df.filter(df['hdr']).select("name").show()

df.groupBy(df["organization"]).count().show()

# ### Exercises
#
# - How many teachers from INSA (PR+MC) ?
# - How many MC in STATS team ?
# - How many MC+CR with HDR ?
# - What is the ratio of student supervision (DOC / HDR) ?
# - List number of people for every organization ?
# - List number of HDR people for every team ?
# - Which team contains most HDR ?
# - List number of DOC students for every organization ?
# - Which team contains most DOC ?
# - List people from CNRS that are neither CR nor DR ?

df.select("organization").filter(df["organization"]=="INSA").count()

(df.select(["position", "team1", "team2"])
 .filter((df["team1"]=="STAT") | (df["team2"]=="STAT"))
 .filter(df["position"] == "MC").count())

(df.select(["position", "hdr"])
 .filter((df["position"]=="MC") | (df["position"]=="CR"))
 .filter(df["hdr"]).count())

(df.select("position").filter(df["position"]=="DOC").count() /
 df.select(df["hdr"]).filter(df["hdr"]).count())

(df.select(["hdr", "team1", "team2"])
 .filter("hdr")
 .rdd.flatMap(lambda row: (row.team1, row.team2))
 .filter(lambda v : v != 'NA')
 .map(lambda row : (row,1))
 .reduceByKey(lambda a, b:a+b)
 .sortBy(lambda v: -v[1])
 .collect()
)

(df.select(["position", "team1", "team2"])
 .filter(df.position=="DOC")
 .rdd.flatMap(lambda row: [row.team1, row.team2])
 .filter(lambda v : v != 'NA')
 .map(lambda row : (row,1))
 .reduceByKey(lambda a, b:a+b)
 .sortBy(lambda v: -v[1])
 .collect()
)

# +
import pyspark.sql.functions as f

df1 = (df.select(["position", "team1", "hdr"])
 .filter(df.hdr)
 .groupBy("team1")
 .agg(f.count("position").alias("count1"))
)
# -

df2 = (df.select(["position", "team2", "hdr"])
 .filter(df.hdr)
 .filter(df.team2 != "NA")
 .groupBy("team2")
 .agg(f.count("team2").alias("count2"))
)

df3 = (df1.join(df2, df1.team1 == df2.team2, how="left")
 .na.fill(0)
 .drop("team2"))

df3.withColumn("total", df3.count1+df3.count2).orderBy("total", ascending=False).show()

(df.filter((df.position=="DOC") & (df.team1 == "ANANUM"))
 .select("name")
 .show()
)

(df.select("organization")
 .groupby("organization").count().show())

(df.select(["name","organization","position"])
 .filter((df.position == "DR") | (df.position == "CR"))
 .show())

(df.select(["name","organization","position"])
 .filter(df.organization == "CNRS")
 .filter((df.position != "DR") & (df.position != "CR"))
 .groupBy("position").count().show())


sc.stop()


