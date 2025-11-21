-- Create user
CREATE USER geo_owner WITH PASSWORD 'Password_example';

-- Create database with owner
CREATE DATABASE BDE
    WITH OWNER = geo_owner
    ENCODING 'UTF8'
    LC_COLLATE='es_CO.UTF-8'
    LC_CTYPE='es_CO.UTF-8'
    TEMPLATE=template0;


-- Activate PostGIS
CREATE EXTENSION postgis;
CREATE EXTENSION postgis_topology;



