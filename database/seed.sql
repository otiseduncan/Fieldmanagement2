INSERT INTO users (email, full_name, hashed_password, roles)
VALUES
    ('admin@example.com', 'Admin User', crypt('admin123', gen_salt('bf')), '["admin"]'),
    ('cmr@example.com', 'CMR User', crypt('cmr12345', gen_salt('bf')), '["cmr"]'),
    ('tech@example.com', 'Technician User', crypt('tech12345', gen_salt('bf')), '["technician"]')
ON CONFLICT (email) DO NOTHING;

INSERT INTO clients (name, primary_contact, email, phone, address)
VALUES
    ('Metro Collision', 'Janet Howard', 'janet@metrocollision.com', '+1-555-222-1212', '123 Main St, Austin, TX'),
    ('Premier Auto', 'Rush Cole', 'rush@premierauto.com', '+1-555-333-1313', '88 Ocean Ave, Tampa, FL')
ON CONFLICT (name) DO NOTHING;

INSERT INTO jobs (ro_number, vin, status, client_notes, metadata, technician_id, client_id)
SELECT
    'RO-1001',
    '1HGCM82633A123456',
    'pending',
    'Customer requests ADAS calibration after bumper replacement.',
    '{"region": "south", "service_type": "calibration"}'::jsonb,
    NULL,
    id
FROM clients
WHERE name = 'Metro Collision'
ON CONFLICT DO NOTHING;

INSERT INTO jobs (ro_number, vin, status, client_notes, metadata, technician_id, client_id)
SELECT
    'RO-1002',
    '2C3CDXHG8FH123456',
    'assigned',
    'Vehicle ready at bay 4.',
    '{"region": "east", "service_type": "windshield"}'::jsonb,
    (SELECT id FROM users WHERE email = 'tech@example.com'),
    id
FROM clients
WHERE name = 'Premier Auto'
ON CONFLICT DO NOTHING;
