select * from restaurantes;
select * from direcciones;
select * from contactos;

-- Insertar la dirección del restaurante
INSERT INTO direcciones (restaurante_id, calle, ciudad, estado, latitud, longitud) 
VALUES ('a800b93f-a55e-4c6b-9ccd-c709daf4c95f', 'Calle Principal 123', 'Ciudad de Ejemplo', 'Estado de Ejemplo', 123.456, -78.910);

-- Insertar el contacto del restaurante
INSERT INTO contactos (restaurante_id, sitio_web, email, telefono) 
VALUES ('a800b93f-a55e-4c6b-9ccd-c709daf4c95f', 'www.ejemplo.com', 'info@ejemplo.com', '+123456789');

SELECT restaurantes.id AS restaurante_id,
       restaurantes.rating,
       restaurantes.imagen,
       restaurantes.nombre AS nombre_restaurante,
       direcciones.calle,
       direcciones.ciudad,
       direcciones.estado,
       direcciones.latitud,
       direcciones.longitud,
       contactos.sitio_web,
       contactos.email,
       contactos.telefono
FROM restaurantes
LEFT JOIN direcciones ON restaurantes.id = direcciones.restaurante_id
LEFT JOIN contactos ON restaurantes.id = contactos.restaurante_id
WHERE restaurantes.id = 'a800b93f-a55e-4c6b-9ccd-c709daf4c95f';

UPDATE restaurantes
SET rating = 10
WHERE id = '5167010c-db6d-4b7f-9c34-fc2fcc209f99';

DELETE FROM restaurantes 
WHERE id = '5167010c-db6d-4b7f-9c34-fc2fcc209f99';