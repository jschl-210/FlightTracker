CREATE SCHEMA rh;
ALTER SCHEMA rh OWNER to postgres;

CREATE EXTENSION postgis;
CREATE EXTENSION postgis_raster;
--CREATE EXTENSION postgis_sfcgal; --not currently supported in the bitnami image
CREATE EXTENSION fuzzystrmatch;
CREATE EXTENSION address_standardizer;
CREATE EXTENSION address_standardizer_data_us;
CREATE EXTENSION postgis_tiger_geocoder;
CREATE EXTENSION postgis_topology;