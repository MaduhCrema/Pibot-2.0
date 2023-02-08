# Implementação da movimentação do robot em Python

# importa as bibliotecas necessárias
import RPi.GPIO as GPIO
import time
import getch 
#=======================================================================
# Definições globais?
#=======================================================================
#Seta o valor máximo dos pinos PWM
GPIO.setmode(GPIO.BCM)  # seta o modo BCM
GPIO.setwarnings(False) #desabilita warnings

# Pinos PWM
pwmA = 13 # enable A (motor esquerdo)
pwmB = 20 # enable B (motor direito)

# estabelece os pinos para saída dos motores
ForwRight = 19  # frente direita
BackRight = 16  # trás direita
BackLeft = 26   # trás esquerda
ForwLeft = 21   # frente esquerda

#Seta o valor máximo dos pinos PWM
GPIO.setmode(GPIO.BCM)  # seta o modo BCM
GPIO.setwarnings(False) #desabilita warnings

# Pinos PWM
pwmA = 13 # enable A (motor esquerdo)
pwmB = 20 # enable B (motor direito)

# estabelece os pinos para saída dos motores
ForwRight = 19  # frente direita
BackRight = 16  # trás direita
BackLeft = 26   # trás esquerda
ForwLeft = 21   # frente esquerda

#=======================================================================
# Setup_motors()
# Realiza a configuração inicial dos motores
#=======================================================================
def setup_motors():
    #seta os valores iniciais dos pinos motores
    GPIO.setup(ForwRight, GPIO.OUT, initial = GPIO.LOW)
    GPIO.setup(BackRight, GPIO.OUT, initial = GPIO.LOW)
    GPIO.setup(BackLeft, GPIO.OUT, initial = GPIO.LOW)
    GPIO.setup(ForwLeft, GPIO.OUT, initial = GPIO.LOW)
    
    #inicializa os pinos pwm com potência 0
    pwmA.start(0)
    pwmB.start(0)

#=======================================================================
# Mover para frente
# move_forward(powerLeft, powerRight)
# Parâmetros:
#   powerLeft: potência a ser aplicada no motor esquerdo
#   powerRight: potência a ser aplicada no moter direito
#
#       A função foi construída para permitir que potências diferentes 
#   possam ser aplicadas aos motores, permitindo que o controle via 
#   joystick no app possa controlar os motores usando as informações de 
#   ângulo e distância do centro fornecidas pelo joystick. Para tanto 
#   deve-se calcular as componentes nos eixos x e y do joystick e 
#   determinar as potências corretas a serem aplicadas aos motores, o 
#   que permitira a realização de curvas fora do eixo do robô. 
#=======================================================================
def move_forward(powerLeft, powerRight):
    pwmA.ChangeDutyCycle(powerLeft) #Altera a potência do motor esquerdo
    pwmB.ChangeDutyCycle(powerRight)#Altera a potência do motor direito
    
    GPIO.output(ForwLeft, GPIO.HIGH)    #esteira esquerda para frente
    GPIO.output(ForwRight, GPIO.HIGH)   #esteira direita para frente
    GPIO.output(BackLeft, GPIO.LOW)     
    GPIO.output(BackRight, GPIO.LOW)
    
#=======================================================================
# Mover para trás
# move_backward(powerLeft, powerRight)
# Parâmetros:
#   powerLeft: potência a ser aplicada no motor esquerdo
#   powerRight: potência a ser aplicada no moter direito
#       
#       Idem a função move_forward(powerLeft, powerRight).
#=======================================================================
def move_backward(powerLeft, powerRight):
    pwmA.ChangeDutyCycle(powerLeft)  #muda a potência do motor esquerdo
    pwmB.ChangeDutyCycle(powerRight) #muda a potência do motor direito
    
    GPIO.output(BackLeft, GPIO.HIGH)    #esteira esquerda para trás
    GPIO.output(BackRight, GPIO.HIGH)   #esteira direita para trás
    GPIO.output(ForwLeft, GPIO.LOW)     
    GPIO.output(ForwRight, GPIO.LOW)

#=======================================================================
# Mover para esquerda no próprio eixo
# move_left(power)
# Parâmetros:
#   power: potência a ser aplicada em ambos os motores, já que o 
#       objetivo é girar sobre o próprio eixo (Talvez não seja útil no 
#       app). 
#=======================================================================
def move_left(power):
    pwmA.ChangeDutyCycle(power) #muda a potência dos motores
    pwmB.ChangeDutyCycle(power) #para girar no próprio eixo

    GPIO.output(BackLeft, GPIO.HIGH)    #esteira esquerda para trás
    GPIO.output(ForwRight, GPIO.HIGH)   #esteira direita para frente
    GPIO.output(ForwLeft, GPIO.LOW)
    GPIO.output(BackRight, GPIO.LOW)

#=======================================================================
# Mover para direita no proprio eixo
# move_right(power)
# Parâmetros:
#   power: potência a ser aplicada em ambos os motores, já que o 
#       objetivo é girar sobre o próprio eixo (Talvez não seja útil no 
#       app). 
#=======================================================================
def move_right(power):
    pwmA.ChangeDutyCycle(power) #muda a potência dos motores
    pwmB.ChangeDutyCycle(power) #para girar no próprio eixo

    GPIO.output(BackRight, GPIO.HIGH)   #esteira direita para trás
    GPIO.output(ForwLeft, GPIO.HIGH)    #esteira esquerda para frente
    GPIO.output(BackLeft, GPIO.LOW)     
    GPIO.output(ForwRight, GPIO.LOW)

#=======================================================================
# Pára os motores
#=======================================================================
def stop():
    pwmA.ChangeDutyCycle(0) #atribui potência 0
    pwmB.ChangeDutyCycle(0) #para ambos os motores

    GPIO.output(BackRight, GPIO.LOW)    #Desliga todos os sinais de 
    GPIO.output(ForwLeft, GPIO.LOW)     #controle das esteiras
    GPIO.output(BackLeft, GPIO.LOW)
    GPIO.output(ForwRight, GPIO.LOW)

#=======================================================================
# lê o comando do teclado
# Os seguintes comandos são possíveis:
#   w: move para a frente
#   s: move para trás
#   a: move para esquerda
#   d: move para a direita
#   x: para os motores
#   q: encerra o programa
#=======================================================================
def get_command():
    pl = 25 #potência aplicada ao motor esquerdo
    pr = 25 #potência aplicada ao motor direito
    p = 35  #potência aplicad a ambos os motores quando girar à esquerda
            #ou à direita no próprio eixo.
            
    while True:
        command = getch.getch()
        if command == 'w':
            move_forward(pl, pr)
        elif command == 's':
            move_backward(pl, pr)
        elif command == 'a':
            move_left(p)
        elif command == 'd':
            move_right(p);
        elif command == 'x':
            stop()
        elif command == 'q':
            break;

#=======================================================================
# Programa principal
#=======================================================================

#seta os pinos PWM como pinos de saida e seus valores iniciais
GPIO.setup(pwmA, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(pwmB, GPIO.OUT, initial = GPIO.LOW)

pwmA = GPIO.PWM(13, 100)
pwmB = GPIO.PWM(20, 100)
    
#setup_motors() # configuração inicial dos motores

#get_command() #lê e processa os comandos do piloto

# para os motores 
#pwmA.stop()
#pwmB.stop()

#limpa a configuração dos pinos GPIO
#GPIO.cleanup()