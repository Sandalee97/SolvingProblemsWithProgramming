Quick run instructions

1. Create and activate a virtual environment (optional but recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

3. Run the document-tracker app (cupboard/drawer UI):

```powershell
python .\application\app.py
```

Open http://127.0.0.1:5000/ in your browser. Use credentials from `application/data.json` (e.g. `hr1@company.com` / `hrpass1`).

Notes
- If Windows PowerShell blocks script execution for the virtualenv activation, run `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` as admin or use `cmd.exe` activation scripts.
- If you see "No module named 'flask'", make sure you installed dependencies into the Python interpreter you're using to run the app. You can check which python is used with `Get-Command python` or `python -m site`.
