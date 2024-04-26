from app import app
from posts.blueprint import posts
import views

app.register_blueprint(posts, url_prefix = '/blog')

if __name__ == '__main__':
    app.run()