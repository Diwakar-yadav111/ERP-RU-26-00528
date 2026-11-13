
import os
import sys
import tempfile

DONOR_FILE = "donors.txt"
VALID_GROUPS = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]


# ---------- Data ----------
def initial_stock():
    """Initial stock: A+ 10, B+ 5, O+ 8, AB+ 2, all others 0."""
    stock = {g: 0 for g in VALID_GROUPS}
    stock.update({"A+": 10, "B+": 5, "O+": 8, "AB+": 2})
    return stock


def load_donors(filename=DONOR_FILE):
    """Read donors from file. Each line: name,group,units"""
    donors = []
    if not os.path.exists(filename):
        return donors
    with open(filename, "r") as f:
        for line in f:
            parts = [p.strip() for p in line.strip().split(",")]
            if len(parts) == 3 and parts[2].isdigit():
                donors.append({"name": parts[0], "group": parts[1],
                               "units": int(parts[2])})
    return donors


def save_donor(donor, filename=DONOR_FILE):
    with open(filename, "a") as f:
        f.write(f"{donor['name']},{donor['group']},{donor['units']}\n")


# ---------- Validation ----------
def valid_group(group):
    return group in VALID_GROUPS


def valid_units(text):
    """Positive whole number only."""
    text = str(text).strip()
    return text.isdigit() and int(text) > 0


def invalid_group_msg():
    return "Invalid blood group. Valid groups: " + ", ".join(VALID_GROUPS) + "."


# ---------- Core features ----------
def add_donor(stock, donors, name, group, units, filename=DONOR_FILE):
    group = group.strip().upper()
    if not name.strip():
        return "Invalid name. Name cannot be empty."
    if not valid_group(group):
        return invalid_group_msg()
    if not valid_units(units):
        return "Invalid units. Enter a positive whole number."
    units = int(units)
    donor = {"name": name.strip(), "group": group, "units": units}
    donors.append(donor)
    save_donor(donor, filename)
    stock[group] += units
    return (f"Donor saved to {os.path.basename(filename)}. "
            f"Stock of {group} is now {stock[group]} units.")


def issue_blood(stock, group, units):
    group = group.strip().upper()
    if not valid_group(group):
        return invalid_group_msg()
    if not valid_units(units):
        return "Invalid units. Enter a positive whole number."
    units = int(units)
    if stock[group] < units:
        return (f"Insufficient stock: only {stock[group]} unit(s) "
                f"of {group} available.")
    stock[group] -= units
    return (f"{units} unit(s) of {group} issued. "
            f"Stock of {group} is now {stock[group]} units.")


def view_stock(stock):
    lines = ["Blood Group | Units", "-" * 20]
    for g in VALID_GROUPS:
        lines.append(f"{g:<11} | {stock[g]}")
    return "\n".join(lines)


def search_donors(donors, group):
    group = group.strip().upper()
    if not valid_group(group):
        return invalid_group_msg()
    found = [d for d in donors if d["group"] == group]
    if not found:
        return f"No donors found for blood group {group}."
    lines = [f"Donors with blood group {group}:"]
    for i, d in enumerate(found, 1):
        lines.append(f"{i}. {d['name']} - {d['units']} unit(s)")
    lines.append(f"Total donors found: {len(found)}")
    return "\n".join(lines)


# ---------- Menu ----------
def menu():
    print("\n=== Blood Bank Management System ===")
    print("1. Add donor")
    print("2. Issue blood")
    print("3. View stock")
    print("4. Search donors")
    print("5. Exit")


def main():
    stock = initial_stock()
    donors = load_donors()
    while True:
        menu()
        choice = input("Enter choice (1-5): ").strip()
        if choice == "1":
            name = input("Name: ")
            group = input("Blood group: ")
            units = input("Units: ")
            print(add_donor(stock, donors, name, group, units))
        elif choice == "2":
            group = input("Blood group: ")
            units = input("Units: ")
            print(issue_blood(stock, group, units))
        elif choice == "3":
            print(view_stock(stock))
        elif choice == "4":
            group = input("Blood group: ")
            print(search_donors(donors, group))
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-5.")


# ---------- Automated tests (4 test cases) ----------
def run_tests():
    tmp = os.path.join(tempfile.gettempdir(), "donors_test.txt")

    def fresh(content=""):
        with open(tmp, "w") as f:
            f.write(content)
        return initial_stock(), load_donors(tmp)

    print("Test Case 1: Normal input")
    stock, donors = fresh()
    print(add_donor(stock, donors, "Anil Verma", "B+", "1", tmp))
    assert stock["B+"] == 6

    print("\nTest Case 2: Boundary / minimum input")
    stock, donors = fresh()
    print(issue_blood(stock, "AB+", "2"))
    assert stock["AB+"] == 0

    print("\nTest Case 3: Invalid input")
    stock, donors = fresh()
    print("(a)", issue_blood(stock, "A-", "3"))
    print("(b)", add_donor(stock, donors, "Rina Das", "C+", "1", tmp))
    assert "Insufficient" in issue_blood(stock, "A-", "3")
    assert "Invalid blood group" in add_donor(stock, donors, "Rina Das", "C+", "1", tmp)

    print("\nTest Case 4: Different valid scenario")
    stock, donors = fresh("Meena Joshi,O+,1\nSuresh Rao,O+,2\n")
    print(search_donors(donors, "O+"))
    assert len([d for d in donors if d["group"] == "O+"]) == 2

    os.remove(tmp)
    print("\nAll 4 test cases passed.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    else:
        main()