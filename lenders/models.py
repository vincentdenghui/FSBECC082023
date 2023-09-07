from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator, RegexValidator

class LenderFieldConstrains:

    code_format_regex = RegexValidator(r'^[A-Z]*$', 'only capital alphabets [A-Z] are allowed.')

    name_min_length = 1
    name_max_length = 1024

    code_min_length = 3
    code_max_length = 3

    upfront_commission_rate_min = 0.0
    upfront_commission_rate_max = 500.0

    trial_commission_rate_min = 0.0
    trial_commission_rate_max = 500.0

class Lender(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(blank=False,
                            max_length=LenderFieldConstrains.name_max_length,
                            validators=[
                                MinLengthValidator(LenderFieldConstrains.name_min_length)])

    code = models.CharField(unique=True,
                            max_length=LenderFieldConstrains.code_max_length,
                            validators=[
                                MinLengthValidator(LenderFieldConstrains.code_min_length),
                                LenderFieldConstrains.code_format_regex,])

    upfront_commission_rate = models.FloatField(validators=[MinValueValidator(LenderFieldConstrains.upfront_commission_rate_min),
                                                            MaxValueValidator(LenderFieldConstrains.upfront_commission_rate_max)])

    trial_commission_rate = models.FloatField(validators=[MinValueValidator(LenderFieldConstrains.trial_commission_rate_min),
                                                          MaxValueValidator(LenderFieldConstrains.trial_commission_rate_max)])
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']