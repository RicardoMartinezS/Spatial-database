import geopandas as gpd
import pandas as pd
from sqlalchemy import create_engine
import psycopg2
import tkinter as tk
from tkinter import filedialog, messagebox
import sys
import os

# -------------------------------
# Función para seleccionar archivo
# -------------------------------
def seleccionar_archivo():
    root = tk.Tk()
    root.withdraw()
    ruta = filedialog.askopenfilename(
        title="Seleccionar archivo GeoJSON",
        filetypes=[("GeoJSON Files", "*.geojson"), ("JSON Files", "*.json"), ("Todos los archivos", "*.*")]
    )
    root.destroy()
    return ruta

# -------------------------------
# Cargar GeoJSON con GeoPandas (CORREGIDO)
# -------------------------------
def cargar_geojson_geopandas(host, port, dbname, user, password, tabla, archivo):
    try:
        print(f"\n📌 Leyendo archivo GeoJSON con GeoPandas...")
        
        # Intentar diferentes métodos de lectura si hay problemas de codificación
        try:
            gdf = gpd.read_file(archivo)
        except UnicodeDecodeError:
            print("⚠️  Problema de codificación, intentando con latin-1...")
            gdf = gpd.read_file(archivo, encoding='latin-1')
        except Exception as e:
            print(f"⚠️  Error leyendo archivo: {e}")
            # Último intento con diferentes codificaciones
            for encoding in ['cp1252', 'iso-8859-1', 'utf-8']:
                try:
                    gdf = gpd.read_file(archivo, encoding=encoding)
                    print(f"✅ Cargado con codificación: {encoding}")
                    break
                except:
                    continue
            else:
                raise Exception("No se pudo leer el archivo con ninguna codificación")
        
        print(f"✅ Archivo cargado exitosamente")
        print(f"📊 Número de registros: {len(gdf)}")
        print(f"📊 Columnas: {list(gdf.columns)}")
        print(f"📊 Sistema de referencia: {gdf.crs}")
        
        # Limpiar datos problemáticos de QGIS
        print("📌 Limpiando datos de QGIS...")
        gdf_clean = limpiar_geodataframe(gdf)
        
        # Crear string de conexión
        connection_str = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
        
        print("📌 Conectando a la base de datos...")
        engine = create_engine(connection_str)
        
        # Verificar conexión
        with engine.connect() as conn:
            print("✅ Conexión a PostgreSQL establecida")
        
        print("📌 Insertando en la base de datos...")
        
        # Opciones para to_postgis
        gdf_clean.to_postgis(
            name=tabla,
            con=engine,
            if_exists='replace',  # 'replace', 'append', o 'fail'
            index=False,
            chunksize=1000,  # Para archivos grandes
        )
        
        print(f"\n✅ CARGA COMPLETADA CON GEOPANDAS")
        print(f"   • Registros insertados: {len(gdf_clean)}")
        print(f"   • Tabla creada: {tabla}")
        print(f"   • Columnas: {list(gdf_clean.columns)}")
        
        # Mostrar información de la tabla creada
        try:
            with engine.connect() as conn:
                result = conn.execute(f"SELECT COUNT(*) FROM {tabla}")
                count = result.scalar()
                print(f"   • Verificación en BD: {count} registros")
        except:
            pass
        
        engine.dispose()

    except Exception as e:
        print(f"\n❌ Error durante la carga:")
        print(f"   Tipo: {type(e).__name__}")
        print(f"   Mensaje: {str(e)}")
        return False
    
    return True

# -------------------------------
# Limpiar GeoDataFrame de valores problemáticos
# -------------------------------
def limpiar_geodataframe(gdf):
    """Limpia valores problemáticos de QGIS en un GeoDataFrame"""
    
    # Hacer una copia para no modificar el original
    gdf_clean = gdf.copy()
    
    # Para cada columna que no sea la geometría
    for col in gdf_clean.columns:
        if col != 'geometry':  # No tocar la columna de geometría
            # Reemplazar valores problemáticos con None
            gdf_clean[col] = gdf_clean[col].replace(['-', 'NULL', 'null', '', 'NaN', 'nan'], None)
            
            # Intentar convertir columnas que parecen numéricas
            if gdf_clean[col].dtype == 'object':  # Solo para columnas de texto
                try:
                    # Intentar convertir a numérico
                    converted = pd.to_numeric(gdf_clean[col], errors='coerce')
                    # Si se pudo convertir al menos un valor, usar la conversión
                    if not converted.isna().all():
                        gdf_clean[col] = converted
                except:
                    pass  # Mantener como está si falla
    
    print(f"✅ Datos limpiados. Columnas finales: {list(gdf_clean.columns)}")
    return gdf_clean

# -------------------------------
# Método alternativo si GeoPandas falla
# -------------------------------
def cargar_geojson_manual(host, port, dbname, user, password, tabla, archivo):
    """Método manual como fallback"""
    try:
        import json
        import chardet
        
        print("🔧 Usando método manual de carga...")
        
        # Leer y detectar codificación
        with open(archivo, 'rb') as f:
            raw_data = f.read()
            
        # Detectar codificación
        detection = chardet.detect(raw_data)
        encoding = detection['encoding'] or 'latin-1'
        print(f"📝 Codificación detectada: {encoding} (confianza: {detection['confidence']:.2f})")
        
        # Decodificar
        try:
            content = raw_data.decode(encoding)
        except:
            content = raw_data.decode('latin-1', errors='replace')
            
        data = json.loads(content)
        
        # Conectar a PostgreSQL
        conn = psycopg2.connect(
            host=host, port=port, dbname=dbname, 
            user=user, password=password
        )
        cur = conn.cursor()
        
        # Crear tabla si no existe
        cur.execute(f"""
            DROP TABLE IF EXISTS {tabla};
            CREATE TABLE {tabla} (
                id SERIAL PRIMARY KEY,
                geom GEOMETRY(GEOMETRY, 4326),
                properties JSONB
            );
        """)
        
        # Insertar features
        for i, feature in enumerate(data['features']):
            if i % 100 == 0:
                print(f"📊 Procesando registro {i}...")
                
            geometry = json.dumps(feature['geometry'])
            properties = json.dumps(feature.get('properties', {}))
            
            cur.execute(f"""
                INSERT INTO {tabla} (geom, properties)
                VALUES (ST_GeomFromGeoJSON(%s), %s)
            """, (geometry, properties))
        
        conn.commit()
        cur.close()
        conn.close()
        
        print(f"✅ Carga manual completada: {len(data['features'])} registros")
        return True
        
    except Exception as e:
        print(f"❌ Error en método manual: {e}")
        return False

# -------------------------------
# INTERFAZ GRÁFICA
# -------------------------------
def menu_principal():
    """Menú principal con interfaz gráfica"""
    
    root = tk.Tk()
    root.title("Cargar GeoJSON a PostGIS")
    root.geometry("550x500")
    
    # Variables
    host = tk.StringVar(value="localhost")
    port = tk.StringVar(value="5432")
    dbname = tk.StringVar()
    user = tk.StringVar()
    password = tk.StringVar()
    tabla = tk.StringVar()
    archivo_path = tk.StringVar()
    
    def seleccionar_archivo_gui():
        path = seleccionar_archivo()
        if path:
            archivo_path.set(path)
            nombre_archivo = os.path.basename(path)
            lbl_archivo.config(text=f"Archivo: {nombre_archivo}")
            
            # Previsualizar información del archivo
            try:
                gdf = gpd.read_file(path)
                info_text = f"Registros: {len(gdf)}\nColumnas: {list(gdf.columns)}\nCRS: {gdf.crs}"
                lbl_info.config(text=info_text)
            except Exception as e:
                try:
                    # Intentar con otra codificación
                    gdf = gpd.read_file(path, encoding='latin-1')
                    info_text = f"Registros: {len(gdf)}\nColumnas: {list(gdf.columns)}\nCRS: {gdf.crs}\n(Usando Latin-1)"
                    lbl_info.config(text=info_text)
                except:
                    lbl_info.config(text=f"Error al leer archivo. Posible problema de codificación.")
    
    def ejecutar_carga():
        if not all([dbname.get(), user.get(), tabla.get(), archivo_path.get()]):
            messagebox.showerror("Error", "Todos los campos marcados con * son obligatorios")
            return
        
        # Ocultar ventana durante la carga
        root.withdraw()
        
        success = False
        try:
            # Intentar con GeoPandas primero
            success = cargar_geojson_geopandas(
                host.get(), port.get(), dbname.get(), 
                user.get(), password.get(), tabla.get(), 
                archivo_path.get()
            )
            
            if not success:
                # Si falla, intentar método manual
                print("🔄 Intentando con método manual...")
                success = cargar_geojson_manual(
                    host.get(), port.get(), dbname.get(), 
                    user.get(), password.get(), tabla.get(), 
                    archivo_path.get()
                )
                
        except Exception as e:
            messagebox.showerror("Error", f"Error durante la carga:\n{str(e)}")
        finally:
            root.deiconify()
            
            if success:
                messagebox.showinfo("Éxito", "Carga completada correctamente")
            else:
                messagebox.showerror("Error", "No se pudo completar la carga. Revisa la consola para más detalles.")
    
    # INTERFAZ GRÁFICA
    tk.Label(root, text="CARGADOR GEOJSON A POSTGIS", 
             font=("Arial", 16, "bold"), fg="darkblue").pack(pady=15)
    
    frame = tk.Frame(root)
    frame.pack(padx=25, pady=10, fill="both", expand=True)
    
    # Campos de conexión
    campos = [
        ("Host:*", host, "localhost"),
        ("Puerto:*", port, "5432"),
        ("Base de datos:*", dbname, ""),
        ("Usuario:*", user, ""),
        ("Contraseña:", password, ""),
        ("Tabla:*", tabla, "")
    ]
    
    for i, (label, var, default) in enumerate(campos):
        tk.Label(frame, text=label, font=("Arial", 9)).grid(row=i, column=0, sticky="w", pady=6)
        entry = tk.Entry(frame, textvariable=var, font=("Arial", 9))
        entry.grid(row=i, column=1, sticky="ew", pady=6, padx=8)
        if default:
            var.set(default)
    
    frame.columnconfigure(1, weight=1)
    
    # Botón de archivo
    tk.Button(root, text="📁 Seleccionar GeoJSON", 
              command=seleccionar_archivo_gui, 
              bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
              padx=20, pady=8).pack(pady=15)
    
    lbl_archivo = tk.Label(root, text="No se ha seleccionado archivo", 
                          fg="red", font=("Arial", 9))
    lbl_archivo.pack(pady=2)
    
    lbl_info = tk.Label(root, text="", justify="left", font=("Arial", 8),
                       wraplength=500)
    lbl_info.pack(pady=8)
    
    # Botón de ejecución
    tk.Button(root, text="🚀 EJECUTAR CARGA", 
              command=ejecutar_carga, 
              bg="#2196F3", fg="white", font=("Arial", 12, "bold"),
              padx=30, pady=12).pack(pady=20)
    
    # Información de dependencias
    lbl_deps = tk.Label(root, text="Requiere: geopandas, sqlalchemy, psycopg2, geoalchemy2", 
                       font=("Arial", 7), fg="gray")
    lbl_deps.pack(side="bottom", pady=5)
    
    root.mainloop()

# -------------------------------
# Verificación de dependencias
# -------------------------------
def verificar_dependencias():
    """Verificar que todas las dependencias estén instaladas"""
    paquetes_requeridos = {
        'geopandas': 'geopandas',
        'sqlalchemy': 'sqlalchemy',
        'psycopg2': 'psycopg2',
        'geoalchemy2': 'geoalchemy2',
        'pandas': 'pandas'
    }
    
    faltantes = []
    for nombre, paquete in paquetes_requeridos.items():
        try:
            __import__(paquete)
            print(f"✅ {nombre}")
        except ImportError:
            print(f"❌ {nombre}")
            faltantes.append(paquete)
    
    if faltantes:
        print(f"\n❌ Faltan paquetes. Instala con:")
        print(f"pip install {' '.join(faltantes)}")
        return False
    
    return True

# -------------------------------
# PROGRAMA PRINCIPAL
# -------------------------------
if __name__ == "__main__":
    print("="*60)
    print("       CARGADOR GEOJSON A POSTGIS")
    print("="*60)
    print("Verificando dependencias...")
    
    if not verificar_dependencias():
        sys.exit(1)
    
    print("\n✅ Todas las dependencias están instaladas")
    print("🚀 Iniciando interfaz...")
    
    menu_principal()