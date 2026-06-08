CREATE TABLE IF NOT EXISTS transazioni (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data DATE NOT NULL,
    descrizione VARCHAR(255) NOT NULL,
    importo DECIMAL(10, 2) NOT NULL,
    categoria VARCHAR(100)
);


INSERT INTO transazioni (data, descrizione, importo, categoria) 
VALUES ('2026-06-05', 'Caffè di prova', 1.50, 'Svago');