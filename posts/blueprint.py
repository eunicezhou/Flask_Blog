from flask import Blueprint,render_template
from flask import request, redirect, url_for
from models import Post, session, Tag
from .forms import PostForm
from app import db

posts = Blueprint('posts', __name__, 
                  template_folder= 'templates')

@posts.route('/create', methods = ['POST', 'GET'])
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
    return render_template('posts/posts.html', posts = posts)

@posts.route('/<slug>')
def post_detail(slug):
    post = session.query(Post).filter(Post.slug == slug).first()
    return render_template('posts/post_detail.html', post = post)

@posts.route('/tags/<slug>')
def tag_detail(slug):
    tag = session.query(Tag).filter(Tag.slug == slug).first()
    return render_template('posts/tag_detail.html', tag = tag)