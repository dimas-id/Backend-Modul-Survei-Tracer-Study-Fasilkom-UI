from atlas.apps.survei.models import Survei
from django.db import (transaction)
from django.contrib.auth import get_user_model


class SurveiService:

    @transaction.atomic
    def register_suvei(self, request, nama, deskripsi, tanggal_dikirim=None, sudah_dikirim=False):
        user_model = get_user_model()

        try :
            user = user_model.objects.get(email=request.user)
            survei = Survei.objects.create(
                nama=nama, deskripsi=deskripsi, creator=user, tanggal_dikirim=tanggal_dikirim, sudah_dikirim=sudah_dikirim)
            return survei
        except:
            return None
    
    @transaction.atomic
    def list_survei(self):
        return Survei.objects.all()
    
    @transaction.atomic
    def list_survei_sent(self):
        return Survei.objects.filter(sudah_dikirim=True)
    
    @transaction.atomic
    def list_survei_not_sent(self):
        return Survei.objects.filter(sudah_dikirim=False)