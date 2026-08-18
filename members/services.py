from django.contrib.auth import get_user_model
from django.db.models import Max

from .models import Member

import secrets
import string


User = get_user_model()


