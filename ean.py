#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Universidad EAN (Bogotá - Colombia)
# Departamento de Sistemas
# Faculta de Ingeniería
#
# Proyecto EAN Python Collections
# @author Luis Cobo (lacobo@universidadean.edu.co)
# Fecha: Mar 09 2026
# Versión: 0.0.1 -> 16 de febrero de 2026 -> Implementación inicial
# Versión: 0.0.2 -> 09 de marzo de 2026 -> Implementación de nodos
# Versión: 0.0.3 -> 14 de marzo de 2026 -> Implementación de pilas
# Versión: 0.0.5 -> 20 de abril de 2026 -> Árboles Binarios
# Versión: 0.0.6 -> 28 de abril de 2026 -> Clase Carro
# Versión: 0.0.7 -> 29 de abril de 2026 -> Operaciones comparadoras
# Versión: 0.0.9 -? 24 de mayo de 2026 -> La clase Vector
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import math
from datetime import datetime
from math import sqrt, pi
from dataclasses import dataclass

# Definición de elementos genéricos que usaremos a continuación
from typing import TypeVar, Generic, Callable


# La clase Nulo: representa un nodo nulo
class Nulo:
    def __init__(self):
        pass

    def __str__(self):
        return "nulo"

    def __repr__(self):
        return "Nulo()"

    def __getattr__(self, nombre: str):
        raise AttributeError(f"El atributo {nombre} no existe en el nodo nulo")

    def __eq__(self, otro: object) -> bool:
        if otro is None:
            raise ValueError("El valor nulo no puede ser comparado con None")
        return isinstance(otro, Nulo)

    def __ne__(self, otro: object) -> bool:
        if otro is None:
            raise ValueError("El valor nulo no puede ser comparado con None")
        return not self.__eq__(otro)

    @property
    def es_nulo(self) -> bool:
        return True

    @property
    def no_es_nulo(self) -> bool:
        return False

# ----------------------------------------

# Variable global que representa el valor nulo.
nulo = Nulo()

# ------------------------------------------------------------

T = TypeVar('T')

# Los nodos son objetos que permiten almacenar información
# Cada nodo contiene un atributo llamado "información"
# y otro llamado "sig".
class Nodito(Generic[T]):
    def __init__(self, informacion : T):
        self.__informacion = informacion
        self.__siguiente  = nulo
        if informacion is None or informacion == nulo:
            raise ValueError("El valor nulo no puede ser almacenado en un nodo")

    @property
    def es_nulo(self) -> bool:
        return False

    @property
    def no_es_nulo(self) -> bool:
        return True

    @property
    def info(self) -> T:
        return self.__informacion

    @info.setter
    def info(self, valor: T):
        if valor is None or valor == nulo:
            raise ValueError("El valor nulo no puede ser almacenado en un nodo")
        self.__informacion = valor

    @property
    def sig(self) -> 'Nodito | Nulo':
        return self.__siguiente

    @sig.setter
    def sig(self, sig: 'Nodito | Nulo'):
        if sig is None:
            raise ValueError("En este curso nunca usamos None con Noditos. Revise la presentación")
        self.__siguiente = sig

    def __getattr__(self, attr : str):
        raise AttributeError(f"El atributo {attr} no existen en los noditos.\nEn este curso un nodito solo tiene informacion y sig.")

    def __eq__(self, otro: object) -> bool:
        if otro is None:
            raise ValueError("Un nodito no puede ser comparado con None. Uso nulo en su lugar")
        return isinstance(otro, Nodito) and self.informacion == otro.informacion

    def __ne__(self, otro: object) -> bool:
        if otro is None:
            raise ValueError("Un nodito no puede ser comparado con None. Use nulo en su lugar")
        return not self.__eq__(otro)

    def __setattr__(self, attr : str, valor: object):
        if attr == "data" or attr == "value" or attr == "next" or attr == "siguiente" or attr == "valor" or attr == "informacion" or attr == "dato":
            raise AttributeError(f"El atributo {attr} no existe en los noditos.\nEn este curso un nodito solo tiene informacion y sig.")
        super().__setattr__(attr, valor)

    def __str__(self):
        return f"{str(self.informacion)} -> {str(self.sig)}"


# ---------------------------------------------------------------------

# ----------------------------------------------------------------------------------------
# Un pair es una pareja de valores en Python
# ----------------------------------------------------------------------------------------
@dataclass
class Pair[P, T]:
    first : P
    second : T

    def __getitem__(self, key: int) -> P | T:
        if key == 0:
            return self.first
        elif key == 1:
            return self.second
        else:
            raise IndexError(f"El índice {key} no existe en el pair")

    def __setitem__(self, key: int, value: P | T) -> None:
        if key == 0:
            self.first = value
        elif key == 1:
            self.second = value
        else:
            raise IndexError(f"El índice {key} no existe en el pair")

    def __len__(self) -> int:
        return 2

    def __repr__(self) -> str:
        return f"Pair({self.first}, {self.second})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Pair):
            return self.first == other.first and self.second == other.second
        return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __contains__(self, item: P | T) -> bool:
        return item in (self.first, self.second)

    def __hash__(self) -> int:
        return hash((self.first, self.second))

    def __getattr__(self, name: str) -> P | T:
        if name == "primero" or name == "suma" or name == "tamaño":
            return self.first
        elif name == "segundo" or name == "contador":
            return self.second
        else:
            raise AttributeError(f"El atributo {name} no existe en el pair")

    def __setattr__(self, name: str, value: P | T) -> None:
        if name == "first" or name == "primero" or name == "suma" or name == "tamaño":
            super().__setattr__("first", value)
        elif name == "second" or name == "segundo" or name == "contador":
            super().__setattr__("second", value)
        else:
            raise AttributeError(f"El atributo {name} no existe en el pair")

    def __add__(self, other: "Pair[P, T]") -> "Pair[P, T]":
        return Pair(self.first + other.first, self.second + other.second)

# ----------------------------------------------------------------------------------------
# Un vector es una estructura de datos lineal, parecida a un arreglo, pero con
# la capacidad de eliminar y agregar en posiciones específicas de la estructura
# de datos
# ----------------------------------------------------------------------------------------
# ------- Iterador del vector ----------------
class Vec2Iterator[T]:
    """
    Clase iterador que permite iterar, o sea, tener un acceso secuencial sobre un vector
    """

    def __init__(self, vector_head: Nodito[T] | Nulo):
        self.__current = vector_head
        self.__vector_head = vector_head

    def go_to_first(self) -> None:
        """
        Coloca el iterador en el primer elemento del vector
        :return:
        """
        self.__current = self.__vector_head

    def go_to_last(self) -> None:
        """
        Coloca el iterador en el último elemento del vector
        :return:
        """
        self.__current = self.__vector_head
        while self.__current.sig is not nulo:
            self.__current = self.__current.sig

    def go_to_next(self) -> None:
        """
        Avanza el iterador al siguiente elemento
        :return:
        """
        if self.__current is not nulo:
            self.__current = self.__current.sig

    @property
    def current(self) -> "T | Nulo":
        if self.__current is not nulo:
            return self.__current.info
        raise "El nodo actual no existe"

    @current.setter
    def current(self, value: "T | Nulo") -> None:
        if self.__current is not nulo:
            self.__current.info = value
        else:
            raise "El nodo actual no existe"

    def at_the_end(self) -> bool:
        """
        Permite saber si ya estamos al final del vector
        :return: true si ya estamos al final del vector, false en caso contrario
        """
        return self.__current is nulo

# --------------------------------------------------------------------

def menor_que[T](elemento1: T, elemento2: T, attribute: str | Nulo = nulo) -> bool:
    if attribute is nulo:
        return elemento1 < elemento2
    else:
        if attribute.endswith(")"):
            nomatrib = attribute.split("(")[0].strip()
        else:
            nomatrib = attribute
        if not hasattr(elemento1, nomatrib):
            raise AttributeError(f"El objeto no tiene el atributo {nomatrib}")
        if not hasattr(elemento2, nomatrib):
            raise AttributeError(f"El objeto no tiene el atributo {nomatrib}")
        if attribute.endswith(")"):
            valor1 = getattr(elemento1, nomatrib)()
            valor2 = getattr(elemento2, nomatrib)()
        else:
            valor1 = getattr(elemento1, nomatrib)
            valor2 = getattr(elemento2, nomatrib)
        if valor1 < valor2:
            return True
        else:
            return False

# --------------------------------------------------------------------
class Vec2[T]:
    """
    Clase Vector que permite manipular y gestionar un grupo de objetos.
    Un vector es una secuencia de cero o más elementos de un mismo tipo.
    """

    # Constructor
    def __init__(self):
        """
        Constructor de la clase. Crea un vector vacío
        """
        self.__head = nulo
        self.__size = 0

    # Métodos
    def size(self) -> int:
        """
        Retona el número de elementos que hacen parte del vector
        :return: el tamaño del vector
        """
        return self.__size

    def is_empty(self) -> bool:
        """
        Retorna `true` si la lista está vacía (no contiene elementos), `false` si tiene al menos un elemento
        """
        return self.__size == 0

    def clear(self) -> None:
        """
        Elimina todos los elementos de esta lista
        :return:
        """
        self.__head = nulo
        self.__size = 0

    def delete_first(self) -> None:
        """
        Elimina el primer elemento de la lista!
        :return:
        """
        if self.is_empty():
            raise "El vector está vacío. No hay elementos para eliminar"
        self.__head = self.__head.sig
        self.__size -= 1

    def delete_last(self) -> None:
        """
        Elimina el último elemento de la lista!
        :return:
        """
        if self.is_empty():
            raise "El vector está vacío. No hay elementos para eliminar"
        aux = self.__head
        while aux.sig.sig is not nulo:
            aux = aux.sig
        aux.sig = nulo
        self.__size -= 1

    def delete_at(self, index: int) -> None:
        """
        Elimina el elemento que se encuentra en la posición index
        :param index: la posición a eliminar
        :return: Nada
        """
        real_index = index if index >= 0 else self.__size + index
        if real_index not in range(self.__size):
            raise "Posición fuera de rango"
        aux = self.__head
        if real_index == 0:
            self.__head = self.__head.sig
        else:
            for i in range(real_index - 1):
                aux = aux.sig
            aux.sig = aux.sig.sig
        self.__size -= 1

    def add_first(self, element: T) -> None:
        """
        Agrega un elemento al principio del vector
        :param element: el elemento a agregar
        :return: Nada
        """
        nodo = Nodito(element)
        nodo.sig = self.__head
        self.__head = nodo
        self.__size += 1

    def add_last(self, element: T) -> None:
        """
        Agrega un elemento al final del vector
        :param element: el elemento a agregar
        :return: Nada
        """
        if self.is_empty():
            self.add_first(element)
        else:
            aux = self.__head
            while aux.sig is not nulo:
                aux = aux.sig
            aux.sig = Nodito(element)
            self.__size += 1

    def add(self, element: T, index: int) -> None:
        """"
        Agrega un elemento en la posicion index del vector
        """
        real_index = index if index >= 0 else self.__size + index
        if real_index not in range(self.__size + 1):
            raise "Posicion fuera de rango"
        if real_index == 0:
            self.add_first(element)
        else:
            aux = self.__head
            for i in range(real_index - 1):
                aux = aux.sig
            nodito = Nodito(element)
            nodito.sig = aux.sig
            aux.sig = nodito
            self.__size += 1

    def __str__(self) -> str:
        """
        Permite obtener una representación como String de la lista
        :return: la lista guardada como un string
        """
        resultado = 'Vec2['
        n = 1
        act = self.__head
        while act is not nulo:
            elemento = act.info
            resultado += str(elemento)
            if n < self.size():
                resultado += ', '
            n += 1
            act = act.sig
        resultado += ']'
        return resultado

    def get_iterator(self, index: int = 0) -> "Vec2Iterator[T]":
        act = self.__head
        i = 0
        while i < index:
            act = act.sig
            i += 1
        return Vec2Iterator(act)

    def index_of(self, element: T) -> int | Nulo:
        """
        Obtiene el índice del primer elemento que coincide con el elemento dado
        :param element: el elemento a buscar
        :return: el índice del primer elemento que coincide con el elemento dado, o nulo si no se encuentra
        """
        nodo = self.__head
        i = 0
        while nodo is not nulo:
            if nodo.info == element:
                return i
            nodo = nodo.sig
            i += 1
        return nulo

    def __contains__(self, element: T) -> bool:
        """
        Permite saber si el elemento está dentro del vector
        :param element: el elemento a buscar
        :return: true si el elemento pertenece al vector, false en caso contrario
        """
        return self.index_of(element) is not nulo


    def slice(self, start: int, end: int) -> "Vec2[T]":
        """"
        Permite obtener un nuevo vector con los elementos ubicados entre start y end
        """
        result = Vec2[T]()
        act = self.__head
        i = 0
        while i < start:
            act = act.sig
            i += 1
        while i < end:
            result.add_last(act.info)
            act = act.sig
            i += 1
        return result

    def __eq__(self, otra_lista) -> bool:
        """
        Permite saber si dos vectores son iguales
        :param otra_lista:  el vector con el que nos comparamos
        :return: True si son iguales, False si no
        """
        if isinstance(otra_lista, Vec2):
            if self.size() != otra_lista.size():
                return False
            act1 = self.__head
            act2 = otra_lista.__head
            while act1 is not nulo:
                if act1.info != act2.info:
                    return False
                act1 = act1.sig
                act2 = act2.sig
            return True
        else:
            return False

    def bsort(self, attribute: str | Nulo = nulo, asc: bool = True) -> None:
        """
        Este método ordena un vector de acuerdo a lo que indique el parámetro
        :param: attribute: el atributo que se va a ordenar, si no se indica, se ordena por el valor por defecto
        NOTA: agregar el parámetro asc para saber si se ordena ascendentemente o descendentemente
        """

        for _ in range(self.size() - 1):
            p = self.__head
            q = p.sig

            while q is not nulo:
                if not asc and menor_que(p.info, q.info, attribute):
                    aux = q.info
                    q.info = p.info
                    p.info = aux
                elif asc and menor_que(q.info, p.info, attribute):
                    aux = q.info
                    q.info = p.info
                    p.info = aux
                p = p.sig
                q = q.sig


    def select(self, attribute: str) -> "Vec2":
        """
        Permite obtener un nuevo vector con los elementos seleccionados
        :param attribute: los atributos que se van a seleccionar
        :return: un vector con los elementos seleccionados
        """
        result = Vec2()
        act = self.__head
        while act is not nulo:
            element = act.info
            if attribute.endswith(")"):
                nomatrib = attribute.split("(")[0].strip()
            else:
                nomatrib = attribute
            if not hasattr(element, nomatrib):
                raise AttributeError(f"El elemento {element} no tiene el atributo {nomatrib}")
            if attribute.endswith(")"):
                valor_atributo = getattr(element, nomatrib)()
            else:
                valor_atributo = getattr(element, nomatrib)
            result.add_last(valor_atributo)
            act = act.sig

        return result

    def where(self, predicate: Callable[..., bool]) -> 'Vec2[T]':
        """
        Obtiene un vector con los elementos del vector que cumplen con el predicado
        :param predicate: una función que devuelve True si el elemento cumple con el predicado
        :return: el vector de los elementos que cumplen con el predicado
        """
        resultado = Vec2[T]()
        act = self.__head
        while act.no_es_nulo:
            elem = act.info
            if predicate(elem):
                resultado.add_last(elem)
            act = act.sig
        return resultado

    def sum(self) -> int | float:
        """
        Halla la suma de todos los elementos del vector
        :return: la suma de los elementos del vector
        """
        if self.size() == 0:
            return 0.0
        sumax = 0.0
        act = self.__head
        while act is not nulo:
            dato = act.info
            if type(dato) == int or type(dato) == float:
                sumax += dato
            else:
                raise "Solo podemos trabajar con valores numéricos"
            act = act.sig
        return sumax

    def average(self) -> float:
        """
        Halla el promedio de los elementos del vector de números
        :return: el promedio de los elementos del vector. Retorna cero
                 si el tamaño del vector es cero.
        """
        if self.size() == 0:
            return 0.0

        sumax = 0.0
        act = self.__head
        while act is not nulo:
            dato = act.info
            act = act.sig
            if type(dato) == int or type(dato) == float:
                sumax += dato
            else:
                raise "Solo podemos trabajar con valores numéricos"
        return sumax / self.size()

    def count(self) -> int:
        """
        Retorna el tamaño del vector
        :return: la cantidad de elementos del vector
        """
        return self.__size

    @property
    def first(self) -> T | Nulo:
        """
        Obtiene el primer elemento del vector
        :return: el primer elemento del vector o nulo si el vector está vacío
        """
        if self.is_empty():
            return nulo
        return self.__head.info

    @property
    def last(self) -> T | Nulo:
        """
        Permite obtener el último elemento del vector
        """
        if self.is_empty():
            return nulo
        aux = self.__head
        while aux.sig is not nulo:
            aux = aux.sig
        return aux.info


    def highest(self, atributte: str | Nulo = nulo) -> T | Nulo:
        """
        Otiene el meyo elemento del vector
        :param atributte: el selector de atributo que se va a usar para ordenar el vector
        :return: el elemento del vector con el mejor valor del atributo
        """
        if self.size() == 0:
            return nulo
        mayor = self.__head.info
        act = self.__head.sig
        while act is not nulo:
            if menor_que(mayor, act.info, atributte):
                mayor = act.info
            act = act.sig
        return mayor

    def lowest(self, atributte: str | Nulo = nulo) -> T | Nulo:
        """
        Otiene el menor elemento del vector
        :param atributte: el selector de atributo que se va a usar para ordenar el vector
        :return: el elemento del vector con el menor valor del atributo
        """
        if self.size() == 0:
            return nulo
        menor = self.__head.info
        act = self.__head.sig
        while act is not nulo:
            if menor_que(act.info, menor, atributte):
                menor = act.info
            act = act.sig
        return menor

    def __call__(self, index: int) -> T | Nulo:
        """
        Permite obtener el objeto almacenado en la posición con el índice dado
        :param index: la posición del objeto que se va a obtener
        :return: el objeto que se encuentra en la posición dada del vector o
                 nulo si la posición no existe
        """
        n = self.size()
        if not (-n <= index < n):
            return nulo
        real_index = index if index >= 0 else n + index
        act = self.__head
        i = 0
        while i < real_index:
            act = act.sig
            i += 1
        return act.info

#-------------- End of class Vec2  -----------------------

def copy_vector[T](vec: Vec2[T]) -> Vec2[T]:
    """
    Crea una copia de un vector
    :param vec: el vector a copiar
    :return: la copia del vector
    """
    result = Vec2[T]()
    iterador = vec.get_iterator()
    while not iterador.at_the_end():
        result.add_last(iterador.current)
        iterador.go_to_next()
    return result

def vec2[T](*elements: T) -> Vec2[T]:
    """
    Crea un vector con los diversos elementos recibidos como parámetros
    :param elements: los elementos que se van a agregar al vector
    :return: el vector creado
    """
    result = Vec2[T]()
    for element in elements:
        result.add_last(element)
    return result





# ------------------------------------------------------------------------------

# ---------------------------------------------------------------------
import pandas as pd
from dataclasses import dataclass

@dataclass(frozen=True)
class Persona:
    """
    Clase que representa una persona
    """

    # Atributos de la clase Persona
    cedula: int
    nombre: str
    edad: int
    es_hombre: bool
    es_mujer: bool
    num_hijos: int
    llego_a_primaria: bool
    llego_a_secundaria: bool
    llego_a_universidad: bool
    llego_a_postgrado: bool
    estrato: int
    ingresos: int
    peso: int
    altura: int
    fuma: bool
    usa_lentes: bool
    tiene_casa: bool
    tiene_carro: bool

    # Métodos de la clase persona
    def año_nacimiento(self) -> int:
        return datetime.now().year - self.edad

    def peso_ideal(self) -> float:
        return (self.altura - 100) * 0.9

    def imc(self) -> float:
        return self.peso / (self.altura / 100) ** 2

def vector_personas() -> Vec2[Persona]:
    """
    Permite crear un vector con las personas que están
    en el archivo
    :return: el vector con las personas
    """
    archivo = "https://github.com/luiscobo/poo/raw/refs/heads/main/people.csv"
    df = pd.read_csv(archivo, sep=";", encoding="utf-8")

    vector = Vec2[Persona]()

    for index, row in df.iterrows():
        cedula = int(row["Cedula"])
        nombre = str(row["Nombres"]).upper()
        edad = int(row["Edad"])
        es_hombre = str(row["Genero"]) == "HOMBRE"
        es_mujer = str(row["Genero"]) == "MUJER"
        num_hijos = int(row["No de hijos"])
        nivel_educativo = str(row["Nivel Educativo"])
        llego_a_primaria = nivel_educativo == "PRIMARIA"
        llego_a_secundaria = nivel_educativo == "SECUNDARIA"
        llego_a_universidad = nivel_educativo == "PREGRADO"
        llego_a_postgrado = nivel_educativo == "POSTGRADO"
        estrato = int(row["Estrato Socio"])
        ingresos = int(row["Ingresos"])
        peso = int(row["Peso"])
        altura = int(row["Talla"])
        fuma = str(row["Fuma"]) == "SI"
        usa_lentes = str(row["Usa Lentes"]) == "SI"
        tiene_casa = str(row["Tiene Casa"]) == "SI"
        tiene_carro = str(row["Tiene Automovil"]) == "SI"
        p = Persona(cedula, nombre, edad, es_hombre, es_mujer, num_hijos, llego_a_primaria, llego_a_secundaria, llego_a_universidad, llego_a_postgrado, estrato, ingresos, peso, altura, fuma, usa_lentes, tiene_casa, tiene_carro)
        vector.add_last(p)

    return vector

# ----------------------------------------------------------------------------------------------------------
from inspect import Signature, Parameter, isclass

def verificar_params_funcion(encab_func : Signature, prim_param: str, tipo_vec: tuple[str], tipo_retorno: str | None = None) -> bool:
    params = encab_func.parameters
    if prim_param not in params:
        print(f"El primer parámetro no está bien escrito. Debe llamarse '{prim_param}'")
        return False
    else:
        param_tipo = params[prim_param].annotation
        if param_tipo == Parameter.empty:
            print(f"El primer parámetro debe tener tipo. En este caso debe comenzar por 'Vec2{'' if len(tipo_vec) == 0 else '_de_' + tipo_vec[0]}'")
            return False
        elif len(tipo_vec) == 0:
            if param_tipo == "Vec2":
                return True
            print(f"El primer parámetro no está bien escrito. Debe tener como tipo solo 'Vec2'")
            return False
        elif not param_tipo.startswith("Vec2_de_"):
            print(f"El primer parámetro no está bien escrito. Debe tener como tipo 'Vec2_de_{tipo_vec[0]}'")
            return False
        for tipo in tipo_vec:
            if tipo == "int":
                opciones_tipo = (tipo, "Numeros", "Enteros", "Reales")
            elif tipo == "str":
                opciones_tipo = (tipo, "Cadenas", "Texto", "Palabras", "Letras")
            elif tipo == "bool":
                opciones_tipo = (tipo, "Booleanos", "Logicos")
            elif tipo == "float":
                opciones_tipo = (tipo, "Reales", "Decimales")
            else:
                opciones_tipo = (tipo, tipo + "s", tipo + "es")
            if param_tipo.endswith(opciones_tipo):
                # Verificamos el dato de salida
                dato_salida = encab_func.return_annotation

                if tipo_retorno is None and dato_salida == Signature.empty:
                    return True
                else:
                    if hasattr(dato_salida, "__name__"):
                        dato_salida_nom = dato_salida.__name__
                    else:
                        dato_salida_nom = str(dato_salida)
                    if tipo_retorno is not None and dato_salida != Signature.empty and dato_salida_nom == tipo_retorno:
                        return True
                    else:
                        print(f"El dato de salida no es el correcto. Debe ser de tipo '{tipo_retorno}'")
                        return False
        print(f"El primer parámetro no está bien escrito. Debe tener como tipo 'Arbol_de_{tipo_vec[0]}'")
        return False

if __name__ == '__main__':
    v = vector_personas()
    per = v.slice(0, 10).worst("imc()")
    if per is nulo:
        print("No hay")
    else:
        print(per.nombre)

