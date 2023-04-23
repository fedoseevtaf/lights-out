import flask


app = flask.Flask(__name__)

app.route('/')
def _():
	return {'wall': 13}

