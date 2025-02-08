import pymysql
from mysql.connector import Error

class KoneksiDB:
    def __init__(self):
        try:
            self.connection = pymysql.connect(
                host='localhost',
                user='root',  # Ganti dengan username MySQL Anda
                password='',  # Ganti dengan password MySQL Anda
                database='2210010017_agama'  # Ganti dengan nama database Anda
            )
            # Memastikan koneksi berhasil
            if self.connection.open:
                print("Koneksi berhasil")
                self.cursor = self.connection.cursor()
        except Exception as e:
            print(f"Terjadi kesalahan: {e}")

    def get_connection(self): # Mendapatkan koneksi database.
        return self.connection

    def get_cursor(self): #Mendapatkan cursor database.
        return self.cursor

    def close(self):
        self.connection.close()


