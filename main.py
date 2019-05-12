from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz123@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))

    def __init__(self, title, body):
        self.title = title
        self.body = body

# Main page that lists all of the posts
@app.route('/', methods=['POST', 'GET'])
def index():
    blogpost_id = request.args.get('id')
    if (blogpost_id):
        single_post = Blog.query.get(blogpost_id)
        return render_template('blogpost.html', single_post=single_post)


    all_blog_posts = Blog.query.all()

    return render_template('bloglistings.html',title="Blog Posts",
        blog_posts=all_blog_posts)

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
            new_post = Blog(blog_title, blog_post)
            db.session.add(new_post)
            db.session.commit()
            blogpost_link = "/?id=" + str(new_post.id)
            return redirect(blogpost_link)

        return render_template('addentry.html', title='Nothing Posted', 
            title_error=title_error, blog_entry_error=blog_entry_error,
            blog_post=blog_post, blog_title=blog_title)
    
    return render_template('addentry.html',title="Add Post")

@app.route('/login', methods=['POST', 'GET'])
def login():
    return render_template('login.html')

#User signs up for the first time
@app.route('/signup', methods=['POST', 'GET'])
def signup():

    if request.method =='GET':
        return render_template('signup.html')
    
    username = request.form['username']
    password = request.form['password']
    verify = request.form['verify']
    email = request.form['email']

    user_name_error = ''
    password_verify_error = ''
    password_not_valid_error = ''
    email_error = ''
    test = ''

    if len(username) > 20 or len(username) < 3:
        user_name_error = "That's not a valid username."
    elif test in username == True:
        user_name_error = "That's not a valid username."


    if len(password) > 20 or len(password) < 3:
        password_not_valid_error = "That's not a valid password."
        password = ''
    elif ' ' in password == True:
        password_not_valid_error = "That's not a valid password."
        password = ''

    if password != verify:
        password_verify_error = "Passwords don't match"
        verify = ''
    
    if not user_name_error and not password_not_valid_error and not \
    password_verify_error and not email_error:
        return redirect('/valid?username={0}'.format(username))
    else: 
        return render_template('index.html', 
            password_not_valid_error=password_not_valid_error,
            password_verify_error=password_verify_error, 
            user_name_error=user_name_error, 
            email_error=email_error,
            username=username, email=email)

if __name__ == '__main__':
    app.run()
# where user can login 
#@app.route('/login', methods=['POST', 'GET'])
#def login():


#User clicks logout

#@app.route('/logout' methods=['POST'])
#def logout():

#route for listing all users AKA home
#@app.route('/home', methods=['POST', 'GET'])
#def users_listing():

#if __name__ == '__main__':
