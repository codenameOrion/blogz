from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from validator import validator

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:password@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = False
db = SQLAlchemy(app)
app.secret_key = 'Thisismysecret'

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    password = db.Column(db.String(30))
    blogs = db.relationship('Blog', backref=db.backref('owner', lazy=True))


    def __init__(self, username, password):
        self.username = username
        self.password = password
        

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner
        


@app.route('/', methods=['GET'])
def index():
   
    users = User.query.all()
    return render_template('index.html',title="Blogz", 
        users=users)    
    


@app.route('/blog', methods=['POST', 'GET'])
def blog():

    if 'user' in request.args:

        user_id = request.args.get('user')
        owner = User.query.get(user_id)
        #filter_by(username=session['username']).first()
        blogs = Blog.query.filter_by(owner=owner).all()
        return render_template('singleUser.html', title = owner.username + "'s Posts", blogs=blogs)

    else:
        all_blogs = Blog.query.all()
        return render_template('blog.html', title = 'Blogz', blogs=all_blogs )    

@app.before_request        
def require_login():
    allowed_routes = ['','login', 'signup', 'blog', 'index']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')


@app.route('/newpost', methods=['GET', 'POST'])
def addpost():

    if request.method == 'POST':
        blog_title = request.form['title']
        blog_content = request.form['entry']
        owner = User.query.filter_by(username=session['username']).first()
                
        if blog_title == '' or blog_content == '':
            
            if blog_title == '':
                flash('Please enter a title...')
            if blog_content == '':
                flash('Please enter some content here...')
            
            return render_template('/newpost.html', title=blog_title, entry=blog_content)
        
        new_blog = Blog(blog_title, blog_content, owner)
        db.session.add(new_blog)
        db.session.commit()    
        
        return redirect('/blog?id='+str(new_blog.id))

    return render_template('newpost.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            
            session['username'] = username
            return redirect('/')
        else:
            
            return '<h1>Failed!</h1>'

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'GET':
        return render_template('signup.html')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        email = request.form['email']
        is_error, error_user, error_pass, error_pass_val, error_email = validator(username, password, email, verify)
        
        
        if not is_error:
            session['username'] = username
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            
            return redirect('/')

    return render_template('signup.html', error_user=error_user, error_pass=error_pass, error_pass_val=error_pass_val, error_email=error_email)

    
@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')

if __name__ == '__main__':
    
    db.create_all()
    app.run()