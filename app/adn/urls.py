from app.ext.register import url

from app.adn.views.view_adn import ViewAdn
from app.adn.views.view_statistics import ViewStatistics

urlpatterns = [
    url(ViewAdn, endpoint=['/mutant', '/mutant/<id>'], namespace="View_Adn"),
    url(ViewStatistics, endpoint=['/stats', '/stats/<id>'], namespace="View_Statistics"),
]
