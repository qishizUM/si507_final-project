class Node:
    def __init__(self,name, father=None):          
        self.name = name
        self.father = father
        self.children = []

#set up a tree that descibes database,tables and atrributes     
def construct_str_database(database_name,table_names,attribute_names):
    root = Node(database_name)    
    
    for i in range(len(table_names)):
        table = Node(table_names[i],root)
        #table.father=root
        root.children.append(table)
        table.children= attribute_names[i]   
    return root
 
#by root, a database is built
def create_database(root):
    #create a MySQL database.
    #connect mysql to python.
    mydb = mysql.connector.connect(host="localhost",user="root",password="SQL0809")
    mycursor = mydb.cursor() 
    
    #create a database(name) if there is no this database
    mycursor.execute("CREATE DATABASE IF NOT EXISTS " + root.name)   
    
    #delete the database
    #mycursor.execute("DROP DATABASE IF EXISTS " + root.name)

    #show database
    #mycursor.execute("SHOW DATABASES")   
    #for x in mycursor:
    #  print(x)

#by root, a database is built
def create_tables_attributes(root):
    #open the dababase and build the connection
    mydb = mysql.connector.connect(host="localhost",user="root",password="SQL0809",database=root.name)     
    mycursor = mydb.cursor()
    #and id is automatically generated 
    for i in range(-1,-len(root.children)-1,-1): 
        table = root.children[i]    
        
        #delete the table if it exixts   
        mycursor.execute(f"DROP TABLE IF EXISTS {table.name}")    
               
        str_attribute =""           
        for j in range(len(table.children)): 
            attr = table.children[j]
            #For simplicity, fields are designed whose type and length are all "VARCHAR(25)"
            str_attribute += attr + " VARCHAR(100) "
            
            #first attribute is PRIMARY KEY
            if j==0:
                str_attribute += " PRIMARY KEY "     
            
           
            if i == 0 and attr == root.children[1].children[0]:
                #foreign key is 
                str_attribute += f" FOREIGN KEY REFERENCES {root.children[1].name}({root.children[1].children[0]})"
             
            # use ',' for segregation. consider that there is no segregation at the end
            if attr != table.children[-1]:
                str_attribute += ',' 

        # execute SQL, create the table
        sql = f"create table {table.name} ({str_attribute})"  
        mycursor.execute(sql)     

    mycursor.close()   
    mydb.close()

def into_database(root,list_data):
    #open the dababase and build the connection
    mydb = mysql.connector.connect(host="localhost",user="root",password="SQL0809",database=root.name)     
    mycursor = mydb.cursor()
    
    #fill data  
    ##format: sql = ("""INSERT INTO {table} (name, age, gender) VALUES (%s, %s, %s)"""
    for i in range(len(root.children)):  
        table = root.children[i]   
        
        data = list_data[i]  
        str_attribute =""    #like name, age, gender
        str_type = ""        #like %s, %s, %s
        for attr in table.children:  
            str_attribute += attr
            str_type += "%s"
            
            # use ',' for segregation. consider that there is no segregation at the end
            if attr != table.children[-1]:
                str_attribute += ',' 
                str_type +=  ','   
    
        sql = f"INSERT INTO {table.name} ({str_attribute}) VALUES ({str_type})"
        #insert a set
        mycursor.executemany(sql,data)   
       
    mydb.commit()
    mycursor.close()   
    mydb.close()

###----------------------------------------------------------------------------------------------------------------------
#put tree structure that describes database structure into jason style.
def get_structure(root):
    dict_database = {}
    for table in root.children:
        dict_database[table.name] = table.children
    return dict_database

#a function which saves "dicts" into filename parameter.
def save_dicts(filename,dicts):
    with open(filename,'w') as file_obj:
        js.dump(dicts,file_obj)

#read data from filename
def Load_json_file(filename):
    #open filename
    with open(filename) as file_obj:
        #return the data
        return js.load(file_obj)
    
#change list of attributes into dictionary formats.
def data_into_dict(table,attribute_data):

    attr_data_dicts=[]
    for arrt in attribute_data:
        attr_data_dict={}
        for j in range(len(arrt)):
            attr_data_dict[table.children[j]] = arrt[j]
        attr_data_dicts.append(attr_data_dict)
    return attr_data_dicts     

def database_into_jason(root,list_data):
    dict1 = data_into_dict(root.children[0], list_data[0])
    dict2 = data_into_dict(root.children[1], list_data[1])   
                             
    database_dicts = {}
    database_dicts [root.children[0].name] = dict1

    #consider the primary key and the foreign key                                                         '
    for dic in dict1:
        for dic2 in dict2:
            if dic2['artistName'] == dic['artistName']:   
                dic['artistName'] = dic2     
                break     

    return database_dicts   
###-----------------------------------------------------------------------------------------------------------------
