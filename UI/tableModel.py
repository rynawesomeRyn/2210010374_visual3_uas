from PyQt6.QtCore import Qt, QAbstractTableModel, QDate

class TableModel(QAbstractTableModel):
    def __init__(self, data, headers):
        super().__init__()
        self._data = data
        self._headers = headers

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._headers)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if index.isValid() and role == Qt.ItemDataRole.DisplayRole:
            value = self._data[index.row()][index.column()]
            column_name = self._headers[index.column()].lower()

            # Periksa apakah kolom adalah kolom tanggal
            if "tanggal" in column_name or "tgl" in column_name:
                if isinstance(value, str):
                    return value  # Jika sudah string, tampilkan langsung
                elif isinstance(value, QDate):
                    return value.toString("dd-MM-yyyy")  # Format QDate
                elif hasattr(value, "strftime"):
                    return value.strftime("%d-%m-%Y")  # Format datetime.date
                else:
                    return str(value)  # Fallback untuk tipe lainnya

            return str(value)  # Format default untuk kolom lain
        return None

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self._headers[section]
            else:
                return section + 1  # Menampilkan nomor baris jika vertikal
        return None
