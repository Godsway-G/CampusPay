from .models import (
    AssociationSettings,
    BrandingSettings,
    GeneralConfiguration,
    ReceiptSettings,
)


def association_settings(request):
    """
    Makes association information available
    throughout CampusPay.
    """

    association = (
        AssociationSettings.objects
        .filter(is_active=True)
        .first()
    )

    branding = (
        BrandingSettings.objects.first()
    )

    return {
        "association": association,
        "branding": branding,
    }


def system_settings(request):
    """
    Makes system configuration available
    throughout CampusPay.
    """

    settings = (
        GeneralConfiguration.objects.first()
    )

    if settings is None:
        settings = GeneralConfiguration()

    return {
        "system_settings": settings,
    }
    


def branding_settings(request):
    """
    Makes CampusPay branding available
    throughout the application.
    """

    branding = BrandingSettings.objects.first()

    if branding is None:
        branding = BrandingSettings()

    return {
        "branding": branding,
    }    
    
    
    
def receipt_settings(request):
    """
    Makes receipt settings available
    throughout CampusPay.
    """

    settings = (
        ReceiptSettings.objects.first()
    )

    if settings is None:

        settings = ReceiptSettings()

    return {

        "receipt_settings": settings,

    }    