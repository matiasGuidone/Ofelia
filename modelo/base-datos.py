import sqlite3

conexion=sqlite3.connect("data-ofelia.db")
try:
    conexion.execute("""create table CategoriaGastos (
                              id_cat_gasto integer primary key autoincrement,
                              nombre_cat_gasto text
                        )""")

    conexion.execute("""create table SubcategoriaGastos (
                              id_subcat_gasto integer primary key autoincrement,
                              nomb_subcat text,
                              descr_subcat text,
                              empleado_id integer,
                              proveedor_id integer,
                              sueldo real,
                              adelanto real,
                              contacto text,
                              f_h_adelanto integer,
                              f__h_pago integer,
                              CategoriaGastos_id_cat_gasto integer,
                              cuenta real,
                              FOREIGN KEY(CategoriaGastos_id_cat_gasto) REFERENCES CategoriaGastos(id_cat_gasto)
                        )""")

    conexion.execute("""create table Usuarios (
                              id_usu integer primary key autoincrement,
                              nombre_usu text,
                              tipo_usu text,
                              contraseña text
                        )""")

    conexion.execute("""create table Turnos (
                              id_turno integer primary key autoincrement,
                              turno text,
                              caja_ini_turno real,
                              fecha integer,
                              f_h_apertura integer,
                              f_h_cierre integer,
                              Usuarios_id_usu integer,
                              FOREIGN KEY(Usuarios_id_usu) REFERENCES Usuarios(id_usu)
                        )""")

    conexion.execute("""create table TiposDePagos (
                              id_tipo_pago integer primary key autoincrement,
                              nombre_tipo_pago text
                        )""")

    conexion.execute("""create table Ventas (
                              id_venta integer primary key autoincrement,
                              f_h_venta integer,
                              monto_venta real,
                              borrado integer,
                              f_h_borrado integer,
                              observacion text,
                              Turnos_id_turno integer,
                              TiposDePagos_id_tipo_pago integer,
                              caja integer,
                              FOREIGN KEY(Turnos_id_turno) REFERENCES Turnos(id_turno),
                              FOREIGN KEY(TiposDePagos_id_tipo_pago) REFERENCES TiposDePagos(id_tipo_pago)
                        )""")

    conexion.execute("""create table CategoriaProductos (
                              id_cat_prod integer primary key autoincrement,
                              descr_categ text
                        )""")

    conexion.execute("""create table ProductosPorMayor (
                              id_productos integer primary key autoincrement,
                              nombre_producto text,
                              monto_producto real,
                              CategoriaProductos_id_cat_prod integer,
                              FOREIGN KEY(CategoriaProductos_id_cat_prod) REFERENCES CategoriaProductos(id_cat_prod)
                        )""")

    conexion.execute("""create table Gastos (
                              id_gasto integer primary key autoincrement,
                              monto_gasto real,
                              observacion_gasto text,
                              TiposDePagos_id_tipo_pago integer,
                              Turnos_id_turno integer,
                              SubcategoriaGastos_id_subcat_gasto integer,
                              FOREIGN KEY(TiposDePagos_id_tipo_pago) REFERENCES TiposDePagos(id_tipo_pago),
                              FOREIGN KEY(Turnos_id_turno) REFERENCES Turnos(id_turno)
                              FOREIGN KEY(SubcategoriaGastos_id_subcat_gasto) REFERENCES SubcategoriaGastos(id_subcat_gasto)
                        )""")
   
    print("se creo la base de datos")                        
except sqlite3.OperationalError:
    print("La tabla articulos ya existe")                    
conexion.close()

 