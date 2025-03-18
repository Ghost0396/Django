### Step 1: Clone the repository

```bash
git clone https://github.com/Ghost0396/Django.git
```

### Step 2: Navigate to the cloned directory
After the clone process completes, you can navigate into the cloned repository's directory:
```bash
cd DJANGO/project/
```

### Step 3: Install packages using `pip`
Once you have your `requirements.txt` file, you can install all the listed packages with the following command in your terminal or command prompt (in the same directory as the `requirements.txt` file):
```bash
pip install -r requirements.txt
```

### Step 4: Ensure your project is set up
Make sure your Django project is set up and you have migrated the database. If you haven't done this yet, run:
```bash
python manage.py makemigrations
python manage.py migrate

```

### Step 5: Create the superuser
Run the following command to create a superuser:

```bash
python manage.py createsuperuser
```

### Step 6: Enter the superuser details
After running the command, Django will prompt you for the following details:

1. **Username**: Enter the desired username for the superuser (e.g., `admin`).
2. **Email address**: Enter the email address for the superuser. (Not required)
3. **Password**: Enter a strong password for the superuser.
4. **Confirm password**: Re-enter the password to confirm.

If everything is correct, Django will create the superuser.

### Step 7: Run server
Once the superuser is created, you can running your development server:

```bash
python manage.py runserver
```

Now, go to your browser and visit the following URL:
```
http://127.0.0.1:8000/admin/
```
