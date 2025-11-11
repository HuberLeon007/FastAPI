-- Inventarverwaltung Database Schema
-- PostgreSQL Initialisierung

CREATE TABLE IF NOT EXISTS inventoryitem (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    status VARCHAR(50),
    location VARCHAR(255),
    assigned_to VARCHAR(255)
);

-- Index für häufige Abfragen
CREATE INDEX IF NOT EXISTS idx_inventory_location ON inventoryitem(location);
CREATE INDEX IF NOT EXISTS idx_inventory_status ON inventoryitem(status);
CREATE INDEX IF NOT EXISTS idx_inventory_assigned ON inventoryitem(assigned_to);

-- Beispieldaten (optional)
INSERT INTO inventoryitem (name, category, status, location, assigned_to) VALUES
    ('Laptop Dell XPS', 'Hardware', 'verfügbar', 'Lager A1', NULL),
    ('Monitor 24 Zoll', 'Hardware', 'in Verwendung', 'Büro 101', 'Max Mustermann'),
    ('Tastatur Logitech', 'Zubehör', 'verfügbar', 'Lager B1', NULL),
    ('Drucker HP LaserJet', 'Hardware', 'Wartung', 'Technikraum', 'IT-Abteilung')
ON CONFLICT DO NOTHING;
