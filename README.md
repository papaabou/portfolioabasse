Django Portfolio Website
========================

A modern, admin-driven portfolio website built with Django. This project is designed for developers, freelancers, and creatives who want full control over their website content, branding, and SEO using the Django admin panel.

### This repository can be used as:

*   A personal developer portfolio
    
*   A freelancer website
    
*   A client-facing showcase site
    
*   A learning reference for Django project structure
    

FEATURES
--------

*   **Admin-controlled site settings:** Site title, favicon, SEO, and footer management.
    
*   **Dynamic Content:** Home and About pages driven by the database.
    
*   **Profile-based management:** Easily update your skills, services, projects, and testimonials.
    
*   **Blog / Journal:** Built-in support for posting articles.
    
*   **SEO-ready:** Structured for search engine optimization.
    
*   **Clean UI:** Minimalist and scalable architecture.
    

TECH STACK
----------

*   **Backend:** Django
    
*   **Frontend:** HTML, CSS
    
*   **Database:** SQLite (default)
    
*   **Media Handling:** Django Media Files
    
*   **Admin Panel:** Django Admin
    

GETTING STARTED
---------------

### 1\. Clone the repository

```
git clone https://github.com/osama2kabdullah/portfolio.git
cd your-repo-name
```

### 2\. Create a virtual environment

```
python -m venv .venv  
.venv/bin/activate      # Linux / macOS  source   
.venv\Scripts\activate  # Windows
```

### 3\. Install dependencies

```
pip install -r requirements.txt
```

### 4\. Run migrations

```
python manage.py migrate
```

### 5\. Create a superuser

```
python manage.py createsuperuser
```

### 6\. Run the development server

```
python manage.py runserver   
```

Open your browser and visit: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

IMPORTANT INITIAL SETUP
-----------------------

This project uses a singleton SiteSettings model. After the first run, create the site settings instance via the Django shell:


```
python manage.py shell
```

```
from core.models import SiteSettings  SiteSettings.load()
```

Then open the **Django admin** to configure:

*   Site title
    
*   Favicon
    
*   SEO metadata
    
*   Footer content
    

PROJECT STRUCTURE (SIMPLIFIED)
------------------------------

*   core/: Site-wide settings and base logic
    
*   about/: Profile, journey, and skills
    
*   projects/: Portfolio project management
    
*   services/: Services offered
    
*   blog/: Posts and journal entries
    
*   testimonials/: Client feedback
    
*   templates/: HTML templates
    
*   static/: CSS and static assets
    
*   media/: Uploaded images and files
    

CONTRIBUTING / FORKING
----------------------

You are free to fork this repository and use it for your own website.

**If you fork this project:**

*   Replace all personal branding and content.
    
*   Do not claim the original design as your own.
    
*   Credit is appreciated but not required.
    

**Contributions are welcome:**

*   Bug fixes and improvements.
    
*   Refactoring and documentation updates.
    

Please open a pull request with a clear description of your changes.

LICENSE
-------

This project is licensed under the **MIT License**. You are free to use, modify, and distribute it.

CONTACT
-------

*   **Author:** Osama Abdullah
    
*   **GitHub:** [https://github.com/osama2kabdullah](https://github.com/osama2kabdullah)
    
*   **Portfolio:** [https://osama-abdullah.vercel.app](https://osama-abdullah.vercel.app)
    

**Happy building!**