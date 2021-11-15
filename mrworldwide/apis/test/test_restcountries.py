import unittest
from django.test import TestCase
from apis import restcountries as rc

class RestCountriesTest(TestCase):

    # Test consistente en hacer una petición a la API, extraer los datos
    # de un país cualquiera (para el caso, Italia y Canada), y comprobar
    # que los resultados son los esperados
    def test_get_info(self):
        allcountries = rc.get_all_countries()
        italy = allcountries.loc['ITA']
        self.assertEquals(italy.countryName, "Italy")
        self.assertEquals(italy.region, "Europe")
        self.assertEquals(italy.alpha2Code, "IT")
        self.assertEquals(italy.capital, "Rome")
        canada = allcountries.loc['CAN']
        self.assertEquals(canada.countryName, "Canada")
        self.assertEquals(canada.region, "Americas")
        self.assertEquals(canada.alpha2Code, "CA")
        self.assertEquals(canada.capital, "Ottawa")

    # Test consistente en intentar extraer información de un país que no existe
    @unittest.expectedFailure
    def test_get_mordor(self):
        allcountries = rc.get_all_countries()
        mordor = allcountries.loc['Mordor']

    # Test consistente en sacar los códigos de algunos países por su nombre
    def test_iso3code(self):
        self.assertEquals(rc.get_iso3code("Spain"), "ESP")
        self.assertEquals(rc.get_iso3code("Portugal"), "PRT")
    
    # Si el pais no existe, el método falla
    @unittest.expectedFailure
    def test_iso3codefail(self):
        self.assertEquals(rc.get_iso3code("Republica Independent de Catalunya", "CAT"))

    # Test consistente en hacer una petición a la API para sacar un país concreto por su nombre
    def test_get_pornombre(self):
        alemania = rc.get_countries_by_name("Germany").iloc[0]
        self.assertEquals(alemania.demonym, "German")
        self.assertEquals(alemania.capital, "Berlin")
        self.assertEquals(alemania.currencies, "Euro")
        self.assertEquals(alemania.callingCodes, "49")

    # Igual que el anterior pero pidiendolo por código
    def test_get_porcodigo(self):
        portugal = rc.get_country_by_code("PRT").iloc[0]
        self.assertEquals(portugal.demonym, "Portuguese")
        self.assertEquals(portugal.capital, "Lisbon")
        self.assertEquals(portugal.currencies, "Euro")
        self.assertEquals(portugal.callingCodes, "351")
