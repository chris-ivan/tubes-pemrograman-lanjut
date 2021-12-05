from flask import Flask, render_template, request, redirect, url_for
from utils.functions import (
    get_options,
    get_initial_values,
    parse_form,
    validate_form,
    get_prediction_data,
    parse_json,
)

import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
modelFile = open("cinema_ticket_regression_model.pkl", "rb")


import pickle

model = pickle.load(modelFile)


@app.route("/", methods=["GET", "POST"])
def index():
    options = get_options()
    if request.method == "GET":
        values = get_initial_values(options["titles"][1])

        return render_template("index.html", options=options, initial_values=values)

    else:
        form_value = parse_form(request.form)
        errors = validate_form(form_value)

        if len(errors):
            return render_template(
                "index.html", options=options, initial_values=form_value, errors=errors
            )

        else:
            return redirect(url_for("predict", value=form_value))


@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "GET":
        form_value = request.args.get("value")
        form_value = parse_json(form_value)
        errors = validate_form(form_value)

        if len(errors):
            return redirect("/")

        result = get_prediction_data(form_value, model)

        return render_template("result.html", result=result)

    else:
        return redirect("/")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 80))
    # port = 5050
    app.run(host="0.0.0.0", port=port, debug=False)
