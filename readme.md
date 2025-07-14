## 🚀 Finance Tracker Application

### 1. Clone and Setup
```bash
git clone 
cd Ptracker
python3 -m pip install virtualenv # If virtualenv is not installed
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment Setup
```bash
cp .env.example .env
# Edit .env with your configuration
```

### 3. Database Setup
```bash
python scripts/setup_db.py
```

### 4. Run Application
```bash
python run.py
```

### 5. Access Application
- Frontend: http://localhost:7000
- API: http://localhost:7000/api

## 👥 Team Development Workflow

### Branch Strategy
- `main` - Production ready code
- `feature/developer-name/feature-description` - Individual features

### Daily Workflow
1. Pull latest changes from main
2. Create feature branch
3. Work on assigned tasks
4. Test locally
5. Create pull request to main
6. Code review by team
7. Merge after approval

## 📚 Learning Resources

### Flask Documentation
- [Flask Quickstart](https://flask.palletsprojects.com/quickstart/)
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)

### Frontend Resources
- [Bootstrap Documentation](https://getbootstrap.com/docs/)
- [Chart.js Documentation](https://www.chartjs.org/docs/)

### Database Design
- [SQLAlchemy Relationships](https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html)
