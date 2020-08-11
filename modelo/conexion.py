
import sqlite3

class conexion:

    con=sqlite3.connect("data-ofelia.db")

    def insert_case(self, argument):
        switcher = {
            "Usuarios": "insert into Usuarios (nombre_usu,tipo_usu,contraseña) values (?,?,?)",
            "": "insert into ",
            "": "insert into ",
            "": "insert into ",
            "": "insert into ",
            "": "insert into ",
            "": "insert into ",
            "": "insert into ",
            "": "insert into ",
        }

    def update_case(self, argument):
        switcher = {
            "Usuarios": "update Usuarios set nombre_usu = ? ,tipo_usu = ? ,contraseña = ? where id_usu = ?",
            "": "update ",
            "": "update ",
            "": "update ",
            "": "update ",
            "": "update ",
            "": "update ",
            "": "update ",
            "": "update "
        }

    def selectId_case(self, argument):
        switcher = {
            "Usuarios": "select * from Usuarios where id_usu = ?",
            "": "select * from ",
            "": "select * from ",
            "": "select * from ",
            "": "select * from ",
            "": "select * from ",
            "": "select * from ",
            "": "select * from ",
            "": "select * from "
        }

    def delete_case(self, argument):
        switcher = {
            "Usuarios": "delete from Usuarios where id_usu = ?",
            "": "delete from ",
            "": "delete from ",
            "": "delete from ",
            "": "delete from ",
            "": "delete from ",
            "": "delete from ",
            "": "delete from ",
            "": "delete from "
        }
 

    def insert(self, parameter_list, tabla):
        con.execute(insert_case(tabla),parameter_list)
    
    def update(self, parameter_list, tabla):
        con.execute(insert_case(tabla),parameter_list)

    def delete(self, id, tabla):
        con.execute(delete_case(tabla),id)

    def selectId(self, id, tabla):
        cursor=con.execute(selectId_case(tabla),id)
        return cursor

    def selectAll(self, tabla):
        cursor=con.execute("select * from "+tabla)
        return cursor
            
 