"""Módulo responsável pela geração de gráficos a partir dos dados coletados."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import List, Optional

import matplotlib.pyplot as plt

DB_PATH = Path(__file__).parent.parent / "data" / "projeto_ion.db"
OUTPUT_DIR = Path(__file__).parent.parent / "output"


def fetch_data(db_path: Path = DB_PATH) -> dict:
    """
    Busca todos os registros do banco de dados.

    Returns:
        Dicionário com listas de potencia, tensao, corrente, valor e tempo.
    """
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    cursor.execute("SELECT Potencia, Tensao, Corrente, Valor, Tempo FROM Registros")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    if not rows:
        raise ValueError("Nenhum registro encontrado no banco de dados.")

    return {
        "potencia": [row[0] for row in rows],
        "tensao": [row[1] for row in rows],
        "corrente": [row[2] for row in rows],
        "valor": [row[3] for row in rows],
        "tempo": [row[4] for row in rows],
    }


def generate_chart(
    x: list,
    y: list,
    title: str,
    xlabel: str,
    ylabel: str,
    ylim: tuple,
    filename: str,
    output_dir: Path = OUTPUT_DIR,
    color: str = "red",
) -> Path:
    """
    Gera um gráfico e salva como imagem PNG.

    Args:
        x: Dados do eixo X.
        y: Dados do eixo Y.
        title: Título do gráfico.
        xlabel: Rótulo do eixo X.
        ylabel: Rótulo do eixo Y.
        ylim: Limites do eixo Y (min, max).
        filename: Nome do arquivo de saída.
        output_dir: Diretório de saída.
        color: Cor da linha do gráfico.

    Returns:
        Caminho do arquivo gerado.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    filepath = output_dir / filename

    plt.figure(figsize=(10, 6))
    plt.title(title, fontsize=14, fontweight="bold")
    plt.ylim(*ylim)
    plt.xlim(0, max(x))
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.plot(x, y, color=color, linewidth=1.5)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(str(filepath), dpi=150)
    plt.close()

    print(f"Gráfico salvo: {filepath}")
    return filepath


def generate_all_charts(
    db_path: Path = DB_PATH,
    output_dir: Path = OUTPUT_DIR,
) -> list[Path]:
    """
    Gera todos os gráficos do projeto.

    Returns:
        Lista de caminhos dos arquivos gerados.
    """
    data = fetch_data(db_path)
    tempo = data["tempo"]
    charts = []

    # Gráfico de Valor/Custo
    charts.append(generate_chart(
        x=tempo,
        y=data["valor"],
        title="Gráfico de Custo Energético (R$)",
        xlabel="Tempo (s)",
        ylabel="Valor (R$)",
        ylim=(0, max(data["valor"]) * 1.2 if max(data["valor"]) > 0 else 0.30),
        filename="1_valor.png",
        output_dir=output_dir,
    ))

    # Gráfico de Tensão
    charts.append(generate_chart(
        x=tempo,
        y=data["tensao"],
        title="Gráfico de Tensão da Rede (V)",
        xlabel="Tempo (s)",
        ylabel="Tensão (V)",
        ylim=(80, 140),
        filename="2_tensao.png",
        output_dir=output_dir,
    ))

    # Gráfico de Corrente
    charts.append(generate_chart(
        x=tempo,
        y=data["corrente"],
        title="Gráfico de Corrente da Rede (A)",
        xlabel="Tempo (s)",
        ylabel="Corrente (A)",
        ylim=(0, max(data["corrente"]) * 1.5 if max(data["corrente"]) > 0 else 2),
        filename="3_corrente.png",
        output_dir=output_dir,
    ))

    return charts


if __name__ == "__main__":
    generate_all_charts()
