import sys
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import ui.main as main_window
import sqlite3
import resources.res_1

x = 0
idx = 2


class MainWindow(QMainWindow, main_window.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setupUi(self)

        # Stretch table 2 to fill the space
        self.table_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_2.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # connect buttons
        self.handle_buttons()

    def handle_buttons(self):
        self.refresh_button.clicked.connect(self.get_data)
        self.search_button.clicked.connect(self.search)
        self.check_button.clicked.connect(self.level)
        self.update_button.clicked.connect(self.update_entry)
        self.delete_button.clicked.connect(self.delete_entry)
        self.add_button.clicked.connect(self.add_entry)
        self.next_button.clicked.connect(self.next_entry)
        self.previous_button.clicked.connect(self.previous_entry)
        self.last_button.clicked.connect(self.last_entry)
        self.first_button.clicked.connect(self.first_entry)

    def get_data(self):
        # Connect to Sqlite3 database and fill GUI table with data.
        db = sqlite3.connect("data_base/parts.db")
        cursor = db.cursor()

        command = ''' SELECT * from parts_table '''

        result = cursor.execute(command)

        self.table.setRowCount(0)

        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)

            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        # Display references number and type number in Statistics Tab

        cursor2 = db.cursor()
        cursor3 = db.cursor()

        parts_nbr = ''' SELECT COUNT (DISTINCT PartName) from parts_table '''
        ref_nbr = ''' SELECT COUNT (DISTINCT Reference) from parts_table '''

        result_ref_nbr = cursor2.execute(ref_nbr)
        result_parts_nbr = cursor3.execute(parts_nbr)

        self.label_ref_number.setText(str(result_ref_nbr.fetchone()[0]))
        self.label_part_number.setText(str(result_parts_nbr.fetchone()[0]))

        # Display 4 results: Min, Max Nbr holes in addition to their respective reference names

        cursor4 = db.cursor()
        cursor5 = db.cursor()

        min_holes = ''' SELECT MIN(NumberOfHoles), Reference from parts_table '''
        max_holes = ''' SELECT MAX(NumberOfHoles), Reference from parts_table '''

        result_min_holes = cursor4.execute(min_holes)
        result_max_holes = cursor5.execute(max_holes)

        r1 = result_min_holes.fetchone()
        r2 = result_max_holes.fetchone()

        self.label_min_holes.setText(str(r1[0]))
        self.label_max_holes.setText(str(r2[0]))

        self.label_min_holes_2.setText(str(r1[1]))
        self.label_max_holes_2.setText(str(r2[1]))

        self.first_entry()
        self.navigate()

    def search(self):
        db = sqlite3.connect("data_base/parts.db")
        cursor = db.cursor()

        nbr = int(self.count_filter_txt.text())

        command = ''' SELECT * from parts_table WHERE count<?'''

        result = cursor.execute(command, [nbr])

        self.table.setRowCount(0)

        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)

            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def level(self):
        # Connect to Sqlite3 database and fill GUI table with data.
        db = sqlite3.connect("data_base/parts.db")
        cursor = db.cursor()

        command = ''' SELECT Reference, PartName, Count from parts_table order by Count asc LIMIT 3'''

        result = cursor.execute(command)

        self.table_2.setRowCount(0)

        for row_number, row_data in enumerate(result):
            self.table_2.insertRow(row_number)

            for column_number, data in enumerate(row_data):
                self.table_2.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def navigate(self):
        global idx
        db = sqlite3.connect("data_base/parts.db")
        cursor = db.cursor()

        command = ''' SELECT * from parts_table WHERE ID=?'''

        result = cursor.execute(command, [idx])

        value = result.fetchone()

        self.id_label.setText(str(value[0]))
        self.reference_label.setText(str(value[1]))
        self.part_name_label.setText(str(value[2]))
        self.min_area_label.setText(str(value[3]))
        self.max_area_label.setText(str(value[4]))
        self.hole_number_label.setText(str(value[5]))
        self.min_diameter_label.setText(str(value[6]))
        self.max_diameter_label.setText(str(value[7]))
        self.count_spin_box.setValue(value[8])

    def next_entry(self):
        db = sqlite3.connect("data_base/parts.db")
        cursor = db.cursor()
        command = ''' SELECT ID FROM parts_table'''
        result = cursor.execute(command)
        val = result.fetchall()
        tot = len(val)
        global x
        global idx
        x = x+1
        if x < tot:
            idx = val[x][0]
            self.navigate()
        else:
            x = tot - 1
            print('end of file')

    def previous_entry(self):
        db = sqlite3.connect("data_base/parts.db")
        cursor = db.cursor()
        command = ''' SELECT ID FROM parts_table'''
        result = cursor.execute(command)
        val = result.fetchall()
        tot = len(val)
        global x
        global idx
        x = x - 1
        if x > -1:
            idx = val[x][0]
            self.navigate()
        else:
            x = 0
        print('beginning of file')

    def first_entry(self):
        db = sqlite3.connect("data_base/parts.db")
        cursor = db.cursor()
        command = ''' SELECT ID FROM parts_table'''
        result = cursor.execute(command)
        val = result.fetchall()
        tot = len(val)
        global x
        global idx
        x = 0
        if x > -1:
            idx = val[x][0]
            self.navigate()
        else:
            x = 0
        print('beginning of file')

    def last_entry(self):
        db = sqlite3.connect("data_base/parts.db")
        cursor = db.cursor()
        command = ''' SELECT ID FROM parts_table'''
        result = cursor.execute(command)
        val = result.fetchall()
        tot = len(val)
        global x
        global idx
        x = tot - 1
        if x < tot:
            idx = val[x][0]
            self.navigate()
        else:
            x = tot - 1
        print('end of file')

    def update_entry(self):
        db = sqlite3.connect("data_base/parts.db")
        cursor = db.cursor()

        id_new = int(self.id_label.text())
        reference_new = self.reference_label.text()
        part_name_new = self.part_name_label.text()
        min_area_new = self.min_area_label.text()
        max_area_new = self.max_area_label.text()
        number_of_holes_new = self.hole_number_label.text()
        min_diameter_new = self.min_diameter_label.text()
        max_diameter_new = self.max_diameter_label.text()
        count_new = str(self.count_spin_box.value())

        row = (reference_new,
               part_name_new,
               min_area_new,
               max_area_new,
               number_of_holes_new,
               min_diameter_new,
               max_diameter_new,
               count_new,
               id_new)

        command = ''' UPDATE parts_table SET Reference=?,
                                             PartName=?,
                                             MinArea=?,
                                             MaxArea=?,
                                             NumberOfHoles=?,
                                             MinDiameter=?,
                                             MaxDiameter=?,
                                             Count=?
                                             WHERE ID=?'''

        cursor.execute(command, row)

        db.commit()

    def delete_entry(self):
        db = sqlite3.connect("data_base/parts.db")
        cursor = db.cursor()

        d = self.id_label.text()

        command = ''' DELETE FROM parts_table WHERE ID=? '''

        cursor.execute(command, [d])

        db.commit()

    def add_entry(self):
        db = sqlite3.connect("data_base/parts.db")
        cursor = db.cursor()

        reference_new = self.reference_label.text()
        part_name_new = self.part_name_label.text()
        min_area_new = self.min_area_label.text()
        max_area_new = self.max_area_label.text()
        number_of_holes_new = self.hole_number_label.text()
        min_diameter_new = self.min_diameter_label.text()
        max_diameter_new = self.max_diameter_label.text()
        count_new = str(self.count_spin_box.value())

        row = (reference_new,
               part_name_new,
               min_area_new,
               max_area_new,
               number_of_holes_new,
               min_diameter_new,
               max_diameter_new,
               count_new)

        command = ''' INSERT INTO parts_table (Reference,
                                               PartName,
                                               MinArea,
                                               MaxArea,
                                               NumberOfHoles,
                                               MinDiameter,
                                               MaxDiameter,
                                               Count)
                                               VALUES
                                               (?,?,?,?,?,?,?,?) '''

        cursor.execute(command, row)

        db.commit()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
