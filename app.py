from flask import Flask, render_template, request
import model

app = Flask(__name__)

@app.route("/")
def base():
    return render_template("base.html")

@app.route("/text", methods=['POST', 'GET'])
def text():
    article = request.args.get('article')
    if article == None:
        return render_template("text.html")
    else:
        pred, stat = model.prediction(article)
        return render_template("text.html", prediction = pred, status = stat)


if __name__ == "__main__":
    app.run(debug=True)