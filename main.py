from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import mysql.connector
import hashlib

app = FastAPI()

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="reciclaje"
)
cursor = mydb.cursor()

# Modelos Pydantic para cada tabla
class ClienteModel(BaseModel):
    nombre: str
    telefono: str
    direccion: str

class PedidoModel(BaseModel):
    id_cliente: int
    fecha_pedido: str  # formato 'YYYY-MM-DD'
    estado: str

class FacturaModel(BaseModel):
    id_pedido: int
    id_cliente: int
    tipo_mt: str
    precio_por_k: float
    total: float

class DomiciliarioModel(BaseModel):
    id_factura: int
    nombre: str
    tipo_vehiculo: str
    capacidad_carga: float
    contacto: str

class EmpleadosModel(BaseModel):
    nombre: str
    cargo: str

class SistemaModel(BaseModel):
    id_empleados: int
    usuarios_em: str
    contrasena_em: str

class ProveedorModel(BaseModel):
    nombre: str
    tipo_insumo: str
    correo: str

class RecepcionMaterialModel(BaseModel):
    id_proveedor: int
    fecha_recepcion: str  # formato 'YYYY-MM-DD'
    precio_por_k: float

class MaterialModel(BaseModel):
    id_recepcion: int
    tipo_mt: str
    cantidad_mt: float
    descripcion: str

class InventarioModel(BaseModel):
    id_material: int
    id_pedido: int
    id_proveedor: int
    fecha_ac: str  # formato 'YYYY-MM-DD'
    cantidad: float

@app.post("/material", status_code=status.HTTP_201_CREATED)
def create_material(material: MaterialModel):
    query = "INSERT INTO material (id_recepcion, tipo_mt, cantidad_mt, descripcion) VALUES (%s, %s, %s, %s)"
    values = (material.id_recepcion, material.tipo_mt, material.cantidad_mt, material.descripcion)
    try:
        cursor.execute(query, values)
        mydb.commit()
        return {"message": "Material creado exitosamente"}
    except mysql.connector.Error as err:
        print("MySQL Error:", err)  # Agrega esta línea
        raise HTTPException(status_code=400, detail=str(err))

@app.post("/inventario", status_code=status.HTTP_201_CREATED)
def create_inventario(inventario: InventarioModel):
    query = "INSERT INTO inventario (id_material, id_pedido, id_proveedor, fecha_ac, cantidad) VALUES (%s, %s, %s, %s, %s)"
    values = (inventario.id_material, inventario.id_pedido, inventario.id_proveedor, inventario.fecha_ac, inventario.cantidad)
    try:
        cursor.execute(query, values)
        mydb.commit()
        return {"message": "Inventario creado exitosamente"}
    except mysql.connector.Error as err:
        print("MySQL Error:", err)  # Agrega esta línea
        raise HTTPException(status_code=400, detail=str(err))

class PagoProveedorModel(BaseModel):
    id_proveedor: int
    total_pago: float
    fecha_pago: str  # formato 'YYYY-MM-DD'
    estado: str

@app.post("/pago_proveedor", status_code=status.HTTP_201_CREATED)
def create_pago_proveedor(pago: PagoProveedorModel):
    query = "INSERT INTO pago_proveedor (id_proveedor, total_pago, fecha_pago, estado) VALUES (%s, %s, %s, %s)"
    values = (pago.id_proveedor, pago.total_pago, pago.fecha_pago, pago.estado)
    try:
        cursor.execute(query, values)
        mydb.commit()
        return {"message": "Pago a proveedor creado exitosamente"}
    except mysql.connector.Error as err:
        print("MySQL Error:", err)  # Agrega esta línea
        raise HTTPException(status_code=400, detail=str(err))

@app.post("/cliente", status_code=status.HTTP_201_CREATED)
def create_cliente(cliente: ClienteModel):
    query = "INSERT INTO cliente (nombre, telefono, direccion) VALUES (%s, %s, %s)"
    values = (cliente.nombre, cliente.telefono, cliente.direccion)
    try:
        cursor.execute(query, values)
        mydb.commit()
        return {"message": "Cliente creado exitosamente"}
    except mysql.connector.Error as err:
        print("MySQL Error:", err)  # Agrega esta línea
        raise HTTPException(status_code=400, detail=str(err))

@app.post("/pedido", status_code=status.HTTP_201_CREATED)
def create_pedido(pedido: PedidoModel):
    query = "INSERT INTO pedido (id_cliente, fecha_pedido, estado) VALUES (%s, %s, %s)"
    values = (pedido.id_cliente, pedido.fecha_pedido, pedido.estado)
    try:
        cursor.execute(query, values)
        mydb.commit()
        return {"message": "Pedido creado exitosamente"}
    except mysql.connector.Error as err:
        print("MySQL Error:", err)  # Agrega esta línea
        raise HTTPException(status_code=400, detail=str(err))

@app.post("/factura", status_code=status.HTTP_201_CREATED)
def create_factura(factura: FacturaModel):
    query = "INSERT INTO factura (id_pedido, id_cliente, tipo_mt, precio_por_k, total) VALUES (%s, %s, %s, %s, %s)"
    values = (factura.id_pedido, factura.id_cliente, factura.tipo_mt, factura.precio_por_k, factura.total)
    try:
        cursor.execute(query, values)
        mydb.commit()
        return {"message": "Factura creada exitosamente"}
    except mysql.connector.Error as err:
        print("MySQL Error:", err)  # Agrega esta línea
        raise HTTPException(status_code=400, detail=str(err))

@app.post("/domiciliario", status_code=status.HTTP_201_CREATED)
def create_domiciliario(domiciliario: DomiciliarioModel):
    query = "INSERT INTO domiciliario (id_factura, nombre, tipo_vehiculo, capacidad_carga, contacto) VALUES (%s, %s, %s, %s, %s)"
    values = (domiciliario.id_factura, domiciliario.nombre, domiciliario.tipo_vehiculo, domiciliario.capacidad_carga, domiciliario.contacto)
    try:
        cursor.execute(query, values)
        mydb.commit()
        return {"message": "Domiciliario creado exitosamente"}
    except mysql.connector.Error as err:
        print("MySQL Error:", err)  # Agrega esta línea
        raise HTTPException(status_code=400, detail=str(err))

@app.post("/empleados", status_code=status.HTTP_201_CREATED)
def create_empleados(empleado: EmpleadosModel):
    query = "INSERT INTO empleados (nombre, cargo) VALUES (%s, %s)"
    values = (empleado.nombre, empleado.cargo)
    try:
        cursor.execute(query, values)
        mydb.commit()
        return {"message": "Empleado creado exitosamente"}
    except mysql.connector.Error as err:
        print("MySQL Error:", err)  # Agrega esta línea
        raise HTTPException(status_code=400, detail=str(err))

@app.post("/sistema", status_code=status.HTTP_201_CREATED)
def create_sistema(sistema: SistemaModel):
    query = "INSERT INTO sistema (id_empleados, usuarios_em, contrasena_em) VALUES (%s, %s, %s)"
    values = (sistema.id_empleados, sistema.usuarios_em, sistema.contrasena_em)
    try:
        cursor.execute(query, values)
        mydb.commit()
        return {"message": "Sistema creado exitosamente"}
    except mysql.connector.Error as err:
        print("MySQL Error:", err)  # Agrega esta línea
        raise HTTPException(status_code=400, detail=str(err))

@app.post("/proveedor", status_code=status.HTTP_201_CREATED)
def create_proveedor(proveedor: ProveedorModel):
    query = "INSERT INTO proveedor (nombre, tipo_insumo, correo) VALUES (%s, %s, %s)"
    values = (proveedor.nombre, proveedor.tipo_insumo, proveedor.correo)
    try:
        cursor.execute(query, values)
        mydb.commit()
        return {"message": "Proveedor creado exitosamente"}
    except mysql.connector.Error as err:
        print("MySQL Error:", err)  # Agrega esta línea
        raise HTTPException(status_code=400, detail=str(err))

@app.post("/recepcion_material", status_code=status.HTTP_201_CREATED)
def create_recepcion_material(recepcion: RecepcionMaterialModel):
    query = "INSERT INTO recepcion_material (id_proveedor, fecha_recepcion, precio_por_k) VALUES (%s, %s, %s)"
    values = (recepcion.id_proveedor, recepcion.fecha_recepcion, recepcion.precio_por_k)
    try:
        cursor.execute(query, values)
        mydb.commit()
        return {"message": "Recepción de material creada exitosamente"}
    except mysql.connector.Error as err:
        print("MySQL Error:", err)  # Agrega esta línea
        raise HTTPException(status_code=400, detail=str(err))
