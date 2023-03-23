from aux_files import db
from sqlalchemy.orm import relationship

class FoodGroup(db.Model):
    __tablename__ = 'food_groups'
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(255), nullable=True)

    def __init__(self, group_name):
        self.group_name = group_name

    def to_json(self):
        return {
            'id': self.id,
            'group_name': self.group_name
        }

class FoodDetails(db.Model):
    __tablename__ = 'food_details'
    id = db.Column(db.Integer, primary_key=True)
    food = db.Column(db.String(255), nullable=True)
    glycemic_index = db.Column(db.Integer, nullable=True)
    group_id = db.Column(db.Integer, db.ForeignKey('food_groups.id'), nullable=True)
    group = relationship('FoodGroup', backref=db.backref('food_details', lazy=True))

    def __init__(self, food, glycemic_index, group):
        self.food = food
        self.glycemic_index = glycemic_index
        self.group = group

    def to_json(self):
        return {
            'id': self.id,
            'food': self.food,
            'glycemic_index': self.glycemic_index,
            'group': self.group.to_json() if self.group else None
        }

class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(255), nullable=True)
    mean_sugar_level = db.Column(db.Integer, nullable=True)
    recommended_glycemic_index = db.Column(db.Integer, nullable=True)

    def __init__(self, patient_name, mean_sugar_level, recommended_glycemic_index):
        self.patient_name = patient_name
        self.mean_sugar_level = mean_sugar_level
        self.recommended_glycemic_index = recommended_glycemic_index

    def to_json(self):
        return {
            'id': self.id,
            'patient_name': self.patient_name,
            'mean_sugar_level': self.mean_sugar_level,
            'recommended_glycemic_index': self.recommended_glycemic_index
        }

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    is_admin = db.Column(db.Boolean, default= False)

    def __init__(self, username, password, is_admin):
        self.username = username
        self.password = password
        self.is_admin = is_admin

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'is_admin': self.is_admin
        }
