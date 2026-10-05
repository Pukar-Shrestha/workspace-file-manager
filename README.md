# Workspace File Manager

A lightweight, automated, cross-platform Python script that cleans up project workspaces by automatically sorting loose assets, documents, diagrams, presentations, and scripts into structured, categorized folders.

---

## ⚡ Features

* **Zero External Dependencies:** Built using Python standard libraries (`os`, `shutil`, `pathlib`). Works out of the box on **Windows**, **macOS**, and **Linux**.
* **Smart Extension & Context Routing:**
  * `.docx`, `.doc` $\rightarrow$ `File Management/DOCX/`
  * `.pdf` (SRS, reports) $\rightarrow$ `File Management/PDFs/`
  * `.pptx`, slides & presentation PDFs $\rightarrow$ `File Management/Presentation/`
  * `.puml`, `.drawio` $\rightarrow$ `File Management/Diagrams/`
  * `.py` utilities $\rightarrow$ `File Management/Scripts/`
  * `.txt` $\rightarrow$ `File Management/Others/`
* **Root Protection:** Never touches critical project files (`README.md`, `LICENSE`, `.gitignore`, `.env`, virtual environments, etc.).
* **Process Lock Aware:** Safely skips active documents currently locked by external programs (such as Microsoft Word) without crashing.
* **Duplicate Detection:** Automatically cleans duplicate root files if an identical copy already exists in the destination folder.

---

## 🚀 How to Use

Simply place `manage_files.py` in your project root directory and run:

```bash
python manage_files.py
```

### Example Output:
```text
=================================================================
>> Workspace File Manager
   Root Directory: C:\Users\user\Downloads\Dcoker
   Destination:    C:\Users\user\Downloads\Dcoker\File Management
=================================================================
  [MOVED] presentation_deck.pptx -> File Management/Presentation/
  [MOVED] software_requirements.pdf -> File Management/PDFs/
  [CLEAN] Removed duplicate diagram.puml (already in File Management/Diagrams/)
-----------------------------------------------------------------
Organization complete! (3 organized, 0 skipped/protected)
=================================================================
```

---

## 📁 Resulting Structure

```
├── manage_files.py          # Standalone organizer script
├── README.md                # Documentation
└── File Management/         # Auto-generated category folders
    ├── DOCX/                # Word documents (.docx, .doc)
    ├── PDFs/                # Documents and specifications (.pdf)
    ├── Presentation/        # Slide decks (.pptx, presentation PDFs, HTML)
    ├── Diagrams/            # Architecture & PlantUML diagrams (.puml)
    ├── Scripts/             # Helper and generator scripts (.py)
    └── Others/              # Plain text and miscellaneous assets
```
