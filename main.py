from flask import Flask, render_template, url_for, request, make_response
from utils import *
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.jinja')
@app.route('/api/signup/', methods=['POST'])
def signup():
    x = request.form["username"]
    y = request.form["password"]
    if search("USER","{'account': "+"'"+x+"'") == None:
        newAccountHandler(x,y)
        return "success"
    return "Name Taken"
@app.route('/api/usercheck/<name>/')
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
        res.set_cookie('auth', result1, max_age=60*60*24*30)
        return res
    return "403 Not Authorized", 403
@app.route('/api/edit/<name>/<new>/', methods=['POST'])
def bioedit(name, new):
    if verify(name,request.cookies.get('auth')):
        editAccount(name,"bio",new,"USER","{'account': '"+name)
        return "Success"
    else:
        return "403 Not Authorized", 403
@app.route('/api/follow/<name>/')
def follow(name):
    try:
        user = list(cache.keys())[list(cache.values()).index(request.cookies.get("auth"))]
        user2 = ast.literal_eval(grab(search("USER","{'account': '"+user)))
        try:
            user2["following"]
            if name in user2["following"]:
                return "Allready exists on databace"
            editAccount(user, "following", user2["followers"].append(name), "USER","{'account': '"+user)
            addFollower(user2['username'],name)
            return "Success"
        except:
            try:
                editAccount(user, "following", [name], "USER","{'account': '"+user)
                addFollower(user2['account'],name)
                return "Success"
            except:
                return "500 internal error", 500
    except ValueError:
        return "Cookie invalid, signin again", 400
@app.route('/api/unfollow/<name>/')
def unfollow(name):
    try:
        user = list(cache.keys())[list(cache.values()).index(request.cookies.get("auth"))]
        user2 = ast.literal_eval(grab(search("USER","{'account': '"+user)))
        try:
            user2["following"]
            y = user2["following"].remove(name)
            if y == None:
                y = []
            editAccount(user, "following",y, "USER","{'account': '"+user)
            removeFollower(user,name)
            return "Success"
        except:
            return "Not following: "+name
    except:
        return "Cookie invalid, signin again", 400
@app.route('/api/followermap/')
def followermap():
    try:
        try:
            x = ast.literal_eval(grab(search("USER","{'account': '"+list(cache.keys())[list(cache.values()).index(request.cookies.get("auth"))])))["followers"]
        except:
            x = ""
        return str(ast.literal_eval(grab(search("USER","{'account': '"+list(cache.keys())[list(cache.values()).index(request.cookies.get("auth"))])))["following"])+str(x)
    except:
        return "Cookie invalid, signin again", 400
@app.route('/api/block/<name>/',  methods=['POST'])
def block(name):
    try:
        user = list(cache.keys())[list(cache.values()).index(request.cookies.get("auth"))]
        user2 = ast.literal_eval(grab(search("USER","{'account': '"+user)))
        try:
            user2["blocked"]
            if name in user2["blocked"]:
                return "User is allready blocked!", 400
            editAccount(user, "blocked", user2["blocked"].append(name), "USER","{'account': '"+user)
            return "Success"
        except:
            try:
                editAccount(user, "blocked", [name], "USER","{'account': '"+user)
                return "Success"
            except:
                return "500 internal error", 500
    except ValueError:
        return "Cookie invalid, signin again", 403
@app.route('/api/blocked/')
def blockedusers():
    try:
        return str(ast.literal_eval(grab(search("USER","{'account': '"+list(cache.keys())[list(cache.values()).index(request.cookies.get("auth"))])))["blocked"])
    except:
        return "Cookie invalid, signin again", 400
if __name__ == '__main__':
    app.run(debug=True)
