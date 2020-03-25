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

def readTable(db, table):
    con = sql.connect(db)
    cur = con.cursor()
    table=(table,)
    sqlcode="SELECT * FROM ?"   
    cur.execute(sqlcode, (table,))
    results=cur.fetchall()
    return results

#======================================================================================================================================================================

def writeSQL6(db,table , newValue):
    con = sql.connect(db)
    cur = con.cursor()
    table=(table,)    
    sqlcode="INSERT INTO ? VALUES (?,?,?,?,?,?) "   
    cur.execute(sqlcode,(table, newValue[0], newValue[1], newValue[2], newValue[3], newValue[4], newValue[5]))
    cur.fetchall()
    
def writeSQL5(db,table , newValue):
    con = sql.connect(db)
    cur = con.cursor()
    table=(table,)    
    sqlcode="INSERT INTO ? VALUES (?,?,?,?,?,?) "   
    cur.execute(sqlcode,(table, newValue[0], newValue[1], newValue[2], newValue[3], newValue[4],))
    cur.fetchall()

def writeSQL4(db,table , newValue):
    con = sql.connect(db)
    cur = con.cursor()
    table=(table,)    
    sqlcode="INSERT INTO ? VALUES (?,?,?,?,?,?) "   
    cur.execute(sqlcode,(table, newValue[0], newValue[1], newValue[2], newValue[3],))
    cur.fetchall()

def writeSQL3(db,table , newValue):
    con = sql.connect(db)
    cur = con.cursor()
    table=(table,)    
    sqlcode="INSERT INTO ? VALUES (?,?,?,?,?,?) "   
    cur.execute(sqlcode,(table, newValue[0], newValue[1], newValue[2],))
    cur.fetchall()
    
def writeSQL2(db,table , newValue):
    con = sql.connect(db)
    cur = con.cursor()
    table=(table,)    
    sqlcode="INSERT INTO ? VALUES (?,?,?,?,?,?) "   
    cur.execute(sqlcode,(table, newValue[0], newValue[1],))
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