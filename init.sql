CREATE TABLE incidents (
    id SERIAL PRIMARY KEY,
    reporter VARCHAR(100),
    description TEXT,
    status VARCHAR(20) DEFAULT 'pendiente',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO incidents (reporter, description, status) VALUES 
('Juan Pérez', 'La impresora no imprime en color.', 'pendiente'),
('María López', 'La conexión a internet es muy lenta.', 'pendiente'),
('Carlos Gómez', 'El sistema no responde al intentar abrir aplicaciones.', 'pendiente'),
('Ana Martínez', 'El teclado no responde al presionar algunas teclas.', 'pendiente'),
('Luis Fernández', 'La pantalla de la computadora está parpadeando.', 'pendiente'),
('Ricardo Sánchez', 'No puedo acceder a la red Wi-Fi.', 'pendiente'),
('Laura Torres', 'El software de contabilidad se cierra inesperadamente.', 'pendiente'),
('Pedro Ramírez', 'El monitor no se enciende.', 'pendiente'),
('Julia Rodríguez', 'La impresora se atasca con frecuencia.', 'pendiente'),
('Oscar García', 'El sonido no funciona en el equipo.', 'pendiente'),
('Patricia Pérez', 'El sistema se congela al intentar abrir archivos grandes.', 'pendiente'),
('Eduardo Díaz', 'No puedo acceder a la red interna de la empresa.', 'pendiente'),
('Susana Jiménez', 'El mouse no se mueve correctamente.', 'pendiente'),
('Mario Delgado', 'La computadora se reinicia por sí sola.', 'pendiente'),
('Carolina Ruiz', 'La luz del teclado está apagada.', 'pendiente'),
('Javier Mendoza', 'El software de video no reproduce archivos multimedia.', 'pendiente'),
('Teresa Gómez', 'El servidor de archivos está caído.', 'pendiente'),
('Fernando García', 'El monitor tiene líneas horizontales.', 'pendiente'),
('Isabel López', 'El sistema se congela al intentar realizar una actualización.', 'pendiente'),
('Carlos Martínez', 'No puedo acceder al servidor de correo electrónico.', 'pendiente');