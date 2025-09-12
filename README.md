
# Django Oscar E-commerce Project 🛒

## Overview
A feature-rich e-commerce platform built with Django Oscar framework, offering a complete online shopping solution.

## 🚀 Features
-  Responsive product catalog with categories
-  Shopping cart functionality
-  Secure checkout process
-  Cash on Delivery (COD) payment option
-  User authentication and accounts
-  Admin dashboard
-  Search functionality
-  Product image management

## 🛠️ Tech Stack
- Python 3.12
- Django
- Django Oscar
- SQLite3
- HTML/CSS
- JavaScript

## ⚙️ Installation

1. **Clone the repository**
```bash
git clone https://github.com/Arunsaini88/djnao_ecom.git
cd djnao_ecom
```

2. **Set up virtual environment**
```bash
pip install uv
uv venv
.\venv\Scripts\activate
```

3. **Install dependencies**
```bash
uv pip install -r requirements.txt
```

4. **Database setup**
```bash
python manage.py migrate
```

5. **Create admin user**
```bash
python manage.py createsuperuser
```

6. **Start development server**
```bash
python manage.py runserver
```

## 📁 Project Structure
```
oscar_ecom/
├── apps/
│   ├── basket/
│   ├── catalogue/
│   ├── checkout/
│   ├── dashboard/
│   ├── search/
│   └── shipping/
├── media/
├── static/
├── templates/
├── manage.py
└── requirements.txt
```

## ⚙️ Configuration
- Settings: `oscar_ecom/settings.py`
- URLs: `oscar_ecom/urls.py`
- Static files: `static/`
- Media files: `media/`

## 🤝 Contributing
1. Fork the repository
2. Create feature branch (`git checkout -b feature/NewFeature`)
3. Commit changes (`git commit -m 'Add NewFeature'`)
4. Push to branch (`git push origin feature/NewFeature`)
5. Open a Pull Request

## 📝 License
This project is licensed under the MIT License.

## 📞 Contact
Arun Saini - [GitHub](https://github.com/Arunsaini88)

Project Link: [https://github.com/Arunsaini88/djnao_ecom](https://github.com/Arunsaini88/djnao_ecom)

## 🙏 Acknowledgments
- [Django Oscar Documentation](https://django-oscar.readthedocs.io/)
- [Django Documentation](https://docs.djangoproject.com/)