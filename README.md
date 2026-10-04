# Lógica Computacional - trabalhos práticos 2026/2027

Adicionado o TP1.2 (Sudoku genérico), falta o TP1.1 (horário escolar).

## TP1.2

- [Notebook Marimo e código](TP1.2/sudoku.py)
- [Cópia PDF do notebook](TP1.2/sudoku.pdf)
- [Relatório técnico e apresentação](TP1.2/RELATORIO.md)
- [Testes automáticos](TP1.2/test_sudoku.py)
- [Enunciado original do professor](TP1.2/enunciado_professor.py)

### Executar neste PC

O ambiente `.venv` já foi criado com Python 3.14.8, Marimo 0.24.2 e OR-Tools 9.15.6755. A partir da raiz do repositório:

```bash
.venv/bin/marimo edit TP1.2/sudoku.py
```

O editor abre um endereço local no browser. Para apresentar o notebook sem
controlos de edição, usamos `marimo run`; para verificar o código, corremos os testes:

```bash
.venv/bin/marimo run TP1.2/sudoku.py
.venv/bin/python -m unittest discover -s TP1.2 -v
.venv/bin/marimo check TP1.2/sudoku.py
```

### Recriar o ambiente noutra máquina

É necessário instalar [uv](https://docs.astral.sh/uv/getting-started/installation/)
ou disponibilizar Python 3.14 por outro método. Com `uv`:

```bash
uv venv --python 3.14 .venv
uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/marimo edit TP1.2/sudoku.py
```

Versão python==3.14, dependências: marimo==0.24.2 , ortools==9.15.6755