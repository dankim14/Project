from flask_app import app

from flask_app.controllers import professors
from flask_app.controllers import courses
if __name__=="__main__":
    app.run(debug=True)