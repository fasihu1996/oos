from pywinauto.application import Application

# diese Variante scheint auf Win 11 nicht mehr zu funktionieren
app = Application().start("notepad.exe", timeout=10)

# main_dialog = app.window(title_re=".*Notepad")
main_dialog = app.UntitledNotepad

main_dialog.Edit.type_keys("asdf")

font_menu = main_dialog.menu_select("Format->Schriftart...")
