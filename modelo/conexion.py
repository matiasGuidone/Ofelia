
import sqlite3

class conexion:

    con=sqlite3.connect("data-ofelia.db")

    def insert_case(self, argument):
            if argument == "Usuarios" : return "insert into Usuarios (nombre_usu,tipo_usu,contraseña,sesion) values (?,?,?,0)"
            elif argument == "CategoriaGastos": return "insert into CategoriaGastos (nombre_cat_gasto) values (?)"
            elif argument == "SubcategoriaGastos": return "insert into SubcategoriaGastos ( nomb_subcat, descr_subcat, empleado_id, proveedor_id, sueldo, adelanto, contacto, f_h_adelanto, f__h_pago, CategoriaGastos_id_cat_gasto, cuenta) values (?,?,?,?,?,?,?,?,?,?,?)"
            elif argument == "Turnos": return "insert into Turnos (turno, caja_ini_turno, fecha, f_h_apertura, f_h_cierre, Usuarios_id_usu, estado) values (?,?,?,?,?,?,?)"
            elif argument == "TiposDePagos": return "insert into TiposDePagos (nombre_tipo_pago) values (?)"
            elif argument == "Ventas": return "insert into Ventas (f_h_venta, monto_venta, borrado, f_h_borrado, observacion, Turnos_id_turno, TiposDePagos_id_tipo_pago, caja ) values (?,?,?,?,?,?,?,?)"
            elif argument == "CategoriaProductos": return "insert into CategoriaProductos (descr_categ) values (?)"
            elif argument == "ProductosPorMayor": return "insert into ProductosPorMayor (nombre_producto, monto_producto, CategoriaProductos_id_cat_prod ) values (?,?,?)"
            elif argument == "Gastos": return "insert into Gastos (monto_gasto, observacion_gasto, Turnos_id_turno, SubcategoriaGastos_id_subcat_gasto, fecha) values (?,?,?,?,?)"
        

    def update_case(self, argument):
            if argument == "Usuarios": return "update Usuarios set nombre_usu = ? ,tipo_usu = ? ,contraseña = ?,sesion = ? where id_usu = ?"
            elif argument == "CategoriaGastos": return "update CategoriaGastos set nombre_cat_gasto = ? where id_cat_gasto = ?"
            elif argument == "SubcategoriaGastos": return "update SubcategoriaGastos set nomb_subcat = ?, descr_subcat = ?, empleado_id = ?, proveedor_id = ?, sueldo = ?, adelanto = ?, contacto = ?, f_h_adelanto = ?, f__h_pago = ?, CategoriaGastos_id_cat_gasto = ?, cuenta = ? where id_subcat_gasto = ?"
            elif argument == "Turnos": return "update Turnos set turno = ?, caja_ini_turno = ?, fecha = ?, f_h_apertura = ?, f_h_cierre = ?, Usuarios_id_usu = ?, estado = ? where id_turno = ?"
            elif argument == "TiposDePagos": return "update TiposDePagos set nombre_tipo_pago = ? where id_tipo_pago = ?"
            elif argument == "Ventas": return "update Ventas set f_h_venta = ?, monto_venta = ?, borrado = ?, f_h_borrado = ?, observacion = ?, Turnos_id_turno = ?, TiposDePagos_id_tipo_pago = ?, caja = ?  where id_venta = ?"
            elif argument == "CategoriaProductos": return "update CategoriaProductos set descr_categ = ? where id_cat_prod = ?"
            elif argument == "ProductosPorMayor": return "update ProductosPorMayor set nombre_producto = ?, monto_producto = ?, CategoriaProductos_id_cat_prod = ? where id_productos = ?"
            elif argument == "Gastos": return "update Gastos set monto_gasto = ?, observacion_gasto = ?, TiposDePagos_id_tipo_pago = ?, Turnos_id_turno = ?, SubcategoriaGastos_id_subcat_gasto = ?, fecha = ? where id_gasto = ?"
       

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
 
    #reportes

    def getReporteDiario(self, dia):##DD-MM-YY
        consulta = "SELECT fecha, hora, turno, montoingreso, montoegreso, observacion FROM (SELECT Turnos.fecha as fecha, Ventas.f_h_venta as hora, Turnos.turno as turno, Ventas.monto_venta as montoingreso, '' as montoegreso, 'caja: '||Usuarios.nombre_usu||', tipo pago: '||TiposDePagos.nombre_tipo_pago as observacion from Ventas join Turnos on Turnos.id_turno = Ventas.Turnos_id_turno join Usuarios on Usuarios.id_usu = Turnos.Usuarios_id_usu join TiposDePagos on Ventas.TiposDePagos_id_tipo_pago = TiposDePagos.id_tipo_pago UNION SELECT Turnos.fecha as fecha, substr(Gastos.fecha,11,17) as hora, Turnos.turno as turno, '' as montoingreso, Gastos.monto_gasto as montoegreso, 'caja: '||Usuarios.nombre_usu||', gasto: '|| SubcategoriaGastos.nomb_subcat as observacion from Gastos join Turnos on Turnos.id_turno = Gastos.Turnos_id_turno join Usuarios on Usuarios.id_usu = Turnos.Usuarios_id_usu join SubcategoriaGastos on Gastos.SubcategoriaGastos_id_subcat_gasto = SubcategoriaGastos.id_subcat_gasto ) where fecha = ? ORDER BY hora ASC"
        con = sqlite3.connect("data-ofelia.db")
        cursor=con.execute(consulta,[dia])
        return cursor.fetchall()
        pass

    def getReporteMensual(self, mes): ##MM-YY
        con=sqlite3.connect("data-ofelia.db")
        consulta = "select Turnos.fecha as dia, ifnull(totalmanana,0) as turno_mañana, ifnull(totaltarde,0) as turno_tarde, (ifnull(totaltarde,0)+ifnull(totalmanana,0)) as total_diario, ((ifnull(totaltarde,0)+ifnull(totalmanana,0))*0.03) as porcentaje , ifnull(totalgastos,0) as gastos from Turnos left join ( select Turnos.fecha, SUM(Ventas.monto_venta) as totalmanana from Ventas join Turnos on ventas.Turnos_id_turno = Turnos.id_turno where Turnos.turno like 'Mañana' group by Turnos.fecha) T1 on Turnos.fecha = T1.fecha left join ( select Turnos.fecha, SUM(Ventas.monto_venta) as totaltarde from Ventas join Turnos on ventas.Turnos_id_turno = Turnos.id_turno where Turnos.turno like 'Tarde' group by Turnos.fecha) T2 on Turnos.fecha = T2.fecha left join ( select Turnos.fecha, SUM(Gastos.monto_gasto ) as totalgastos from Gastos join Turnos on Gastos.Turnos_id_turno = Turnos.id_turno group by Turnos.fecha) T3 on Turnos.fecha = T3.fecha where substr(Turnos.fecha,4,5) = ?"
        cursor=con.execute(consulta,[mes])
        return cursor.fetchall()
        pass

    def getReporteCancelados(self, dia):
        consulta = "select ventas.observacion , ventas.f_h_borrado , ventas.f_h_venta, ventas.monto_venta, usuarios.nombre_usu from ventas join turnos on ventas.Turnos_id_turno = turnos.id_turno join Usuarios on turnos.Usuarios_id_usu = usuarios.id_usu where ventas.borrado = 1 and turnos.fecha = ?"
        con=sqlite3.connect("data-ofelia.db")
        cursor=con.execute(consulta,[dia])
        return cursor.fetchall()
        pass

    #consultas
    def insert(self, parameter_list, tabla):
        con=sqlite3.connect("data-ofelia.db")
        cur = con.cursor()
        cur.execute(self.insert_case(tabla), parameter_list)
        con.commit()
    
    def update(self, parameter_list, tabla):
        con=sqlite3.connect("data-ofelia.db")
        cur = con.cursor()
        cur.execute(self.update_case(tabla), parameter_list)
        con.commit()

    def delete(self, id, tabla):
        con=sqlite3.connect("data-ofelia.db")
        cur = con.cursor()
        cur.execute(self.delete_case(tabla),[id])
        con.commit()

    def selectId(self, id, tabla):
        con=sqlite3.connect("data-ofelia.db")
        cursor=con.execute(self.selectId_case(tabla),[id])
        return cursor.fetchall()

    def selectAll(self, tabla, condiciones = None):
        con=sqlite3.connect("data-ofelia.db")
        if condiciones == None :
            cursor=con.execute("select * from "+tabla)
            return cursor.fetchall()
        else :
            consulta = "select * from "+tabla
            consulta += " where 1 = 1 "
            for i in range(len(condiciones)):
                if i%2==0 :
                    consulta += "and "+str(condiciones[i])
                else :
                    consulta += " = "+str(condiciones[i])
            cursor=con.execute(consulta)
            return cursor.fetchall()