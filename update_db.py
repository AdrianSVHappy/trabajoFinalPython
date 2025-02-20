from dbInit import Base, engine

print("🔄 Eliminando tablas...")
Base.metadata.drop_all(engine)  # Elimina todas las tablas
print("✅ Tablas eliminadas.")

print("🛠 Creando nuevas tablas...")
Base.metadata.create_all(engine)  # Vuelve a crearlas con la nueva estructura
print("✅ Base de datos actualizada con éxito.")
