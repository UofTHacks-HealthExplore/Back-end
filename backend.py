from flask import Flask
app = Flask(__name__)

@app.route('/hello')
def hello_world():
   return "Hello Word"

@app.route('/hello/<name>')
def hello_name(name):
   return f'Hello {name}!'

@app.route('/blog/<int:postID>')
def show_blog(postID):
   return 'Blog Number %d' % postID

@app.route('/rev/<float:revNo>')
def revision(revNo):
   return 'Revision Number %f' % revNo

if __name__ == '__main__':
   app.run(debug=True)
