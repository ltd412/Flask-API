from flask import Flask, request, jsonify, Response
from pymongo import MongoClient
from bson import json_util, ObjectId


app = Flask(__name__)
myclient = MongoClient("mongodb+srv://ledat:ledat@demodatabase.eujgi.mongodb.net"
                       "/myFirstDatabase?retryWrites=true&w=majority")
mydb = myclient["phonelist"]


@app.route("/phone", methods=["POST", "GET"])
def list_devices():
    if request.method == "POST":
        phonename = request.json["phonename"]
        branch = request.json["branch"]
        color = request.json["color"]
        capacity = request.json["capacity"]
        price = request.json["price"]

        if phonename and branch and color and capacity:
            mydb.list_phone.insert_one({
                "phonename": phonename,
                "branch": branch,
                "color": color,
                "capacity": capacity,
                "price": price
            })
            return "Added success"
        else:
            return "Enter full information"
    else:
        return Response(json_util.dumps(mydb.list_phone.find()), mimetype="application/json")


@app.route("/phone/<id>", methods=["GET", "PUT", "DELETE"])
def device_information(id):
    if request.method == "GET":
        device = mydb.list_phone.find_one({"_id": ObjectId(id)})
        response = json_util.dumps(device)
        return Response(response, mimetype="application/json")
    elif request.method == "PUT":
        phonename = request.json["phonename"]
        branch = request.json["branch"]
        color = request.json["color"]
        capacity = request.json["capacity"]
        price = request.json["price"]
        if phonename and branch and color and capacity:
            mydb.list_phone.update_one({
                "_id": ObjectId(id)},
                {"$set": {
                    "phonename": phonename,
                    "branch": branch,
                    "color": color,
                    "capcity": capacity,
                    "price": price
                }
                }
            )
            return "Edit succcess"
        else:
            return "Enter full information"
    else:
        mydb.list_phone.delete_one({"_id": ObjectId(id)})
        return f"Delete {id} success"


@app.errorhandler(404)
def not_found(e):
    response = jsonify({"warning": "Page not found", "status": 404})
    response.status_code = 404
    return response


if __name__ == "__main__":
    app.run()
