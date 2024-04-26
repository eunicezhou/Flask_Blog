from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from time import time
import re
import os

base_dir = os.path.dirname(os.path.abspath(__name__))
engine = create_engine('sqlite:///' + os.path.join(base_dir, 'database.db'))
Base = declarative_base()

# 生成 slug 函數
# Slug 是一種簡化的、URL 友好的字串表示形式，通常用於將標題或名稱轉換成網址的一部分
def slugify(s):
    pattern = r'[^\w+]' # 表示匹配不是字母、數字或底線的字符
    return re.sub(pattern, '-', s) # Python 中 re 模組的 sub() 函數，用於替換符合指定模式的字串。這個函數需要提供兩個參數：要替換的模式和替換後的內容

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key = True)
    title = Column(String(140))
    slug = Column(String(140), unique = True)
    body = Column(Text)
    created = Column(DateTime, default = datetime.now())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.title:
            self.slug = slugify(self.title)
        else:
            self.slug = str(int(time()))

    def __repr__(self):
        return f"<Post id: {self.id}, title: {self.title}>"
    
Base.metadata.create_all(engine)

Session = sessionmaker(bind = engine)
session = Session()

# 測試輸入資料到資料庫
test_p1 = Post(title = "First post", body = "First post body")
test_p2 = Post(title = "Second post", body = "Sencond post body")
test_p3 = Post(title = "Third post", body = "Third post body")
# session.add(test_p1)
# session.add(test_p2)
# session.add(test_p3)
# session.commit()

posts = session.query(Post).all()
p1 = session.query(Post).filter(Post.title.contains('First')).all()
p2 = session.query(Post).filter_by(body = "First post body").all()
print(posts, p1, p2)