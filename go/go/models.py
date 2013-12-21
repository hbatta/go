from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

import random, string

# Create your models here.
class URL( models.Model ):
    owner = models.ForeignKey( User )
    date_created = models.DateTimeField( default=timezone.now() )

    target = models.URLField( max_length = 1000 )
    short = models.CharField( primary_key = True, max_length = 20 )
    clicks = models.IntegerField( default = 0 )
    expires = models.DateTimeField( blank = True, null = True )

    def __unicode__(self):
        return '<URL: %s>' % self.short

    class Meta:
        ordering = ['short']

    @staticmethod
    def generate_valid_short():
        selection = string.ascii_lowercase + string.digits
        tries = 0
        while True:
            short = ''.join(random.choice(selection) for i in range(5))
            try:
                urls = URL.objects.get( short__iexact = short )
                tries += 1
            except URL.DoesNotExist:
                return short
            if tries > 100:
                return None

