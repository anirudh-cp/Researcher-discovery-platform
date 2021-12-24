import xlwt as wb


def write_line(self, line_index, line):
    for index, term in enumerate(line):
        self.write(line_index, index, term)


wb.Worksheet.write_line = write_line


class WorkBook(wb.Workbook):

    def __init__(self, encoding):
        super().__init__(encoding)
        self.sheet = {}

    def add_sheet(self, name, header=None):
        table = wb.Workbook.add_sheet(self, name)
        for index, term in enumerate(header):
            table.write(0, index, term)
        self.sheet[name] = table
