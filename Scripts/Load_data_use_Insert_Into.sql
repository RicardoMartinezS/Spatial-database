--Paisaje -- 
ALTER TABLE paisaje 
ALTER COLUMN nombre TYPE VARCHAR(40);

INSERT INTO paisaje (nombre) VALUES
('Montaña fluvio-gravitacional'),
('Cuerpo de agua'),
('Lomerío fluvio-gravitacional'),
('Montaña plegada'),
('Piedemonte mixto'),
('Planicie aluvial'),
('Valle'),
('Altiplanicie estructural'),
('Lomerío estructural'),
('Montaña glacio-estructural'),
('Montaña plegada fluvio-gravitacional'),
('Zona urbana'),
('Peniplanicie'),
('Lomerío'),
('Macizo'),
('Altillanura'),
('Planicie aluvial'),
('Valle aluvial'),
('Macizo estructural denudativo'),
('Peniplanicie denudativa'),
('Lomerío erosional'),
('Altillanura'),
('Montaña estructural erosional');

--Clima -- 

ALTER TABLE clima 
ALTER COLUMN nombre_clima TYPE VARCHAR(50);

INSERT INTO clima (nombre_clima) VALUES
('Medio pluvial y cálido muy húmedo'),
('Cuerpo de agua'),
('Cálido muy húmedo'),
('Cálido húmedo a subhúmedo'),
('Frío pluvial'),
('Cálido y medio muy húmedo'),
('Medio y cálido muy húmedo'),
('Cálido húmedo y muy húmedo'),
('Cálido húmedo'),
('Extremadamente frío pluvial y muy frío muy húmedo'),
('Zona urbana'),
('Cálido húmedo a muy húmedo'),
('Cálido, húmedo'),
('Templado muy húmedo y húmedo'),
('Frío muy húmedo y húmedo');


--Relieve -- 
ALTER TABLE relieve 
ALTER COLUMN nombre_relieve TYPE VARCHAR(70);

INSERT INTO relieve (nombre_relieve) VALUES ('Filas y vigas');
INSERT INTO relieve (nombre_relieve) VALUES ('Cuerpo de agua');
INSERT INTO relieve (nombre_relieve) VALUES ('Lomas');
INSERT INTO relieve (nombre_relieve) VALUES ('Colinas y lomas');
INSERT INTO relieve (nombre_relieve) VALUES ('Lomas y colinas asociadas con glacís mixtos');
INSERT INTO relieve (nombre_relieve) VALUES ('Cuestas');
INSERT INTO relieve (nombre_relieve) VALUES ('Abanicos subactuales');
INSERT INTO relieve (nombre_relieve) VALUES ('Plano de inundación');
INSERT INTO relieve (nombre_relieve) VALUES ('Vallecitos coluvio-aluviales');
INSERT INTO relieve (nombre_relieve) VALUES ('Mesas y superficies onduladas');
INSERT INTO relieve (nombre_relieve) VALUES ('Terraza agradacional nivel 1');
INSERT INTO relieve (nombre_relieve) VALUES ('Terraza agradacional nivel 2');
INSERT INTO relieve (nombre_relieve) VALUES ('Cuestas y crestones');
INSERT INTO relieve (nombre_relieve) VALUES ('Campo de artesas y circos. Espinazos, barras y cuestas');
INSERT INTO relieve (nombre_relieve) VALUES ('Crestas y crestones');
INSERT INTO relieve (nombre_relieve) VALUES ('Crestas, crestones y espinazos');
INSERT INTO relieve (nombre_relieve) VALUES ('Filas y vigas, crestas y crestones');
INSERT INTO relieve (nombre_relieve) VALUES ('Terrazas');
INSERT INTO relieve (nombre_relieve) VALUES ('Abanicos subcrecientes');
INSERT INTO relieve (nombre_relieve) VALUES ('Abanicos recientes');
INSERT INTO relieve (nombre_relieve) VALUES ('Mesas y terrazas agradacional nivel superior');
INSERT INTO relieve (nombre_relieve) VALUES ('Terraza agradacional nivel inferior');
INSERT INTO relieve (nombre_relieve) VALUES ('Terraza agradacional nivel 3');
INSERT INTO relieve (nombre_relieve) VALUES ('Terraza agradacional nivel 4 (inferior)');
INSERT INTO relieve (nombre_relieve) VALUES ('Zona urbana');
INSERT INTO relieve (nombre_relieve) VALUES ('Peniplanos');
INSERT INTO relieve (nombre_relieve) VALUES ('Mesas y cuestas');
INSERT INTO relieve (nombre_relieve) VALUES ('Afloramientos rocosos');
INSERT INTO relieve (nombre_relieve) VALUES ('Ondulaciones');
INSERT INTO relieve (nombre_relieve) VALUES ('Vallecitos');
INSERT INTO relieve (nombre_relieve) VALUES ('Lomas y colinas');
INSERT INTO relieve (nombre_relieve) VALUES ('Terraza media');
INSERT INTO relieve (nombre_relieve) VALUES ('Terraza alta');
INSERT INTO relieve (nombre_relieve) VALUES ('Terrazas medias');
INSERT INTO relieve (nombre_relieve) VALUES ('Valles estrechos con influencia coluvioaluvial');
INSERT INTO relieve (nombre_relieve) VALUES ('Ondulaciones (superficies planas y planos inclinados)');
INSERT INTO relieve (nombre_relieve) VALUES ('Valles estrechos');
INSERT INTO relieve (nombre_relieve) VALUES ('Terrazas bajas');
INSERT INTO relieve (nombre_relieve) VALUES ('Ondulaciones (superficies ligeramente planas y planos inclinados)');
INSERT INTO relieve (nombre_relieve) VALUES ('Colinas');
INSERT INTO relieve (nombre_relieve) VALUES ('Escarpes y afloramientos rocosos');
INSERT INTO relieve (nombre_relieve) VALUES ('Glacís');
INSERT INTO relieve (nombre_relieve) VALUES ('Terrazas altas');
INSERT INTO relieve (nombre_relieve) VALUES ('Peniplanos altos (ondulados y localmente alomados)');
INSERT INTO relieve (nombre_relieve) VALUES ('Hogbacks y espinazos');
INSERT INTO relieve (nombre_relieve) VALUES ('Crestones)');




select * 
from relieve