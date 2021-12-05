import csv
import json
from datetime import datetime


def get_movie_titles():
    titles = []
    with open("data/movies.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            titles.append(row["film_title"])
    return titles


def get_cities():
    cities = []
    with open("data/cinemas.csv", "r") as f:
        reader = csv.DictReader(f)

        for row in reader:
            city = row["city"]
            if city in cities:
                continue
            cities.append(city)

    return cities


def get_value_from_cinema_data(valueColumn, value, searchedColumn):
    with open("data/cinemas.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row[valueColumn] == value:
                return row[searchedColumn]
    return ""


def get_value_from_film_data(valueColumn, value, searchedColumn):
    with open("data/movies.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row[valueColumn] == value:
                return row[searchedColumn]
    return ""


def get_options():
    return {
        "titles": get_movie_titles(),
        "cities": get_cities(),
    }


def get_initial_values(initial_title):
    now = str(datetime.now())

    title = initial_title
    city = "Semua"
    date = {"year": "2021", "month": now[5:7], "day": now[8:10]}
    time = {"hour": now[11:13], "minute": now[14:16]}

    return {
        "title": title,
        "city": city,
        "time": time,
        "date": date,
    }


def parse_form(form):
    year = form.get("year")
    if not year:
        year = "2021"

    return {
        "title": form.get("title"),
        "city": form.get("city"),
        "date": {
            "day": form.get("day"),
            "month": form.get("month"),
            "year": year,
        },
        "time": {
            "hour": form.get("hour"),
            "minute": form.get("minute"),
        },
    }


def get_title_error(title):
    errors = []
    if not title:
        errors.append("Judul film tidak boleh kosong")
    elif title not in get_movie_titles():
        errors.append("Film tidak ditemukan")
    return errors


def get_city_error(city):
    errors = []
    if not city:
        errors.append("Kota tidak boleh kosong")
    if city not in get_cities():
        errors.append("Kota tidak ditemukan")
    return errors


def get_hour_error(hour):
    errors = []
    if not hour:
        errors.append("Jam tidak boleh kosong")
    if not hour.isdigit():
        errors.append("Jam harus berupa angka")
    elif int(hour) < 0 and int(hour) > 23:
        errors.append("Jam harus bernilai 0-23")

    return errors


def get_minute_error(minute):
    errors = []
    if not minute:
        errors.append("Menit tidak boleh kosong")
    if not minute.isdigit():
        errors.append("Menit harus berupa angka")
    elif int(minute) < 0 and int(minute) > 59:
        errors.append("Menit harus bernilai 0-59")

    return errors


def get_date_error(date):
    correctDate = True
    try:
        newDate = datetime(2021, int(date["month"]), int(date["day"]))
        return []
    except:
        return ["Tanggal tidak valid"]


def is_string(text):
    return isinstance(text, str)


def parse_json(form_value):
    parsed_form = form_value

    if is_string(form_value):
        parsed_form = parsed_form.replace("'", '"')
        parsed_form = json.loads(parsed_form)

    return parsed_form


#  The received form params is a parsed form using `parse_form` function.
#  if the data is still a JSON string, convert it using `parse_json` function.
#  Don't use raw form data from Flask
def validate_form(parsed_form):
    errors = []

    title_error = get_title_error(parsed_form["title"])
    city_error = get_city_error(parsed_form["city"])
    hour_error = get_hour_error(parsed_form["time"]["hour"])
    minute_error = get_minute_error(parsed_form["time"]["minute"])
    date_error = get_date_error(parsed_form["date"])

    errors += title_error
    errors += city_error
    errors += hour_error
    errors += minute_error
    errors += date_error

    return errors


def get_film_code(film_title):
    return get_value_from_film_data("film_title", film_title, "film_code")


def get_cinema_code(location):
    return get_value_from_cinema_data("location", location, "cinema_code")


def get_column_average(film_code, cinema_code, column):
    film_data = get_value_from_film_data("film_code", film_code, column)
    cinema_data = get_value_from_cinema_data("cinema_code", cinema_code, column)
    return (float(film_data) + float(cinema_data)) / 2


def get_total_sales(film_code, cinema_code):
    return get_column_average(film_code, cinema_code, "total_sales")


def get_tickets_sold(film_code, cinema_code):
    return get_column_average(film_code, cinema_code, "tickets_sold")


def get_ticket_use(film_code, cinema_code):
    return get_column_average(film_code, cinema_code, "ticket_use")


def get_capacity(cinema_code):
    return get_value_from_cinema_data("cinema_code", cinema_code, "capacity")


def predict(parsed_form, location, model):
    # validation is already done inside main.py
    # it is assumed that all input is valid

    film_code = get_film_code(parsed_form["title"])
    cinema_code = get_cinema_code(location)

    total_sales = get_total_sales(film_code, cinema_code)
    tickets_sold = get_tickets_sold(film_code, cinema_code)
    ticket_use = get_ticket_use(film_code, cinema_code)
    capacity = get_capacity(cinema_code)

    show_time = int(parsed_form["time"]["hour"])
    month = int(parsed_form["date"]["month"])
    day = int(parsed_form["date"]["day"])

    quarter = (month - 1) // 3 + 1

    values = [
        film_code,
        cinema_code,
        total_sales,
        tickets_sold,
        show_time,
        ticket_use,
        capacity,
        month,
        quarter,
        day,
    ]

    return model.predict([values])


def cinemas_in_city(city):
    cinemas = []

    with open("data/cinemas.csv", "r") as f:
        reader = csv.DictReader(f)

        for row in reader:
            if row["city"] == city:
                cinemas.append(row["location"])

    return cinemas


def parse_money(number):
    parsed_number = "{:,.2f}".format(number)

    parsed_number = parsed_number.replace(",", "#")
    parsed_number = parsed_number.replace(".", ",")
    parsed_number = parsed_number.replace("#", ".")

    return "Rp " + parsed_number


def predict_from_city(parsed_form, model):
    # validation is already done inside main.py
    # it is assumed that all input is valid

    prices = []
    selected_city = parsed_form["city"]
    cinemas = cinemas_in_city(selected_city)

    for cinema in cinemas:
        val = predict(parsed_form, cinema, model)[0]
        prices.append({"location": cinema, "price": val})

    cheapest_data = prices[0]

    price_sum = 0

    for price in prices:
        price_sum += price["price"]

        if float(price["price"]) < float(cheapest_data["price"]):
            cheapest_data = price

    avg_price = price_sum / len(prices)

    avg_data = {"price": parse_money(avg_price), "location": selected_city}

    cheapest_data["price"] = parse_money(cheapest_data["price"])
    cheapest_data["location"] = cheapest_data["location"] + ", " + selected_city

    return [avg_data, cheapest_data]


def get_prediction_data(parsed_form, model):
    [avg_data, cheapest_data] = predict_from_city(parsed_form, model)

    date = parsed_form["date"]["day"] + "-" + parsed_form["date"]["month"]
    time = parsed_form["time"]["hour"] + ":" + parsed_form["time"]["minute"]
    title = parsed_form["title"]

    return {
        "avg_price": avg_data,
        "cheapest_price": cheapest_data,
        "date": date,
        "time": time,
        "title": title,
    }
