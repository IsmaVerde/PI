import unittest
from django.test import TestCase
from apis import aqicn

class AQICNTest(TestCase):
    # Test consistente en leer los datos de la ciudad de Bilbao. Como
    # no sabemos de antemano cuales van a ser los datos, solo podemos
    # comprobar que no son nulos, que son del tipo correcto, y que tienen
    # sentido (i.e. no son negativos, NaN...)
    def test_bilbao(self):
        aire = aqicn.get_datos_ciudad("Bilbao")
        self.assertEquals(type(aire.loc['Bilbao'].no2), float)
        self.assertTrue(aire.loc['Bilbao'].o3 > 0)


    # Igual que el anterior pero pidiendo por coordenadas en vez de por
    # nombre de la ciudad. Las comprobaciones son similares
    def test_coords(self):
        aire = aqicn.get_datos_coords(lat=42, lon=-8)
        self.assertEquals(type(aire.iloc[0].p), float)
        self.assertTrue(aire.iloc[0].co > 0)
