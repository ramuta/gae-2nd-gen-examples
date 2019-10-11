import os
from flask import Flask
from handlers import public, dashboard

app = Flask(__name__)

# URLs
app.add_url_rule(rule="/", endpoint="index", view_func=public.index, methods=["GET"])
app.add_url_rule(rule="/dashboard", endpoint="dashboard.main", view_func=dashboard.dashboard_main, methods=["GET"])
app.add_url_rule(rule="/dashboard/env-vars/create", endpoint="dashboard.env_var.create", view_func=dashboard.dashboard_env_var_create, methods=["GET", "POST"])
app.add_url_rule(rule="/dashboard/env-var/<var_id>", endpoint="dashboard.env_var.details", view_func=dashboard.dashboard_env_var_details, methods=["GET"])


if __name__ == '__main__':
    if os.getenv('GAE_ENV', '').startswith('standard'):
        app.run()  # production
    else:
        app.run(port=8080, host="localhost", debug=True)  # localhost
