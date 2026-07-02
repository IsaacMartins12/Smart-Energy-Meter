"""Módulo responsável pela geração do relatório em PDF."""

from pathlib import Path

from PIL import Image

OUTPUT_DIR = Path(__file__).parent.parent / "output"


def generate_pdf(
    image_dir: Path = OUTPUT_DIR,
    output_filename: str = "relatorio_energia.pdf",
) -> Path:
    """
    Gera um PDF com todas as imagens PNG do diretório especificado.

    Args:
        image_dir: Diretório contendo as imagens PNG.
        output_filename: Nome do arquivo PDF de saída.

    Returns:
        Caminho do arquivo PDF gerado.
    """
    image_dir.mkdir(parents=True, exist_ok=True)
    png_files = sorted(image_dir.glob("*.png"))

    if not png_files:
        raise FileNotFoundError(
            f"Nenhuma imagem PNG encontrada em: {image_dir}"
        )

    # Converte imagens RGBA para RGB (necessário para salvar como PDF)
    rgb_images = []
    for img_path in png_files:
        img = Image.open(img_path)
        if img.mode == "RGBA":
            background = Image.new("RGB", img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])
            rgb_images.append(background)
        else:
            rgb_images.append(img.convert("RGB"))

    # Salva o PDF
    pdf_path = image_dir / output_filename
    first_image = rgb_images[0]
    remaining_images = rgb_images[1:] if len(rgb_images) > 1 else []

    first_image.save(
        str(pdf_path),
        "PDF",
        resolution=150.0,
        save_all=True,
        append_images=remaining_images,
    )

    print(f"PDF gerado: {pdf_path}")
    return pdf_path


if __name__ == "__main__":
    generate_pdf()
