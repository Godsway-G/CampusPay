from django.db import transaction


def generate_reference(model, field_name, prefix):
    """
    Generate sequential references.

    Example:
    PAY-2026-000001
    RCP-2026-000001
    """

    from django.utils import timezone

    current_year = timezone.now().year

    with transaction.atomic():

        last_object = (
            model.objects.select_for_update()
            .filter(**{
                f"{field_name}__startswith": f"{prefix}-{current_year}-"
            })
            .order_by(f"-{field_name}")
            .first()
        )

        if last_object:

            last_reference = getattr(last_object, field_name)

            last_number = int(last_reference.split("-")[-1])

            next_number = last_number + 1

        else:

            next_number = 1

        return f"{prefix}-{current_year}-{next_number:06d}"