from flask import Flask
from flask import render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newflask.db'
db = SQLAlchemy(app)


# nav = [
#     {'id': 0, 'name': 'Главная', 'url': url_for('index')},
#     {'id': 1, 'name': 'О нас', 'url': url_for('about')},
#     {'id': 2, 'name': 'Создать пост', 'url': url_for('create')},
#     {'id': 3, 'name': 'Все посты', 'url': url_for('posts')}]


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    text = db.Column(db.Text, nullable=False)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']

        post = Post(title=title, text=text)

        try:
            db.session.add(post)
            db.session.commit()
            return redirect('/')
        except:
            return 'Возникла ошибка при добавлении!'
    else:
        return render_template('create.html')


@app.route('/posts')
def posts():
    posts = Post.query.all()
    return render_template("posts.html", posts=posts)


@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.filter(Post.id == post_id).first_or_404()
    return render_template("post.html", post=post)


if __name__ == "__main__":
    app.run(debug=True)
