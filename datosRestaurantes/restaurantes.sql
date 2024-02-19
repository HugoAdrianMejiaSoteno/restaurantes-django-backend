-- Primero creamos la base de datos restaurantes en postgresql

--como vamos a usar la extension de uuid
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";


-- Crear tabla de restaurantes
CREATE TABLE restaurantes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    rating INTEGER,
    imagen TEXT,
    nombre TEXT
);

-- Crear tabla de direcciones
CREATE TABLE direcciones (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    restaurante_id UUID UNIQUE,
    calle TEXT,
    ciudad TEXT,
    estado TEXT,
    latitud DOUBLE PRECISION,
    longitud DOUBLE PRECISION,
    FOREIGN KEY (restaurante_id) REFERENCES restaurantes(id) ON DELETE CASCADE
);

-- Crear tabla de contactos
CREATE TABLE contactos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    restaurante_id UUID UNIQUE,
    sitio_web TEXT,
    email TEXT,
    telefono TEXT,
    FOREIGN KEY (restaurante_id) REFERENCES restaurantes(id) ON DELETE CASCADE
);


-- Insertar el restaurante
INSERT INTO restaurantes (rating, imagen, nombre) VALUES (4, 'ruta/a/imagen.jpg', 'Restaurante Ejemplo');

-- Insertar la dirección del restaurante
INSERT INTO direcciones (restaurante_id, calle, ciudad, estado, latitud, longitud) 
VALUES (restaurante_id, 'Calle Principal 123', 'Ciudad de Ejemplo', 'Estado de Ejemplo', 123.456, -78.910);

-- Insertar el contacto del restaurante
INSERT INTO contactos (restaurante_id, sitio_web, email, telefono) 
VALUES (restaurante_id, 'www.ejemplo.com', 'info@ejemplo.com', '+123456789');


-- Esta seria la consulta que se tendria que hacer para ver los datos del registro que hicimos

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
WHERE restaurantes.id = '8c525c7c-a7e3-4872-aa7a-dede2c639d2e';