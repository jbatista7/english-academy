#Get-ChildItem -path "*/migrations/*.py" -Exclude "__init__.py" -Include *.py -Recurse | Remove-Item

#Get-ChildItem -path "*/migrations/" -Exclude "__init__.py" -Include *.py -Recurse | Remove-Item




Get-ChildItem -path "*/migrations/*.py" -Exclude "__init__.py" -Recurse | Remove-Item
remove-item * -Include "__pycache__" -Recurse
rd .\db.sqlite3