# Smart Waste Management System (SWMS)

Python project with **Text Mode (CLI)** and **Graphical Mode (tkinter GUI)**.

## Why it didn’t work on your Mac (but worked on Windows)

- **Windows:** The usual Python install includes **tkinter**, so the GUI runs without extra setup.
- **Mac:** Many Mac setups use **Homebrew Python**, which often **does not** include tkinter. So `import tkinter` fails and the app couldn’t start until we fixed it.

So the same code works on your friend’s Windows PC but needed small changes (and the right Python) on your Mac.

## How to run

### Option A: `npm start` (recommended)

From the project root:

```bash
npm start
```

Then choose **1** (Text Mode) or **2** (Graphical Mode).

- **Windows:** Usually works for both modes (Python + tkinter are typically installed).
- **Mac:** If you get “Falling back to Text Mode” when you choose 2, use Option B or C below for the GUI.

### Option B: Mac – GUI with Python that has tkinter

If you installed Python from [python.org](https://www.python.org/downloads/) (not only Homebrew), that build usually has tkinter. Use it explicitly:

```bash
npm run start:gui
```

If your Python 3.12 is elsewhere, edit `package.json` and set the `"start:gui"` script to use your Python path, for example:

```json
"start:gui": "/path/to/your/python3 SWMS_Project/run.py"
```

### Option C: Mac – Use Homebrew Python with tkinter

Fix Homebrew permissions (if needed), then install tkinter for Homebrew Python 3.13:

```bash
sudo chown -R $(whoami) /opt/homebrew /Users/$(whoami)/Library/Caches/Homebrew /Users/$(whoami)/Library/Logs/Homebrew
brew install python-tk@3.13
```

After that, `python3` should have tkinter and `npm start` → option 2 should work.

### Run without npm

From project root:

```bash
python3 SWMS_Project/run.py
```

Or:

```bash
cd SWMS_Project
python3 run.py
```

Use a Python that has tkinter if you want Graphical Mode (option 2).

## Summary

| Platform | `npm start` → Option 1 (Text) | `npm start` → Option 2 (GUI) |
|----------|-------------------------------|-------------------------------|
| Windows  | ✅                             | ✅ (if Python has tkinter)    |
| Mac      | ✅                             | ✅ if you use a Python with tkinter (e.g. `npm run start:gui` or after installing `python-tk@3.13`) |

The code is the same; the difference is whether the Python you’re using was built with tkinter (common on Windows, not always on Mac).
