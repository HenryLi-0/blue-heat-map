from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def test():
    return render_template("test2.html")

@app.route('/original')
def hmm():
    return render_template("test.html")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
