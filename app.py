#pip install flask

import uuid

from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

businesses = [
    {
        "id": 1,
        "name": "Sam's",
        "town": "London",
        "rating": 4,
        "reviews": [
            {"id": 1, "username": "sonu", "comment": "Great!", "star": 5},
            {"id": 2, "username": "bikash", "comment": "All Good.", "star": 4}
        ]
    },
    {
        "id": 2,
        "name": "Nandos",
        "town": "Camden",
        "rating": 4,
        "reviews": [
            {"id": 1, "username": "nikee", "comment": "Wow!", "star": 5},
        ]
    },
    {
        "id": 3,
        "name": "Chicken Cottage",
        "town": "Farringdon",
        "rating": 5,
        "reviews": [
            {"id": 1, "username": "ulster", "comment": "Amazing, I love it!", "star": 5},
        ]
    }
]


@app.route('/', methods=['GET'])

def home():
    return jsonify({"message": "Welcome to Flask API Home Page!"})


@app.route('/businesses', methods=['GET'])
def get_businesses():
    return make_response(jsonify({"businesses": businesses}))

@app.route('/businesses', methods=['POST'])
def add_businesses():
    data = request.form
    if data and "name" in data and "town" in data and "rating" in data:
        id = str(uuid.uuid4())
        new_business = {
            "id": id,
            "name": data.get("name"),
            "town": data.get("town"),
            "rating": int(data.get("rating", 0)), 
            "reviews": []
        }
        businesses.append(new_business)
        return make_response(jsonify(new_business), 200)
    else:
        return make_response(jsonify({"error": "Invalid data"}), 400)

    
@app.route('/businesses/<int:id>', methods=['PUT'])
def update_businesses(id):
    data = request.form
    for business in businesses:
        if business["id"] == id:
            business["name"] = data.get("name")
            business["town"] = data.get("town")
            business["rating"] = data.get("rating", 0)
            break
    return make_response(jsonify(business), 200)

@app.route('/businesses/<int:id>', methods=['DELETE'])
def delete_businesses(id):
    global businesses
    for index, business in enumerate(businesses):
        if business["id"] == id:
            del businesses[index]
            return make_response(jsonify({"message": "Business deleted successfully"}), 200)
    return make_response(jsonify({"error": "Business not found"}), 404)

@app.route('/businesses/<int:id>/reviews', methods=['GET'])
def get_all_reviews(id):
    for business in businesses:
        if business["id"] == id:
            return make_response(jsonify({"reviews": business["reviews"]}), 200)
    return make_response(jsonify({"error": "Business not found"}), 404)


@app.route('/businesses/<int:id>/reviews', methods=['POST'])
def add_new_review(id):
    data = request.form
    for business in businesses:
        if business["id"] == id:
            if len(business["reviews"]) == 0:
                new_review_id = 1
            else:
                new_review_id = business["reviews"][-1]["id"] + 1
            new_review = {
                "id": new_review_id,
                "username": data.get("username"),
                "comment": data.get("comment"),
                "star": data.get("star")  # Ensure the star rating is an integer
            }      
            # Append the review to the correct business
            business["reviews"].append(new_review)
            return make_response(jsonify(new_review), 200)  # Return response inside the loop
    return make_response(jsonify({"error": "Business not found"}), 404)

@app.route('/businesses/<int:id>/reviews/<int:review_id>', methods=['GET'])
def get_review(id, review_id):
    for business in businesses:
        if business["id"] == id:
            for review in business["reviews"]:
                if review["id"] == review_id:
                    return make_response(jsonify(review), 200)
            return make_response(jsonify({"error": "Review not found"}), 404)
    return make_response(jsonify({"error": "Business not found"}), 404)

@app.route('/businesses/<int:id>/reviews/<int:review_id>', methods=['PUT'])
def update_reviews(id, review_id):
    data = request.form 
    for business in businesses:
        if business["id"] == id:
            for review in business["reviews"]:
                if review["id"] == review_id:
                    review["username"] = data.get("username", review["username"])
                    review["comment"] = data.get("comment", review["comment"])
                    review["star"] = int(data.get("star", review["star"]))
                    return make_response(jsonify(review), 200)
            return make_response(jsonify({"error": "Review not found"}), 404)
    return make_response(jsonify({"error": "Business not found"}), 404)

@app.route('/businesses/<int:id>/reviews/<int:review_id>', methods=['DELETE'])
def delete_review(id, review_id):
    for business in businesses:
        if business["id"] == id:
            for review in business["reviews"]:
                if review["id"] == review_id:
                    business["reviews"].remove(review)
                    return make_response(jsonify({"message": "Review deleted successfully"}), 200)
            return make_response(jsonify({"error": "Review not found"}), 404)
    return make_response(jsonify({"error": "Business not found"}), 404)
    
if __name__ == '__main__':
    app.run(port=5001, debug = True)