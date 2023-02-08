from flask import Flask, request, render_template, app
import json
from threading import Thread

#from distancia import setup_sensor, roda_medicao, get_distancia
from controle import setup_motors, move_forward, move_backward, move_right, move_left, stop
 
app = Flask(__name__)

pl = 25 #potencia aplicada ao motor esquerdo
pr = 25 #potencia aplicada ao motor direito
p = 25  #potencia aplicad a ambos os motores quando girar a esquerda
            #ou a direita no proprio eixo.  

@app.before_first_request
def _run_on_start():
    setup_motors()
           

@app.route('/',methods=['GET'])
def form():
    return render_template('form.html')


@app.route("/", methods=["POST"])
def receive_data():
    data = request.get_json()
    angle = data['angle']
    print(angle)
   
    if(45 <= angle < 135):
        move_forward(pl, pr)
    if(225 <= angle < 315):
        move_backward(pl, pr)
    if(135 <= angle < 225):
        move_left(p)
    if(angle < 45 and angle >= 315):
        move_right(p)
    if(angle == 0):
        stop()
    return ('',204) 


if __name__ == "__main__":
    app.run(host='localhost') 
