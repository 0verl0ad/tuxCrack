# -*- encoding: utf-8 -*-

#from __future__ import division
import crypt
import sys


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
                    print "Usuario: " + u[0] + "   Contraseña: " + vdiccionario[i]
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

    usuarios = leeSombra(sombra)
    palabras = leeDic(diccionario)

    crackUsuarios(usuarios, palabras)


if __name__ == "__main__":
    main()
