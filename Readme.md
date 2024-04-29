# 遷移腳本
## 為什麼要遷移腳本 ?
使用 ORM 時，當我們需要對資料庫進行結構性變更（如添加新表格、修改列或刪除表格）時，可以使用遷移腳本來管理這些變更

遷移腳本能夠捕獲我們對資料庫結構所做的變更，並將這些變更應用到您的開發、測試和生產環境中

遷移腳本的主要優點包括：
1. 版本控制： 遷移腳本能夠記錄您對資料庫結構所做的每一個變更，從而實現對資料庫結構的版本控制。這使得團隊成員可以追蹤資料庫結構的變化，並且能夠在需要時回退到先前的版本。
2. 可重現性： 遷移腳本能夠確保您的開發、測試和生產環境中的資料庫結構保持一致。您可以使用相同的遷移腳本在不同的環境中應用資料庫變更，從而確保環境之間的一致性。
3. 安全性： 遷移腳本通常會生成 SQL 語句，並在應用這些語句之前對其進行驗證。這可以防止意外地對資料庫進行不正確的變更，從而提高資料庫操作的安全性。

## 遷移腳本會使用到的套件
### Flask-Migrate
Flask-Migrate 使用 Alembic 來處理 Flask 應用中的 SQLAlchemy 資料庫遷移。透過 Flask 命令行界面，可以使用資料庫操作。

## 具體實行步驟
### Step 1 安裝 Flask-Migrate
使用 `pip install Flask-Migrate` 這個指令

### Step 2 初始化 db，並建立資料庫表格
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

with app.app_context():
    db.create_all()
```
### Step 3 建立資料實例
```python
with app.app_context():
    session = db.session()

    # 測試輸入資料到資料庫
    test_p1 = Post(title = "First post", body = "First post body")
    test_p2 = Post(title = "Second post", body = "Sencond post body")
    test_p3 = Post(title = "Third post", body = "Third post body")
    session.add(test_p1)
    session.add(test_p2)
    session.add(test_p3)
    session.commit()

    posts = session.query(Post).all()
    p1 = session.query(Post).filter(Post.title.contains('First')).all()
    p2 = session.query(Post).filter_by(body = "First post body").all()
    print(posts, p1, p2)
```
### Step 4 創建遷移儲存庫
使用 `flask db init` 這個指令。這個指令將會在應用程式中建立一個名為 'migration' 的資料夾

### Step 5 生成一個初始遷移腳本
使用 `$ flask db migrate -m "Initial migration."` 這個指令，使用這個指令時 Flask-Migrate 會檢查應用程式中的資料庫模型和最後一個已遷移的版本之間的差異，然後根據這些差異生成一個新的遷移腳本

### Step 6 將腳本描述的更改更新到資料庫中
使用 `$ flask db upgrade` 這個指令
