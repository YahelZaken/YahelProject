from aux_files import app, db

@app.route('/')
def home():
    return 'Welcome to the Food GI Calculator!'

@app.route('/food-group/food', methods=['GET']) 
def food_group():
    cursor = db.cursor()
    cursor.execute("SELECT food_groups.group_name, food_details.food FROM food_groups INNER JOIN food_details ON food_groups.id = food_details.group_id")
    result = cursor.fetchall()
    return jsonify(result)


@app.route('/food-group/food/g_i', methods=['GET'])
def food_group_gi():
    cursor = db.cursor()
    cursor.execute("SELECT food_groups.group_name, food_details.food, food_details.glycemic_index FROM food_groups INNER JOIN food_details ON food_groups.id = food_details.group_id")
    result = cursor.fetchall()

    food_groups = []
    for row in result:
        group_name, food, glycemic_index = row
        food_groups.append({
            'group_name': group_name,
            'food': food,
            'glycemic_index': glycemic_index
        })
    return jsonify(food_groups)

@app.route('/recommended_food_groups/under/<float:num>', methods=['GET']) 
def recommended_food_groups_under_num(num):
    cursor = db.cursor()
    query = "SELECT food_groups.group_name, food_details.food FROM food_groups JOIN food_details ON food_groups.id = food_details.group_id WHERE food_details.glycemic_index < %s "
    cursor.execute(query, (num, ))
    result = cursor.fetchall()
    
    return jsonify(result)

@app.route('/recommended_food_groups/above/<float:num>', methods=['GET']) 
def recommended_food_groups_above_num(num):
    cursor = db.cursor()
    query = "SELECT food_groups.group_name, food_details.food FROM food_groups JOIN food_details ON food_groups.id = food_details.group_id WHERE food_details.glycemic_index > %s "
    cursor.execute(query, (num,))
    result = cursor.fetchall()
    
    return jsonify(result)

@app.route('/average/food_groups', methods=['GET']) 
def average():
    cursor = db.cursor()
    cursor.execute("SELECT food_groups.group_name, AVG(food_details.glycemic_index) AS avg_gi FROM food_details JOIN food_groups ON food_details.group_id = food_groups.id GROUP BY food_groups.group_name")
    result = cursor.fetchall()
    
    return jsonify(result)

@app.route('/food_groups/food_name/min', methods=['GET']) 
def min():
    cursor = db.cursor()
    cursor.execute("SELECT food FROM food_details WHERE glycemic_index = (SELECT MIN(glycemic_index) FROM food_details)")
    result = cursor.fetchall()
    
    return jsonify(result)

@app.route('/foods/<int:gi>')
def get_foods_by_gi(gi):
    cursor = db.cursor()

    cursor.execute("SELECT food FROM food_details WHERE glycemic_index <= %s ORDER BY RAND() LIMIT 4", (gi,))  
    rows = cursor.fetchall()
    result = {'foods': []}
    for row in rows:
        result['foods'].append({'food_name': row[0]})
    return jsonify(result)

@app.route('/food_groups/food_name/max', methods=['GET']) 
def max():
    cursor = db.cursor()
    cursor.execute("SELECT food FROM food_details WHERE glycemic_index = (SELECT MAX(glycemic_index) FROM food_details)")
    result = cursor.fetchall()
    
    return jsonify(result)


@app.route('/foods/<float:min_gi>/<float:max_gi>', methods=['GET'])
def get_foods_by_gi_range(min_gi, max_gi):

    query = f"SELECT food FROM food_details WHERE glycemic_index >= {min_gi} AND glycemic_index <= {max_gi}"
    cursor.execute(query)

    foods = []
    for row in cursor:
        foods.append(row[0])

    foods_str = "\n".join(foods)

    return f"Foods with glycemic index between {min_gi} and {max_gi}:\n{foods_str}"

@app.route('/food_details', methods=['GET'])
def get_food_details():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM food_details")
    result = cursor.fetchall()
    
    return jsonify(result)

@app.route('/food_details/recommended_food_by_mean_sugar/<float:mean_sugar_level>', methods=['GET'])
def mean_sugar_level_gi(mean_sugar_level):
    glycemic_index_value = mean_sugar_level / 4

    query = "SELECT food FROM food_details WHERE glycemic_index = %s"
    cursor.execute(query, (glycemic_index_value,))
    results = cursor.fetchall()

    response = []
    for result in results:
        response.append(result[0])

    return jsonify(response)

@app.route('/food_details', methods=['POST'])
def add_food_details():
    cursor = db.cursor()
    food = request.json['food']
    glycemic_index = request.json['glycemic_index']
    group_id = request.json['group_id']

    values = (id, food, glycemic_index, group_id)
    sql = "INSERT INTO jobs (id, food, glycemic_index, group_id) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, values)
    db.commit()
    
    return jsonify({"message": "food_details added successfully"})

@app.route('/food_details/<int:id>', methods=['PUT'])
def update_food_details(id):
    cursor = db.cursor()
    sql = "SELECT * FROM food_details WHERE id = %s"
    food_id = (id ,)
    cursor.execute(sql, food_id)
    json = cursor.fetchone()
    food = request.json.get('food', json[1])
    glycemic_index = request.json.get('glycemic_index', json[2])
    group_id = request.json.get('group_id', json[3])
    values = (food, glycemic_index, group_id, id)
    sql = "UPDATE food_details SET food = %s, glycemic_index = %s, group_id = %s WHERE id = %s"
    cursor.execute(sql, values)
    db.commit()
    
    return jsonify({"message": "food_details updated successfully"})

@app.route('/food_details/<int:id>', methods=['DELETE'])
def delete_food_details(id):
    cursor = db.cursor()
    sql = "DELETE FROM food_details WHERE id = %s"
    cursor.execute(sql, (id,))
    db.commit()
    
    return jsonify({"message": "food_details deleted successfully"})


if __name__ == '__main__':
    app.run(debug=True)

    db.close()

