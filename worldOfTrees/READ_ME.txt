pip install pandas openpyxl
pip install pillow
pip install qrcode[pil]
pip install reportlab


/*visitors counter*/
After running migrations:

python manage.py shell
from core.models import SiteStats
SiteStats.objects.get_or_create(pk=1)


/*restore db command*/
python manage.py loaddata db_backup.json