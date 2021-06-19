from flask import Flask, jsonify, request
import os
import pyrebase
import json

# curl -X POST -H "Content-Type: application/json" -d '{"data":"test"}' http://127.0.0.1:5000/test


app = Flask(__name__)


CONF_PATH = ""
# print(os.listdir(CONF_PATH))
# print(CONF_PATH)

with open(CONF_PATH + "../config.json", "r") as f:
    conf = json.load(f)

# Variables
msg0 = {"status": "failed", "message": "Unkown reason."}
msg1 = {"status": "failed", "message": "Content error"}
msg2 = {"status": "success"}

firebase = pyrebase.initialize_app(conf['firebase'])
fdb = firebase.database()


@ app.route(os.path.join(conf["root"], '/'), methods=['GET'])
def message():
    return jsonify({"message": "Stake Everything API. Documentation here: https://github.com/stake-everything/se-api"})


@ app.route(os.path.join(conf["root"], 'coins'), methods=['GET'])
def get_coins():
    coins = list(fdb.child("coins").get().val().keys())
    return jsonify(coins)


@ app.route(os.path.join(conf["root"], 'farms'), methods=['GET'])
def get_farms():
    data = dict(fdb.child("coins").get().val())

    coins = list(data.keys())
    sites = []
    for coin in coins:
        els = data[coin]["info"]
        for el in els:
            sites.append({"site": el["site"], "url": el["url"]})

    return jsonify(sites)


@ app.route(os.path.join(conf["root"], 'farms/tags'), methods=['GET'])
def get_farm_tags():
    data = list(fdb.child("sites").get().val())

    rd = {}
    for site in data:
        rd[site["name"]] = site["tag"]

    return jsonify(rd)


@ app.route(os.path.join(conf["root"], 'farms/<tag>'), methods=['GET', 'POST', 'DELETE'])
def farm(tag):
    def check_format(pd):
        k = pd.keys()
        check0 = "url" not in k
        check1 = "url" not in k
        check2 = "code" not in k
        if check0 or check1 or check2:
            return False
        else:
            return True

    #data = list(fdb.child("farms").get().val())
    if request.method == 'GET':
        out = fdb.child("farms").child(tag).get().val()
        return jsonify(out)
    elif request.method == 'POST':
        pd = request.json
        if pd:
            if check_format(pd):
                out = fdb.child("farms").child(tag).update(pd)
                print(out)
                return jsonify(msg2)
            else:
                return jsonify(msg1)
        else:
            return jsonify(msg1)


@ app.route(os.path.join(conf["root"], 'info'), methods=['GET'])
def get_info():
    data = dict(fdb.child("coins").get().val())

    coins = list(data.keys())
    for coin in coins:
        del data[coin]["image_uri"]

    return jsonify(data)


@ app.route(os.path.join(conf["root"], 'images'), methods=['GET'])
def get_images():
    data = dict(fdb.child("coin_images").get().val())
    return jsonify(data)


@ app.route(os.path.join(conf["root"], 'images/<coin>'), methods=['GET', 'POST', 'DELETE'])
def coin_images(coin):

    if request.method == 'GET':
        data = fdb.child("coin_images").child(coin).get().val()
        return jsonify(data)
    elif request.method == 'POST':
        pd = request.json
        if pd and len(pd) == 1:
            out = fdb.child("coin_images").update(pd)
            if out == pd:
                return jsonify(msg2)
            else:
                return jsonify(msg0)
        else:
            return jsonify(msg1)
    elif request.method == 'DELETE':
        out = fdb.child("coin_images").child(coin).remove()
        return jsonify(msg2)


@ app.route(os.path.join(conf["root"], 'info/<coin>'), methods=['GET'])
def get_coin_info(coin):
    data = dict(fdb.child("coins").get().val())
    return jsonify(data[coin.upper()])


@ app.route(os.path.join(conf["root"], 'coins/<farm_tag>'), methods=['GET'])
def get_farm_coins(farm_tag):
    data = dict(fdb.child("coins").get().val())
    farms = list(fdb.child("sites").get().val())
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
