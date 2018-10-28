from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = False
db = SQLAlchemy(app)
app.secret_key = 'Thisismysecret'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))


    def __init__(self, title, body):
        self.title = title
        self.body = body
        


@app.route('/', methods=['POST', 'GET'])
def index():
    
    blog_id = request.args.get('id')
    if blog_id:
    
        separate_entry = Blog.query.filter_by(id = blog_id).all()
        print(separate_entry)
        return render_template('blog.html', blogs=separate_entry)

    blogs = Blog.query.all()
    blog_entries = Blog.query.all()
    return render_template('blog.html',title="Build-a-blog", 
        blogs=blogs)
        


@app.route('/newpost', methods=['GET', 'POST'])
def addpost():

    if request.method == 'POST':
        blog_title = request.form['title']
        blog_content = request.form['entry']
                
        if blog_title == '' or blog_content == '':
            
            if blog_title == '':
                flash('Please enter a title...')
            if blog_content == '':
                flash('Please enter some content here...')
            
            return render_template('/newpost.html', title=blog_title, entry=blog_content)
        
        new_blog = Blog(blog_title, blog_content)
        db.session.add(new_blog)
        db.session.commit()    
        
        return redirect('/')

    return render_template('newpost.html')

if __name__ == '__main__':
    app.run()