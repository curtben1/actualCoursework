import sqlite3 as sql
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa

"""
Contains functions necessary for reading/writing to an sql database
"""

def readSQL(db, table, columnName, searchTerm):
    con = sql.connect(db)
    cur = con.cursor()
    table=(table,)
    columnName=(columnName,)
    searchTerm=(searchTerm,)
    sqlcode="SELECT * FROM ? WHERE ? LIKE ? "   
    cur.execute(sqlcode, (table, columnName ,searchTerm, ))
    results=cur.fetchall()
    return results

def readsList():
    con = sql.connect("mainDatabase.db")
    cur = con.cursor()
    #table=(table,)  
    cur.execute("SELECT *FROM serverList")
    results=cur.fetchall()
    return results

def readStats():
    con = sql.connect("mainDatabase.db")
    cur = con.cursor()
    #table=(table,)  
    cur.execute("SELECT *FROM Statitics")
    results=cur.fetchall()
    return results

#======================================================================================================================================================================
    
def writeHost(new1, new2):
    con = sql.connect("mainDatabase.db")
    cur = con.cursor()   
    sqlcode="INSERT INTO serverList VALUES (Null,?,?,1) "   
    cur.execute(sqlcode,(new1, new2))
    con.commit()
    cur.fetchall()

def writeSQL1(db,table , newValue):
    con = sql.connect(db)
    cur = con.cursor()
    table=(table,)    
    sqlcode="INSERT INTO ? VALUES (?,?,?,?,?,?) "   
    cur.execute(sqlcode,(table, newValue[0],))
    cur.fetchall()
    
#======================================================================================================================================================================

def encWriteSQL(db,table,uName,pWord):
    pass

def encReadSQL(db,table,uName,pWord):
    
    pass

def decrypt(value, privKey):
    pass