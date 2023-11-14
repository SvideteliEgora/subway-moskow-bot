import json
import gspread
import functions

gc = gspread.service_account(filename="venv/calm-vine-332204-924334d7332a.json")
sh_connection = gc.open_by_url('https://docs.google.com/spreadsheets/d/1fUu3aU7DhJoZl6X_KAX0GQVGvhqCW9f5iI0GbPPI5OA/edit')
worksheet1 = sh_connection.sheet1
list_of_lists = worksheet1.get_all_values()

data = functions.json_converter(list_of_lists)

with open("data.json", "w", encoding="UTF-8") as file:
    json.dump(data, file, indent=4, ensure_ascii=False)


