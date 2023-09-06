from pyspark.mllib.recommendation import ALS
from pyspark.sql import SparkSession
from pyspark.sql import Row
from pprint import pprint

if __name__ == '__main__':
    spark=SparkSession.builder.getOrCreate()
    sc=spark.sparkContext

    # 读取文件
    # rdd1=sc.textFile("hdfs://mycluster/book/hits.txt")实时文件
    rdd1=sc.textFile("hdfs://mycluster/book/hits.txt")
    ratingsRDD=rdd1.map(lambda x:x.split('\t'))
    print(ratingsRDD.take(3))
    user_row=ratingsRDD.map(lambda x:Row(userid=int(x[0]),bookid=int(x[1]),hitnum=int(x[2])))

    # jiangrdd转为spark的df
    user_df=spark.createDataFrame(user_row)
    user_df.printSchema()
    user_df.show()
    # 将df创建为临时表
    user_df.createOrReplaceTempView('test')

    dataable=spark.sql("""
    select userid,bookid,sum(hitnum) as hitnum from test group by userid, bookid
    """)
    dataable.show()

    bookrdd=dataable.rdd.map(lambda x:(x.userid,x.bookid,x.hitnum))

    #     使用ALS 训练数据，特着急数量，迭代次数，正则因子
    model=ALS.trainImplicit(bookrdd,10,10,0.01)
    #     测试
    # pprint(model.recommendProducts(169,5))

    #保存模型

    import os
    import shutil
    #用来删除存在的目录
    if os.path.exists('/root/recommendModel_1'):
        shutil.rmtree('/root/recommendModel_1')
    model.save(sc, 'file:///root/recommendModel_1')
    print("训练完成！！！")

