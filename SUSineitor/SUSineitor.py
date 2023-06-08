import cv2
import numpy as np
import os



def imprimirMatriz(matriz):
    for i in matriz:
            for j in i:
                print(j)
            print("\n")
            print("-------------------------------")
            print("\n")



def estaColorEnLista(colorGBR, listaDeColores):
    
    #In     :   Un color en formato GBR y una lista con colores en GBR (Hay un color transparente alfa=0)
    #Out    :   Un booleano indicando si el color se encuentra en la lista o no

    buscando = True
    contador = 0
    
    if colorGBR[3] == 0 :
        buscando = False

    while buscando and contador < len(listaDeColores):

        if np.array_equal(colorGBR,listaDeColores[contador]):
            buscando = False
        contador += 1
        
    return not buscando



def colorATupla(color):

    #In     :   Un color en forma de matriz de 4 elementos
    #Out    :   Una tupla con los 4 elementos
    if(len(color) == 4):
        ret = (color[0],color[1],color[2],color[3])
    else:
        ret = (color[0],color[1],color[2],255)
    return ret



def obtenerListaPaletaDeImagen(imagenEntrada):
    
    #In     :   Una imagen
    #Out    :   Una lista con los diferentes colores (en formato GBR) que se encuentran en la imagen

    #Coste : largo*ancho*numMedioColoresPaleta

    listaTuplasColores = [(0,0,0,0)]      
    
    for i in range(0, len(imagenEntrada)):                                                          # Recorremos cada fila
        for j in range(0, len(imagenEntrada[i])):                                                   # Y cada elemento de la fila
                                                                                                    # Es decir, recorremos la imagen como si fuese una matriz

            if estaColorEnLista(colorATupla(imagenEntrada[i][j]), listaTuplasColores) == False:     # Si es la primera vez que vemos el color
                listaTuplasColores.append(colorATupla(imagenEntrada[i][j]))                         # lo añadimos
                
    return listaTuplasColores
           


def ordenarDeClaroAOscuro(lista):
    
    # In    :   Una lista con colores
    # Out   :   Una lista con colores ordenados de oscuro a claro segun su distancia vectorial al color negro (No se tiene en cuenta la transparencia)

    listaPuntosDistancias = []

    for i in lista:

                                                                                                    # La distancia (d) entre un punto P1(a,b,c) a otro punto  P2(x,y,z) se define como 
        
        suma = (i[0])**2 + (i[1])**2 + (i[2])**2                                                    #       d = sqrt( (x-a)^2 + (y-b)^2 + (z-c)^2 )
                                                                                            
                                                                                                    # Como comparamos con el punto (0, 0, 0) :
                                                                                            
        distancia = np.sqrt(suma)                                                                   #       d = sqrt( (0-a)^2 + (0-b)^2 + (0-c)^2 ) = sqrt( a^2 + b^2 + c^2 )

        listaPuntosDistancias.append([i, distancia])                                                # En la lista previamente creado guardamos los pares (color, distancia)


                                                                                                    # Los colores se ordenan usando el metodo de ordenacion por burbuja
                                                                                                    # Recorre toda la lista comparando cada color con su siguiente y cambiandolos de orden si es necesario
                                                                                                    # Recorre la lista tantas veces como sea necesario hasta que este ordenado
                                                                                                    # No es eficiente, pero es facil (Para mejorar a futuro)

    cambios = 1 
    while cambios > 0:  
        cambios = 0
        cont = 1
        while cont < len(listaPuntosDistancias)-1:
            aux = []
            if listaPuntosDistancias[cont][1] < listaPuntosDistancias[cont + 1][1]:
                aux = listaPuntosDistancias[cont]
                listaPuntosDistancias[cont] = listaPuntosDistancias[cont + 1]
                listaPuntosDistancias[cont + 1] = aux
                cambios += 1
            cont += 1

    return listaPuntosDistancias



def obtenerDistanciaEntrePuntosPaleta(paleta):

    #In     :   Una paleta de colores
    #Out    :   Una lista de vectores (distancia al color de su derecha en la lista)
    
    listaResultado = [0]       

    for i in range(1, len(paleta)-1):                                                               # Calculamos la distancia que hay de cada color a su siguiente de la misma forma que previamente se a usado

        sumando1 = (( float(paleta[i][0][0]) - float(paleta[i+1][0][0]) ) /10 ) **2                 # (x - a)^2        (Se divide entre 10 para trabajar con numeros mas pequeños y luego se arregla haciendo *10)

        sumando2 = (( float(paleta[i][0][1]) - float(paleta[i+1][0][1]) ) /10 ) **2                 # (y - b)^2

        sumando3 = (( float(paleta[i][0][2]) - float(paleta[i+1][0][2]) ) /10 ) **2                 # (z - c)^2

        suma = float(sumando1 + sumando2 + sumando3)                                                # (x - a)^2 + (y - b)^2 + (z - c)^2

        listaResultado.append(10*(np.sqrt(suma)))                                                   # sqrt( (x - a)^2 + (y - b)^2 + (z - c)^2 )

    return listaResultado



def ampliarPaleta(paletaActual, numeroDeElementosNecesarios):

    #In     :   Una paleta de colores con x colores
    #Out    :   Una paleta de colores con y colores sabiendo que y>=x

    if len(paletaActual) >= numeroDeElementosNecesarios:                                            # Si la paleta ya cumple las condiciones minimas
        return paletaActual                                                                         # Se devuelve sin hacer nada


    while len(paletaActual) < numeroDeElementosNecesarios:

        listaDistanciasColores = obtenerDistanciaEntrePuntosPaleta(paletaActual)                    # Obtenemos la distancia de cada color al color de su derecha
        auxDis = 0          
        auxPos = 0          

        for i in range(1, len(listaDistanciasColores)-1):                                           # Se busca el par de colores que mas alejados esten
            if listaDistanciasColores[i] > auxDis:          
                auxDis = listaDistanciasColores[i]          
                auxPos = i          
                                                                                                    # Y de la media de ambos se hace un nuevo color
        a = (paletaActual[auxPos][0][0])/2 + (paletaActual[auxPos + 1][0][0])/2         
        b = (paletaActual[auxPos][0][1])/2 + (paletaActual[auxPos + 1][0][1])/2         
        c = (paletaActual[auxPos][0][2])/2 + (paletaActual[auxPos + 1][0][2])/2         

    
        paletaActual.insert(auxPos+1, [np.array([a, b, c, 255], dtype=np.uint8), 0])                # El color se añade a la paleta de colores

    return paletaActual

    

def indiceEnLista(lista, color):

    # In    :   Una lista de colores y un color
    # Out   :   La posicion del color en la lista

    cont = 0
     
    if(color[3] == 0):
        while cont < len(lista) and lista[cont][0][3] != 0:
            cont += 1

    else:
        while cont < len(lista) and (np.array_equal(lista[cont][0], color) == False):
            cont += 1

    return cont



def obtenerPlantillaDeImagen(imagen):

    # In    :   Una imagen
    # Out   :   Una matriz con numeros del 0 a la cantidad de colores de la imagen, ordenados de oscuro a claro, y la cantidad de colores


    paletaImagen = obtenerListaPaletaDeImagen(imagen)                                               # Obtenemos la paleta de la imagen

    paletaImagenOrdenada = ordenarDeClaroAOscuro(paletaImagen)                                      # y la ordenamos

    matriz = []                                                                                     # Creamos una matriz vacia que servira de plantilla

    for i in range(0,len(imagen)):                                  
        matriz.append([])                                   
        for j in range(0,len(imagen[0])):                                   
            matriz[i].append([])                                    


    ind = 0                                 
    indaux = 0                                  

    for i in range(0,len(matriz)):                                                                  # En la matriz previamente vacia colocamos el color que le corresponde, o mejor dicho 
        for j in range(0,len(matriz[0])):                                                           # su posicion en la paleta
            
            ind = indiceEnLista(paletaImagenOrdenada, imagen[i][j])

            if ind > indaux:
                indaux = ind

            matriz[i][j] = ind

    return matriz, indaux+1


    
def obetenerImagenDePaleta(imagenPlantilla, paleta, imagenLienzo):

    # In    :   Una matriz que hace de plantilla, la paleta de colores que se usara para rellenar la plantilla y una imagen vacia
    # Out   :   La imagen vacia se modificara para dar como resultado una imagen que representa la plantilla coloreada

    longitudNecesaria = 0                
                                                                                                    # Obtenemos la plantilla sobre la que se dibujara la nueva imagen
    matrizPlantilla, longitudNecesaria = obtenerPlantillaDeImagen(imagenPlantilla)                  # La variable longitudNecesaria indica cuantos colores diferentes son necesarios para pintar la plantilla


    if len(paleta) == 1:
        for i in range(0, len(matrizPlantilla)):
  
            for j in range(0, len(matrizPlantilla[i])):

                #imagenLienzo[i][j] = (paleta[0][0])[:]
                imagenPlantilla[i][j] = (paleta[0][0])[:]

    else:

        paletaAmpliada = ampliarPaleta(paleta, longitudNecesaria)                                       # Nos aseguramos de que haya suficientes colores en la paleta

        for i in range(0, len(matrizPlantilla)):
  
            for j in range(0, len(matrizPlantilla[i])):

                #imagenLienzo[i][j] = (paletaAmpliada[matrizPlantilla[i][j]][0])[:]
                imagenPlantilla[i][j] = (paletaAmpliada[matrizPlantilla[i][j]][0])[:]

    return imagenPlantilla
    


def SUSineitor(pathImagenColor, pathImagenForma):

    imagenColor = cv2.imread(pathImagenColor,-1)

    imagenForma = cv2.imread(pathImagenForma,-1)

    
    paletaColores = obtenerListaPaletaDeImagen(imagenColor)                                         # Obtenemos la lista con los colores, los colores se guardan como tuplas de 4 valores

    paletaOrdenada = ordenarDeClaroAOscuro(paletaColores)                                           # Ordenamos la paleta de colores de claro a oscuro (Dejando el color (0,0,0,0) el primero, es decir, el color negro segun RGBA)

    resultadoFinal = obetenerImagenDePaleta(imagenForma, paletaOrdenada, imagenColor)               # Obtenemos la imagen

    return resultadoFinal


#           ------------------------ Inicio ----------------------------------------------------------------------------------


print("\n")
print("    0000    00  00    0000    000000   0   00   000000   000000   000000    0000    00000  ")
print("   00       00  00   00         00     00  00   00         00       00     00  00   00  00 ")
print("   00       00  00   00         00     000 00   00         00       00     00  00   00  00 ")
print("    0000    00  00    0000      00     00 000   00000      00       00     00  00   00000  ")
print("       00   00  00       00     00     00  00   00         00       00     00  00   00 00  ")
print("       00   00  00       00     00     00  00   00         00       00     00  00   00  00 ")
print("    0000     0000     0000    000000   00  00   000000   000000     00      0000    00  00 ")

print("\n")
print("\t---MENU---")
print()
print("\t(1) Iniciar")
print("\t(2) Ayuda")
print("\t(3) Salir")
seleccion = int(input())

if seleccion == 1:
                                                                                                    # Se imprimen las dos opciones
    print("\t(1) Tomar la forma de la imagen en input")
    print("\t(2) Tomar el color de la imagen en input")
    print("\t(3) Cancelar")
    seleccion = int(input())
    

    if seleccion != 3:

                                                                                                    # Definicion de las direcciones a las carpetas de entrada de datos
        pathInput = os.path.dirname(os.path.abspath(__file__)) + '\Input'
        contenidoInput = os.listdir(pathInput)
        numImagenes = len(contenidoInput)

        pathOutput = os.path.dirname(os.path.abspath(__file__)) + '\Output'                         # Definicion de las direcciones a las carpetas de salida
                                                                                                   
        print()
        print("\tNombre de la imagen (añadir extension)")
        objeto = input()                                                                            # Nombre del objeto de la carpeta input a tomar como base
        correcto = False                                                               
        
        pathObjeto = os.path.join(pathInput, objeto)
        correcto = os.path.isfile(pathObjeto)            

        print()
        print("\t(1) Aplicar a todas las imagenes")
        print("\t(2) Aplicar a una unica imagen")
        seleccion2 = int(input())
        correcto2 = True

        if(seleccion2 == 2):
            print()
            print("\tNombre de la imagen (añadir extension)")
            objetoTarget = input()                                                                  # Nombre del objeto de la carpeta input a tomar como base
            correcto2 = False                                                               

            pathObjetoTarget = os.path.join(pathInput, objetoTarget)
            correcto2 = os.path.isfile(pathObjetoTarget)

        if correcto and correcto2:
            contadorProgreso = 1
            print()
            print("Procesando...")

            if (seleccion == 1):
                if (seleccion2 == 2):
                    cv2.imwrite(os.path.join(pathOutput,objetoTarget), SUSineitor(pathObjetoTarget, pathObjeto)) 

                else:
                    for i in contenidoInput:
                        #          (filename                  , image     ( color                   , forma     ))
                        cv2.imwrite(os.path.join(pathOutput,i), SUSineitor(os.path.join(pathInput,i), pathObjeto)) 

                        print("Progreso : " + str(int((contadorProgreso/numImagenes)*100)) + "% : " + "|" * int((contadorProgreso/numImagenes)*100))
                        contadorProgreso += 1
                


            elif (seleccion == 2):
                if (seleccion2 == 2):
                    cv2.imwrite(os.path.join(pathOutput,objetoTarget), SUSineitor(pathObjeto, pathObjetoTarget)) 

                else:
                    for i in contenidoInput:
                        #          (filename                  , image     ( color    , forma                    ))
                        cv2.imwrite(os.path.join(pathOutput,i), SUSineitor(pathObjeto, os.path.join(pathInput,i))) 

                        print("Progreso : " + str(int((contadorProgreso/numImagenes)*100)) + "% : " + "|" * int((contadorProgreso/numImagenes)*100))
                        contadorProgreso += 1

        else:
            print("\tERROR : Imagen no encontrada")

elif seleccion == 2:
    print()
    print("\tQue hace el programa : ")
    print("\t\tCoge la forma de una imagen y le aplica el color de otra")

    print()
    print("\tFuncionamiento : ")
    print("\t\tDado el nombre de una imagen, (debera estar en la carpeta input) obligatoriamente .png, selecciona la opcion mas conveniente :")
    print()
    print("\t\t(0) Tomar la forma de la imagen en input")
    print("\t\t\tEsta opcion creara nuevas imagenes para cada elemento de la carpeta input, pero con la forma de la imagen provista")
    print()
    print("\t\t(1) Tomar el color de la imagen en input")
    print("\t\t\tEsta opcion creara nuevas imagenes para cada elemento de la carpeta input, pero con los colores imagen provista")
    print()
    print("\t\tUna vez escogida una opcion, se daran dos nuevas opciones : ")
    print()
    print("\t\t(0) Aplicar a todas las imagenes")
    print("\t\t\tCon esta opcion se transformaran todas las imagenes de la carpeta input")
    print()
    print("\t\t(1) Aplicar a una unica imagen")
    print("\t\t\tEn este caso se te pedira la imagen la cual sufrira la transformacion, ya sea de color o forma")
    print()
    print("\t\tLos resultados quedaran guardados en la carpeta output. Ten cuidado, porque si lo ejecutas varias veces puedes sobrescribir")
    print("\t\talguna imagen si no la cambias de carpeta")

elif seleccion == 3:
    print("\tAdios")

else:
    print("\tERROR : Opcion no valida")

print("\n\tFin del proceso")
