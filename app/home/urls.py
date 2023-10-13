from app.home.views.home import ViewHome

from app.ext.register import url


urlpatterns = [
    url(ViewHome, endpoint=['/'], namespace="register_home")
]
