# clientepaginador.py
# Programa para probar el servicio de paginacion
#
import socket
import os
import signal
import psutil
import time
import getopt,sys

def findProcess(name):    
    procs = list()
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            if proc.name() == name and proc.status() == psutil.STATUS_RUNNING:
                pid = proc.pid
                procs.append(pid)         	
        except:
            pass      
    return procs

argumentList = sys.argv[1:]
# Options
options = "hs:dp:"
# Long options
long_options = ["Debug", "Port=", "Sleep=", "Help"]
debug=False
puerto=7777
sleeptime=10 #segundos
try:
    # Parsing argument
    arguments, values = getopt.getopt(argumentList, options, long_options)
     
    # checking each argument
    for currentArgument, currentValue in arguments:
        if currentArgument in ("-d", "--Debug"):
            debug=True

        elif currentArgument in ("-p", "--Port"):
            puerto=currentValue
        
        elif currentArgument in ("-s", "--Sleep"):
            sleeptime=int(currentValue)
        
        elif currentArgument in ("-h", "--Help"):
            print("Uso: cliente.py [-d] [-p puerto] [-s segundos]")
            print(" -d, --Debug: Muestra informacion de depuracion")
            print(" -p, --Port: Puerto de conexion al servicio de paginacion")
            print(" -s, --Sleep: Tiempo de espera entre envios de paquetes")
            print(" -h, --Help: Muestra esta ayuda")
            sys.exit(0)
except getopt.error as err:
    # output error, and return with an error code
    print (str(err))

print ("Debug:", debug)
print ("Puerto:",puerto)
print ("Espera:",sleeptime, "segundos")

paquete="""<package><method>paginador</method><time>Fri Dec 13 12:58:54 CEST 2019</time><id>4C114560</id><textin> 
Este es un mensaje de prueba para el servicio de paginación.
</textin></package>"""


PROGRAM = r'servicio_paginador_corrector.exe'
HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = int(puerto)  # The port used by the server
processes = findProcess(PROGRAM)
while True:
    if debug:
        print('PID:',processes)
    time.sleep(sleeptime)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            s.sendall(bytes(paquete,'utf-8'))
            data = s.recv(1024)
            processes = findProcess(PROGRAM)
            if " #LF# " not in data.decode('utf-8'):
                print("No pagina bien, reiniciamos el servicio")
                for pid in processes:
                    os.kill(pid, signal.SIGTERM)
                time.sleep(2) #esperamos a que se cierre y se relance automaticamente el proceso

            if debug:
                print(f"Received {data!r}")
        except socket.error:
            print("Error de conexion al servicio de paginacion")
            break

