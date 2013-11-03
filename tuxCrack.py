# -*- encoding: utf-8 -*-

#from __future__ import division
import crypt
import sys
from mpi4py import MPI
import subprocess
import math
import os
import time

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()


def parteDiccionario(dic):
    ruta = os.path.dirname(sys.argv[2])
    parte = " parte_"
    if ruta != '':
        parte = " " + ruta + "/parte_"
    comando = 'wc -l ' + dic
    c = subprocess.Popen([comando], shell=True,
        stdout=subprocess.PIPE).communicate()[0]
    lineas = c.split(' ')
    fragmento = math.ceil((float(lineas[0]))/size)+1
    comando_separar = 'split -l ' + str(int(fragmento)) + ' -d -a 3 ' + dic + \
        parte
    separar = subprocess.Popen([comando_separar], shell=True)


def leeSombra(f):
    """
    Lee el fichero shadow pasado como parámetro
    """
    linea = f.readline()
    vusuarios = []
    while linea != "":
        linea = linea.rstrip('\n')
        vlinea = linea.split(":")
        if vlinea[1] != "!" and vlinea[1] != "*":
            vusuarios.append(vlinea)
        linea = f.readline()
    return vusuarios


def leeDic(dic):
    """
    Lee el diccionario pasado como parámetro
    """
    ruta = os.path.dirname(sys.argv[2])
    if ruta != '':
        dic = ruta + "/" + dic
    diccionario = open(dic)
    print "Leyendo diccionario...."
    print ""
    linea = diccionario.readline()
    vdic = []
    while linea != "":
        linea = linea.rstrip("\n")
        vdic.append(linea)
        linea = diccionario.readline()
    diccionario.close()
    return vdic


def crackUsuarios(usuario, vdiccionario):
    """
    Funcion encargada de realizar fuerza bruta a un fichero shadow
    con un diccionario
    """
    print "Iniciando ataque de fuerza bruta..."
    udata = usuario[1].split("$")
    if udata[1] == '6':
        final = False
        i = 0
        print "  Cifrado -> SHA-512"
        salt = "$" + str(6) + "$" + udata[2] + "$"
        while i < len(vdiccionario) or final is False:
        # for i in range(len(vdiccionario)):
            #para mostrar el porcentaje de fichero probado
            # escala = (i+1) * 100 / len(vdiccionario)
            # sys.stdout.write("\r%d%%" % escala)
            # sys.stdout.flush()
            pcifrada = crypt.crypt(vdiccionario[i], salt)
            if pcifrada == usuario[1]:
                print ""
                print rank
                print "Usuario: " + usuario[0] + "   Contraseña: " \
                    + vdiccionario[i]
                final = True
                final = comm.bcast(True, root=0)
                sys.exit()
            #print ""
            #print "Contraseña no encontrada :("
            #print
            i += 1


def main():
    if len(sys.argv) == 3:
        sombra = open(sys.argv[1])
    else:
        print
        print "Uso python <fichero shadow> <diccionario>"
        print
        sys.exit()

    if rank == 0:
    #si somos el primer procesador dividimos los diccionarios
        parteDiccionario(sys.argv[2])
        usuarios = leeSombra(sombra)
        time.sleep(2)
        for i in range(0, len(usuarios)):
            print "Usuario -> " + usuarios[i][0]
            #enviamos el usuario a todos los procesadores
            for j in range(0, size):
                comm.send(usuarios[i], dest=j, tag=j)
            #calcula su parte
            p_dic = "parte_00" + str(rank)
            palabras = leeDic(p_dic)
            crackUsuarios(usuarios[i], palabras)
    elif rank > 0 and rank < 10:
        u = comm.recv(source=0, tag=rank)
        p_dic = "parte_00" + str(rank)
        palabras = leeDic(p_dic)
        crackUsuarios(u, palabras)
        print final


if __name__ == "__main__":
    main()
