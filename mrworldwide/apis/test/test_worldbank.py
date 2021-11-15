import unittest
from django.test import TestCase
from apis import worldbank as wb

class WorldBankTest(TestCase):

    # Test consistente en comprobar que los temas se sacan correctamente
    def test_get_topics(self):
        self.alltopics = wb.get_topics_list()
        self.assertEquals(self.alltopics.loc['4'].topicName, "Education")
        self.assertEquals(self.alltopics.loc['11'].topicName, "Poverty")

    # Test consistente en sacar un identificador de la API, para luego poder
    # hacer consultas en base a ese indicador
    def test_get_indicator(self):
        education_indicators = wb.get_indicators_from_topic("4")
        self.illiteracy_ind = education_indicators.loc["UIS.LP.AG15T99"]
        self.assertEquals(self.illiteracy_ind.indicatorName,
                          'Adult illiterate population, 15+ years, both sexes (number)')

    # Test consistente en sacar el dato concreto de un país en un año concreto,
    # de un indicador concreto. Usamos un dato antiguo porque suponemos que no va a cambiar
    def test_get_value(self):
        spain_illiteracy = wb.get_indicator("esp", "UIS.LP.AG15T99")
        self.assertEquals(spain_illiteracy.value.loc['2008'].values[0], 931368)

    # Test para probar la funcion que dado un codigo da la descripcion detallada de un indicador
    def test_get_def(self):
        realdef = wb.get_indicator_definition("UIS.LP.AG15T99")
        expecteddef = "Total number of adults over age 15 who cannot both read and write with understanding a short simple statement on their everyday life."
        self.assertEquals(realdef, expecteddef)

    def test_get_ind_name(self):
        self.assertEquals(wb.get_indicator_name("SP.URB.TOTL"), "Urban population")

    def test_get_ind_code(self):
        self.assertEquals(wb.get_indicator_code("Rural population"), "SP.RUR.TOTL")
