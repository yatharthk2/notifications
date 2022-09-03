from mongoengine import connect

def global_init():
    # connect('core', host='mongodb://localhost:27017/core')
    connect(db = 'OpenNotif' ,alias = "core" , host = "mongodb+srv://opennotification:9YW4qcxLgA76gv5@cluster0.xgaxv.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

