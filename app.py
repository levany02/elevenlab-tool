from sanic import Sanic
from sanic.response import json
from sanic_ext import Extend
from datetime import datetime
import json as json_p
import datetime

from data_retrieval import TIME_TABLE, UPSALE_SERVICE, IMPROVE_TIME_TABLE

app = Sanic("HelloWorldApp")
Extend(app)

@app.middleware("response")
async def add_cors_headers(request, response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type"

@app.route("/")
async def hello_world(request):
    return json({"date": datetime.datetime.now().strftime("%A, %d/%m/%Y")})


@app.route("/is_therapist_available", methods=['POST'])
async def is_available(request):
    data = request.body
    print(data)
    try:
        data = json_p.loads(data)
        time_table = IMPROVE_TIME_TABLE.get(data['service'].title(), TIME_TABLE)

        if data['date'].title() == 'Tomorrow':
            tomorrow = datetime.date.today() + datetime.timedelta(days=1)
            data['date'] = tomorrow.strftime("%A")

        if data['name'] == "" and data['date'] == "":
            data['name'] = list(time_table.keys())[0]

        
        if data['name'] != "" and data['name'] not in list(time_table.keys()):

            _tmp_valid = ", ".join(list(time_table.keys()))
            return json({
                "check": f"{data['name']} is not available. Here is some available therapist: {_tmp_valid}"
            })


        if data['name'] == "" and data['date'] in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            for _name, _value in time_table.items():
                if time_table[_name][data['date']] != "Off":
                    return json({
                        "check": _name + " is available from: " + _value[data['date']]
                    })
                    break
                

        elif data['name'] != "" and data['date'] not in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            for _date, _time in time_table[data['name']].items():
                if time_table[data['name']][_date] != "Off":
                    return json({
                        "check": data['name'] + " is available from: " + time_table[data['name']][_date]
                    })
                    break

        elif time_table[data['name']][data['date']] != "Off":
            return json({
                "check": data['name']+ " is available from: " + time_table[data['name']][data['date']]
            })
        else:
            other_date = [f"{data['name']} is available on {_date} from {_time}" for _date, _time in time_table[data['name']].items() if _time != "Off"]
            other_tech = [f"{_name} is available on {data['date']} from {time_table[_name][data['date']]}" for _name, _ in time_table.items() if time_table[_name][data['date']] != "Off"]
            return json({
                "check": f"""
                 {data['name']} is off on {data['date']} but {other_date[0]} ,
                 Would you like to change to that day.
                 Or we have {other_tech[0]}
                """
            })
    except Exception as err:
        print("Error: ", err)
        return json({"check": IMPROVE_TIME_TABLE})


@app.route("/upsale_service", methods=['POST'])
async def upsale_service(request):
    data = request.body
    try:
        data = json_p.loads(data)
        return json({
            "upsale_service_infor": "\n".join(UPSALE_SERVICE[data['service']])
        })
    except Exception as err:
        print("Error: ", err)
        return json({"upsale_service_infor": "There are no information detail for this service."})




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
