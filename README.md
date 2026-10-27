# Multi-Utility Toolkit

A single-file, menu-driven Python program that brings together practical date and time tools, mathematical calculations, random data generation, UUID creation, safe text-file operations, and Python module exploration.

## Requirements

- Python 3.10 or newer
- No external packages are needed. The program uses only Python's standard library.

## Run the program

Save `main.py` and this `README.md` in the same folder. Open a terminal in that folder and run:

```powershell
python main.py
```

On Windows, if the `python` command is not recognized, try:

```powershell
py main.py
```

## Menu features

### 1. Date and time operations

- Display the current local date and time.
- Find the absolute difference between two dates entered as `YYYY-MM-DD`.
- Format the current date/time with a custom Python `strftime` format.
- Use a keyboard-controlled stopwatch.
- Run a countdown in seconds.

### 2. Mathematical operations

- Calculate factorials for non-negative integers.
- Calculate annual compound interest and the final amount.
- Calculate sine, cosine, and tangent for an angle in degrees.
- Find the area of a circle, rectangle, or triangle.

### 3. Random data generation

- Generate a random integer or list of integers.
- Create a secure password using Python's `secrets` module.
- Generate a numeric OTP (4–10 digits).
- Select a random sample from comma-separated items.
- Simulate rolls of a die with a configurable number of sides.

### 4. UUID generation

Create one or more UUID version 4 identifiers.

### 5. File operations

Create, read, write, or append files in the `outputs` folder beside `main.py`. Accepted extensions are `.txt`, `.md`, `.log`, and `.csv`. Enter a filename only; folder paths are not accepted.

### 6. Module exploration

Use `dir()` to list attributes of the built-in modules `datetime`, `time`, `math`, `random`, `uuid`, `string`, and `secrets`. The program displays names only; it does not execute selected attributes.

## Project layout

```text
main.py       Complete application
README.md     Project guide
outputs/      Files created by the file operations menu
```

The `outputs` folder is created automatically when you first use a file operation.

## Assumptions and limits

- Date/time displays use the computer's local timezone. Date differences are absolute whole-day differences.
- Compound interest is compounded annually: `A = P × (1 + r/100)^t`.
- Trigonometry accepts degrees. Tangent is reported as undefined where cosine is effectively zero.
- Triangle area uses Heron's formula and requires positive side lengths that satisfy the triangle inequality.
- Passwords require at least eight characters and include lowercase, uppercase, numeric, and symbol characters.
- OTPs are numeric strings, so a generated code may begin with zero. Do not treat an OTP as a permanent password.
- File operations are restricted to simple filenames in the local `outputs` folder.

## Example

To calculate `5!`, start the program, choose **2** for Mathematical Operations, choose **1** for Factorial, and enter `5`. The result is `120`.
