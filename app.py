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
cors = CORS(app, resources={r'/*': {'origins': '*'}})


def serializer(object):
    ser = []
    for item in object:
        ser.append(item.serialize)
    return ser


def VerifyUser(token):
    if token != 'undefined':
        token = json.loads(token)
        user = db.session.query(User).filter_by(id=token['id']).first()
        if user.auth_token == token['auth_token']:
            return user
        else:
            return False
    else:
        return False


@app.route('/api/categories', methods=['GET'])
def getCategories():
    categories = db.session.query(Category).all()
    return jsonify(serializer(categories))

@app.route('/api/<category>/posts', methods=['GET'])
def getPosts(category):
    category = db.session.query(Category).filter_by(title=category).first()
    posts = db.session.query(Post).filter_by(category_id=category.id).all()
    obj = {'category':category.serialize, 'posts':serializer(posts)}
    return jsonify(obj)

@app.route('/api/posts/<post_id>', methods=['GET'])
def getPost(post_id):
    post = db.session.query(Post).filter_by(id=post_id).first()
    return jsonify(post.serialize)

@app.route('/api/posts/create', methods=['POST'])
def createPost():
    data = request.json
    user = VerifyUser(data['auth_token'])
    if user:
        post = Post(title=data['title'], body=data['body'], category_id=data['category_id'], poster_id=data['poster_id'])
        db.session.add(post)
        db.session.commit()
        return 'success'
    else:
        return 'failed'

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
                print(f'Like {category.title}')
                return user.favorites
            else:
                like = db.session.query(CategoryLike).filter_by(category_id=category.id).first()
                db.session.delete(like)
                db.session.commit()
                print(f'Unlike {category.title}')
                return user.favorites
        else:
            return 'failed'
    else:
        return 'failed'

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

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    user = db.session.query(User).filter_by(username=data['username'].lower()).first()
    if user:
        return 'failed'
    else:
        newUser = User(username=data['username'].lower(), password_hash=data['password'], ip=request.remote_addr, email=data['email'], description=data['description'], dob=datetime.strptime(data['dob'], '%Y-%m-%d'),gender=data['gender'], nickname=data['nickname'])
        db.session.add(newUser)
        db.session.commit()
        return 'success'

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user = db.session.query(User).filter_by(username=data['username'].lower()).first()
    print(f"User: {user}, Data: {data}")
    if user and user!=None:
        if user.password_hash == data['password']:
            # user.connected = True
            user.auth_token = uuid.uuid4().hex
            user.ip = request.remote_addr
            db.session.commit()
            auth_token = jsonify({'username':user.username, 'id':user.id, 'avatar':user.avatar, 'auth_token':user.auth_token})
            return auth_token
        else:
            return 'failed'
    

@app.route('/api/validate-token', methods=['POST'])
def validateToken():
    data = request.json
    user = VerifyUser(data['auth_token'])
    if user:
        return jsonify({'username':user.username, 'id':user.id, 'avatar':user.avatar, 'color':user.color, 'nickname':user.nickname, 'liked_categories':serializer(user.liked_categories)})
    else:
        return 'failed'

@app.route('/api/link-preview', methods=['POST','GET'])
def linkPreview():
    data = request.json
    try:
        prev = link_preview.generate_dict(data['url'])
        return prev
    except:
        print('Link Not Available')
        return {}

@app.route('/api/profile/', methods=['POST'])
def getUserData():
    data = request.json
    user = VerifyUser(data['auth_token'])
    if user:
        return jsonify(user.serialize)
    else:
        return 'failed'

@app.route('/storage/images/<image_name>', methods=['GET'])
def getImage(image_name):
    # open the file with the image name from images folder
    image_file = open(f'images/{image_name}', 'rb')
    return send_file(image_file, mimetype='image')


@app.route('/storage/images/<image_folder>/<image_name>', methods=['GET'])
def getImageInFolder(image_folder,image_name):
    # open the file with the image name from images folder
    image_file = open(f'images/{image_folder}/{image_name}', 'rb')
    return send_file(image_file, mimetype='image')

@app.route('/api/profile/setprofpic', methods=['POST'])
def setProfilePic():
    data = request.json
    print(f'Data: {data}')
    user = VerifyUser(data['auth_token'])
    if user:
        user.avatar = data['avatar']
        db.session.commit()
        return jsonify(user.serialize)
    else:
        return 'failed'

# upload file route
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

if __name__ == '__main__':
    app.debug = True
    # socketio.run(app, host='0.0.0.0', port=2310)
    app.run(host='0.0.0.0', port=2310)
