from flask import redirect, url_for, request
from datetime import datetime
from time import time
import re
import os

from flask_admin.contrib.sqla import ModelView
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin

from app import app, db

# 生成 slug 函數
# Slug 是一種簡化的、URL 友好的字串表示形式，通常用於將標題或名稱轉換成網址的一部分
def slugify(s):
    pattern = r'[^\w+]' # 表示匹配不是字母、數字或底線的字符
    return re.sub(pattern, '-', s) # Python 中 re 模組的 sub() 函數，用於替換符合指定模式的字串。這個函數需要提供兩個參數：要替換的模式和替換後的內容

posts_tags = db.Table('posts_tags',
                       db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key = True),
                       db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key = True))

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key = True),
                       db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key = True))
# class PostTag(db.Model):
#     __tablename__ = "posts_tags"
#     post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), primary_key = True)
#     tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"), primary_key = True)

# class RoleUser(db.Model):
#     __tablename__ = "roles_users"
#     user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key = True)
#     role_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key = True)

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(140))
    slug = db.Column(db.String(140), unique = True)
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, default = datetime.now())
    tags = db.relationship("Tag", secondary = "posts_tags", backref = db.backref("posts"), lazy = "dynamic")

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
    
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(140))
    slug = db.Column(db.String(140), unique = True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slug = self.generate_slug(self.title)

    def generate_slug(self):
        if self.title:
            self.slug = slugify(self.title)
        else:
            self.slug = str(int(time()))

    def __repr__(self):
        return f"<Tag id: {self.id}, title: {self.title}>"
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(100), unique = True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean)
    roles = db.relationship('Role', secondary = 'roles_users',
                            backref = db.backref('users'), lazy = 'select')
    fs_uniquifier = db.Column(db.String(64), unique=True) 

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), unique = True)

# with app.app_context():
#     db.create_all()

from flask_admin.contrib.sqla import ModelView
from flask_security import current_user
from flask_admin import Admin

class AdminMixin:
    def is_accessible(self):
        return current_user.has_role('admin')

# 還沒有加 class AdminMixin 的寫法
# class AdminView(ModelView):
#     def is_accessible(self):
#         return current_user.has_role('admin')
    
#     def inaccessible_callback(self, name, **kwargs):
#         return redirect(url_for('security.login', next = request.url))

class AdminView(AdminMixin, ModelView):
    pass

from flask_admin import AdminIndexView

# 還沒有加 class AdminMixin 時的寫法
# class HomeAdminView(AdminIndexView):
#     def is_accessible(self):
#         return current_user.has_role('admin')
    
#     def inaccessible_callback(self, name, **kwargs):
#         return redirect(url_for('security.login', next = request.url))

class HomeAdminView(AdminMixin, AdminIndexView):
    pass

class BaseModelView(ModelView):
    def on_model_change(self, form, model, is_created):
        if is_created:
            model.generate_slug()
        return super().on_model_change(form, model, is_created)
    
class PostAdminView(AdminMixin, BaseModelView):
    form_columns = ['title', 'body', 'tags']

class TagAdminView(AdminMixin, BaseModelView):
    pass

admin = Admin(app, 'FlaskApp', url = '/',
              index_view = HomeAdminView(name = 'Home'))

admin.add_view(PostAdminView(Post, db.session))
admin.add_view(TagAdminView(Tag, db.session))

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

with app.app_context():
    session = db.session()

    # 測試輸入資料到資料庫
    # test_p1 = Post(title = "First post", body = "First post body")
    # test_p2 = Post(title = "Second post", body = "Sencond post body")
    # test_p3 = Post(title = "Third post", body = "Third post body")
    # flask = Tag(title = "flask", slug = "flask")
    # db.session.add(flask)
    # db.session.commit()
    # db.session.add(test_p1)
    # db.session.add(test_p2)
    # db.session.add(test_p3)
    # db.session.commit()

    # posts = session.query(Post).all()
    # p1 = session.query(Post).filter(Post.title.contains('First')).all()
    # p2 = session.query(Post).filter_by(body = "First post body").all()
    # print(posts, p1, p2)

    # 在 post 訊息中加入一個 tag
    # tags = session.query(Tag).all()
    # post = session.query(Post).first()

    # for tag in tags:
    #     post.tags.append(tag)

    # print(post.tags.all())
    # db.session.add(post)
    # db.session.commit()

    # 創建 user
    # user = user_datastore.create_user(email = 'admin@test.com', password = 'admin')
    # db.session.add(user)
    # db.session.commit()
    user = session.query(User).first()
    # print(user.id)
    # print(user.email)

    # 創建 role
    # role = user_datastore.create_role(name = 'admin')
    # db.session.add(role)
    # db.session.commit()
    # user_datastore.add_role_to_user(user, role)
    # db.session.commit()