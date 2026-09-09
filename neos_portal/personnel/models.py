from django.db import models

# NOTE: unlike every other module in this app, there was no existing
# Streamlit tab_personnel.py or database schema to mirror — this is a
# reasonable default (name, position, contact, employee ID) based on the
# roles that show up throughout your other forms (Slickline Supervisor,
# Crane Operator, Banksman, etc.), not a spec you actually gave me. Treat
# the fields here as a starting point to adjust, not a locked-in design.


class Personnel(models.Model):
    full_name = models.CharField(max_length=150)
    employee_id = models.CharField(max_length=50, blank=True, default="")
    position = models.CharField(max_length=100, blank=True, default="")
    phone = models.CharField(max_length=30, blank=True, default="")
    email = models.EmailField(blank=True, default="")
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["full_name"]
        verbose_name_plural = "Personnel"

    def __str__(self):
        return self.full_name
