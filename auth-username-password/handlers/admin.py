from flask import render_template

from utils.decorators import admin_required


@admin_required
def main(**params):
    return render_template("admin/main.html", **params)
