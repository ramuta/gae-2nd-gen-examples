from flask import render_template, request, redirect, url_for
from models.env_var import EnvVar


def dashboard_main():
    env_vars = EnvVar.fetch_all()

    return render_template("dashboard/main.html", env_vars=env_vars)


def dashboard_env_var_create():
    if request.method == "POST":
        name = request.form.get("name")
        value = request.form.get("value")

        EnvVar.create(name=name, value=value)
        return redirect(url_for("dashboard.main"))
    else:
        return render_template("dashboard/env_var_create.html")


def dashboard_env_var_details(var_id):
    env_var = EnvVar.get(name=var_id)
    return env_var
