#Import de app
from flask_app import app
#Import de Controlares
from flask_app.controllers import user_controller
from flask_app.controllers import task_controller
#Ejecucion de App
if __name__ == '__main__':
    app.run(debug=True)