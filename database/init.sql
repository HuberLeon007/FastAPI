-- Inventarverwaltung Database Schema-- Inventarverwaltung Database Schema

-- PostgreSQL Initialisierung-- PostgreSQL Initialisierung



CREATE TABLE IF NOT EXISTS inventoryitem (CREATE TABLE IF NOT EXISTS inventory_item (

    id SERIAL PRIMARY KEY,    id SERIAL PRIMARY KEY,

    name VARCHAR(255) NOT NULL,    name VARCHAR(255) NOT NULL,

    category VARCHAR(100),    description TEXT,

    status VARCHAR(50),    quantity INTEGER DEFAULT 0 NOT NULL,

    location VARCHAR(255),    location VARCHAR(255),

    assigned_to VARCHAR(255)    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL

););



-- Index für häufige Abfragen-- Index für häufige Abfragen nach Location

CREATE INDEX IF NOT EXISTS idx_inventory_location ON inventoryitem(location);CREATE INDEX IF NOT EXISTS idx_inventory_location ON inventory_item(location);

CREATE INDEX IF NOT EXISTS idx_inventory_status ON inventoryitem(status);

CREATE INDEX IF NOT EXISTS idx_inventory_assigned ON inventoryitem(assigned_to);-- Beispieldaten (optional)

INSERT INTO inventory_item (name, description, quantity, location) VALUES

-- Beispieldaten (optional)    ('Laptop Dell XPS', 'Business Laptop mit 16GB RAM', 5, 'Lager A1'),

INSERT INTO inventoryitem (name, category, status, location, assigned_to) VALUES    ('Monitor 24 Zoll', 'Full HD Monitor', 12, 'Lager A2'),

    ('Laptop Dell XPS', 'Hardware', 'verfügbar', 'Lager A1', NULL),    ('Tastatur Logitech', 'Mechanische Tastatur', 8, 'Lager B1')

    ('Monitor 24 Zoll', 'Hardware', 'in Verwendung', 'Büro 101', 'Max Mustermann'),ON CONFLICT DO NOTHING;

    ('Tastatur Logitech', 'Zubehör', 'verfügbar', 'Lager B1', NULL),
    ('Drucker HP LaserJet', 'Hardware', 'Wartung', 'Technikraum', 'IT-Abteilung')
ON CONFLICT DO NOTHING;
