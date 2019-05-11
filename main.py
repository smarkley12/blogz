from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:blogbuilder@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/', methods=['POST', 'GET'])
def index():
    blogpost_id = request.args.get('id')
    if (blogpost_id):
        single_post = Blog.query.get(blogpost_id)
        return render_template('blogpost.html', single_post=single_post)


    all_blog_posts = Blog.query.all()

    return render_template('bloglistings.html',title="Blog Posts",
        blog_posts=all_blog_posts)

@app.route('/addentry', methods=['POST', 'GET'])
def addentry():

    if request.method == 'POST':
        title_error = ""
        blog_entry_error = ""

        blog_title = request.form['blog_title']
        blog_post = request.form['blog_post']

        if not (blog_title):
            title_error = "Title is Needed!"

        if not (blog_post):
            blog_entry_error = "Need Something In Body!"

        if (blog_title) and (blog_post):
            new_post = Blog(blog_title, blog_post)
            db.session.add(new_post)
            db.session.commit()
            blogpost_link = "/?id=" + str(new_post.id)
            return redirect(blogpost_link)
          #  return render_template('blogpost.html', title="Entry Added!",
          #  blog_post=blog_post, blog_title=blog_title)

        return render_template('addentry.html', title='Nothing Posted', 
            title_error=title_error, blog_entry_error=blog_entry_error,
            blog_post=blog_post, blog_title=blog_title)
    
    return render_template('addentry.html',title="Add Post")

if __name__ == '__main__':
    app.run()