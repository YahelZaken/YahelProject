from flask import jsonify, request
from aux_files import app, db
from aux_files.models import FoodDetails, FoodGroup, Patient
from sqlalchemy import func
from aux_files.models import User
from functools import wraps
from flask import url_for, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
new_user = User(username='admin', password='password123', is_admin=True)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session or not session['user']['is_admin']:
            return jsonify({'message': 'You are not authorized to perform this action'}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/', methods=['GET', 'POST'])
def home():
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login Form"""
    if request.method == 'GET':
        return render_template('login.html')
    else:
        name = request.form['username']
        passw = request.form['password']
        try:
            data = User.query.filter_by(username=name, password=passw).first()
            if data is not None:
                session['logged_in'] = True
                return redirect(url_for('home'))
            else:
                return 'Username/Password is wrong'
        except:
            return 'Username/Password is wrong'


@app.route('/register/', methods=['GET', 'POST'])
def register():
    """Register Form"""
    if request.method == 'POST':
        new_user = User(
            username=request.form['username'],
            password=request.form['password'],
            is_admin = False)
        db.session.add(new_user)
        db.session.commit()
        return render_template('login.html')
    return render_template('register.html')


@app.route("/logout")
def logout():
    """Logout Form"""
    session['logged_in'] = False
    return redirect(url_for('home'))


"""
@app.route('/')
def home():
    return 'Welcome to the Food GI Calculator!'
"""

@app.route('/food-group/food', methods=['GET']) 
def food_group():
    result = db.session.query(FoodGroup.group_name, FoodDetails.food).join\
    (FoodDetails,FoodDetails.group_id==FoodGroup.id).all()
    element = []
    for row in result:
        element.append({
            'group_name': row[0],
            'food': row[1]
        })
    return jsonify(element)

@app.route('/food-group/food/g_i', methods=['GET'])
def food_group_gi():
    result = db.session.query(FoodGroup.group_name, FoodDetails.food,\
     FoodDetails.glycemic_index).join(FoodDetails).all()

    food_groups = []
    for row in result:
        group_name, food, glycemic_index = row
        food_groups.append({
            'group_name': group_name,
            'food': food,
            'glycemic_index': glycemic_index
        })
    return jsonify(food_groups)

@app.route('/recommended_food_groups/under', methods=['GET']) 
def recommended_food_groups_under_num():
    num = float(request.args.get('num'))
    result = db.session.query(FoodGroup.group_name, FoodDetails.food).join\
    (FoodDetails).filter(FoodDetails.glycemic_index < num).all()
    
    element = []
    for row in result:
        element.append({
            'group_name': row[0],
            'food': row[1]
        })
    return jsonify(element)

@app.route('/recommended_food_groups/above', methods=['GET']) 
def recommended_food_groups_above_num():
    num = float(request.args.get('num'))
    result = db.session.query(FoodGroup.group_name, FoodDetails.food).join\
    (FoodDetails).filter(FoodDetails.glycemic_index > num).all()  
    element = []
    for row in result:
        element.append({
            'group_name': row[0],
            'food': row[1]
        })
    return jsonify(element)

@app.route('/food_groups/average', methods=['GET']) 
def average():
    result = db.session.query(FoodGroup.group_name, db.func.avg\
    (FoodDetails.glycemic_index).label('avg_gi')).join(FoodDetails)\
        .group_by(FoodGroup.group_name).all()
    element = []
    for row in result:
        element.append({
            'group_name': row[0],
            'avg_gi': row[1]
        })    
    return jsonify(element)

@app.route('/food_groups/food_name/min', methods=['GET']) 
def min():
    result = db.session.query(FoodDetails.food).filter\
        (FoodDetails.glycemic_index == db.session.query\
         (db.func.min(FoodDetails.glycemic_index))).all()

    return jsonify(result[0]._asdict())


@app.route('/food_groups/food_name/max', methods=['GET']) 
def max():
    result = db.session.query(FoodDetails.food).filter\
        (FoodDetails.glycemic_index == db.session.query\
         (db.func.max(FoodDetails.glycemic_index))).all()

    return jsonify(result[0]._asdict())

@app.route('/foods/make_meal', methods=['GET'])
def get_foods_by_gi():
    gi = float(request.args.get('gi'))
    result = db.session.query(FoodDetails.food).filter\
        (FoodDetails.glycemic_index <= gi).order_by\
            (db.func.rand()).limit(4).all()
    
    foods = []
    for row in result:
        foods.append({'food_name': row[0]})
    
    return jsonify({'foods': foods})

#/foods?min_gi=40&max_gi=70
@app.route('/foods', methods=['GET'])
def get_foods_by_gi_range():
    min_gi = float(request.args.get('min_gi'))
    max_gi = float(request.args.get('max_gi'))

    f_d = db.session.query(FoodDetails.food, FoodDetails.glycemic_index)\
        .filter(FoodDetails.glycemic_index >= min_gi, FoodDetails.glycemic_index <= max_gi)
    
    element = []
    for row in f_d:
        element.append({
            'food': row[0],
            'glycemic_index': row[1]
        })

    return jsonify(element)


@app.route('/food_details/recommended_food_by_mean_sugar', methods=['GET'])
def mean_sugar_level_gi():
    mean_sugar_level = float(request.args.get('mean_sugar_level'))

    glycemic_index_value = mean_sugar_level / 4

    results = db.session.query(FoodDetails.food)\
            .filter(FoodDetails.glycemic_index == glycemic_index_value)\
            .all()

    response = [result[0] for result in results]
    return jsonify(response)

@app.route('/food_details', methods=['GET'])
def get_food_details():
    f_d = FoodDetails.query.all()
    
    return jsonify([row.to_json() for row in f_d])

@app.route('/patients', methods=['GET'])
def get_patients():
    f_d = Patient.query.all()
    
    return jsonify([row.to_json() for row in f_d])

@app.route('/food_groups', methods=['GET'])
def get_food_groups():
    f_d = FoodGroup.query.all()
    
    return jsonify([row.to_json() for row in f_d])

@app.route('/patients', methods=['POST'])
def add_patients():
    data = request.get_json()
    f_d = Patient(**data)
    db.session.add(f_d)
    db.session.commit()
    
    return jsonify({"message": "patient added successfully"})

@app.route('/food_groups', methods=['POST'])
@admin_required
def add_food_groups():
    data = request.get_json()
    f_d = FoodGroup(**data)
    db.session.add(f_d)
    db.session.commit()
    
    return jsonify({"message": "food_groups added successfully"})

@app.route('/food_details', methods=['POST'])
@admin_required
def add_food_details():
    data = request.get_json()
    f_d = FoodDetails(**data)
    db.session.add(f_d)
    db.session.commit()
    
    return jsonify({"message": "food_details added successfully"})

@app.route('/food_groups', methods=['PUT'])
@admin_required
def update_food_groups():
    id = float(request.args.get('id'))
    f_d = FoodGroup(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(f_d, key, value)
    db.session.commit()
    
    return jsonify({"message": "food_groups updated successfully"})

@app.route('/patients', methods=['PUT'])
def update_patients():
    id = float(request.args.get('id'))
    f_d = Patient(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(f_d, key, value)
    db.session.commit()
    
    return jsonify({"message": "patients updated successfully"})

@app.route('/food_details', methods=['PUT'])
@admin_required
def update_food_details():
    id = float(request.args.get('id'))
    f_d = FoodDetails(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(f_d, key, value)
    db.session.commit()
    
    return jsonify({"message": "food_details updated successfully"})

@app.route('/patients', methods=['DELETE'])
@admin_required
def delete_patients():
    id = float(request.args.get('id'))
    f_d = Patient.query.get(id)
    db.session.delete(f_d)
    db.session.commit()

    return jsonify({"message": "patient deleted successfully"})

@app.route('/food_groups', methods=['DELETE'])
@admin_required
def delete_food_groups():
    id = float(request.args.get('id'))
    f_d = FoodGroup.query.get(id)
    db.session.delete(f_d)
    db.session.commit()

    return jsonify({"message": "food_groups deleted successfully"})

@app.route('/food_details', methods=['DELETE'])
@admin_required
def delete_food_details():
    id = float(request.args.get('id'))
    f_d = FoodDetails.query.get(id)
    db.session.delete(f_d)
    db.session.commit()

    return jsonify({"message": "food_details deleted successfully"})