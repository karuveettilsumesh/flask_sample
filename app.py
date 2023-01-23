from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Dream for $ure@127.0.0.1:5432/samp_db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    def __init__(self, name, email):
        self.name = name
        self.email = email
        
    def __repr__(self):
        return '<User %r>' % self.name
        
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }

# Create new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data['name']
    email = data['email']
    new_user = User(name, email)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({
        'message': 'New user created'
    }), 201

# Get all users
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users])

# Get user by id
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if user:
        return jsonify(user.serialize())
    else:
        return jsonify({
            'message': 'User not found'
        }), 404

# Update user by id
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
  user = User.query.get(id)
  if user:
    data = request.get_json()
    user.name = data['name']
    user.email = data['email']
    db.session.commit()
    return jsonify({
    'message': 'User updated'
    }), 200
  else:
    return jsonify({
    'message': 'User not found'
    }), 404
    
#Delete user by id
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
  user = User.query.get(id)
  if user:
    db.session.delete(user)
    db.session.commit()
    return jsonify({
    'message': 'User deleted'
    }), 200
  else:
    return jsonify({
    'message': 'User not found'
    }), 404

  if name == 'main':
 	 app.run(debug=True)

