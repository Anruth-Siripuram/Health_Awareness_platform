import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from auth import login_user, logout_user
from disease_data import load_diseases_df, save_diseases_df, get_next_id
from knn_search import knn_search
from file_utils import UPLOAD_FOLDER, save_file

app = Flask(__name__)
app.secret_key = "supersecretkey"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# ---------------- Routes ---------------- 
@app.route("/")
def index():
    df = load_diseases_df()
    diseases = df.to_dict(orient="records")
    for d in diseases:
        if not d.get("summary"):
            ov = d.get("overview","") or ""
            d["summary"] = (ov[:120] + "...") if len(ov) > 120 else ov
    return render_template("index.html", diseases=diseases, query="")

@app.route("/disease/<int:d_id>")
def disease(d_id):
    df = load_diseases_df()
    row = df[df["id"] == int(d_id)]
    if row.empty:
        flash("Disease not found", "error")
        return redirect(url_for("index"))
    disease = row.iloc[0].to_dict()
    return render_template("disease.html", disease=disease)

@app.route("/search")
def search():
    q = request.args.get("q","").strip().lower()
    df = load_diseases_df()
    if q:
        df = knn_search(q, df)
    diseases = df.to_dict(orient="records")
    return render_template("index.html", diseases=diseases, query=q)

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        u = request.form.get("username")
        p = request.form.get("password")
        if login_user(u, p):
            session["logged_in"] = True
            flash("Logged in successfully","success")
            return redirect(url_for("host_panel"))
        flash("Invalid credentials","error")
    return render_template("login.html")

@app.route("/logout")
def logout():
    logout_user()
    flash("Logged out","success")
    session.pop("logged_in", None)
    return redirect(url_for("index"))

@app.route("/host", methods=["GET","POST"])
def host_panel():
    if not session.get("logged_in"):
        flash("Please login", "error")
        return redirect(url_for("login"))

    df = load_diseases_df()

    if request.method == "POST":
        title = request.form.get("title","").strip()
        summary = request.form.get("summary","").strip()
        overview = request.form.get("overview","").strip()
        symptoms = request.form.get("symptoms","").strip()
        prevention = request.form.get("prevention","").strip()
        file = request.files.get("image")

        img_filename = save_file(file) if file else ""
        new_id = get_next_id(df)
        new_row = {
            "id": new_id,
            "title": title,
            "summary": summary,
            "overview": overview,
            "symptoms": symptoms,
            "prevention": prevention,
            "image": img_filename
        }
        df = df.append(new_row, ignore_index=True)
        save_diseases_df(df)
        flash("Added disease.", "success")
        return redirect(url_for("host_panel"))

    diseases = df.to_dict(orient="records")
    return render_template("host_panel.html", diseases=diseases)

@app.route("/edit/<int:d_id>", methods=["GET","POST"])
def edit_disease(d_id):
    if not session.get("logged_in"):
        flash("Please login", "error")
        return redirect(url_for("login"))

    df = load_diseases_df()
    row = df[df["id"] == int(d_id)]
    if row.empty:
        flash("Not found", "error")
        return redirect(url_for("host_panel"))

    if request.method == "POST":
        title = request.form.get("title","").strip()
        summary = request.form.get("summary","").strip()
        overview = request.form.get("overview","").strip()
        symptoms = request.form.get("symptoms","").strip()
        prevention = request.form.get("prevention","").strip()
        file = request.files.get("image")

        img_filename = row.iloc[0].get("image","")
        if file:
            img_filename = save_file(file)

        df.loc[df["id"] == int(d_id), ["title","summary","overview","symptoms","prevention","image"]] = [
            title, summary, overview, symptoms, prevention, img_filename
        ]
        save_diseases_df(df)
        flash("Updated disease.", "success")
        return redirect(url_for("host_panel"))

    disease = row.iloc[0].to_dict()
    return render_template("edit_disease.html", disease=disease)

@app.route("/delete/<int:d_id>", methods=["GET","POST"])
def delete_disease(d_id):
    if not session.get("logged_in"):
        flash("Please login", "error")
        return redirect(url_for("login"))

    df = load_diseases_df()
    row = df[df["id"] == int(d_id)]
    if row.empty:
        flash("Not found", "error")
        return redirect(url_for("host_panel"))

    if request.method == "POST":
        image = row.iloc[0].get("image","")
        if image:
            try:
                os.remove(f"{UPLOAD_FOLDER}/{image}")
            except:
                pass
        df = df[df["id"] != int(d_id)]
        save_diseases_df(df)
        flash("Deleted disease.", "success")
        return redirect(url_for("host_panel"))

    disease = row.iloc[0].to_dict()
    return render_template("confirm_delete.html", disease=disease)

@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    from flask import send_from_directory
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

if __name__ == "__main__":
    app.run(debug=True)
