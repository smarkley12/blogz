from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz123@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y323uh231l1'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner_id = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'blog', 'index', 'signup', 'single_blog_post']
    if 'username' not in session and request.endpoint not in allowed_routes:
        return redirect('/login')

# Main page that lists all of the posts
@app.route('/', methods=['POST', 'GET'])
def index():

    users = User.query.order_by("username").all()

    return render_template('index.html', title='Blogz Home', 
    users=users)
    
# when a user wants to add an entry 
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
            owner = User.query.filter_by(username=session['username']).first()
            new_post = Blog(blog_title, blog_post, owner.id)
            db.session.add(new_post)
            db.session.commit()
            blogpost_link = "single_blog_post?id=" + str(new_post.id)
            return redirect(blogpost_link)

        return render_template('addentry.html', title='Nothing Posted', 
            title_error=title_error, blog_entry_error=blog_entry_error,
            blog_post=blog_post, blog_title=blog_title)
    
    return render_template('addentry.html',title="Add Post")

@app.route('/login', methods=['POST', 'GET'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            session['username'] = username

            return redirect('/addentry')

        if user:


            if user.password != password:
                password_not_valid_error = "Password Is Incorrect"

            if password == "":
                password_not_valid_error = "Password Cannot Be Blank"

            return render_template('login.html', 
            password_not_valid_error=password_not_valid_error, 
            username=username)

        user_name_error = "User Does Not Exist"
        return render_template('login.html', user_name_error=user_name_error, 
        username=username)

    return render_template('login.html')

@app.route('/logout')
def logout():
    if 'username' not in session:
        return redirect('/')

    del session['username']
    return redirect('/blog')

    return render_template('login.html')
    
@app.route('/single_blog_post')
def single_blog_post():
    
    blogpost_id = request.args.get('id')
    if (blogpost_id):
        single_post = Blog.query.get(blogpost_id)
        return render_template('blogpost.html', single_post=single_post)

    #route for listing all users AKA home
@app.route('/blog', methods=['POST', 'GET'])
def blog():

    if request.method == 'GET':
        blog_id = request.args.get('id')
        user_id = request.args.get('user')

        if blog_id:
            single_post = Blog.query.filter_by(id=blog_id).first()
            return render_template("blogpost.html", single_post=single_post)

        if user_id:
            blog_entries = Blog.query.filter_by(owner_id=user_id).all()
            return render_template('singleUser.html', blog_entries=blog_entries)

    all_blog_posts = Blog.query.all()

    return render_template('bloglistings.html',title="Blog Posts",
        blog_posts=all_blog_posts)

@app.route('/signup', methods=['POST', 'GET'])
def signup():

    if request.method =='GET':
        return render_template('signup.html')

    if request.method =='POST':
    
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']


        user_name_error = ''
        password_verify_error = ''
        password_not_valid_error = ''


        if len(username) > 20 or len(username) < 3:
            user_name_error = "That's not a valid username."
        
        if len(password) > 20 or len(password) < 3:
            password_not_valid_error = "That's not a valid password."
            password = ''
        
        if ' ' in password == True:
            password_not_valid_error = "That's not a valid password."
            password = ''

        if password != verify:
            password_verify_error = "Passwords don't match"
            verify = ''

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            user_name_error = "Username Already Exists."
        
        if user_name_error or password_not_valid_error or \
        password_verify_error:

            return render_template('signup.html', password_not_valid_error=password_not_valid_error, 
            password_verify_error=password_verify_error, 
            user_name_error=user_name_error, username=username)
        

        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
        
            return redirect('/addentry')

        
if __name__ == '__main__':
    app.run()