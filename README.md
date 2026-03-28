# GUI Codespaces Starter

This is a minimal desktop GUI project for learning how to build a Windows executable while working online in GitHub Codespaces.

## Files

- `app.py`: simple Tkinter GUI that adds two numbers
- `requirements.txt`: packaging dependency
- `.github/workflows/build-windows-exe.yml`: GitHub Actions workflow that builds a Windows `.exe`
- `.gitignore`: ignores build output

## Run the app locally inside the environment

```bash
python app.py
```

## Build the Windows executable online

1. Push the repo to GitHub.
2. Open the **Actions** tab.
3. Run **Build Windows EXE**.
4. Download the artifact `AdderGUI-Windows`.
5. Extract it and run `AdderGUI.exe` on Windows.

## PyInstaller command used by the workflow

```bash
pyinstaller --onefile --windowed --name AdderGUI app.py
```
