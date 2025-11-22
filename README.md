# Spatial-database

Repository for the spatial database exercise using PostgreSQL + PostGIS (Spatial Databases — Master's in Geomatics, UNAL).

## Main contents
- SQL scripts:
  - Scripts/Create_Database.sql
  - Scripts/Create_Tables.sql
  - Scripts/Load_data_use_Insert_Into.sql
- GeoJSON loader script:
  - Scripts/Load_geojson.py
- Example data and auxiliary SQL (not included as links due to size):
  - Data/TablesSQL/*.sql
  - Data/Geojson/*.geojson

## Requirements
- PostgreSQL with PostGIS extension installed.
- psql client.
- Python 3 for the GeoJSON loader (optional).
- Privileges to create databases and extensions.

## Workflow (summary)
1. Create the database and enable PostGIS:
   - psql -f Scripts/Create_Database.sql
2. Create spatial tables:
   - psql -d <DB_NAME> -f Scripts/Create_Tables.sql
   - Tables typically use SRID 4326 for geometry columns.
3. Load tabular data (INSERT statements):
   - psql -d <DB_NAME> -f Scripts/Load_data_use_Insert_Into.sql
4. Load GeoJSON data (optional):
   - Use the Python loader: python Scripts/Load_geojson.py --db <DB_NAME> --user <USER> --password <PW>
   - Or use ogr2ogr, for example:
     - ogr2ogr -f "PostgreSQL" PG:"dbname=<DB_NAME> user=<USER> password=<PW>" Data/Geojson/Departamento.geojson -nln departamento -append -nlt MULTIPOLYGON -a_srs EPSG:4326

## Notes
- Ensure geometry column types match the GeoJSON geometry (Point, LineString, Polygon, Multi*).
- Review Scripts/Create_Tables.sql for primary/foreign keys and exact geometry definitions.
- Use Data/TablesSQL for supplemental inserts or fixes when needed.

## Quick commands
- Create DB and tables:
  - psql -f Scripts/Create_Database.sql
  - psql -d <DB_NAME> -f Scripts/Create_Tables.sql
- Load data:
  - psql -d <DB_NAME> -f Scripts/Load_data_use_Insert_Into.sql
