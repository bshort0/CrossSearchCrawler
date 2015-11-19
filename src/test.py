import unittest
import main

class maintests(unittest.TestCase):

	def setUp(self):
		# Real header names example taken from an IEEE CSV file
		self.headerNames = ["Document Title","Authors","Author Affiliations","Publication Title","Date Added To Xplore","Year","Volume","Issue","Start Page","End Page","Abstract","ISSN","ISBN","EISBN","DOI","PDF Link","Author Keywords","IEEE Terms","INSPEC Controlled Terms","INSPEC Non-Controlled Terms","MeSH Terms","Article Citation Count","Patent Citation Count","Reference Count","Copyright Year","Online Date","Issue Date","Meeting Date","Publisher","Document Identifier"]
		

	def test_smoke(self):
		self.assertTrue(True)


	"""
	Tests both functions main.validateCSVLine and main.parseCSVLine.

	Occasionally, when there are multiple commas within an entry or 
	there were originally quotation marks within an entry, the way 
	that the IEEE export citations module works inserts quotation marks 
	into entries in a way that messes with a normal CSV parser.

	To solve this problem, main.validateCSVLine was implemented to 
	remove any inner quoation marks in entries. By removing these
	quotation marks, a normal CSV parser is able to effectively parse 
	the lines of CSV data.

	This test ensures that this functionality is in correct working order.
	"""
	def test_validateCSVLine1(self):
		# Actual row taken from an IEEE CSV file
		# This particular line has a special case with quotation mark usage
		row = '"Auditing cloud computing migration","Mateescu, G.; Vladescu, M.; Sgarciu, V.","Dept. of Autom. & Comput. Sci., Univ. "Polyteh." of Bucharest, Bucharest, Romania","Applied Computational Intelligence and Informatics (SACI), 2014 IEEE 9th International Symposium on","20140619","2014","","","263","268","This paper presents a tool used to audit the cloud adoption within a company. The first section states the main advantages of the cloud computing environment together with its biggest challenges that can introduce significant risks within a company. In order to assess properly the cloud computing adoption, we developed a web based tool that assists the internal auditor in the pre-migration process. Section II describes in details the Migration Assessment Tool (MAT). Starting with its architecture, we presented the main objects manipulated by our application in order to implement a cloud adoption assessment. In order to compute the impact, we classified the questions in different domains and we defined the dependencies between the questions. At the end of section II, we presented the process implemented in MAT when assessing a cloud migration. The paper ends with conclusions that state the main benefits of our approach and future improvements for MAT.","","","","10.1109/SACI.2014.6840073","http://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=6840073","","Best practices;Cloud computing;Companies;Computational modeling;Computer architecture","auditing;business data processing;cloud computing","MAT;Web based tool;cloud adoption assessment;cloud computing migration auditing;company;internal auditor;migration assessment tool;premigration process","","0","","8","","","15-17 May 2014","","IEEE","IEEE Conference Publications"'
		newRow = main.validateCSVLine(row)

		# Parse the validated row
		entry = main.parseCSVLine(newRow, self.headerNames)

		# Assert that values were placed where they should be
		self.assertTrue(entry['Year'] == '2014')
		self.assertTrue(entry['Document Title'] == "Auditing cloud computing migration")
		self.assertTrue(entry['Authors'] == "Mateescu, G.; Vladescu, M.; Sgarciu, V.")
		self.assertTrue(entry['DOI'] == "10.1109/SACI.2014.6840073")


	"""
	This test is doing the same thing as test_validateCSVLine1.
	The only difference is the string value being used for the row.
	The one used here represents a different special case that must 
	be handled by the CSV validator.
	"""
	def test_validateCSVLine2(self):
		# Actual row taken from an IEEE CSV file
		# This particular line has a special case with quotation mark usage
		row = '"A self-routing protocol for distributed consensus on logical information","Fagiolini, A.; Martini, S.; Di Baccio, D.; Bicchi, A.","Interdept. Res. Center "Enrico Piaggio", Univ. of Pisa, Pisa, Italy","Intelligent Robots and Systems (IROS), 2010 IEEE/RSJ International Conference on","20101203","2010","","","5151","5156","In this paper, we address decision making problems, depending on a set of input events, with networks of dynamic agents that have partial visibility of such events. Previous work by the authors proposed so-called logical consensus approach, by which a network of agents, that can exchange binary values representing their local estimates of the events, is able to reach a unique and consistent decision. The approach therein proposed is based on the construction of an iterative map, whose computation is centralized and guaranteed under suitable conditions on the input visibility and graph connectivity. Under the same conditions, we extend the approach in this work by allowing the construction of a logical linear consensus system that is globally stable in a fully distributed way. The effectiveness of the proposed method is showed through the real implementation of a wireless sensor network as a framework for the surveillance of an urban area.","2153-0858","978-1-4244-6674-0","","10.1109/IROS.2010.5650096","http://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=5650096","","","decision making;graph theory;multi-agent systems;multi-robot systems;routing protocols;surveillance;wireless sensor networks","decision making problem;dynamic agents network;iterative map;logical consensus approach;logical linear consensus system;self-routing protocol;wireless sensor network","","0","","20","","","18-22 Oct. 2010","","IEEE","IEEE Conference Publications"'
		newRow = main.validateCSVLine(row)

		# Print statements for comparing the difference between the non-validated and validated CSV rows
		# print("Row1: " + row)
		# print("Row2: " + newRow)

		entry = main.parseCSVLine(newRow, self.headerNames)

		self.assertTrue(entry['Year'] == '2010')
		self.assertTrue(entry['Document Title'] == "A self-routing protocol for distributed consensus on logical information")
		self.assertTrue(entry['Authors'] == "Fagiolini, A.; Martini, S.; Di Baccio, D.; Bicchi, A.")
		self.assertTrue(entry['DOI'] == "10.1109/IROS.2010.5650096")
