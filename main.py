from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)     
    title = db.Column(db.Text)  
    post = db.Column(db.Text)   

    def __init__(self, title, post):
        self.title = title
        self.post = post 

@app.route('/')
def index():
    all_posts = Blog.query.all()
    return render_template('all_posts.html', posts=all_posts)

@app.route('/blog')
def show_blog():
    post_id = request.args.get('id')
    if (post_id):
        one_post = Blog.query.get(post_id)
        return render_template('one_post.html', one_post=one_post)
    else:
        post_id = request.args.get('id')
        all_posts = Blog.query.all()
        return render_template('all_posts.html', posts=all_posts)

@app.route('/newpost', methods=['POST', 'GET'])
def add_entry():
    if request.method == 'POST':

        blog_title_error = ""
        blog_entry_error = ""

        post_title = request.form['blog_title']
        post_entry = request.form['blog_post']
        post_new = Blog(post_title, post_entry)

        if empty_val(post_title) and empty_val(post_entry):
            db.session.add(post_new)
            db.session.commit()
            post_link = "/blog?id=" + str(post_new.id)
            return redirect(post_link)
        else:
            if not empty_val(post_title) and not empty_val(post_entry):
                blog_title_error = "Please enter blog title"
                blog_entry_error = "Please enter blog entry"
                return render_template('new_post.html', blog_entry_error=blog_entry_error, blog_title_error=blog_title_error)
            elif not empty_val(post_title):
                blog_title_error = "Please enter blog title"
                return render_template('new_post.html', blog_title_error=blog_title_error, post_entry=post_entry)
            elif not empty_val(post_entry):
                blog_entry_error = "Please enter blog entry"
                return render_template('new_post.html', blog_entry_error=blog_entry_error, post_title=post_title)
    else:
        return render_template('new_post.html')

def empty_val(x):
    if x:
        return True
    else:
        return False
        
if __name__ == '__main__':
    app.run()