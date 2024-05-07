from flask import Blueprint,render_template
from flask import request, redirect, url_for
from flask_security import login_required
from models import Post, session, Tag
from .forms import PostForm
from app import db

posts = Blueprint('posts', __name__, 
                  template_folder= 'templates')

@posts.route('/create', methods = ['POST', 'GET'])
@login_required
def post_create():
    form = PostForm()

    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')
        try:
            post = Post(title = title, body = body)
            db.session.add(post)
            db.session.commit()
        except:
            print('traceback')
        return redirect(url_for('posts.post_detail', slug = post.slug))
    
    return render_template('posts/post_create.html', form = form)

@posts.route('/')
def posts_list():
    q = request.args.get("q") # 獲取 form 中 name 為 q 的欄位的值

    if q:
        posts = session.query(Post).filter(Post.title.contains(q) | Post.body.contains(q)).all()
    else:
        posts = session.query(Post).order_by(Post.created.desc())

    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    pages = posts.paginate(page = page, per_page = 1)

    return render_template('posts/posts.html', posts = posts, pages = pages)

@posts.route('/<slug>')
def post_detail(slug):
    post = session.query(Post).filter(Post.slug == slug).first_or_404()
    return render_template('posts/post_detail.html', post = post)

@posts.route('/tags/<slug>')
def tag_detail(slug):
    tag = session.query(Tag).filter(Tag.slug == slug).first_or_404()
    return render_template('posts/tag_detail.html', tag = tag)

@posts.route('/<slug>/edit', methods = ['POST', 'GET'])
@login_required
def post_update(slug):
    post = session.query(Post).filter(Post.slug == slug).first_or_404()

    if request.method == 'POST':
        # 使用了 Flask-WTF 提供的表單類 PostForm，將現有的 POST 請求中的表單資料 (request.form) 傳遞給表單
        # 同時將 post 物件作為 obj 參數傳遞給表單
        # 目的是將現有的 post 物件的資料填充到表單中，以便在表單中顯示出 post 物件的內容供使用者進行編輯
        form = PostForm(formdata = request.form, obj = post)
        # 將表單中的資料填充到指定的目標物件中
        # 在 Flask-WTF 中，`populate_obj()`這個方法常用於將表單中的資料填充到資料庫模型物件中，從而更新資料庫中的記錄
        form.populate_obj(post)
        db.session.commit()
        return redirect(url_for('posts.post_detail', slug = post.slug))
    
    form = PostForm(obj = post)
    return render_template('posts/edit.html', post = post, form = form)
    