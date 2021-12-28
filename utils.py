import random
import string
import ast
cache = {}
def search(mapspace:str, target:str):
    file = open("db.dump", "r")
    data = file.read()
    file.close()
    data = data.split("\n")
    if len(data)<3 or len(data)==3:
        return None
    del data[0]
    line = []
    for i in data:
        if i == "":
            raise Exception("Could not find the given mapspace")
        line = i.split('-')
        if line[2] == mapspace:
            break
    line[0] = int(line[0])-1
    line[1] = int(line[1])-1
    if line[0] == line[1] and data[int(line[0])-2].startswith(target):
        return int(line[0]+1)
    else:
        newdata = data
        del newdata[0]
        del newdata[0]
        i = line[0]-3
        for j in range(len(newdata)):
            if newdata[j+i].startswith(target):
                return j+i+4
def newAccountHandler(account,password):
    publish = {"account":account,"password":password, "bio":"None"}
    file = open("db.dump", "a")
    z = "\n"+str(publish)
    file.write(z)
    file.close()
    file = open("db.dump", "r")
    contents = file.read()
    newContents = contents.split("\n")
    line = (newContents[1].split('-'))
    if not(line[0] == "0" and line[1] == "0"):
        line[1] = str(int(line[1])+1)
        newContents[1] = line[0]+"-"+line[1]+"-"+line[2]
        returncontents = '\n'.join(newContents)
        file.close()
        file = open("db.dump", "w")
        file.write(returncontents)
    else:
        line[0] = str(len(newContents))
        line[1] = str(len(newContents))
        newContents[1] = line[0]+"-"+line[1]+"-"+line[2]
        returncontents = '\n'.join(newContents)
        print(returncontents)
        file.close()
        file = open("db.dump", "w")
        file.write(returncontents)
def authentication(username:string, password:string, result1:string):
    if search("USER", "{'account': '"+username+"', 'password': '"+password+"',") == None:
        return False
    else:
        cache[username] = result1
        print(cache)
        return True
def verify(user:string,token:string) -> bool:
    print(cache)
    if cache[user] == token:
        return True
    else:
        return False
def editAccount(username:string, key:string, replacement:string, mapspace:string, begining:string) -> None:
    location = search(mapspace,begining)
    file = open("db.dump", "r")
    lines = file.readlines()
    line = lines[location-1:location][0]
    file.close()
    record = ast.literal_eval(line)
    record[key] = replacement
    file = open("db.dump", "w")
    ptr = 1
    newlines = []
    for i in lines:
        if ptr != location:
            try:
                z = lines[ptr-1]
                newlines.append(i)
            except:
                raise Exception('No user: "'+username+'" found in the databace')
        else:
            try:
                z = lines[location]
                newlines.append(str(record)+"\n")
            except:
                newlines.append(str(record))
        ptr += 1
    write = "".join(newlines)
    file.write(write)
    file.close()
def grab(line):
    file = open("db.dump", "r")
    lines = file.readlines()
    out = lines[line-1]
    file.close()
    return out
def addFollower(name,user):
    user2 = ast.literal_eval(grab(search("USER","{'account': '"+user)))
    try:
        user2["followers"]
        editAccount(
            user, "followers", 
            user2["followers"].append(name),
            "USER","{'account': '"+user)
    except:
        editAccount(user, "followers", [name], "USER","{'account': '"+user)
def removeFollower(name,user):
    user2 = ast.literal_eval(grab(search("USER","{'account': '"+user)))
    y = user2["followers"].remove(name)
    if y == None:
        y = []
    editAccount(user,"followers", y, "USER","{'account': '"+user )
#tests
#editAccount("Sumaira","bio","test")
#print(grab(5))
