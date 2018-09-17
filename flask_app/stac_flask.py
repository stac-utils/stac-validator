"""
Description: Built during STAC/ARD Workshop Menlo Park 2018
A lot of ideas taken from cog_validator

"""

from flask import Flask, request as flask_request, render_template
from import stac_validator
import json

app = Flask(__name__)
# http://docs.aws.amazon.com/lambda/latest/dg/limits.html
app.config["MAX_CONTENT_LENGTH"] = 6 * 1024 * 1024

@app.route("/api/validate", methods=["GET"])
def api_validate():
    if flask_request.method == "GET":
        args = {}
        for k in flask_request.args:

            if k == "url":
                args[k] = flask_request.args[k]
                url = args.get("url")
                errors = stac_validitor.stac_validate(url)
                if len(errors) == 0:
                    details = "Valid"
                    return (
                        json.dumps(
                            {"status": "success", "url": url, "details": details}
                        ),
                        200,
                        {"Content-Type": "application/json"},
                    )
                else:
                    return (
                        json.dumps(
                            {
                                "status": "failure",
                                "url": url,
                                "details": "Invalid",
                                "validation_errors": errors,
                            }
                        ),
                        400,
                        {"Content-Type": "application/json"},
                    )


@app.route("/html", methods=["GET"])
def html():
    root_url = flask_request.url_root[0:-1]
    return render_template("main.html", root_url=root_url)


@app.route("/html/validate", methods=["GET"])
def html_validate():
    root_url = flask_request.url_root[0:-1]
    ret, _, _ = api_validate()
    print(ret)
    ret = json.loads(ret)
    errors = None

    if "url" in flask_request.form and flask_request.form["url"] != "":
        name = flask_request.form["url"]
    else:
        name = ret["url"]

    if "status" in ret and ret["status"] == "success":
        global_result = (
            f"Validation succeeded! <br/> {name} is a valid STAC catalog or STAC item."
        )
    else:
        global_result = (
            f"Validation failed ! {name} is NOT a valid STAC catalog or STAC item."
        )
        if "error" in ret:
            errors = [ret["error"]]
        elif "validation_errors" in ret:
            errors = ret["validation_errors"]
    return render_template(
        "result.html", root_url=root_url, global_result=global_result, errors=errors
    )
