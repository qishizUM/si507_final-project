#!/usr/bin/python
# -*- coding: UTF-8 -*-
#first,download and install graphviz,and then pip
from os import name
from graphviz import Digraph 
import numpy as np
#from plotly.graph_objs import Bar,Layout
#from plotly import offline
import matplotlib.pyplot as plt
import json as js
import requests
import mysql.connector
import re
#import time   
#import secrets

#get json string from base_url and search key words
#each source captures at 200 records
def getJson_0(base_url,term): 
    #require>100
    url_param={'term': term,'limit': 200}     
    response = requests.get(base_url,url_param)    
    text = response.text  
    json_str = js.loads(text)    
    return json_str

#get json string from base_url and search key words
def getJson(url):     
    response = requests.get(url)    
    text = response.text      
    json_str = js.loads(text)    
    return json_str 

#use a regex operation to split the strings into words.
def split_string_into_words(strings):
    words = re.findall('\w+',strings)
    return words

#grab data from iTunes API according to term parameter
def get_iTunes_data(term):  
    base_url = "https://itunes.apple.com/search"   
    jsons = getJson_0(base_url,term)
    json_data = jsons['results']  
    ###data:'trackID','trackName','artistName','trackCount','trckPrice','collectionPrice'
    ### x.get('kind'):considering the case in which there is no 'kind'  
    data = []
    for x in json_data:
        if term not in x.get('kind'):
            continue  
        try:
            record = [x['trackId'],x['trackName'],x['artistName'],x['trackCount'],x['trackPrice'],x['trackId']]
            data.append(record)
        except:
            continue     
    return data      
  

#get the introduce of name for url
#grab data based on name that retrieved from iTunes API.
def get_name_data1(name):  
    #data = "123"
    name = split_string_into_words(name)[0]
    base_url = "https://api.agify.io/"
    url = f"{base_url}?name={name}"
    test = getJson(url)
    data = test.get('age')
    return data    

def get_name_data2(name):  
    #data ="456"
    name = split_string_into_words(name)[0]
    url = "https://api.nationalize.io/?name=" + name   
    test = getJson(url) 
    data = test.get('country')
    if len(data) > 0:
        data = data[0]
    else:
        data = {}

    return data     


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
 
#use graphviz to draw data structure
def draw_database_structure(root):
    g = Digraph(name='database_structure')
    g.node(name='d',label= root.name,color='red')
    g.node(name='t1',label = root.children[0].name)
    g.node(name='t2',label = root.children[1].name)
    g.edge('d','t1')
    g.edge('d','t2')
    for attribute in root.children[0].children:
        #g.node(name='att'+str(index),label = attribute,color='blue')
        g.edge('t1',attribute)

    for atribute in root.children[1].children:
        #g.node(name='att',label = atribute,color='blue')
        g.edge('t2',atribute)  
    g.view()

#numbers and artist (top 10)
def histogram_draw(labels,data): 
    #x_axis
    ind = [i for i in range(len(labels))]

    #drawing
    plt.bar(ind,data)

    #mark x-axis labels, words are 'vertical' 
    plt.xticks(ind,labels,rotation ='vertical')

    #mark chart title
    plt.title("TrackPrices of trackNames")

    #show drawing
    plt.show()    

# 
def line_draw(data):   
    fig,ax = plt.subplots()

    #set linewidth, and x_values is default
    ax.plot(data,linewidth=2)  
    
    #set title
    ax.set_title("TrackPrices and trackNames",fontsize = 14)

    #set words of x
    ax.set_xlabel("TrackNames",fontsize = 10)

    ax.set_ylabel("TrackPrices",fontsize = 10)    
     
    plt.show()
 
def scatter_draw(x_values,y_values):   
    plt.style.use('seaborn')
    fig,ax = plt.subplots()
    ax.scatter(x_values,y_values,s=100)
    plt.show()
 
def draw_data(data):
    #The first 10:trckPrice of trackNames
    trackNames = [x[1] for x in data]
    trackPrices = [float(x[4]) for x in data]
    trackCounts = [int(x[3]) for x in data]
    
    #chart(x-axis, y-axis)
    histogram_draw(trackNames,trackPrices)  

    line_draw(trackPrices)

    # trackCount and trckPrice
    scatter_draw(trackCounts,trackPrices) 
    

def bubbleSort(data): 
    for i in range(len(data)-1):
        for j in range(len(data)-1,i,-1):
            #if out of order  
            if data[j][0]<data[j-1][0]:
                #swap    
                temp =data[j].copy()
                data[j] = data[j-1]
                data[j-1] =  temp     

if __name__ == "__main__":  
    #the database is called  "mydatabase"
    #"mydatabase" has two tables:"iTunes" and "artist"
    #"iTunes"has 6 attributes('trackID' is the primary key,'artistName' is the foreign key ): 
    #'trackID','trackName','artistName','trackCount','trckPrice','collectionPrice'   
    #"artist"has 2 attributes:'artistName','introduce', where 'artistName' is the primary key 
    database = 'mydatabase'
    tables = ['iTunes','artist']
    attributes = [['trackID','trackName','artistName','trackCount','trckPrice','collectionPrice'],['artistName','intro1','intro2']]

    #set up a tree that describes the database  
    root=construct_str_database(database,tables,attributes)

    #-----------------------------------------
    jason_database_structure0=get_structure(root)
    save_dicts("Qiushi_structure.jason",jason_database_structure0)  
    jason_database_structure = Load_json_file("Qiushi_structure.jason")
    #-----------------------------------------

    ##show the tree
    draw_database_structure(root)    

    
    

    ##owing to above tree,create database 
    #create database  
    create_database(root)      

    #create tables and their attributes
    create_tables_attributes(root)


    # 'trackID','trackName','artistName','trackCount','trckPrice','collectionPrice'
    data1=get_iTunes_data("movie")
    
    #get introduce of a artistName  
    #first,get artistName ？？？？？？？？？？？？？？？？？？？？？？？？？
    repeat_artist_names=[da[2] for da in data1]
    #repeat_artist_names=[da[2] for da in data1]

    unique_artist_names = []
    for name in repeat_artist_names:
        if name not in unique_artist_names:
            unique_artist_names.append(name)
    
    data2=[]   #data2 is artist table data
     
    for name in unique_artist_names:
        # da[0] is artistName
        #x = get_name_data(da)
        result1= get_name_data1(name)  
        result2= get_name_data2(name)  
        result=[name,result1,result2]
        data2.append(result)     

    
    #into string
    for i in range(len(data1)):
        for j in range(len(data1[i])):
            if type(data1[i][j]) is not str:
                data1[i][j] = str(data1[i][j])
    for i in range(len(data2)):
        for j in range(len(data2[i])):
            if type(data2[i][j]) is not str:
                data2[i][j] = str(data2[i][j])
                
    #sort:note compair by str,not int considering database
    bubbleSort(data1)
    bubbleSort(data2) 
                
    #take data into the database
    list_data = [data1,data2]

   

    into_database(root,list_data)
    
    #get data from database
    database_data = get_data(root)     

    ###------------------------------------------------
    jason_data0 = database_into_jason(root,database_data)

    save_dicts("Qiushi.jason",jason_data0)

    jason_data = Load_json_file("Qiushi.jason")
    #---------------------------------------------

    #get 10 data
    #in the database,database_data is automatically sorted owing to keys(string) 
    base_data = [database_data[0][i] for i in range(10)]
    #   
    ori_data = [data1[i] for i in range(10)]   

   
   
    for i in range(10):
        #for j in range(10):
        #    x=str(ori_data[i][j])
        #    y=base_data[i][j]
            #xx =  (str(ori_data[i][j])!=base_data[i][j])
            if (ori_data[i][0]!=base_data[i][0]):
                #y=int(base_data[i][j])
                #z=(ori_data[i][j]==int(base_data[i][j]))

                print(i)
                print(ori_data[i],base_data[i])


    #by drawing, compaire the data before and after
    #
    ori_trackNames = [x[1] for x in ori_data]   
    ori_trackPrices = [float(x[4]) for x in ori_data]
    ori_trackCounts = [int(x[3]) for x in ori_data]
    base_trackNames = [x[1] for x in base_data]   
    base_trackPrices = [float(x[4]) for x in base_data]
    base_trackCounts = [int(x[3]) for x in base_data]
    
    #chart(x-axis, y-axis)
    histogram_draw(ori_trackNames,ori_trackPrices) 
    histogram_draw(base_trackNames,base_trackPrices)

    line_draw(ori_trackPrices)
    line_draw(base_trackPrices)

    # trackCount and trckPrice
    scatter_draw(ori_trackCounts,ori_trackPrices) 
    scatter_draw(base_trackCounts,base_trackPrices)