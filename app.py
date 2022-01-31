from flask import Flask,request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from link_preview import link_preview
import uuid, json
from datetime import datetime,date
from PIL import Image

from config import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)
app.config['SECRET_KEY'] = 'TsOpAnOxWrIaThS'

from models import *
# Allow cross origin
cors = CORS(app, resources={r'/*': {'origins': '*'}})

# Use the .serialize method for all the objects in a list of objects from the DB to create a list of json objects
def serializer(object):
    ser = []
    for item in object:
        ser.append(item.serialize)
    return ser

# Use the .info method for all the user objects in a list of user objects from the DB to create a list of json user objects
def serializeUsers(object):
    ser = []
    for item in object:
        ser.append(item.info)
    return ser

# Verify user by checking the token provided in the request and comparing it to the one in the DB. 
# If the user is not authenticated or not found the function returns False
# Otherwise it returns the User object from the DB
def VerifyUser(token):
    if token != 'undefined':
        # check if token contains a ;
        if '};' in token:
            token = token.split('};')[0] + '}'
        token = json.loads(token)
        user = db.session.query(User).filter_by(id=token['id']).first()
        if user.auth_token == token['auth_token']:
            return user
        else:
            return False
    else:
        return False

# GET request that returns all categories
@app.route('/api/categories', methods=['GET'])
def getCategories():
    categories = db.session.query(Category).all()
    return jsonify(serializer(categories))

# GET request that returns all posts within a category
@app.route('/api/<category>/posts', methods=['GET'])
def getPosts(category):
    category = db.session.query(Category).filter_by(title=category).first()
    posts = db.session.query(Post).filter_by(category_id=category.id).all()
    obj = {'category':category.serialize, 'posts':serializer(posts)}
    return jsonify(obj)

# GET request that returns the post object in json form for a specific post id
@app.route('/api/posts/<post_id>', methods=['GET'])
def getPost(post_id):
    post = db.session.query(Post).filter_by(id=post_id).first()
    return jsonify(post.serialize)

# POST request that is responsible for creating a post based on the request information after verifying the user.
@app.route('/api/posts/create', methods=['POST'])
def createPost():
    data = request.json
    user = VerifyUser(data['auth_token'])
    if user:
        post = Post(title=data['title'], body=data['body'], category_id=data['category_id'], poster_id=data['poster_id'], media=data['media'])
        db.session.add(post)
        db.session.commit()
        return 'success'
    else:
        return 'failed'

# POST request that is responsible for liking a post based on the request information after verifying the user.
@app.route('/api/like/<post_id>', methods=['POST'])
def likePost(post_id):
    data = request.json
    user = VerifyUser(data['auth_token'])
    if user:
        post = db.session.query(Post).filter_by(id=post_id).first()
        if post:
            if post.dislikes.filter_by(user_id=user.id).first():
                db.session.delete(post.dislikes.filter_by(user_id=user.id).first())
                db.session.commit()
            if not post.likes.filter_by(user_id=user.id).first():
                like = Like(user_id=user.id, post_id=post.id)
                db.session.add(like)
                db.session.commit()
                return 'success'
            else:
                db.session.delete(post.likes.filter_by(user_id=user.id).first())
                db.session.commit()
                return 'success'
        else:
            return 'failed'
    else:
        return 'failed'

# POST request that is responsible for disliking a post based on the request information after verifying the user.
@app.route('/api/dislike/<post_id>', methods=['POST'])
def dislikePost(post_id):
    data = request.json
    user = VerifyUser(data['auth_token'])
    if user:
        post = db.session.query(Post).filter_by(id=post_id).first()
        if post:
            if post.likes.filter_by(user_id=user.id).first():               
                db.session.delete(post.likes.filter_by(user_id=user.id).first())
                db.session.commit()
            if not post.dislikes.filter_by(user_id=user.id).first():
                dislike = Dislike(user_id=user.id, post_id=post.id)
                db.session.add(dislike)
                db.session.commit()
                return 'success'
            else:
                db.session.delete(post.dislikes.filter_by(user_id=user.id).first())
                db.session.commit()
                return 'success'
        else:
            return 'failed'
    else:
        return 'failed'

# POST request that is responsible for liking a category based on the request information after verifying the user.
@app.route('/api/categories/like/<category_name>', methods=['POST'])
def likeCategory(category_name):
    data = request.json
    user = VerifyUser(data['auth_token'])
    if user:
        category = db.session.query(Category).filter_by(title=category_name).first()
        if category:
            if not category.likes.filter_by(user_id=user.id, category_id=category.id).first():
                like = CategoryLike(user_id=user.id, category_id=category.id)
                db.session.add(like)
                db.session.commit()
                return user.favorites
            else:
                like = db.session.query(CategoryLike).filter_by(category_id=category.id).first()
                db.session.delete(like)
                db.session.commit()
                return user.favorites
        else:
            return 'failed'
    else:
        return 'failed'

# POST request that is responsible for commenting on a post based on the request information after verifying the user.
@app.route('/api/comment/<post_id>', methods=['POST'])
def commentPost(post_id):
    data = request.json
    user = VerifyUser(data['auth_token'])
    if user:
        post = db.session.query(Post).filter_by(id=post_id).first()
        if post:
            comment = Comment(body=data['body'], user_id=user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
            return 'success'
        else:
            return 'failed'
    else:
        return 'failed'

# POST request that is responsible for registering a user based on the request information
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    user = db.session.query(User).filter_by(username=data['username'].lower()).first()
    if user:
        return 'failed'
    else:
        if not data['avatar']:
            avatar = 'avatar.png'
        else:
            avatar = data['avatar']
        newUser = User(username=data['username'].lower(), password_hash=data['password'], ip=request.remote_addr, email=data['email'], description=data['description'], dob=datetime.strptime(data['dob'], '%Y-%m-%d'),gender=data['gender'], nickname=data['nickname'],avatar=avatar, color='orange')
        db.session.add(newUser)
        db.session.commit()
        return 'success'

# POST request that is responsible for logging in a user based on the request information after verifying the user's credentials.
# After the authentication the user is provided with their new authentication token.
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user = db.session.query(User).filter_by(username=data['username'].lower()).first()
    if user and user!=None:
        if user.password_hash == data['password']:
            # user.connected = True
            user.auth_token = uuid.uuid4().hex
            user.ip = request.remote_addr
            db.session.commit()
            response = jsonify({'auth_token':{'username':user.username, 'id':user.id, 'avatar':user.avatar, 'auth_token':user.auth_token,}, 'user': user.serialize, 'success':True})
            return response
        else:
            return jsonify({'success':'false','message':'The password you entered is incorrect.'})
    else:
        return {'success':False,'message':'The username you entered is incorrect.'}
    
# POST request that is responsible for verifying a user based on the authentication token that the user provided
@app.route('/api/validate-token', methods=['POST'])
def validateToken():
    data = request.json
    user = VerifyUser(data['auth_token'])
    if user:
        return jsonify({'username':user.username, 'id':user.id, 'avatar':user.avatar, 'color':user.color, 'nickname':user.nickname, 'dark_mode':user.dark_mode, 'liked_categories':serializer(user.liked_categories)})
    else:
        return 'failed'

# Not currently implemented. Used to generate a link preview for the posts.
@app.route('/api/link-preview', methods=['POST','GET'])
def linkPreview():
    data = request.json
    try:
        prev = link_preview.generate_dict(data['url'])
        return prev
    except:
        print('Link Not Available')
        return {}

# POST request that is responsible for returning the user information
@app.route('/api/profile/', methods=['POST'])
def getUserData():
    data = request.json
    user = VerifyUser(data['auth_token'])
    if user:
        return jsonify(user.serialize)
    else:
        return 'failed'

# GET request that is responsible for returning an image from the root of the database
@app.route('/storage/images/<image_name>', methods=['GET'])
def getImage(image_name):
    # open the file with the image name from images folder
    image_file = open(f'images/{image_name}', 'rb')
    return send_file(image_file, mimetype='image')


# GET request that is responsible for returning an image from a folder inside the root of the database
@app.route('/storage/images/<image_folder>/<image_name>', methods=['GET'])
def getImageInFolder(image_folder,image_name):
    # open the file with the image name from images folder
    image_file = open(f'images/{image_folder}/{image_name}', 'rb')
    return send_file(image_file, mimetype='image')

# POST request that is responsible for changing the profile picture of a user.
@app.route('/api/profile/setprofpic', methods=['POST'])
def setProfilePic():
    data = request.json
    user = VerifyUser(data['auth_token'])
    if user:
        user.avatar = data['avatar']
        db.session.commit()
        return jsonify(user.serialize)
    else:
        return 'failed'

# POST request that is responsible for changing the favourite theme color of a user.
@app.route('/api/profile/setcolor', methods=['POST'])
def setColor():
    data = request.json
    user = VerifyUser(data['auth_token'])
    if user:
        user.color = data['color']
        db.session.commit()
        return jsonify(user.serialize)
    else:
        return 'failed'

# POST request that is responsible for turning dark mode on or off for a user.
@app.route('/api/profile/setdarkmode', methods=['POST'])
def setDarkMode():
    data = request.json
    user = VerifyUser(data['auth_token'])
    if user:
        user.dark_mode = data['darkmode']
        db.session.commit()
        return jsonify(user.serialize)
    else:
        return 'failed'

# GET request that is responsible for returning all the users information from the DB
@app.route('/api/admin/users', methods=['GET'])
def getUsers():
    users = db.session.query(User).all()
    return jsonify(serializeUsers(users))

# GET request that is responsible for returning all the posts from the DB
@app.route('/api/admin/posts', methods=['GET'])
def getAllPosts():
    posts = db.session.query(Post).all()
    obj = serializer(posts)
    return jsonify(obj)

# POST request that is responsible for creating a new category based on the request data
@app.route('/api/admin/new/category', methods=['POST'])
def newCategory():
    data = request.json
    user = VerifyUser(data['auth_token'])
    if user:
        newCategory = Category(title=data['title'], description=data['description'], image=data['image'], banner=data['banner'])
        db.session.add(newCategory)
        db.session.commit()
        return 'success'
    else:
        return 'failed'

# POST request that is responsible for removing a category based on the category id in the request data
@app.route('/api/admin/remove/category', methods=['POST'])
def removeCategory():
    data = request.json
    user = VerifyUser(data['auth_token'])
    if user:
        category = db.session.query(Category).filter_by(id=data['category_id']).first()
        if category:
            db.session.delete(category)
            # Delete all posts in category
            posts = db.session.query(Post).filter_by(category_id=data['category_id']).all()
            for post in posts:
                db.session.delete(post)
            db.session.commit()
            return 'success'
        else:
            return 'failed'
    else:
        return 'failed'

# POST request that is responsible for removing a category based on the category id in the request data
@app.route('/api/admin/remove/post', methods=['POST'])
def removePost():
    data = request.json
    user = VerifyUser(data['auth_token'])
    if user:
        post = db.session.query(Post).filter_by(id=data['post_id']).first()
        if post:
            db.session.delete(post)
            db.session.commit()
            return 'success'
        else:
            return 'failed'
    else:
        return 'failed'

# POST request that is responsible for uploading a file(for noew only images are supported) and saving it in the local storage
@app.route('/api/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return 'No file part'
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            print('No selected file')
            return 'No selected file'
        if file:
            extension = file.filename.split('.')[-1]
            filename = str(uuid.uuid4()) + '.' + extension
            # resize picture to a smaller size
            img = Image.open(file)
            img.thumbnail((500, 500))
            img.save(f'images/{filename}')
            # file.save(f'images/{filename}')
            return filename
        else:
            return 'failed'

# Run the app, with the provided parameters (such as port)
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=2310)
