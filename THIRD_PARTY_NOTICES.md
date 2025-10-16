Third-Party Notices
===================

This project depends on third-party components. The following summarizes their
licenses and any redistribution obligations. When distributing binaries (e.g.,
via PyInstaller), include this file and the referenced license texts where
required by those licenses.

Dependencies
------------

1) customtkinter 5.2.2
- License: MIT License
- Copyright: Tom Schimansky
- Notes: Preserve copyright and license notice in redistributions.

2) Pillow 10.1.0
- License: PIL Software License (HPND-style permissive)
- Copyright: Secret Labs AB and contributors; Fredrik Lundh
- Notes: Include Pillow’s license notice with redistributions of source or binary packages.

3) PyInstaller 6.3.0
- License: GNU GPL-2.0-or-later with the PyInstaller exception
- Notes: The exception allows building and distributing non-GPL programs with PyInstaller. Include PyInstaller’s license and exception text with redistributions of binaries built with PyInstaller.

Runtime components commonly bundled in the executable
----------------------------------------------------

- CPython runtime and standard library
  - License: Python Software Foundation License (PSF)
  - Notes: When bundled, include the PSF license text.

- Tcl/Tk (used via tkinter)
  - License: BSD-style license (license.terms)
  - Notes: When bundled, include Tcl/Tk license terms.

How to collect and include license texts
----------------------------------------

When preparing a release of the executable, copy the license files from your
Python environment into a `third_party_licenses/` folder alongside the
executable and this THIRD_PARTY_NOTICES.md file.

Suggested layout:

third_party_licenses/
- customtkinter-LICENSE.txt    (from site-packages/customtkinter/LICENSE)
- Pillow-LICENSE.txt           (from site-packages/PIL/LICENSE or LICENSE.rst)
- PyInstaller-LICENSE.txt      (from site-packages/PyInstaller/LICENSE)
- Python-PSF-LICENSE.txt       (from your Python install, e.g., LICENSE or LICENSE.txt)
- TclTk-license.terms          (from your Python install’s tcl/tk directories)

Notes
-----

- This repository’s own code is licensed under the MIT License (see LICENSE).
- Keep this file and the copied license texts with any distributed binaries.
- If you add or remove dependencies, update this document accordingly.

