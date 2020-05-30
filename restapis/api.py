import flask
from flask import request
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True

with open('config.json', 'r') as config:
    polynomials = json.load(config)

sp = int(polynomials['sp'])
print('sp: ', sp)


def eq_evaluator(x_value, degree):
    x_value = float(x_value)
    # Keys stored in json are of string format
    eq = polynomials[str(degree)]

    total = 0
    for index, coefficient in enumerate(reversed(eq)):
        #print(index, '  ', coefficient)
        total = total + (coefficient * (x_value ** (index)))

    # value after evaluting
    return total


@ app.route('/', methods=['GET'])
def home():
    return "Process API is working"

# Get Process values


@ app.route('/pv', methods=['GET'])
def pv():
    mv = request.args['mv']
    degree = request.args['degree']
    pv = eq_evaluator(mv, degree)
    data = {"sp": sp, "pv": pv, "mv": mv}
    return json.dumps(data)

# Modify the sp value


@ app.route('/sp', methods=['GET'])
def ssp():
    global sp
    sp = request.args['sp']
    polynomials['sp'] = int(sp)
    with open('config.json', 'w') as config:
        json.dump(polynomials, config)
    print('new sp set, value : ', sp)
    data = {"sp": sp}
    return json.dumps(data)


app.run()
