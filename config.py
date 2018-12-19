MONGO_URL = "localhost"
MONGO_DB = "taobao"
MONGO_TABLE = "shouji"
import pymongo
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]
def save_mongo(result):
    try:
        if db[MONGO_TABLE].insert_one(result):
            print("success",db[MONGO_TABLE].insert_one(result))
    except Exception as e:
        print ("fail")
        print(e.args)


if __name__ == "__main__":
    result = {'screen_size': '大屏5.5"', 'image': '//g-search3.alicdn.com/img/bao/uploaded/i4/TB1ZPsQcVooBKNjSZPhXXc2CXXa.jpg_220x220.jpg_.webp', 'tittle': '苹果 iPhone 8 Plus 双镜头光学变焦,原彩显示技术,全新感光元件', 'price': '\n¥5238\n', 'customer-number': '61506人付款', 'talk-number': '\n暂无点评\n'}
    save_mongo(result)
    # d = 1
    # s= db["shouji"].find()
    # for i in s:
    #     d = d+1
    #     print(i)
    #     print (d)