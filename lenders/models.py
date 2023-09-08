from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator, RegexValidator

class LenderFieldConstraints:

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
                            max_length=LenderFieldConstraints.name_max_length,
                            validators=[
                                MinLengthValidator(LenderFieldConstraints.name_min_length)])

    code = models.CharField(unique=True,
                            max_length=LenderFieldConstraints.code_max_length,
                            validators=[
                                MinLengthValidator(LenderFieldConstraints.code_min_length),
                                LenderFieldConstraints.code_format_regex,])

    upfront_commission_rate = models.FloatField(validators=[MinValueValidator(LenderFieldConstraints.upfront_commission_rate_min),
                                                            MaxValueValidator(LenderFieldConstraints.upfront_commission_rate_max)])

    trial_commission_rate = models.FloatField(validators=[MinValueValidator(LenderFieldConstraints.trial_commission_rate_min),
                                                          MaxValueValidator(LenderFieldConstraints.trial_commission_rate_max)])
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']