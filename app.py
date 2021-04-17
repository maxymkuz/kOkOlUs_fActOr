from flask import Flask, render_template, request
import json
from backend_main import add_to_db, find_db, get_total_pdf, get_top_n
import json
from math import log

app = Flask(__name__)
connection, cursor = add_to_db()


@app.route("/")
def main():
    return render_template("index.html")


@app.route("/api/query", methods=['POST'])
def get_videos():
    if not request.is_json:
        return json.dumps({"response": "Input is not a json"}), 400
    # Parsing input json
    content = request.get_json()
    print(content)
    # if "query" not in content:
    #     print("wrewprljerlwjklawerjlgasdhjl")
    #     return json.dumps({"response": "No text field in json"}), 400

    print(content)
    res = find_db(connection, cursor, content)
    ret = []
    for i in res:
        ret.append({
            "id": i[1],
            "name": i[2]
        })
    print(ret)
    return json.dumps(ret)


@app.route("/get_timestamp", methods=['POST'])
def get_timestamp():
    if not request.is_json:
        return json.dumps({"response": "Input is not a json"}), 400
    # Parsing input json
    content = request.get_json()
    print("HUI", content)

    try:
        # Retrieving text field from json
        query = content["query"]
        id = content["id"]
        db = content["db"]
        print(query)
        res = find_db(connection, cursor, query, db=db)
        print("____", res)
        volodya_dick = []

        print(id, res)

        for i in res:
            if i[1] == id:
                volodya_dick = i[3]
                break
        print(volodya_dick)

        total = [log(x + 1e-20) for x in get_total_pdf(volodya_dick, 600)]
        x = get_top_n(total, 600, 10)
        ret = [{"timestamp": i[0], "prob": i[1]} for i in x]
        return json.dumps(ret)
    except:
        return json.dumps([{"timestamp": 0, "prob": 0}])


if __name__ == "__main__":
    app.run(debug=True)
