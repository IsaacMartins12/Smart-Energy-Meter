"""
Smart Energy Meter - Aplicação Principal

Lê dados de sensores via porta serial, armazena em banco de dados SQLite,
gera gráficos de monitoramento e exporta relatório em PDF.

Uso:
    python main.py [--port COM3] [--readings 50] [--skip-serial]
"""

import argparse
from pathlib import Path

from src.serial_reader import read_serial
from src.charts import generate_all_charts
from src.pdf_report import generate_pdf


def parse_args() -> argparse.Namespace:
    """Processa argumentos de linha de comando."""
    parser = argparse.ArgumentParser(
        description="Smart Energy Meter - Monitor de energia elétrica"
    )
    parser.add_argument(
        "--port",
        default="COM3",
        help="Porta serial do Arduino (padrão: COM3)",
    )
    parser.add_argument(
        "--baudrate",
        type=int,
        default=9600,
        help="Baudrate da comunicação serial (padrão: 9600)",
    )
    parser.add_argument(
        "--readings",
        type=int,
        default=50,
        help="Número de leituras da serial (padrão: 50)",
    )
    parser.add_argument(
        "--skip-serial",
        action="store_true",
        help="Pular leitura serial e gerar gráficos com dados existentes",
    )
    return parser.parse_args()


def main() -> None:
    """Execução principal do programa."""
    args = parse_args()

    print("=" * 50)
    print("  Smart Energy Meter")
    print("=" * 50)

    # Etapa 1: Leitura serial (se não pulada)
    if not args.skip_serial:
        print("\n[1/3] Lendo dados da porta serial...")
        read_serial(
            port=args.port,
            baudrate=args.baudrate,
            num_readings=args.readings,
        )
    else:
        print("\n[1/3] Leitura serial pulada (--skip-serial)")

    # Etapa 2: Geração de gráficos
    print("\n[2/3] Gerando gráficos...")
    generate_all_charts()

    # Etapa 3: Geração do PDF
    print("\n[3/3] Gerando relatório PDF...")
    generate_pdf()

    print("\n" + "=" * 50)
    print("  Processo concluído com sucesso!")
    print("=" * 50)


if __name__ == "__main__":
    main()
