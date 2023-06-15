from flask import Flask, request, jsonify
import sqlite3
import json

app=Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'


# view posts
@app.route('/api/posts', methods=["GET"])
def posts():
    con = sqlite3.connect("minecraft.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor() 


    try:
        cur.execute("SELECT post_id, post, post_date FROM posts")
    except sqlite3.Error as err:
        con.commit()
        con.close
        print('Database error detected: ', err)
        return jsonify({"error": "Database error"}), 500
    response=[]
    for row in cur:
        response.append({
            "post_id": row['post_id'],
            "post": row['post'],
            "post_date": row['post_date']
        })


    con.commit()
    con.close
    return jsonify(response), 200

# create post
@app.route('/api/post', methods=["POST"])
def create_post():
    con = sqlite3.connect("minecraft.db")
    cur = con.cursor()
    post = request.json['post']
    try:
        cur.execute("INSERT INTO posts (post) VALUES (?)", (post,))
    except sqlite3.Error as err:
        con.commit()
        con.close
        return jsonify({"error": "Database error"}), 500
    con.commit()
    con.close
    return jsonify({"status": "OK", "created_id": cur.lastrowid}), 201

#Delete post
@app.route('/api/post/<int:id>', methods=["DELETE"])
def remove_post(id):
    con = sqlite3.connect("minecraft.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    try:
        cur.execute("DELETE FROM posts WHERE post_id=?", [id])
    except sqlite3.Error as err:
        con.commit()
        con.close
        print('Database error detected: ', err)
        return jsonify({"error": "Database error"}), 500

    # Return Successful Response
    con.commit()
    con.close
    return "OK", 200

# view tips
@app.route('/api/tips', methods=["GET"])
def tips():
    con = sqlite3.connect("minecraft1.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor() 


    try:
        cur.execute("SELECT tip_id, tip, description FROM survival_tips")
    except sqlite3.Error as err:
        con.commit()
        con.close
        print('Database error detected: ', err)
        return jsonify({"error": "Database error"}), 500
    response=[]
    for row in cur:
        response.append({
            "tip_id": row['tip_id'],
            "tip": row['tip'],
            "description": row['description']
        })


    con.commit()
    con.close
    return jsonify(response), 200

#Delete tip
@app.route('/api/tips/<int:id>', methods=["DELETE"])
def remove_tip(id):
    con = sqlite3.connect("minecraft1.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    try:
        cur.execute("DELETE FROM survival_tips WHERE tip_id=?", [id])
    except sqlite3.Error as err:
        con.commit()
        con.close
        print('Database error detected: ', err)
        return jsonify({"error": "Database error"}), 500

    # Return Successful Response
    con.commit()
    con.close
    return "OK", 200

# create tip
@app.route('/api/tips', methods=["POST"])
def create_tip():
    con = sqlite3.connect("minecraft1.db")
    cur = con.cursor()
    tip = request.json['tip']
    description = request.json['description']
    try:
        cur.execute("INSERT INTO survival_tips (tip, description) VALUES (?, ?)", (tip, description))
    except sqlite3.Error as err:
        con.commit()
        con.close
        return jsonify({"error": "Database error"}), 500
    con.commit()
    con.close
    return jsonify({"status": "OK", "created_id": cur.lastrowid}), 201

# edit recpie
@app.route('/api/tips/edit/<int:id>', methods=["PUT"])
def update_tip(id):
    con = sqlite3.connect("minecraft1.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    tip_json = json.dumps(request.json['tip'])
    description_json = json.dumps(request.json['description'])

    try:
        cur.execute("UPDATE survival_tips SET tip=?, description=? WHERE id=?", [tip_json, description_json, id])
    except sqlite3.Error as err:
        con.commit()
        con.close
        print('Database error detected: ', err)
        return jsonify({"error": "Database error"}), 500

    # Return Successful Response
    con.commit()
    con.close
    return "OK", 201
