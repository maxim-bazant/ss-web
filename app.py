from db_api_manager import *
from auth_api_manager import *
from flask_setup import *
from auth_setup import *


def user_logged_in():
    try: 
        return has_admin_role(session["user"]["userinfo"]["sub"])
    except:
        return False



# ---------- AUTH0 ROUTES ----------

@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect(url_for("inventory")) # USER LOGGED IN -> REDIRECTED TO THE INVENTORY ROUTE

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + AUTH0_DOMAIN
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("index", _external=True),
                "client_id": AUTH0_CLIENT_ID,
            },
            quote_via=quote_plus,
        )
    )



# ---------- CUSTOM ROUTES -----------

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        input = request.form["input"]
        return redirect(url_for("material", input=input))
    else:
        return render_template("index.html")


@app.route("/material/<input>")
def material(input):
    material = get_material_detail(input)
    if material:
        return render_template("material_detail.html", material=material)
    else:
        flash(f"Material \"{input}\" is not in the database! \n Please contact the manager.", "red")
        return redirect(url_for("index"))
    

@app.route("/inventory")
def inventory():
    if user_logged_in():
        search_value = request.args.get('search')
        materials = get_materials(value=search_value)

        if materials:
            return render_template("inventory.html", materials=materials, search=search_value)
        else:
            flash(f"There is no \"{search_value}\" in the materials database", "red")
            return render_template("inventory.html", materials=get_materials())
    else:
        flash(f"You can not edit inventory!", "red")
        return redirect(url_for("index"))
        
    
@app.route("/inventory/delete/<code>")
def delete(code):
    if user_logged_in():
        delete_material(int(code))
        flash(f"You have deleted material #{code}.", "red")
        return redirect(url_for("inventory"))
    else:
        flash(f"You can not edit inventory!", "red")
        return redirect(url_for("index"))

@app.route("/inventory/add", methods=["GET", "POST"])
def add():
    if user_logged_in():
        if request.method == "POST":
            content = request.form["content"]
            fragile = request.form["fragile"]
            placement = request.form["placement"]
            instruction = request.form["instruction"]
            units_available = request.form["units_available"]
            unit = request.form["unit"]

            add_new_material(content, fragile, placement, instruction, int(units_available), unit)

            flash("Material added", "green")
            return redirect(url_for("inventory"))
        else:
            placements = get_placements()
            available_places = [fruit for fruit in placements["all_places"] if fruit not in placements["taken_places"]]
            if len(available_places) > 0:
                return render_template("add.html", placements=get_placements(), available_places=available_places)
            else:
                flash(f"There is no more space left in the inventory!", "red")
                return redirect(url_for("inventory"))

    else:
        flash(f"You can not edit inventory!", "red")
        return redirect(url_for("index"))


@app.route("/inventory/edit", methods=["GET", "POST"])
def edit():
    if user_logged_in():
        if request.method == "POST":
            code = request.form["material_code"]
            quantity = request.form["units_edit"]

            if edit_units_available(int(code), int(quantity)):
                flash(f"Material #{code} units available changed.", "green")
            else:
                flash("You can not have negative number of units!", "red")

            return redirect(url_for("inventory"))
        else:
            redirect(url_for("inventory"))
    else:
        flash(f"You can not edit inventory!", "red")
        return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(port=8000, debug=True)