from sanic import Sanic
from sanic.response import json
from sanic_ext import Extend
from datetime import datetime

from data_retrieval import TIME_TABLE

app = Sanic("HelloWorldApp")
Extend(app)

@app.middleware("response")
async def add_cors_headers(request, response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type"

@app.route("/")
async def hello_world(request):
    return json({"date": datetime.now().strftime("%A, %d/%m/%Y")})


@app.route("/is_available", methods=['POST'])
async def is_available(request):
    data = request.body
    print(data)
    try:
        import json as json_p
        data = json_p.loads(data)
        if data['name'] == "" and data['date'] == "":
            return json({
                        "check": "Suggest any available technician."
                    })


        if data['name'] == "" and data['date'] in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            for _name, _value in TIME_TABLE.items():
                if TIME_TABLE[_name][data['date']] != "Off":
                    return json({
                        "check": _name + " is available from: " + _value[data['date']]
                    })
                    break

        elif data['name'] != "" and data['date'] not in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            for _date, _time in TIME_TABLE[data['name']].items():
                if TIME_TABLE[data['name']][_date] != "Off":
                    return json({
                        "check": data['name'] + " is available from: " + TIME_TABLE[data['name']][_date]
                    })
                    break

        elif TIME_TABLE[data['name']][data['date']] != "Off":
            return json({
                "check": data['name']+ " is available from: " + TIME_TABLE[data['name']][data['date']]
            })
        else:
            other_date = [f"{data['name']} is available on {_date} from {_time}" for _date, _time in TIME_TABLE[data['name']].items() if _time != "Off"]
            other_tech = [f"{_name} is available on {data['date']} from {TIME_TABLE[_name][data['date']]}" for _name, _ in TIME_TABLE.items() if TIME_TABLE[_name][data['date']] != "Off"]
            return json({
                "check": f"""
                 {data['name']} is off on {data['date']} but {other_date[0]} ,
                 Would you like to change to that day.
                 Or we have {other_tech[0]}
                """
            })
    except Exception as err:
        print("Error: ", err)
        return json({"check": ""})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
