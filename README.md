# si507_final-project
Automatic generation of SQL database and auto input and output of data

## Introduction
My purpose of this project was to build a automatic SQL database and use auto input and output of data. It would allow users to create database based on name, agg get ingormation about age and nationality based on first name. The project utilized programming techniques in python, including regx operation, Web API crawling, output json file, bubble sort algorithmm, data manipulation using SQL, data visualiting via graphviz and Ploty, etc.

## Data Source
1. iTunes (constructing searches to get attributes results) : https://itunes.apple.com/search?term= 
3. agify.io (estimate the age from a first name that retrieved from iTunes): https://api.agify.io/?name=
4. nationalize.io (estimate nationality from a first name that retrieved from iTunes): https://api.nationalize.io/?name=


## Processing
Just enter the database name, the name of the table and its atributes to automatically generate the database structure, including the ability to automatically input and read attribute data
### First, Data structure and expression
1. The relationship expression of database, table and attribute:
  1) Database structure expression: the database is the root, the table is the child of the database, and the attribute is the child of the table.
    For example, it is known that:
      database ='mydatabase',
      tables = ['iTunes','artist'],
      attributes = [[ 'trackID','trackName','artistName','trackCount ', 'trckPrice','collectionPrice'],['artistName','introduce']
 
  It can be described with general list in data structure, shown as:
     Mydatabase('iTunes'('trackID','trackName','artistName','trackCount),'artist'('artistName','intro1','intro2'))
  To this end, define the class Node() and the function construct_str_database(database,tables,attributes)
  (2) Use "graphviz" to display the tree structure of (1) with a block diagram.
 Function construct_str_database [link to the data structure view](README_data_structure.md)
  (3) jason format expression. 
Function get_structure(root) --- Convert the root of tree structure to jason format. 
Function save_dicts(filename,dicts) ---Save the data in jason format into a file as filename [For example, Qiushi_structure.json]( Qiushi_structure.jason) 
Function Load_json_file(filename) ---Read the file filename, the data is in json format
### Second, Automatic construction of database tables
1. The database is automatically established
Function create_database(root) ---automatically generates a database named root.name. 
Function create_tables_attributes(root) ---constructs a table named root.chiledren[i].name (i=0,1,..,) and adds it to the database. Finally, add the attribute rooot.children[i].children to the i-th data table, root.children[i] is the i-th data table.
2. Automatic data input and output
Function into_database(root,list_data) ---automatically adds the attribute data list_data to the root-rooted database
Function database_data = get_data(root) ---automatically reads out the data of the database. In the example, the attribute'trackID' of the first table "iTunes" is the primary key, and'artistName' is the foreign key of the table "artist".
3. The input and output of Jason data,
Function database_into_jason(root,list_data) ---converts the data list_data into json format, stores and reads the same as 1 (3), the file name is "Qiushi.jason". [link to the json file]( Qiushi_structure.jason) 
### Third, Get data
1. Call the function data1=get_iTunes_data("movie")
Obtained a list of attributes from the "https://itunes.apple.com/search" website, 'trackID','trackName','artistName','trackCount','trckPrice','collectionPrice'
The data collection is put into data1. data1 is the data of the table "iTunes". When fetching data from the website, taking into account the requirements of the job (at least 100), the default 50 is changed to 200.
 2. Take out 'artistName' in data1 and remove the duplicates. For each artistName, obtain the other two attribute values of the artist through the website " agify.io" and the website "nationalize.io".
### Forth, Data display
In order to check whether the database is stored and read, we take 10 numbers from the table "iTunes", and compare them with histogram (Function histogram_draw()), line chart (Function line_draw()), and dot graph (Function scatter_draw). The data is sorted by key value. In order to find the top 10 correspondences, we sort the data (Function bubbleSort()) before saving the database.
