import sqlite3 as sql
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa

"""
Contains functions necessary for reading/writing to an sql database
"""

def readSQL(db, table, columnName, searchTerm):
    con = sql.connect(db)
    cur = con.cursor()
    table = (table,)
    columnName = (columnName,)
    searchTerm = (searchTerm,)
    sqlcode = "SELECT * FROM ? WHERE ? LIKE ? "   
    cur.execute(sqlcode, (table, columnName ,searchTerm, ))
    results = cur.fetchall()
    return results

def readsList():
    con = sql.connect("main.db")
    cur = con.cursor()
    #table = (table,)  
    cur.execute("SELECT *FROM 'server_list'")
    results = cur.fetchall()
    return results

def addServer(ip, name):
    con = sql.connect("main.db")
    cur = con.cursor()
    ip = (ip,)  
    cur.execute("INSERT INTO server_list (name,ip,players,in_game) VALUES (?,?,0,0)",(str(name),str(ip)))
    results = cur.fetchall()
    con.commit()
    return results

def remServer(ip):
    con = sql.connect("main.db")
    cur = con.cursor()
    ip = (ip,)  
    cur.execute("DELETE FROM server_list WHERE ip = ?",ip)
    results = cur.fetchall()
    con.commit()
    return results


def updatePlayers(playerNum):
    con = sql.connect("main.db")
    cur = con.cursor()
    ip = (ip,)  
    cur.execute("INSERT INTO 'server_list' VALUES (Null,?,0,0)",ip)
    #cur.fetchall()


def updateGameState():
    con = sql.connect("main.db")
    cur = con.cursor()
    cur.execute("INSERT INTO 'server_list' VALUES (Null,Null,Null,1)")
    #cur.fetchall()

def readStats(user):
    con = sql.connect("main.db")
    cur = con.cursor()
    user = (user, ) 
    cur.execute("SELECT *FROM Statitics WHERE 'account num' = ?",user)
    results = cur.fetchall()
    return results

def retSalt(userName):
    con = sql.connect("main.db")
    cur = con.cursor()
    userName = (userName,)  
    cur.execute("SELECT *FROM Accounts WHERE name = ?",userName)
    results = cur.fetchall()
    con.commit()
    return results

def checkDetails(userName, hashed):
    con = sql.connect("main.db")
    cur = con.cursor()
    details = (userName,hashed)  
    cur.execute("SELECT *FROM Accounts WHERE name = ? and password = ?",details)
    results = cur.fetchall()

    return results

def writeIP(userName,ip):
    con = sql.connect("main.db")
    cur = con.cursor()
    details = (ip, True, userName)  
    cur.execute("UPDATE Accounts SET ip = ?, loggedIn = ? WHERE name = ?",details)
    results = cur.fetchall()

    return results
#=========================================================================================================================================================


#============================================================================================================================================================

def encWriteSQL(db,table,uName,pWord):
    pass

def encReadSQL(db,table,uName,pWord):
    
    pass

def decrypt(value, privKey):
    pass