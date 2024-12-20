from app import app
import pyrebase
from flask import render_template, request, jsonify  # 수정: request와 jsonify 추가

# Firebase 설정
config = {
#firebase 키값
}


firebase = pyrebase.initialize_app(config)
db = firebase.database()

@app.route("/")
def home():
    # Firebase 데이터 가져오기
    data = db.get().val() or {}  # None일 경우 빈 딕셔너리로 대체

    # 데이터를 HTML로 전달
    return render_template("index.html", data=data)

@app.route("/add-entry", methods=["POST"])
def add_entry():
    data = request.json
    category = data.get("category")
    title = data.get("title")
    author = data.get("author")
    time = data.get("time")
    content = data.get("content")

    if not all([category, title, author, time, content]):
        return jsonify({"error": "All fields are required"}), 400

    # Firebase에 데이터 추가
    try:
        new_entry = {
            "title": title,
            "author_id": author,
            "created_at": time,
            "content": content,
        }
        db.child(category).push(new_entry)  # 카테고리에 새 데이터 추가
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/update-entry", methods=["POST"])
def update_entry():
    data = request.json
    category = data.get("category")
    title = data.get("title")
    author = data.get("author")
    time = data.get("time")
    content = data.get("content")
    key = data.get("key")  # 수정할 항목의 키

    if not all([category, title, author, time, content, key]):
        return jsonify({"error": "All fields and a valid key are required"}), 400

    # Firebase 데이터 수정
    try:
        updated_entry = {
            "title": title,
            "author_id": author,
            "created_at": time,
            "content": content,
        }
        db.child(category).child(key).update(updated_entry)  # 기존 데이터 업데이트
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/delete-entry", methods=["POST"])
def delete_entry():
    data = request.json
    category = data.get("category")
    key = data.get("key")

    if not category or not key:
        return jsonify({"error": "Category and key are required"}), 400

    try:
        db.child(category).child(key).remove()  # Firebase에서 데이터 삭제
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500