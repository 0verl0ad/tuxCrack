# -*- encoding: utf-8 -*-

#from __future__ import division
import crypt
import sys
from mpi4py import MPI
import subprocess
import math

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()


def parteDiccionario(dic, proc):
    comando = 'wc -l ' + dic
    c = subprocess.Popen([comando], shell=True,
        stdout=subprocess.PIPE).communicate()[0]
    lineas = c.split(' ')
    fragmento = math.ceil(float(lineas[0])/proc)
    comando_separar = 'split -l ' + str(int(fragmento)) + ' -d -a 3 ' + dic + \
        ' pruebas/parte_'
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
    print "Leyendo diccionario...."
    print ""
    linea = dic.readline()
    vdic = []
    while linea != "":
        linea = linea.rstrip("\n")
        vdic.append(linea)
        linea = dic.readline()
    return vdic


def crackUsuarios(vusuarios, vdiccionario):
    """
    Funcion encargada de realizar fuerza bruta a un fichero shadow
    con un diccionario
    """
    print "Iniciando ataque de fuerza bruta..."
    for u in vusuarios:
        udata = u[1].split("$")
        if udata[1] == '6':
            print "Usuario -> " + u[0] + "  Cifrado -> SHA-512"
            salt = "$" + str(6) + "$" + udata[2] + "$"
            for i in range(len(vdiccionario)):
                #para mostrar el porcentaje de fichero probado
                escala = (i+1) * 100 / len(vdiccionario)
                sys.stdout.write("\r%d%%" % escala)
                sys.stdout.flush()
                pcifrada = crypt.crypt(vdiccionario[i], salt)
                if pcifrada == u[1]:
                    print ""
                    print "Usuario: " + u[0] + "   Contraseña: " \
                        + vdiccionario[i]
                    sys.exit()
            print ""
            print "Contraseña no encontrada :("
            print


def main():
    if len(sys.argv) == 3:
        sombra = open(sys.argv[1])
        diccionario = open(sys.argv[2])
    else:
        print
        print "Uso python <fichero shadow> <diccionario>"
        print
        sys.exit()
    p = 5
    parteDiccionario(sys.argv[2], int(p))
    #usuarios = leeSombra(sombra)
    #palabras = leeDic(diccionario)

    #crackUsuarios(usuarios, palabras)


if __name__ == "__main__":
    main()
