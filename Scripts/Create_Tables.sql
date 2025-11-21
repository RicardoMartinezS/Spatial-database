-- Create Tables

CREATE TABLE paisaje (
  id_paisaje SERIAL PRIMARY KEY,
  nombre VARCHAR(30)
);

CREATE TABLE clima (
  id_clima SERIAL PRIMARY KEY,
  nombre_clima VARCHAR(20)
);

CREATE TABLE relieve (
  id_relieve SERIAL PRIMARY KEY,
  nombre_relieve VARCHAR(30)
);

CREATE TABLE caracteristica_suelo (
  id_caracteristica SERIAL PRIMARY KEY,
  descripcion VARCHAR(30)
);

CREATE TABLE componente_suelo (
  id_componente SERIAL PRIMARY KEY,
  descripcion VARCHAR(30)
);

CREATE TABLE suelo (
  id_suelo SERIAL PRIMARY KEY,
  ucs VARCHAR(3),
  ucs_f VARCHAR(5),
  id_paisaje INTEGER REFERENCES paisaje(id_paisaje),
  id_clima INTEGER REFERENCES clima(id_clima),
  id_relieve INTEGER REFERENCES relieve(id_relieve),
  id_caracteristica INTEGER REFERENCES caracteristica_suelo(id_caracteristica),
  id_componente INTEGER REFERENCES componente_suelo(id_componente),
  perfil VARCHAR(5),
  porcentaje VARCHAR(20),
  area_ha DOUBLE PRECISION,
  geometry geometry(Polygon, 4326)
);


CREATE TABLE departamento (
  id_departamento SERIAL PRIMARY KEY,
  cod_dane_dep VARCHAR(2) UNIQUE NOT NULL,
  nombre_dep VARCHAR(20) NOT NULL,
  geometry geometry(MultiPolygon, 4326)
);

CREATE TABLE municipio (
  id_municipio SERIAL PRIMARY KEY,
  id_departamento INTEGER REFERENCES departamento(id_departamento),
  cod_dane_mun VARCHAR(5) UNIQUE NOT NULL,
  nombre_mun VARCHAR(30) NOT NULL,
  geometry geometry(MultiPolygon, 4326)
);

CREATE TABLE vereda (
  id_vereda SERIAL PRIMARY KEY,
  id_municipio INTEGER REFERENCES municipio(id_municipio),
  nombre_ver VARCHAR(30) NOT NULL,
  geometry geometry(MultiPolygon, 4326)
);


CREATE TABLE via (
  id_via SERIAL PRIMARY KEY,
  id_vereda INTEGER REFERENCES vereda(id_vereda),
  nombre_via VARCHAR(20),
  longitud DOUBLE PRECISION,
  categoria_via INTEGER,
  sentido INTEGER,
  geometry geometry(LineString, 4326)
);


CREATE TABLE drenajes (
  id_drenaje SERIAL PRIMARY KEY,
  nombre VARCHAR(20),
  longitud DOUBLE PRECISION,
  id_vereda INTEGER REFERENCES vereda(id_vereda),
  id_tipo_drenaje INTEGER,
  geometry geometry(LineString, 4326)
);


CREATE TABLE resguardo_indigena (
  id_resguardo SERIAL PRIMARY KEY,
  nombre_resguardo VARCHAR(30) NOT NULL,
  id_vereda INTEGER REFERENCES vereda(id_vereda),
  geometry geometry(MultiPolygon, 4326)
);


CREATE TABLE mineria (
  id_mineria SERIAL PRIMARY KEY,
  anio INTEGER,
  id_vereda INTEGER REFERENCES vereda(id_vereda),
  geometry geometry(Polygon, 4326)
);

CREATE TABLE zona_urbana (
  id_zona SERIAL PRIMARY KEY,
  anio INTEGER,
  id_vereda INTEGER REFERENCES vereda(id_vereda),
  geometry geometry(Polygon, 4326)
);


CREATE TABLE edificaciones_google_openbuildings (
  id_edificacion SERIAL PRIMARY KEY,
  area_m2 DOUBLE PRECISION,
  confidence DOUBLE PRECISION,
  geometry geometry(Polygon, 4326),
  id_vereda INTEGER REFERENCES vereda(id_vereda)
);


CREATE TABLE zona_protegida (
  id_zona SERIAL PRIMARY KEY,
  nombre_zona VARCHAR(30) NOT NULL,
  geometry geometry(Polygon, 4326),
  id_vereda INTEGER REFERENCES vereda(id_vereda)
);


CREATE TABLE puntos_deforestados (
  id_punto SERIAL PRIMARY KEY,
  latitud DOUBLE PRECISION NOT NULL,
  longitud DOUBLE PRECISION NOT NULL,
  geometry geometry(Point, 4326),
  anio INTEGER NOT NULL,
  id_vereda INTEGER REFERENCES vereda(id_vereda),
  id_suelo INTEGER REFERENCES suelo(id_suelo)
);

