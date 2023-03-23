from aux_files import db

class FoodGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(255), nullable=True)

class FoodDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food = db.Column(db.String(255), nullable=True)
    glycemic_index = db.Column(db.Integer, nullable=True)
    group_id = db.Column(db.Integer, db.ForeignKey('food_group.id'), nullable=True)
    group = db.relationship('FoodGroup', backref=db.backref('food_details', lazy=True))

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(255), nullable=True)
    mean_sugar_level = db.Column(db.Integer, nullable=True)
    recommended_glycemic_index = db.Column(db.Integer, nullable=True)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    is_admin = db.Column(db.Boolean, default= False)
    def __init__(self, username, password, is_admin):
        self.username = username
        self.password = password
        self.is_admin = is_admin

