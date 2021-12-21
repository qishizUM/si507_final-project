
# description

Database structure expression: the database is the root, the table is the child of the database, and the attribute is the child of the table. For example, it is known that: database ='mydatabase', tables = ['iTunes','artist'], attributes = [[ 'trackID','trackName','artistName','trackCount ', 'trckPrice','collectionPrice'],['artistName','introduce']


### First, Data structure and expression
1. The relationship expression of database, table and attribute:  
  （1) Database structure expression: the database is the root, the table is the child of the database, and the attribute is the child of the table.  
    For example, it is known that:  
      database ='mydatabase',
      tables = ['iTunes','artist'],
      attributes = [[ 'trackID','trackName','artistName','trackCount ', 'trckPrice','collectionPrice'],['artistName','introduce']
   
  It can be described with general list in data structure, shown as:
     Mydatabase('iTunes'('trackID','trackName','artistName','trackCount),'artist'('artistName','intro1','intro2'))  
  To this end, define the class Node() and the function construct_str_database(database,tables,attributes)  
  
  (2) Use "graphviz" to display the tree structure of (1) with a block diagram.  
  construct_str_database [link to the data structure view](database_structure.gv.pdf)  
 
  (3) jason format expression.   
*get_structure(root)* --- Convert the root of tree structure to jason format.   
*save_dicts(filename,dicts)* ---Save the data in jason format into a file as filename [For example, Qiushi_structure.json]( Qiushi_structure.jason)   
*Load_json_file(filename)* ---Read the file filename, the data is in json format  
### Second, Automatic construction of database tables
1. The database is automatically established  
*create_database(root)* ---automatically generates a database named root.name.   
*create_tables_attributes(root)* ---constructs a table named root.chiledren[i].name (i=0,1,..,) and adds it to the database.   
Finally, add the attribute rooot.children[i].children to the i-th data table, root.children[i] is the i-th data table.
2. Automatic data input and output  
*into_database(root,list_data)* ---automatically adds the attribute data list_data to the root-rooted database  
*database_data = get_data(root)* ---automatically reads out the data of the database. In the example, the attribute'trackID' of the first table "iTunes" is the primary key, and'artistName' is the foreign key of the table "artist".  
3. The input and output of Jason data  
*database_into_jason(root,list_data)* ---converts the data list_data into json format, stores and reads the same as 1 (3), the file name is "Qiushi.jason". [link to the json file]( Qiushi_structure.jason)  
