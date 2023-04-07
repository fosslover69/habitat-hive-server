from flask import Flask, request
from flask_cors import CORS, cross_origin
from habitability import cal_habitability


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


def gay(value):
    return cal_habitability(value['areacode'], value['windows'], value['doors'], value['furnishing'], value['type'])


@app.route('/process-data', methods=['POST'])
@cross_origin()
def process_data():
    data = request.get_json()
    return gay(data)


if __name__ == '__main__':
    app.run(debug=True)
