"""Módulo responsável pela leitura de dados via porta serial."""

import sqlite3
import serial
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "projeto_ion.db"


def init_database(db_path: Path = DB_PATH) -> None:
    """Cria a tabela de registros caso não exista."""
    with sqlite3.connect(str(db_path)) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS Registros (
                Potencia REAL,
                Tensao REAL,
                Corrente REAL,
                Valor REAL,
                Tempo REAL
            )
        """)
        conn.commit()


def read_serial(
    port: str = "COM3",
    baudrate: int = 9600,
    num_readings: int = 50,
    db_path: Path = DB_PATH,
) -> None:
    """
    Lê dados da porta serial e salva no banco de dados SQLite.

    Args:
        port: Porta serial (ex: COM3, /dev/ttyUSB0).
        baudrate: Taxa de transmissão em bps.
        num_readings: Número de leituras a realizar.
        db_path: Caminho para o banco de dados SQLite.
    """
    init_database(db_path)

    comport = serial.Serial(port, baudrate)
    print(f"Serial iniciada na porta {port} a {baudrate} bps...\n")

    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    try:
        for i in range(num_readings):
            serial_value = str(comport.readline())
            dados = serial_value.split("|")

            potencia = float(dados[0][2:])
            tensao = float(dados[1])
            corrente = float(dados[2])
            valor = float(dados[3])
            tempo = float(dados[4][:4])

            cursor.execute(
                "INSERT INTO Registros (Potencia, Tensao, Corrente, Valor, Tempo) "
                "VALUES (?, ?, ?, ?, ?)",
                (potencia, tensao, corrente, valor, tempo),
            )
            conn.commit()

            print(f"[{i + 1}/{num_readings}] P={potencia:.2f} V={tensao:.1f} "
                  f"I={corrente:.3f} R$={valor:.4f} t={tempo:.1f}s")

    except serial.SerialException as e:
        print(f"Erro na comunicação serial: {e}")
    except (IndexError, ValueError) as e:
        print(f"Erro ao processar dados da serial: {e}")
    finally:
        cursor.close()
        conn.close()
        comport.close()
        print("Conexões encerradas.")


if __name__ == "__main__":
    read_serial()
