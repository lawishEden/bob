import redis
from pyspark import SparkContext
from pyspark.mllib.recommendation import MatrixFactorizationModel
import redis
pool = redis.ConnectionPool(host='192.168.10.10',port=6379)
redis_client=redis.Redis(connection_pool=pool)
from pprint import pprint
# def redisOp():
#     redis_client.set(1,'bob')
#     print(redis_client.get(1))
def getRecommendByUserID(userid,rec_num):
    sc=SparkContext(master='local[*]',appName="book_recommend")
    try:
        model=MatrixFactorizationModel.load(sc,'file:///root/recommendModel_1')
        result = model.recommendProducts(userid,rec_num)
        # pprint(result[0][0])
        temp=''
        for r in result:
            temp += str(r[0]) + ',' + str(r[1]) + ',' + str(r[2]) + '|'
        redis_client.set(userid,temp)
        # print(temp)
        print("load model sucess!!!!!")
    except Exception as e:
        print("load model failed" +str(e))



# if __name__ == '__main__':
#     getRecommendByUserID(189,4)