from oauth2client.service_account import ServiceAccountCredentials
import gspread


class Sheets:
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('ebsb-298213-dcdf54a68048.json', scope)
    client = gspread.authorize(creds)
    password = "admin"
    sheetname = "EBSB Feedback"  # Change to name of Spreadsheet

    def getRow(str , client=client):
        # Gets the complete row of a cell specified by it's label
        sheet = client.open(Sheets.sheetname).sheet1
        row = sheet.row_values(sheet.find(str).row)
        return row

    def createRow(*args, client=client):
        # Creates a new row in the chosen
        sheet = client.open(Sheets.sheetname).sheet1
        sheet.append_row(args)

    def checkID(id , client=client):
        # Checks if ID exists in database and returns corresponding name
        try:
            row = Sheets.getRow(id)
        except gspread.exceptions.CellNotFound:
            return "null"
        return row[1]