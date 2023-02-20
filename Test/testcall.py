class CLanguage:
    # 定义__call__方法
    def __call__(self,name,add):
        print("{}调用__call__()方法:{}",name,add)

clangs = CLanguage()
clangs("时光网","http://douban.com")