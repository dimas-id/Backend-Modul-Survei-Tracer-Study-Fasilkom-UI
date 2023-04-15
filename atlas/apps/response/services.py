from atlas.apps.response.models import Response, Jawaban
from django.db import (transaction)
from django.contrib.auth import get_user_model

class ResponseService:
    @transaction.atomic
    def register_response(self, user_id, survei):
        user_model = get_user_model()
        user = user_model.objects.get(id=user_id)
        response = Response.objects.create(user=user, survei=survei)
        return response
    
    @transaction.atomic
    def register_jawaban(self, pertanyaan, response, jawaban):
        new_jawaban = Jawaban.objects.create(pertanyaan=pertanyaan, response=response, jawaban=jawaban)
        return new_jawaban

    def check_jawaban_validity(self, pertanyaan_id_list, jawaban_keys_list, jawaban):
        jawaban_not_valid = []
        for pid in pertanyaan_id_list:
            pid_str = str(pid)
            if pid_str in jawaban_keys_list:
                if jawaban[pid_str] == '' or jawaban[pid_str] == []:
                    jawaban_not_valid.append(pid_str)
            else:
                jawaban_not_valid.append(pid_str)
        return jawaban_not_valid