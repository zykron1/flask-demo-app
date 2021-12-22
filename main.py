from flask import Flask, render_template, url_for, request, make_response
from utils import *
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.jinja')
@app.route('/api/signup', methods=['POST'])
def signup():
    x = request.form["username"]
    y = request.form["password"]
    if search("USER","{'account': "+"'"+x+"'") == None:
        newAccountHandler(x,y)
        return "success"
    return "Name Taken"
@app.route('/api/usercheck/<name>')
def usercheck(name):
    if search("USER","{'account': "+"'"+name+"'") == None:
        return "All clear!!!"
    else:
        return "Username taken!"
@app.route('/api/signin/', methods=['POST'])
def signin():
    x = request.form["username"]
    y = request.form["password"]
    result1 =''.join((random.choice(string.ascii_uppercase+string.ascii_lowercase) for codenum in range(256))) + str(random.randint(10,100))
    if authentication(x,y,result1):
        res = make_response("Token Created")
        res.set_cookie('auth', result1, max_age=60*60*24*365*2)
        return res
    return "Access Denied"
if __name__ == '__main__':
    app.run(debug=True)