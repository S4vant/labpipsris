from flask import Flask, render_template
name = "Yar"
app = Flask(name)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000,debug=True)

