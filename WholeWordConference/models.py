from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from tinymce.models import HTMLField


class WholeWordConference(models.Model):
    name = models.CharField(
        max_length=300,
        blank=True,
        help_text=_("You can leave this field blank. The name will be updated as Whole Word Conference 'the year in date field e.g: 2024'")
    )
    slug = models.SlugField(verbose_name=_("Category safe URL"), max_length=255, default='wwc')
    date = models.DateField(help_text=_("Whole Word Conference date. This field is required"), default=timezone.now, blank=True)
    end_date = models.DateField(default=timezone.now, blank=True)
    flyer = models.FileField(blank=True, upload_to='wwc_images/')
    email_message = HTMLField()

    class Meta:
        verbose_name = "Whole Word Conference"
        verbose_name_plural = "Whole Word Conferences"

        ordering = ["-date"]

    def save(self, *args, **kwargs):
        """Auto-generate fields if not provided."""
        if not self.name:
            self.name = f"Whole Word Conference {self.date.year}"
        if not self.slug:
            self.slug = f"wwc{self.date.year}"
        super().save(*args, **kwargs)

    def __str__(self):
        
        return f"Whole Word Conference {self.date.year}"


class Attendee(models.Model):
    whole_word_conference = models.ForeignKey(WholeWordConference, on_delete=models.RESTRICT, null=True)
    first_name = models.CharField(max_length=1000, blank=True)
    last_name = models.CharField(max_length=10000, blank=True)
    phone = models.CharField(max_length=100, blank=True)
    ministry = models.CharField(max_length=1000, blank=True)
    ministry_status = models.CharField(max_length=100, blank=True)
    how_did_you_know = models.CharField(max_length=100, blank=True)
    how_will_you_attend = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    godhouse_location = models.CharField(max_length=100, blank=True)
    need_accommodation = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name_plural = "Registrations"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Schedule(models.Model):
    wwc = models.ForeignKey(WholeWordConference, on_delete=models.CASCADE, related_name="schedule")
    session = models.CharField(max_length=255, blank=True)
    time = models.TimeField()

    class Meta:
        verbose_name = _("Schedule")
        verbose_name_plural = _("Schedule")
        
    def __str__(self):
        return f"{self.session}"
        
        
class SlideImage(models.Model):
    wwc = models.ForeignKey(WholeWordConference, on_delete=models.CASCADE, related_name="slide_image")
    image = models.ImageField(verbose_name=_("image"), upload_to="wwc_images/slide_image")
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        verbose_name = _("Slide Image")
        verbose_name_plural = _("Slide Image")
