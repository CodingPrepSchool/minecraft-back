from flask import Flask, request, jsonify
import sqlite3

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
        print('Database error detected: ', err)
        return jsonify({"error": "Database error"}), 500