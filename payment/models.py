from django.db import models


class Order(models.Model):
		amount = models.DecimalField(max_digits=5, decimal_places=2)
		time = models.CharField(max_length=200)
		orderid = models.CharField(max_length=255)
		quote = models.CharField(max_length=255)

		def __str__(self):
			return self.time
