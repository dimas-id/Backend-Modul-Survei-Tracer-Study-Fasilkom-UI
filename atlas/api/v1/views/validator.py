from rest_framework import status, exceptions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from atlas.apps.validator.models import AlumniValidation
from atlas.apps.validator.services import AlumniValidatorService
from atlas.apps.validator.serializers import AlumniValidationSerializer
from atlas.apps.validator.constants import C_DEFAULT_FIELDS


class AlumniValidationView(APIView):
    permission_classes = (IsAdminUser,)
    serializer_class = AlumniValidationSerializer
    validator_service = AlumniValidatorService()

    def get_serializer(self, **kwargs):
        return self.serializer_class(**kwargs)

    def get_custom_alumni_validation_fields(self):
        fields = self.request.query_params.getlist('fields')
        valid_fields = set()
        for fd in fields:
            if fd in C_DEFAULT_FIELDS:
                valid_fields.add(fd)
        return valid_fields

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, partial=True)
        if serializer.is_valid():
            fields = self.get_custom_alumni_validation_fields()
            alumni = AlumniValidation(**serializer.data)

            try:
                if alumni.has_npm():
                    alumni = self.validator_service \
                        .validate_alumni_by_npm(alumni.npm, alumni, fields)
                else:
                    alumni = self.validator_service \
                        .validate_alumni_by_nama(alumni.nama, alumni, fields)

                if alumni.is_valid:
                    serializer = self.get_serializer(instance=alumni)
                    return Response(serializer.data)
                return Response({'is_valid': False})
            except exceptions.APIException as e:
                result_err = {'is_valid': False}
                result_err.update(e.get_full_details())
                return Response(result_err, status=e.status_code)

        result_err = {'is_valid': False}
        result_err.update(serializer.errors)
        return Response(result_err, status=status.HTTP_400_BAD_REQUEST)
