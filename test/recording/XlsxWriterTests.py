import unittest

from recording import XlsxWriter


class XlsxWriterTest(unittest.TestCase):
    """ Tests to make sure that json objects can safely be converted to xlsx files """

    def test_jsonToXlsx(self):
        jsonData = {"NUM_AGENTS": 10,
                    "NUM_SITES": 5,
                    "FILE_NAME": "OtherSomething.txt",
                    "PRED_POSITIONS": [[5, 10], [15, 20]]}
        workbookName = "TestWorkbook"
        sheetName = "TestSheet1"
        XlsxWriter.jsonToXlsx(jsonData, workbookName, sheetName, "ffbe8c", "ffead9", "ffdbbf", False)
        self.assertEqual(1, 1)

    def test_writeSummary(self):
        jsonData = {"NUM_ROUNDS": [1021],
                    "SIM_TIMES": [37.99213457107544],
                    "CHOSEN_HOME_QUALITIES": [250],
                    "CHOSEN_HOME_POSITIONS": [[1300, 700]],
                    "NUM_ARRIVALS": [79],
                    "NUM_DEAD_AGENTS": [9],
                    "TOTAL_AGENTS": [100]}
        workbookName = "TestWorkbook"
        sheetName = "TestSheet2"
        XlsxWriter.jsonToXlsx(jsonData, workbookName, sheetName, "ffbe8c", "ffead9", "ffdbbf")
        ignore = ["SIM_END_TIME", "CHOSEN_HOME_POSITIONS"]
        XlsxWriter.writeSummary(jsonData, workbookName, "Summary", sheetName, ignore, "ffbe8c", "ffead9", "ffdbbf")
        self.assertEqual(1, 1)

    def test_createScatterPlot(self):
        self.test_writeSummary()
        workbookName = "TestWorkbook"
        sheetName = "TestSheet2"
        columnNameX = "Num Rounds"
        columnNameY = "Num Arrivals"
        columnNameRow = 2

        XlsxWriter.createScatterPlot(workbookName, sheetName, columnNameX, columnNameY, columnNameRow, 2)

        workbookName = "TestWorkbook"
        sheetName = "TestSheet2"
        columnNameX = "Num Rounds"
        columnNameY = "Num Dead Agents"
        columnNameRow = 2
        XlsxWriter.createScatterPlot(workbookName, sheetName, columnNameX, columnNameY, columnNameRow, 3)
