# Databricks notebook source
# MAGIC %md
# MAGIC # Lab Exercise:
# MAGIC ## Washingtons and Marthas

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ##![Spark Logo Tiny](https://files.training.databricks.com/images/wiki-book/general/logo_spark_tiny.png) Instructions
# MAGIC
# MAGIC This data was captured in the August before the 2016 US presidential election.
# MAGIC
# MAGIC As a result, articles about the candidates were very popular.
# MAGIC
# MAGIC For this exercise, you will...
# MAGIC 0. Filter the result to the **en** Wikipedia project.
# MAGIC 0. Find all the articles where the name of the article **ends** with **_Washington** (presumably "George Washington", "Martha Washington", etc)
# MAGIC 0. Return all records as an array to the Driver.
# MAGIC 0. Assign your array of Washingtons (the return value of your action) to the variable `washingtons`.
# MAGIC 0. Calculate the sum of requests for the Washingtons and assign it to the variable `totalWashingtons`. <br/>
# MAGIC <img alt="Hint" title="Hint" style="vertical-align: text-bottom; position: relative; height:1.75em; top:0.3em" src="https://files.training.databricks.com/static/images/icon-light-bulb.svg"/>&nbsp;**Hint:** We've not yet covered `DataFrame` aggregation techniques, so for this exercise use the array of records you have just obtained.
# MAGIC
# MAGIC ** Bonus **
# MAGIC
# MAGIC Repeat the exercise for the Marthas
# MAGIC 0. Filter the result to the **en** Wikipedia project.
# MAGIC 0. Find all the articles where the name of the article **starts** with **Martha_** (presumably "Martha Washington", "Martha Graham", etc)
# MAGIC 0. Return all records as an array to the Driver.
# MAGIC 0. Assign your array of Marthas (the return value of your action) to the variable `marthas`.
# MAGIC 0. Calculate the sum of requests for the Marthas and assign it to the variable `totalMarthas`.<br/>
# MAGIC <img alt="Hint" title="Hint" style="vertical-align: text-bottom; position: relative; height:1.75em; top:0.3em" src="https://files.training.databricks.com/static/images/icon-light-bulb.svg"/>&nbsp;**Hint:** We've not yet covered `DataFrame` aggregation techniques, so for this exercise use the array of records you have just obtained.
# MAGIC 0. But you cannot do it the same way twice:
# MAGIC    * In the filter, don't use the same conditional method as the one used for the Washingtons.
# MAGIC    * Don't use the same action as used for the Washingtons.
# MAGIC
# MAGIC **Testing**
# MAGIC
# MAGIC Run the last cell to verify that your results are correct.
# MAGIC
# MAGIC **Hints**
# MAGIC * <img alt="Caution" title="Caution" style="vertical-align: text-bottom; position: relative; height:1.3em; top:0.0em" src="https://files.training.databricks.com/static/images/icon-warning.svg"/> Make sure to include the underscore in the condition.
# MAGIC * The actions we've explored for extracting data include:
# MAGIC   * `first()`
# MAGIC   * `collect()`
# MAGIC   * `head()`
# MAGIC   * `take(n)`
# MAGIC * The conditional methods used with a `filter(..)` include:
# MAGIC   * equals
# MAGIC   * not-equals
# MAGIC   * starts-with
# MAGIC   * and there are others - remember, the `DataFrames` API is built upon an SQL engine.
# MAGIC * There shouldn't be more than 1000 records for either the Washingtons or the Marthas

# COMMAND ----------

# MAGIC %md
# MAGIC ##![Spark Logo Tiny](https://files.training.databricks.com/images/105/logo_spark_tiny.png) Getting Started
# MAGIC
# MAGIC Run the following cell to configure our "classroom."

# COMMAND ----------

# MAGIC %run "./Includes/Classroom-Setup"

# COMMAND ----------

# Mount "/mnt/training" again using "%run "./Includes/Dataset-Mounts-New"" if it is failed in "./Includes/Classroom-Setup"
try:
    files = dbutils.fs.ls("/mnt/training")
except:
    dbutils.fs.unmount('/mnt/training/')


# COMMAND ----------

# MAGIC %run "./Includes/Dataset-Mounts-New"

# COMMAND ----------

# MAGIC %md
# MAGIC ##![Spark Logo Tiny](https://files.training.databricks.com/images/wiki-book/general/logo_spark_tiny.png) Show Your Work

# COMMAND ----------

(source, sasEntity, sasToken) = getAzureDataSource()
spark.conf.set(sasEntity, sasToken)

source = '/mnt/training'
parquetDir = source + "/wikipedia/pagecounts/staging_parquet_en_only_clean/"

# COMMAND ----------

# TODO

# Replace FILL_IN with your code. You will probably need multiple
# lines of code for this problem.
from pyspark.sql.functions import *

washingtonsdf = (spark.read
      .parquet(parquetDir)
      .filter(col('project') == "en")
      .filter(col('article').endswith('_Washington'))
      # .filter( col("article").like("%\\_Washington") )
     )

washingtons = washingtonsdf.collect()

totalWashingtons = 0

for washington in washingtons:
  totalWashingtons += washington["requests"]
  
print("Total Washingtons: {0:,}".format( len(washingtons) ))
print("Total Washington Requests: {0:,}".format( totalWashingtons ))

# COMMAND ----------

washingtonsdf.show(5,False)

# COMMAND ----------

# TODO

# Replace FILL_IN with your code. You will probably need multiple
# lines of code for this problem.

marthadf = (spark.read
      .parquet(parquetDir)
      .filter(col('project') == "en")
      # .filter(col('article').startswith('Martha_'))
      .filter( col("article").like("Martha\\_%") )
     )

marthas = marthadf.take(marthadf.count())

totalMarthas = 0

for martha in marthas:
  totalMarthas += martha["requests"]

print("Total Marthas: {0:,}".format( len(marthas) ))
print("Total Martha Requests: {0:,}".format( totalMarthas ))

# COMMAND ----------

marthadf.show(5,False)

# COMMAND ----------

# MAGIC %md
# MAGIC ##![Spark Logo Tiny](https://files.training.databricks.com/images/wiki-book/general/logo_spark_tiny.png) Verify Your Work
# MAGIC Run the following cell to verify that your `DataFrame` was created properly.

# COMMAND ----------

print("Total Washingtons: {0:,}".format( len(washingtons) ))
print("Total Washington Requests: {0:,}".format( totalWashingtons ))

expectedCount = 466
assert len(washingtons) == expectedCount, "Expected " + str(expectedCount) + " articles but found " + str( len(washingtons) )

expectedTotal = 3266
assert totalWashingtons == expectedTotal, "Expected " + str(expectedTotal) + " requests but found " + str(totalWashingtons)

# COMMAND ----------

print("Total Marthas: {0:,}".format( len(marthas) ))
print("Total Marthas Requests: {0:,}".format( totalMarthas ))

expectedCount = 146
assert len(marthas) == expectedCount, "Expected " + str(expectedCount) + " articles but found " + str( len(marthas) )

expectedTotal = 708
assert totalMarthas == expectedTotal, "Expected " + str(expectedTotal) + " requests but found " + str(totalMarthas)


# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC # My Bonus

# COMMAND ----------

totalWashingtons = (spark.read
      .parquet(parquetDir)
      .filter(col('project') == "en")
      .filter(col('article').endswith('_Washington'))
      .agg({'*' : 'count', 'requests' : 'sum'})
      .collect()
     )
print("Total Washingtons: {0:,}".format( totalWashingtons[0][0] ))
print("Total Washington Requests: {0:,}".format( totalWashingtons[0][1] ))


totalMarthas = (spark.read
      .parquet(parquetDir)
      .filter(col('project') == "en")
      .filter(col('article').startswith('Martha_'))
      .agg({'*' : 'count', 'requests' : 'sum'})
      .collect()
     )
print("Total Marthas: {0:,}".format( totalMarthas[0][0] ))
print("Total Martha Requests: {0:,}".format( totalMarthas[0][1] ))


# COMMAND ----------

print(totalWashingtons)
print(totalMarthas)

# COMMAND ----------

# ANSWER
# BEST ANSWER - this is how you would do it in production

from pyspark.sql.functions import *  # sum(), count()

parquetDir = "/mnt/training/wikipedia/pagecounts/staging_parquet_en_only_clean/"

stats = (spark.read
  .parquet(parquetDir)
  .filter((col("project") == "en") & col("article").endswith("_Washington"))
  .select(sum("requests"), count("*"))
  .first())

totalWashingtons = stats[0]
washingtonCount = stats[1]

print("Total Washingtons: {}".format(washingtonCount) )
print("Total Washingtons Requests: {}".format(totalWashingtons))
