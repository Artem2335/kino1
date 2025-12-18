# SQLAdmin Integration Guide

## 📋 Overview

SQLAdmin is a modern administrative interface for SQLAlchemy models. It provides:
- 🎨 Beautiful, responsive web interface
- 🔐 Authentication and authorization
- 📊 CRUD operations for all models
- 🔍 Search and filtering
- 📱 Mobile-friendly design
- 🎯 Customizable model views

## 🚀 Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `sqladmin==0.13.1` - Admin interface
- `aiosqlite>=0.19.0` - Async SQLite support

### 2. Configure Environment Variables

Create a `.env` file in the project root (copy from `.env.example`):

```bash
cp .env.example .env
```

Edit `.env` and set your admin credentials:

```env
# Admin Panel Configuration
ADMIN_PASSWORD=your_secure_password_here
SECRET_KEY=your_super_secret_key_change_in_production
```

> **⚠️ Important:** Change these values in production!

## 🔑 Admin Credentials

Default admin credentials:
- **Username:** `admin`
- **Password:** Use the value from `ADMIN_PASSWORD` in `.env`

## 🌐 Accessing the Admin Panel

After starting the application:

```bash
python run.py
```

Open your browser and go to:
```
http://localhost:8000/admin
```

You'll see the login page. Enter:
- Username: `admin`
- Password: (your `ADMIN_PASSWORD` from `.env`)

## 📊 Available Models

The admin panel provides full management for:

### 👥 Users
- View all users
- Edit user roles (user, moderator, admin)
- Search by username or email
- Delete users
- **Note:** Passwords are hidden for security

### 🎬 Movies
- Add new movies
- Edit movie details (title, description, genre, year, poster URL)
- Search by title or genre
- Delete movies
- Filter by year

### ⭐ Reviews
- View all reviews
- Approve/reject reviews (toggle `approved` field)
- Edit ratings and text
- Search reviews by content
- Filter by approval status
- View associated user and movie

### ❤️ Favorites
- View user favorites
- Add/remove favorites
- See which users favorited which movies

## 🔧 Features

### Search and Filter
- Use the search bar to find records by searchable fields
- Click column headers to sort
- Filter by specific criteria

### Bulk Operations
- Select multiple records
- Perform bulk actions (delete, update status)

### Data Validation
- Required fields are enforced
- Data types are validated automatically
- Related records are properly linked

## 🎨 Customization

### Modifying Admin Views

Edit `/app/admin.py` to customize:

```python
class UserAdmin(ModelView, model=User):
    # Columns visible in list view
    column_list = [User.id, User.username, User.email, User.is_admin]
    
    # Columns in detail view
    column_details_list = [...]
    
    # Searchable columns
    column_searchable_list = [User.username, User.email]
    
    # Sortable columns
    column_sortable_list = [...]
    
    # Default sort
    column_default_sort = [(User.created_at, True)]  # True = DESC
```

### Adding New Model Views

To add admin interface for a new model:

```python
from app.your_module.models import YourModel

class YourModelAdmin(ModelView, model=YourModel):
    name = 'Your Model'
    name_plural = 'Your Models'
    icon = 'fa-solid fa-icon-name'
    
    column_list = [YourModel.id, YourModel.field1, YourModel.field2]
    column_searchable_list = [YourModel.field1]

# Register in setup_admin()
admin.register_model(YourModelAdmin)
```

## 🔐 Security Best Practices

1. **Change Default Password**
   ```bash
   # Set a strong password in .env
   ADMIN_PASSWORD=VeryStr0ng!P@ssw0rd123
   ```

2. **Change Secret Key**
   ```bash
   # Generate a secure key
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   # Set it in .env
   SECRET_KEY=your_generated_key
   ```

3. **Use HTTPS in Production**
   - Deploy with proper HTTPS certificates
   - Set `secure=True` in session middleware

4. **Restrict Admin Access**
   - Consider implementing IP whitelisting
   - Add additional authentication layers if needed

## 🐛 Troubleshooting

### Admin Panel Not Loading

```bash
# Check all dependencies are installed
pip install -r requirements.txt

# Verify .env file exists and has correct settings
cat .env

# Check if the admin module imports correctly
python -c "from app.admin import setup_admin; print('OK')"
```

### Login Failed

- Verify username is exactly `admin`
- Check `ADMIN_PASSWORD` in `.env` file
- Clear browser cookies and try again
- Check application logs for errors

### Database Sync Issues

```bash
# If models are updated, restart the application
# SQLAlchemy will handle schema updates automatically
python run.py
```

## 📚 Additional Resources

- [SQLAdmin Documentation](https://aminalaee.dev/sqladmin/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

## 📝 File Structure

New files added for SQLAdmin integration:

```
project/
├── app/
│   ├── admin.py              # ← Admin panel configuration
│   ├── main.py               # ← Updated with SessionMiddleware
│   └── ...
├── .env.example              # ← Configuration template
├── requirements.txt          # ← Updated with sqladmin
└── SQLADMIN_SETUP.md         # ← This file
```

## 🎯 Next Steps

1. ✅ Install dependencies: `pip install -r requirements.txt`
2. ✅ Create `.env` file from `.env.example`
3. ✅ Set admin credentials in `.env`
4. ✅ Start the application: `python run.py`
5. ✅ Access admin panel: `http://localhost:8000/admin`
6. ✅ Login with your credentials
7. ✅ Manage your data!

---

**Happy administrating! 🚀**
