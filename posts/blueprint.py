from flask import Blueprint,render_template
from flask import request
from models import Post, session, Tag

posts = Blueprint('posts', __name__, 
                  template_folder= 'templates')

@posts.route('/')
def posts_list():
    q = request.args.get("q") # 獲取 form 中 name 為 q 的欄位的值

    if q:
        posts = session.query(Post).filter(Post.title.contains(q) | Post.body.contains(q)).all()
    else:
        posts = session.query(Post).all()
    return render_template('posts/posts.html', posts = posts)

@posts.route('/<slug>')
def post_detail(slug):
    post = session.query(Post).filter(Post.slug == slug).first()
    return render_template('posts/post_detail.html', post = post)

@posts.route('/tags/<slug>')
def tag_detail(slug):
    tag = session.query(Tag).filter(Tag.slug == slug).first()
    return render_template('posts/tag_detail.html', tag = tag)