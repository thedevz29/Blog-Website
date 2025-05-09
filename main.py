from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/create', methods=['POST'])
def create_post():
    try:
        title = request.form.get('title')
        content = request.form.get('content')
        new_post = BlogPost(title=title, content=content)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('blogs') + '?success=true')
    except Exception as e:
        print(f"Error creating post: {e}")
        return redirect(url_for('home'))

@app.route('/blogs')
def blogs():
    try:
        posts = BlogPost.query.order_by(BlogPost.id.desc()).all()
        return render_template('blogs.html', posts=posts)
    except Exception as e:
        print(f"Error fetching posts: {e}")
        return render_template('blogs.html', posts=[])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)