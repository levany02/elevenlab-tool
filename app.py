from sanic import Sanic
from sanic.response import json
from sanic_ext import Extend
from datetime import datetime
import json as json_p
import datetime

from data_retrieval import TIME_TABLE, UPSALE_SERVICE, IMPROVE_TIME_TABLE

from openai import OpenAI
client = OpenAI(api_key="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")

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

        print(data['date'])

        if data['name'] == "" and data['date'] == "":
            print("0")
            data['name'] = list(time_table.keys())[0]

        
        if data['name'] != "" and (data['name'] not in list(time_table.keys())) and data['date'] not in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            print("1")
            _tmp_valid = ", ".join(list(time_table.keys()))
            return json({
                "check": f"{data['name']} is not available. Here is some available therapist: {_tmp_valid}. Please provide a specific day:"
            })

        if data['name'] != "" and (data['name'] not in list(time_table.keys())) and data['date'] in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            print("2")
            _tmp_valid = []
            for _name, _value in time_table.keys():
                print("Value: ", _name, "Date: ", data['date'], "value: ", _value[data['date']])
                if _value[data['date']] != "Off":
                    _tmp_valid.append(_name)
            if len(_tmp_valid) > 0:
                _tmp_valid = ", ".join(_tmp_valid)
                return json({
                    "check": f"Here is some available therapist on : {_tmp_valid}"
                })
            else:
                return json({
                    "check": f"There is no available therapist on that day."
                })


        if data['name'] == "" and data['date'] in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            print("3")
            for _name, _value in time_table.items():
                if time_table[_name][data['date']] != "Off":
                    return json({
                        "check": _name + " is available from: " + _value[data['date']] + " on " + data['date']
                    })
                    break
                

        elif data['name'] != "" and data['date'] not in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            print("4")
            for _date, _time in time_table[data['name']].items():
                if time_table[data['name']][_date] != "Off":
                    return json({
                        "check": data['name'] + " is available from: " + time_table[data['name']][_date] + " on " + _date
                    })
                    break

        elif time_table[data['name']][data['date']] != "Off":
            print("5")
            return json({
                "check": data['name']+ " is available from: " + time_table[data['name']][data['date']] + " on " + data['date']
            })
        else:
            print("6")
            other_date = [f"{data['name']} is available on {_date} from {_time}" for _date, _time in time_table[data['name']].items() if _time != "Off"]
            other_date = ", or ".join(other_date)
            print(other_date)
            other_tech = [f"{_name} is available on {data['date']} from {time_table[_name][data['date']]}" for _name, _ in time_table.items() if time_table[_name][data['date']] != "Off"]
            other_tech = ", or ".join(other_tech)
            return json({
                "check": f"""
                 {data['name']} is off on {data['date']} but {other_date} ,
                 Would you like to change to that day.
                 Or we have {other_tech}
                """
            })
    except Exception as err:
        print("Error: ", err)
        return json({"check": IMPROVE_TIME_TABLE})


@app.route("/is_therapist_available_v2", methods=['POST'])
async def is_available_v2(request):
    data = request.body
    print(data)
    try:
        data = json_p.loads(data)
        time_table = IMPROVE_TIME_TABLE.get(data['service'].title(), TIME_TABLE)

        if data['date'].title() == 'Tomorrow':
            tomorrow = datetime.date.today() + datetime.timedelta(days=1)
            data['date'] = tomorrow.strftime("%A")

        print(data['date'])

        if data['name'] == "" and data['date'] == "":
            data['name'] = list(time_table.keys())[0]

        
        if data['name'] != "" and (data['name'] not in list(time_table.keys())) and data['date'] not in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            print("1")
            _tmp_valid = ", ".join(list(time_table.keys()))
            return json({
                "check": f"Here is some available therapist: {_tmp_valid}. Please provide a specific day:"
            })

        if data['name'] != "" and (data['name'] not in list(time_table.keys())) and data['date'] in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            print("2")
            _tmp_valid = []

            for _name, _value in time_table.items():
                print("Value: ", _name, "Date: ", data['date'], "value: ", _value[data['date']])
                if _value[data['date']] != "Off":
                    _tmp_valid.append(_name)
            if len(_tmp_valid) > 0:
                _tmp_valid = ", ".join(_tmp_valid)
                return json({
                    "check": f"Here is some available therapist on : {_tmp_valid}"
                })
            else:
                return json({
                    "check": f"There is no available therapist on that day."
                })

        if data['name'] == "" and data['date'] in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            _tmp = []
            for _name, _value in time_table.items():
                if time_table[_name][data['date']] != "Off":
                    _tmp.append(_name + " is available from: " + _value[data['date']] + " on " + data['date'])
            return json({
                "check": ", or ".join(_tmp)
            })
                

        elif data['name'] != "" and data['date'] not in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            _tmp = []
            for _date, _time in time_table[data['name']].items():
                if time_table[data['name']][_date] != "Off":
                    _tmp.append(data['name'] + " is available from: " + time_table[data['name']][_date] + " on " + _date)
            return json({
                "check": ", or ".join(_tmp)
            })

        elif time_table[data['name']][data['date']] != "Off":
            return json({
                "check": data['name']+ " is available from: " + time_table[data['name']][data['date']] + " on " + data['date']
            })
        else:
            other_date = [f"{data['name']} is available on {_date} from {_time}" for _date, _time in time_table[data['name']].items() if _time != "Off"]
            other_date = ", or ".join(other_date)
            print(other_date)
            other_tech = [f"{_name} is available on {data['date']} from {time_table[_name][data['date']]}" for _name, _ in time_table.items() if time_table[_name][data['date']] != "Off"]
            other_tech = ", or ".join(other_tech)
            return json({
                "check": f"""
                 {data['name']} is off on {data['date']} but {other_date} ,
                 Would you like to change to that day.
                 Or we have {other_tech}
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
        print("****** Upsale Service *******\n")
        print("\n".join(UPSALE_SERVICE[data['service'].title()]))

        print("****** End Upsale Service ******* \n")

        return json({
            "upsale_service_infor": "\n".join(UPSALE_SERVICE[data['service'].title()])
        })
    except Exception as err:
        print("Error: ", err)
        return json({"upsale_service_infor": "There are no information detail for this service."})


@app.route("/nearest_location", methods=['POST'])
async def find_nearest_location(request):
    data = request.body
    try:
        data = json_p.loads(data)
        prompt = f"Find 1 Massage Envy location near {data['location']}. Only get location's name and address."
        completion = client.chat.completions.create(
            model="gpt-4o-search-preview",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
        )
        print("Location: ", completion.choices[0].message.content)

        return json({
            "nearest_location": completion.choices[0].message.content
        })
    except Exception as err:
        print("Error: ", err)
        return json({"nearest_location": "There are no nearest franchised."})





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
