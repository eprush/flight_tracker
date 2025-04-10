# Data engineering project for flight service
#### This is a project for a test assignment for the DE internship selection

[Technical task](specification.md)

The Repository pattern is used for data storage. The structure of files
and directories (modules and packages) reflects the architecture:
- 📁 config - project configuration.
  - 📄 config.py - the project configuration file. You can set the time of observation, the water area and name of your table/database.
  - 📄 loading.py - data loading script.
- 📁 datamart - datamart creation.
  - 📄 datamart.py - script that starts the creation of a datamart.
  - 📄 datamart_script.sql - request that creates a datamart.
- 📁 models - data models.
- 📁 parsing - data parsing service.
  - 📄 abstract_parser.py - description of the parsing functionality.
  - 📄 aviastack_parser.py - parsing for a resource [aviastack.com](https://aviationstack.com).
- 📁 repositories - repository for storing data.
  - 📄 abstract_repository.py - repository interface description.
  - 📄 csv_repository.py - repository for storage in a csv file.
- 📁 tests - tests (the directory structure duplicates the project structure)
- 📄 main.py - script that fills a file/database with data after parsing. In it, you can specify what the storage will be (a csv file or a database).
- 📄 .env - file containing a password environment variable (you should create it yourself).

To work with the project, you need to fork it and upload it to your computer. Аfter that install all necessary dependencies using the terminal command
```
pip install -r requirements.txt
```
And before you start using the project, create a file .env with an password environment variable.

To fill in the table/database, you should run the file main.py
```
python main.py
```

To create a datamart, you should run the file datamart.py
```
python datamart/datamart.py
```
