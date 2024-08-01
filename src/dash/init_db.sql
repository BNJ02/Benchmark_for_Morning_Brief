-- init_db.sql

CREATE TABLE IF NOT EXISTS TypesVoix (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Themes (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Jours (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    active INTEGER NOT NULL DEFAULT 1,
    heure TEXT NOT NULL,
    type_voix_id INTEGER NOT NULL,
    themes TEXT NOT NULL,
    son INTEGER NOT NULL CHECK(son BETWEEN 1 AND 100),
    FOREIGN KEY (type_voix_id) REFERENCES TypesVoix(ID)
);

CREATE TABLE IF NOT EXISTS HistoriqueJours (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    jour_id INTEGER NOT NULL,
    date_passage DATE NOT NULL DEFAULT CURRENT_DATE,
    son INTEGER NOT NULL,
    type_voix TEXT NOT NULL,
    lien_son TEXT,
    themes TEXT NOT NULL,
    FOREIGN KEY (jour_id) REFERENCES Jours(ID)
);

INSERT INTO TypesVoix (nom) VALUES
('Douce'),
('Forte'),
('Moderee'),
('Grave'),
('Aigue'),
('Vibrante'),
('Apaisante');

INSERT INTO Themes (nom) VALUES
('Politique'),
('Economie'),
('Technologie'),
('Sport'),
('Sante'),
('Divertissement'),
('Culture'),
('Science'),
('Voyage'),
('Musique'),
('Cuisine'),
('Histoire'),
('Litterature'),
('Nature'),
('Film');

INSERT INTO Jours (nom, heure, type_voix_id, themes, Son) VALUES
('Lundi', '08:00', 1, '[]', 50),
('Mardi', '08:00', 2, '[]', 50),
('Mercredi', '08:00', 3, '[]', 50),
('Jeudi', '08:00', 4, '[]', 50),
('Vendredi', '08:00', 5, '[]', 50),
('Samedi', '08:00', 6, '[]', 50),
('Dimanche', '08:00', 7, '[]', 50);