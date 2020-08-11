
import sqlite3

class conexion:

    con=sqlite3.connect("data-ofelia.db")

    def insert_case(self, argument):
            if argument == "Usuarios" : return "insert into Usuarios (nombre_usu,tipo_usu,contraseña) values (?,?,?)"
            elif argument == "CategoriaGastos": return "insert into CategoriaGastos (nombre_cat_gasto) values (?)"
            elif argument == "SubcategoriaGastos": return "insert into SubcategoriaGastos ( nomb_subcat, descr_subcat, empleado_id, proveedor_id, sueldo, adelanto, contacto, f_h_adelanto, f__h_pago, CategoriaGastos_id_cat_gasto, cuenta) values (?,?,?,?,?,?,?,?,?,?,?)"
            elif argument == "Turnos": return "insert into Turnos (turno, caja_ini_turno, fecha, f_h_apertura, f_h_cierre, Usuarios_id_usu) values (?,?,?,?,?,?)"
            elif argument == "TiposDePagos": return "insert into TiposDePagos (nombre_tipo_pago) values (?)"
            elif argument == "Ventas": return "insert into Ventas (f_h_venta, monto_venta, borrado, f_h_borrado, observacion, Turnos_id_turno, TiposDePagos_id_tipo_pago, caja ) values (?,?,?,?,?,?,?,?)"
            elif argument == "CategoriaProductos": return "insert into CategoriaProductos (descr_categ) values (?)"
            elif argument == "ProductosPorMayor": return "insert into ProductosPorMayor (nombre_producto, monto_producto, CategoriaProductos_id_cat_prod ) values (?,?,?)"
            elif argument == "Gastos": return "insert into Gastos (monto_gasto, observacion_gasto, TiposDePagos_id_tipo_pago, Turnos_id_turno, SubcategoriaGastos_id_subcat_gasto) values (?,?,?,?,?)"
        

    def update_case(self, argument):
            if argument == "Usuarios": return "update Usuarios set nombre_usu = ? ,tipo_usu = ? ,contraseña = ? where id_usu = ?"
            elif argument == "CategoriaGastos": return "update CategoriaGastos set nombre_cat_gasto = ? where id_cat_gasto = ?"
            elif argument == "SubcategoriaGastos": return "update SubcategoriaGastos set nomb_subcat = ?, descr_subcat = ?, empleado_id = ?, proveedor_id = ?, sueldo = ?, adelanto = ?, contacto = ?, f_h_adelanto = ?, f__h_pago = ?, CategoriaGastos_id_cat_gasto = ?, cuenta = ? where id_subcat_gasto = ?"
            elif argument == "Turnos": return "update Turnos set turno = ?, caja_ini_turno = ?, fecha = ?, f_h_apertura = ?, f_h_cierre = ?, Usuarios_id_usu = ? where id_turno = ?"
            elif argument == "TiposDePagos": return "update TiposDePagos set nombre_tipo_pago = ? where id_tipo_pago = ?"
            elif argument == "Ventas": return "update Ventas set f_h_venta = ?, monto_venta = ?, borrado = ?, f_h_borrado = ?, observacion = ?, Turnos_id_turno = ?, TiposDePagos_id_tipo_pago = ?, caja = ?  where id_venta = ?"
            elif argument == "CategoriaProductos": return "update CategoriaProductos set descr_categ = ? where id_cat_prod = ?"
            elif argument == "ProductosPorMayor": return "update ProductosPorMayor set nombre_producto = ?, monto_producto = ?, CategoriaProductos_id_cat_prod = ? where id_productos = ?"
            elif argument == "Gastos": return "update Gastos set monto_gasto = ?, observacion_gasto = ?, TiposDePagos_id_tipo_pago = ?, Turnos_id_turno = ?, SubcategoriaGastos_id_subcat_gasto = ? where id_gasto = ?"
       

    def selectId_case(self, argument):
            if argument == "Usuarios": return "select * from Usuarios where id_usu = ?"
            elif argument == "CategoriaGastos": return "select * from CategoriaGastos where id_cat_gasto = ?"
            elif argument == "SubcategoriaGastos": return "select * from SubcategoriaGastos where id_subcat_gasto = ?"
            elif argument == "Turnos": return "select * from Turnos where id_turno = ?"
            elif argument == "TiposDePagos": return "select * from TiposDePagos where id_tipo_pago = ?"
            elif argument == "Ventas": return "select * from Ventas where id_venta = ?"
            elif argument == "CategoriaProductos": return "select * from CategoriaProductos where id_cat_prod = ?"
            elif argument == "ProductosPorMayor": return "select * from ProductosPorMayor where id_productos = ?"
            elif argument == "Gastos": return "select * from Gastos where id_gasto = ?"
         

    def delete_case(self, argument):
            if argument == "Usuarios": return "delete from Usuarios where id_usu = ?"
            elif argument == "CategoriaGastos": return "delete from CategoriaGastos where id_cat_gasto = ?"
            elif argument == "SubcategoriaGastos": return "delete from SubcategoriaGastos where id_subcat_gasto = ?"
            elif argument == "Turnos": return "delete from Turnos where id_turno = ?"
            elif argument == "TiposDePagos": return "delete from TiposDePagos where id_tipo_pago = ?"
            elif argument == "Ventas": return "delete from Ventas where id_venta = ?"
            elif argument == "CategoriaProductos": return "delete from CategoriaProductos where id_cat_prod = ?"
            elif argument == "ProductosPorMayor": return "delete from ProductosPorMayor where id_productos = ?"
            elif argument == "Gastos": return "delete from Gastos where id_gasto = ?"
 

    def insert(self, parameter_list, tabla):
        con=sqlite3.connect("data-ofelia.db")
        con.execute(self.insert_case(tabla),parameter_list)
    
    def update(self, parameter_list, tabla):
        con=sqlite3.connect("data-ofelia.db")
        con.execute(self.update_case(tabla),parameter_list)

    def delete(self, id, tabla):
        con=sqlite3.connect("data-ofelia.db")
        con.execute(delete_case(tabla),id)

    def selectId(self, id, tabla):
        con=sqlite3.connect("data-ofelia.db")
        cursor=con.execute(selectId_case(tabla),id)
        return cursor

    def selectAll(self, tabla):
        con=sqlite3.connect("data-ofelia.db")
        cursor=con.execute("select * from "+tabla)
        return cursor
            
 