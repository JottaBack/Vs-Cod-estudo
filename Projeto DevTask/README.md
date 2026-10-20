# DevTask

Aplicativo local para organizar tarefas. Os dados ficam salvos no banco SQLite
`devtask.db`, criado automaticamente quando o aplicativo inicia. Esse banco é
um arquivo binário e não deve ser editado como texto no VS Code.

## Executar no Windows

Abra o terminal nesta pasta e execute:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Depois, acesse <http://127.0.0.1:5000>.

Para parar o servidor, pressione `Ctrl+C` no terminal.

## Testes

Com as dependências instaladas, execute:

```powershell
python -m unittest discover -s tests -v
```
