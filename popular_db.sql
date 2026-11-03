-- Desativa temporariamente as cheques de chave estrangeira para evitar conflitos na inserção
SET FOREIGN_KEY_CHECKS = 0;

-- Limpa tabelas existentes (opcional)
TRUNCATE TABLE api_sensorreading;
TRUNCATE TABLE api_sensor;
TRUNCATE TABLE api_sensormodel;

-- 1. Inserção de Modelos de Sensor (SensorModel)
INSERT INTO api_sensormodel (sm_id, sm_name, sm_unit, sm_description) VALUES
(1, 'DHT11', '°C / %', 'Sensor de Temperatura e Umidade Relativa'),
(2, 'LDR', 'lux', 'Sensor de Luminosidade'),
(3, 'MQ-135', 'PPM', 'Sensor de Qualidade do Ar / Gases'),
(4, 'HC-SR04', 'cm', 'Sensor Ultrassônico de Distância');

-- 2. Inserção de Microcontroladores (Microcontroller)
INSERT INTO api_microcontroller (mc_id, mc_name, mc_location, mc_is_active) VALUES
(1, 'ESP32-BlocoA-Sala101', 'Bloco A - Laboratório de Informática 1', 1),
(2, 'ESP32-BlocoA-Sala102', 'Bloco A - Laboratório de Informática 2', 1),
(3, 'ESP32-BlocoB-OficinaMec', 'Bloco B - Oficina Mecânica', 1),
(4, 'ESP32-BlocoC-Auditorio', 'Bloco C - Auditório Principal', 1),
(5, 'ESP32-BlocoD-Biblioteca', 'Bloco D - Biblioteca Central', 0); -- Inativo para testes de restrição

-- 3. Inserção de Sensores (Sensor) - 4 por Microcontrolador (Total: 20)
INSERT INTO api_sensor (sen_id, sen_model_id, sen_mc_id, sen_is_active) VALUES
-- Microcontrolador 1
(1, 1, 1, 1), (2, 2, 1, 1), (3, 3, 1, 1), (4, 4, 1, 1),
-- Microcontrolador 2
(5, 1, 2, 1), (6, 2, 2, 1), (7, 3, 2, 1), (8, 4, 2, 1),
-- Microcontrolador 3
(9, 1, 3, 1), (10, 2, 3, 1), (11, 3, 3, 1), (12, 4, 3, 1),
-- Microcontrolador 4
(13, 1, 4, 1), (14, 2, 4, 1), (15, 3, 4, 1), (16, 4, 4, 1),
-- Microcontrolador 5 (Inativo)
(17, 1, 5, 0), (18, 2, 5, 0), (19, 3, 5, 0), (20, 4, 5, 0);

-- 4. Inserção de Leituras (SensorReading) - Amostra de 100 registros simulados
-- (Exemplo estruturado para associar às chaves estrangeiras corretas sr_sen)
INSERT INTO api_sensorreading (sr_id, sr_measured_value, sr_measured_at, sr_sen_id) VALUES
(1, 23.50, NOW() - INTERVAL 10 HOUR, 1),
(2, 65.20, NOW() - INTERVAL 9 HOUR, 1),
(3, 450.00, NOW() - INTERVAL 9 HOUR, 2),
(4, 12.10, NOW() - INTERVAL 8 HOUR, 3),
(5, 102.50, NOW() - INTERVAL 8 HOUR, 4),
-- (Pode estender gerando via script Python ou repetir o padrão para atingir 100 registros)
(100, 24.80, NOW(), 16);

-- Reativa as cheques de chave estrangeira
SET FOREIGN_KEY_CHECKS = 1;