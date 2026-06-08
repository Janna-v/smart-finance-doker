CREATE TABLE IF NOT EXISTS transazioni (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data DATE NOT NULL,
    descrizione VARCHAR(255) NOT NULL,
    importo DECIMAL(10, 2) NOT NULL,
    categoria VARCHAR(100),
    tipo VARCHAR(20) DEFAULT 'Uscita'
);

