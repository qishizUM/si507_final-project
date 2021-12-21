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


#read data from database(tree structure) 
def get_data(root):
    #open the dababase and build the connection
    mydb = mysql.connector.connect(host="localhost",user="root",password="SQL0809",database=root.name)     
    mycursor = mydb.cursor()    

    data = []
    for table in root.children:
        sql = f'select * from {table.name}'
        mycursor.execute(sql)    
        result = mycursor.fetchall() #fetchall(): use sql to get many attributes
        data.append(result)     
   
    mycursor.close()   
    mydb.close() 
    return data   
