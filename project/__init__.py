from flask import Flask, jsonify
import os
import pyrebase
import json

# curl -X POST -H "Content-Type: application/json" -d '{"hell":"no"}' http://127.0.0.1:5000/test


app = Flask(__name__)

if __name__ == "__main__":
    CONF_PATH = "../../../../"
else:
    CONF_PATH = "../../../"


print(os.listdir(CONF_PATH))
print(CONF_PATH)

with open(CONF_PATH + "config.json", "r") as f:
    conf = json.load(f)

firebase = pyrebase.initialize_app(conf['firebase'])


@ app.route(os.path.join(conf["root"], 'coins'), methods=['GET'])
def get_coins():
    coins = list(firebase.database().child("coins").get().val().keys())
    return jsonify(coins)


@ app.route(os.path.join(conf["root"], 'farms'), methods=['GET'])
def get_farms():
    data = dict(firebase.database().child("coins").get().val())

    coins = list(data.keys())
    sites = []
    for coin in coins:
        els = data[coin]["info"]
        for el in els:
            sites.append({"site": el["site"], "url": el["url"]})

    return jsonify(sites)


# @ app.route(os.path.join(conf["root"], 'countries/<org>'), methods=['GET'])
# def get_orgs_countries(org):
#     client = pymongo.MongoClient(conf["mongo"])
#     db = client["masses"]
#     coll = db[org]
#     return jsonify(coll.find().distinct("country"))


# @ app.route(os.path.join(conf["root"], 'masses'), methods=['GET'])
# def get_all_masses():
#     client = pymongo.MongoClient(conf["mongo"])
#     db = client["masses"]

#     coll1 = client["masses"]["fssp"]
#     coll2 = client["masses"]["sspv"]

#     out = parse_bson(coll1.find(request.args)) + \
#         parse_bson(coll2.find(request.args))

#     return jsonify(out)


# @ app.route(os.path.join(conf["root"], 'masses/<org>'), methods=['GET'])
# def get_org_masses(org):

#     client = pymongo.MongoClient(conf["mongo"])
#     db = client["masses"]

#     coll = client["masses"][org]

#     out = parse_bson(coll.find(request.args))

#     return jsonify(out)


# @ app.route('/masses/<organization>/<id>', methods=['POST'])
# def update_masses():
#     """Return all masses usa.

#     Options: filter by state
#     """
#     # add options
#     location = request.args.get('location')

#     client = pymongo.MongoClient(conf["mongo"])
#     db = client["masses"]
#     fssp = db["fssp"].find_one()
#     sspv = db["sspv"].find_one()
#     del fssp['_id']
#     del sspv['_id']

#     return jsonify(fssp.update(sspv))


# @ app.route(os.path.join(conf["root"], 'test'), methods=['GET', 'POST'])
# def get_test():

#     # msg = request.args.get()
#     request.get_data()
#     msg = request.data

#     # get header info
#     msg = dict(request.headers)

#     # get query parameters:
#     args = request.args

#     u = request.url
#     # request.json
#     f = request.form
#     # msg = request.get_json()
#     # return jsonify(msg)
#     return jsonify({"headers": msg, "args": args, "form": f, "url": u})


if __name__ == "__main__":
    app.run(debug=True)
