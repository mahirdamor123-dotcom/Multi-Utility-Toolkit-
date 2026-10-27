"""Single-file Multi-Utility Toolkit. Run with: python main.py"""
from __future__ import annotations

from datetime import datetime
import math
from pathlib import Path
import random
import secrets
import string
import time
import uuid

# --------------------------- Time and date tools ---------------------------
def current_datetime() -> datetime:
    return datetime.now().astimezone()


def date_difference(first: str, second: str, fmt: str = "%Y-%m-%d") -> str:
    a, b = datetime.strptime(first, fmt), datetime.strptime(second, fmt)
    seconds = int(abs((b - a).total_seconds()))
    days, remainder = divmod(seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, secs = divmod(remainder, 60)
    return f"{days} day(s), {hours:02}:{minutes:02}:{secs:02}"


def run_stopwatch() -> float:
    input("Press Enter to start...")
    start = time.monotonic()
    input("Running. Press Enter to stop...")
    return time.monotonic() - start


def run_countdown(seconds: int) -> None:
    if seconds < 0:
        raise ValueError("Countdown cannot be negative.")
    deadline = time.monotonic() + seconds
    while True:
        left = max(0, math.ceil(deadline - time.monotonic()))
        print(f"\rTime remaining: {left:>3}s", end="", flush=True)
        if left == 0:
            break
        time.sleep(min(1, deadline-time.monotonic()))
    print("\nTime is up!")


# ------------------------------- Math tools --------------------------------
def compound_amount(principal: float, annual_rate_percent: float, years: float) -> float:
    if min(principal, annual_rate_percent, years) < 0:
        raise ValueError("Principal, rate, and years cannot be negative.")
    return principal * (1 + annual_rate_percent/100) ** years


def trig_degrees(degrees: float) -> dict:
    radians = math.radians(degrees)
    cosine = math.cos(radians)
    tangent = "undefined" if math.isclose(cosine, 0, abs_tol=1e-12) else math.tan(radians)
    return {"sin": math.sin(radians), "cos": cosine, "tan": tangent}


def triangle_area(a: float, b: float, c: float) -> float:
    if min(a,b,c) <= 0 or a+b <= c or a+c <= b or b+c <= a:
        raise ValueError("Sides must be positive and satisfy the triangle inequality.")
    s=(a+b+c)/2
    return math.sqrt(s*(s-a)*(s-b)*(s-c))


# ----------------------------- Random utilities ---------------------------
def secure_password(length: int) -> str:
    if length < 8:
        raise ValueError("Use at least 8 characters.")
    alphabet=string.ascii_letters+string.digits+"!@#$%^&*()-_=+"
    chars=[secrets.choice(string.ascii_lowercase),secrets.choice(string.ascii_uppercase),
           secrets.choice(string.digits),secrets.choice("!@#$%^&*()-_=+")]
    chars.extend(secrets.choice(alphabet) for _ in range(length-4))
    secrets.SystemRandom().shuffle(chars)
    return "".join(chars)


def generate_otp(digits: int = 6) -> str:
    if not 4 <= digits <= 10:
        raise ValueError("OTP length must be from 4 to 10.")
    return "".join(secrets.choice(string.digits) for _ in range(digits))


# ------------------------------- File tools --------------------------------
OUTPUTS = Path(__file__).resolve().parent / "outputs"


def output_file(name: str) -> Path:
    candidate=Path(name)
    if candidate.name != name or name in {"", ".", ".."}:
        raise ValueError("Enter a filename only (no folder paths).")
    if candidate.suffix.lower() not in {".txt", ".md", ".log", ".csv"}:
        raise ValueError("Allowed extensions: .txt, .md, .log, .csv")
    OUTPUTS.mkdir(exist_ok=True)
    return OUTPUTS/candidate.name


def file_create(name: str) -> Path:
    path=output_file(name)
    with path.open("x",encoding="utf-8"):
        pass
    return path


def file_write(name: str, text: str) -> Path:
    path=output_file(name)
    path.write_text(text,encoding="utf-8")
    return path


def file_read(name: str) -> str:
    return output_file(name).read_text(encoding="utf-8")


def file_append(name: str, text: str) -> Path:
    path=output_file(name)
    with path.open("a",encoding="utf-8") as stream:
        stream.write(text)
    return path


# --------------------------- Input and submenus ----------------------------
def get_number(prompt: str, *, integer=False, minimum=None) -> float | int:
    while True:
        try:
            value=int(input(prompt)) if integer else float(input(prompt))
            if minimum is not None and value < minimum:
                print(f"Enter a value of at least {minimum}.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")


def date_menu() -> None:
    while True:
        print("\nDATE & TIME\n1 Current date/time\n2 Difference between dates\n3 Custom date format\n4 Stopwatch\n5 Countdown\n6 Back")
        choice=input("Choose: ").strip()
        try:
            if choice=="1": print(current_datetime().strftime("%A, %d %B %Y %H:%M:%S %Z"))
            elif choice=="2":
                a=input("First date (YYYY-MM-DD): ").strip(); b=input("Second date (YYYY-MM-DD): ").strip()
                print("Difference:",date_difference(a,b))
            elif choice=="3": print(current_datetime().strftime(input("Format (e.g. %Y-%m-%d %H:%M): ")))
            elif choice=="4": print(f"Elapsed: {run_stopwatch():.2f} seconds")
            elif choice=="5": run_countdown(get_number("Seconds: ",integer=True,minimum=0))
            elif choice=="6": return
            else: print("Choose 1–6.")
        except (ValueError,OSError) as exc: print("Could not complete:",exc)


def math_menu() -> None:
    while True:
        print("\nMATH\n1 Factorial\n2 Compound interest\n3 Trigonometry\n4 Circle area\n5 Rectangle area\n6 Triangle area\n7 Back")
        choice=input("Choose: ").strip()
        try:
            if choice=="1": print("Factorial:",math.factorial(get_number("Non-negative integer: ",integer=True,minimum=0)))
            elif choice=="2":
                p=get_number("Principal: ",minimum=0); r=get_number("Annual rate (%): ",minimum=0); y=get_number("Years: ",minimum=0)
                amount=compound_amount(p,r,y); print(f"Final amount: {amount:.2f}; interest: {amount-p:.2f}")
            elif choice=="3": print(trig_degrees(get_number("Angle in degrees: ")))
            elif choice=="4":
                radius=get_number("Radius: ",minimum=0); print(f"Circle area: {math.pi*radius**2:.4f}")
            elif choice=="5":
                length=get_number("Length: ",minimum=0); width=get_number("Width: ",minimum=0); print(f"Rectangle area: {length*width:.4f}")
            elif choice=="6": print(f"Triangle area: {triangle_area(*(get_number(f'Side {s}: ',minimum=0) for s in 'abc')):.4f}")
            elif choice=="7": return
            else: print("Choose 1–7.")
        except (ValueError,OverflowError) as exc: print("Could not calculate:",exc)


def random_menu() -> None:
    while True:
        print("\nRANDOM DATA\n1 Random integer\n2 Random integer list\n3 Secure password\n4 OTP\n5 Random sample\n6 Dice simulation\n7 Back")
        choice=input("Choose: ").strip()
        try:
            if choice=="1":
                lo=get_number("Minimum: ",integer=True); hi=get_number("Maximum: ",integer=True); print(random.randint(lo,hi))
            elif choice=="2":
                count=get_number("List length: ",integer=True,minimum=0); lo=get_number("Minimum: ",integer=True); hi=get_number("Maximum: ",integer=True)
                if lo>hi: raise ValueError("Minimum must not exceed maximum.")
                print([random.randint(lo,hi) for _ in range(count)])
            elif choice=="3": print("Generated password:",secure_password(get_number("Length (minimum 8): ",integer=True,minimum=8)))
            elif choice=="4": print("OTP:",generate_otp(get_number("Number of digits (4–10): ",integer=True,minimum=4)))
            elif choice=="5":
                items=[item.strip() for item in input("Items separated by commas: ").split(",") if item.strip()]
                n=get_number("Sample size: ",integer=True,minimum=0)
                if n>len(items): raise ValueError("Sample size cannot exceed number of items.")
                print(random.sample(items,n))
            elif choice=="6":
                n=get_number("Number of rolls: ",integer=True,minimum=1); sides=get_number("Dice sides: ",integer=True,minimum=2)
                print([random.randint(1,sides) for _ in range(n)])
            elif choice=="7": return
            else: print("Choose 1–7.")
        except ValueError as exc: print("Could not generate:",exc)


def file_menu() -> None:
    while True:
        print("\nFILE OPERATIONS (outputs folder)\n1 Create file\n2 Write/replace file\n3 Read file\n4 Append to file\n5 Back")
        choice=input("Choose: ").strip()
        if choice=="5": return
        if choice not in {"1","2","3","4"}: print("Choose 1–5."); continue
        try:
            name=input("Filename (no folders): ").strip()
            if choice=="1": print("Created:",file_create(name))
            elif choice=="2": print("Saved:",file_write(name,input("Text to write: ")))
            elif choice=="3": print(file_read(name))
            else: print("Appended:",file_append(name,input("Text to append: ")))
        except (ValueError,OSError) as exc: print("File operation failed:",exc)


def explore_module() -> None:
    modules={"datetime":datetime,"time":time,"math":math,"random":random,"uuid":uuid,
             "string":string,"secrets":secrets}
    print("Available modules:",", ".join(modules))
    name=input("Module to explore: ").strip()
    if name not in modules:
        print("Choose one of the listed modules."); return
    names=dir(modules[name])
    print(f"Attributes in {name} ({len(names)} total):")
    print(", ".join(names[:100]))
    if len(names)>100: print("... showing first 100")


def main() -> None:
    while True:
        print("\n=================================\n       MULTI-UTILITY TOOLKIT\n=================================\n1 Date and time operations\n2 Mathematical operations\n3 Random data generation\n4 Generate UUID v4\n5 File operations\n6 Explore module attributes (dir)\n7 Exit\n=================================")
        choice=input("Choose an option: ").strip()
        if choice=="1": date_menu()
        elif choice=="2": math_menu()
        elif choice=="3": random_menu()
        elif choice=="4":
            try:
                count=get_number("How many UUIDs? [1]: ",integer=True,minimum=1)
                for _ in range(count): print(uuid.uuid4())
            except ValueError as exc: print(exc)
        elif choice=="5": file_menu()
        elif choice=="6": explore_module()
        elif choice=="7": print("Thank you for using the Multi-Utility Toolkit!"); return
        else: print("Choose a number from 1 to 7.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt,EOFError):
        print("\nGoodbye!")
