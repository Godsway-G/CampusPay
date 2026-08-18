from administration.models import AcademicDefaults


class AcademicConfigurationService:
    """
    Provides centralized academic configuration.
    """

    @staticmethod
    def get_defaults():
        return (
            AcademicDefaults.objects
            .select_related(
                "academic_year",
                "semester",
            )
            .first()
        )

    @staticmethod
    def get_active_semester():
        defaults = AcademicConfigurationService.get_defaults()

        if defaults:
            return defaults.semester

        return None