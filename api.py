from flask import Flask, jsonify, request
import os
import pyrebase
import json

# curl -X POST -H "Content-Type: application/json" -d '{"hell":"no"}' http://127.0.0.1:5000/test


app = Flask(__name__)


CONF_PATH = ""
# print(os.listdir(CONF_PATH))
# print(CONF_PATH)

with open(CONF_PATH + "config.json", "r") as f:
    conf = json.load(f)

firebase = pyrebase.initialize_app(conf['firebase'])


@ app.route(os.path.join(conf["root"], '/'), methods=['GET'])
def message():
    return jsonify({"message": "Stake Everything API. Documentation here: https://github.com/stake-everything/se-api"})


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


@ app.route(os.path.join(conf["root"], 'farms/tags'), methods=['GET'])
def get_farm_tags():
    data = list(firebase.database().child("sites").get().val())

    rd = {}
    for site in data:
        rd[site["name"]] = site["tag"]

    return jsonify(rd)


@ app.route(os.path.join(conf["root"], 'info'), methods=['GET'])
def get_info():
    data = dict(firebase.database().child("coins").get().val())

    coins = list(data.keys())
    for coin in coins:
        del data[coin]["image_uri"]

    return jsonify(data)


@ app.route(os.path.join(conf["root"], 'images'), methods=['GET'])
def get_images():
    data = dict(firebase.database().child("coins").get().val())

    coins = list(data.keys())
    for coin in coins:
        del data[coin]["info"]

    return jsonify(data)


@ app.route(os.path.join(conf["root"], 'info/<coin>'), methods=['GET'])
def get_coin_info(coin):
    data = dict(firebase.database().child("coins").get().val())
    return jsonify(data[coin.upper()])


@ app.route(os.path.join(conf["root"], 'coins/<farm_tag>'), methods=['GET'])
def get_farm_coins(farm_tag):
    data = dict(firebase.database().child("coins").get().val())
    farms = list(firebase.database().child("sites").get().val())
    coins = list(data.keys())

    token_earned = request.args.get('token_earned')
    roi = request.args.get('roi')

    for farm in farms:
        if farm["tag"] == farm_tag:
            farm_name = farm["name"]

    farm_coins = []
    for coin in coins:
        coin_site_list = data[coin]["info"]
        for s in coin_site_list:
            if s["site"] == farm_name:

                el = []
                el.append(coin)
                if roi:
                    try:
                        el.append(s["apr"])
                    except:
                        el.append(s["apy"])

                if token_earned:
                    el.append(s["token_earned"])

                farm_coins.append(el)

    return jsonify({farm_name: farm_coins})


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
    # app.run(debug=False, host="0.0.0.0", port="5000")
