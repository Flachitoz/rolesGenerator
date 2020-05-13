import mysql.connector
from mysql.connector import Error
from utils.utilities import are_fields_present, show_message


class Db:

    def __init__(self):
        self.host = "localhost"
        self.database = "rolesgenerator"
        self.user = "simop"
        self.password = "root"
        self.actors = ["students", "roles"]
        self.months = ["september", "october", "november", "december", "january",
                       "february", "march", "april", "may", "june"]

    def _db_connection(self):
        try:
            connection = mysql.connector.connect(host=self.host, database=self.database,
                                                 user=self.user, password=self.password)
            if connection.is_connected():
                connection.get_server_info()
                cursor = connection.cursor()
                cursor.execute("select database();")
                cursor.fetchone()
                cursor.close()
                return connection
        except Error:
            show_message("Error while connecting to database!")
            return None

    def are_tables_connected(self, tables):
        try:
            connection = self._db_connection()
            if connection is None:
                return False

            cursor = connection.cursor()
            for table in tables:
                cursor.execute("""SELECT COUNT(*) FROM information_schema.tables
                               WHERE table_name = '{}'""".format(table))
                if cursor.fetchone()[0] != 1:
                    return False

            cursor.close()
            connection.close()
            return True
        except Error:
            show_message("Error while connecting to one of the tables in the database!")
            return False

    def drop_tables(self):
        try:
            connection = self._db_connection()
            if connection is None:
                return

            cursor = connection.cursor()
            for table in self.actors + self.months:
                cursor.execute("""DROP TABLE IF EXISTS {}""".format(table))

            cursor.close()
            connection.close()
            show_message("All tables dropped!", "Info")
        except Error:
            show_message("Error while trying to drop all tables!")
            return

    def create_actor_tables(self):
        try:
            connection = self._db_connection()
            if connection is None:
                return

            cursor = connection.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS students (id INT AUTO_INCREMENT PRIMARY KEY, "
                           "name VARCHAR(255), surname VARCHAR(255))")
            cursor.execute("CREATE TABLE IF NOT EXISTS roles (id INT AUTO_INCREMENT PRIMARY KEY, "
                           "role VARCHAR(255))")

            cursor.close()
            connection.close()
            return
        except Error:
            show_message("Error while creating actor tables!")
            return

    def add_actor(self, table, column1, column2=None):
        try:
            connection = self._db_connection()
            if connection is None or not are_fields_present(table, column1, column2):
                return

            if not self.are_tables_connected(["students", "roles"]):
                self.create_actor_tables()

            cursor = connection.cursor()
            if column2:
                cursor.execute("INSERT INTO students (name, surname) VALUES (%s, %s)", (column1.get(), column2.get()))
            else:
                cursor.execute("INSERT INTO roles (role) VALUES (%s)", (column1.get(),))

            connection.commit()

            if cursor.rowcount == 1:
                column1.delete(0, "end")
                if column2:
                    column2.delete(0, "end")

            cursor.close()
            connection.close()
            return
        except Error:
            show_message("Error while adding actors to tables!")
            return

    def retrieve_actors(self):
        try:
            connection = self._db_connection()
            if connection is None:
                return [], []

            if not self.are_tables_connected(["students", "roles"]):
                show_message("Tables have been dropped, no data available!")
                return [], []

            students = []
            roles = []

            cursor = connection.cursor()
            cursor.execute("SELECT name, surname FROM students")
            records = cursor.fetchall()
            for row in records:
                students.append(row[0] + " " + row[1])

            cursor.execute("SELECT role FROM roles")
            records = cursor.fetchall()
            for row in records:
                roles.append(row[0])

            if len(students) == 0 or len(roles) == 0:
                show_message("Actor tables are empty!")
                return [], []

            cursor.close()
            connection.close()
            return students, roles
        except Error:
            show_message("Error while retrieving actor tables!")
            return [], []

    def create_month_table(self, month):
        try:
            connection = self._db_connection()
            if connection is None:
                return

            cursor = connection.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS {} (id INT AUTO_INCREMENT PRIMARY KEY, "
                           "role VARCHAR(255), master VARCHAR(255), vice VARCHAR(255))".format(month))

            cursor.close()
            connection.close()
            return
        except Error:
            show_message("Error while creating table for the month of {}!".format(month))
            return

    def add_month_data(self, month, result):
        try:
            connection = self._db_connection()
            if connection is None and not result:
                return

            cursor = connection.cursor()
            for role, student in result.items():
                cursor.execute("INSERT INTO {} (role, master, vice) VALUES (%s, %s, %s)".format(month),
                               (role, student[0], student[1]))

            connection.commit()

            cursor.close()
            connection.close()
            return
        except Error:
            show_message("Error while adding month data to table {}!".format(month))
            return

    def retrieve_previous_results(self, stop_month):
        try:
            connection = self._db_connection()
            if connection is None:
                return None

            previous_results = []
            cursor = connection.cursor()
            for month in self.months:
                if month == stop_month:
                    break
                cursor.execute("SELECT role, master FROM {}".format(month))
                records = cursor.fetchall()
                for row in records:
                    previous_results.append(row[0] + "," + row[1])

            cursor.close()
            connection.close()
            return previous_results
        except Error:
            show_message("Error while retrieving previous results!")
            return None
