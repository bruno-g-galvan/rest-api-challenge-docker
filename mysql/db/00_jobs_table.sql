CREATE TABLE jobs (
    id INT NOT NULL AUTO_INCREMENT,
    job VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);

INSERT INTO jobs (id, job) values (1, 'Support')