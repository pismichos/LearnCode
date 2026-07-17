δομή του project 

LearnCode/
│
├── templates/
│     └── base.html      ← Κοινό template για όλη την εφαρμογή
│
├── core/
│     └── templates/
│           └── core/
│                 └── home.html
│
├── courses/
│     └── templates/
│           └── courses/
│
├── blog/
│     └── templates/
│           └── blog/

Η αρχική σελίδα θα μπορούσε να έχει:
---------------------------------------------------

LOGO

Αρχική | Μαθήματα | Βίντεο | Blog | Επικοινωνία

---------------------------------------------------

Hero Image

"Μάθε Πληροφορική με σύγχρονο τρόπο"

[Ξεκίνα σήμερα]

---------------------------------------------------

Οι υπηρεσίες σου

🐍 Python

🌐 HTML / CSS

💻 Πανελλήνιες

🎓 Scratch

---------------------------------------------------

Τελευταία Βίντεο

---------------------------------------------------

Τελευταίες Ασκήσεις

---------------------------------------------------

Blog

---------------------------------------------------

Footer

## Installation

```bash
git clone https://github.com/pismichos/LearnCode.git

cd LearnCode

python -m venv .venv

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver
```

## Author

Giannis Pismichos