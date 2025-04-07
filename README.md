# Data engineering project for flight service
#### This is a project for a test assignment for the DE internship selection

[Technical task](specification.md)

The Repository pattern is used for data storage. The structure of files
and directories (modules and packages) reflects the architecture:
- 📁 models - data models
- 📁 parsing - data parsing service
  - 📄 abstract_parser.py - description of the parsing functionality
  - 📄 aviastack_parser.py - parsing for a resource [aviastack.com](https://aviationstack.com)
- 📁 repositories - a repository for storing data
  - 📄 abstract_repository.py - repository interface description
  - 📄 csv_repository.py - repository for storage in a csv file
- 📁 tests - tests (the directory structure duplicates the project structure)

To work with the project, you need to fork it and upload it to your computer.
