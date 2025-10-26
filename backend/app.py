from flask import Flask, jsonify, request, json
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["shop_database"]
collection = db["shops"]

SHOPS_FILE = "shops.json"

def sync_file_with_db():
    """Sync shops.json with MongoDB data."""
    shops = list(collection.find({}, {"_id": 0}))
    with open(SHOPS_FILE, "w") as f:
        json.dump(shops, f, indent=4)


@app.route('/api/shopdetails', methods=['GET'])
def get_shops():
    try:
        sync_file_with_db()

        with open(SHOPS_FILE, "r") as f:
            shops = json.load(f)

        return jsonify(shops), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/add_shop', methods=['POST'])
def add_shop():
    data = request.json

    if not data or not data.get("name") or not data.get("owner"):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        result = collection.insert_one(data)

        data_to_save = data.copy()
        data_to_save["_id"] = str(result.inserted_id)

        if os.path.exists(SHOPS_FILE):
            with open(SHOPS_FILE, "r") as f:
                shops = json.load(f)
        else:
            shops = []

        shops.append(data_to_save)

        with open(SHOPS_FILE, "w") as f:
            json.dump(shops, f, indent=4)

        return jsonify({"message": "Shop added successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    print("✅ Flask server running on http://127.0.0.1:5000")
    print("Use CTRL+C to stop the server.")
    app.run(debug=True)
