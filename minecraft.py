from flask import Flask, request, jsonify
import json
import sqlite3


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'


@app.route('/minecraft/posts', methods=["GET"])
def show_posts():
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
        
    response = []
    for row in cur:
        response.append({
            "post_id": row['post_id'],
            "post": row['post'],
            "post_date": row['post_date'],
        })
    con.commit()
    con.close
    return jsonify(response), 200



#Create post
@app.route('/minecraft/create_post', methods=["POST"])
def create_post():
    # Try to insert to DB
    con = sqlite3.connect("minecraft.db")
    cur = con.cursor()
    post = request.json['post']
    print('Adding', post)
    try:
        cur.execute("INSERT INTO posts (post) VALUES (?)", (post,))
    except sqlite3.Error as err:
        con.commit()
        con.close
        print('Database error detected: ', err)
        return jsonify({"error": "Database error"}), 500

    # Return Successful Response
    con.commit()
    con.close
    return jsonify({"status": "OK", "created_id": cur.lastrowid}), 201