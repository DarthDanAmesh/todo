from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from autoslug import AutoSlugField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from hitcount.models import HitCount
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError
from PIL import Image

# Create your models here.
STATUS = ((0,'Active'),(1,'Completed'),(2,'Due Date Passed'))
COUNTIES = (
    ('Mombasa', 'Mombasa'), ('Nairobi City', 'Nairobi City'), ('Kisumu', 'Kisumu'), ('Nakuru', 'Nakuru'),
    ('Migori', 'Migori'), ('Lamu', 'Lamu'),
    ('Kilifi', 'Kilifi'), ('Kwale', 'Kwale'), ('Kakamega', 'Kakamega'), ('Moyale', 'Moyale'), ('Busia', 'Busia'),
    ('Kiambu', 'Kiambu'), ('Nyamira', 'Nyamira'),
    ('Vihiga', 'Vihiga'), ('Machakos', 'Machakos'), ('Embu', 'Embu'), ('Bomet', 'Bomet'), ('Meru', 'Meru'),
    ('Uasin Gishu', 'Uasin Gishu'), ('Bungoma', 'Bungoma'), ('Siaya', 'Siaya'), ('Narok', 'Narok'),
    ('Mandera', 'Mandera'), ('Nandi', 'Nandi'), ('Nyeri', 'Nyeri'), ('Tharaka Nithi', 'Tharaka Nithi'),
    ('Elgeyo Marakwet', 'Elgeyo Marakwet'), ('Makueni', 'Makueni'), ('Kisii', 'Kisii'), ('Kirinyaga', 'Kirinyaga'),
    ('Kitui', 'Kitui'), ('Kericho', 'Kericho'),
    ('Nyandarua', 'Nyandarua'), ('Marsabit', 'Marsabit'), ('Homa Bay', 'Homa Bay'), ('Kajiado', 'Kajiado'),
    ('Trans Nzoia', 'Trans Nzoia'), ('Taita Taveta', 'Taita Taveta'),
    ('Isiolo', 'Isiolo'), ('Samburu', 'Samburu'), ('Wajir', 'Wajir'), ('Turkana', 'Turkana'),
    ('West Pokot', 'West Pokot'), ('Garissa', 'Garissa'), ('Tana River', 'Tana River'),
    ("Murang'a", "Murang'a"), ('Baringo', 'Baringo'), ('Laikipia', 'Laikipia'),
)

SEX = (('Female', 'Female'),
       ('Male', 'Male'),)
       
class ToDo(models.Model):
    item = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    date_assigned = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    status = models.IntegerField(STATUS, default=0, validators=[MaxValueValidator(120)])

    class Meta:
        ordering = ['-date_assigned']

    def __str__(self):
        return self.item
        
class CustomMzalendoManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('-date_created')


#fix the image issue for new additions.
class Mzalendo(models.Model):
    name = models.CharField(max_length=200)
    gender = models.CharField(max_length=50, choices=SEX, blank=True, null=True)
    county = models.CharField(max_length=150, choices=COUNTIES, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    life = models.TextField(blank=True, null=True)
    dod = models.DateField('Date Deceased', blank=True, null=True)
    author = models.CharField(max_length=255)
    cover = models.ImageField(upload_to="covers/", blank=True, verbose_name="Cover Image")
    image_thumbnail = ImageSpecField(source='cover',
                                      processors=[ResizeToFill(150, 150)],
                                      format='JPEG',
                                      options={'quality': 60})
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="mzalendo_updatedby", null=True, blank=True
    )
    hit_count_generic = GenericRelation(
                HitCount,
                object_id_field='object_pk',
                related_query_name='hit_count_generic_relation'
                )
    objects = CustomMzalendoManager()

    def generate_slug(instance):
        return f"{instance.age}-{instance.name}-{instance.county}"
    
    slug = AutoSlugField(unique=True, always_update=False, populate_from=generate_slug)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_created']

    def clean(self):
        if self.age < 0:
            raise ValidationError('Age cannot be negative')
        super().clean()
    
    def get_absolute_url(self):
        return reverse("mzalendo_detail", kwargs={"slug": self.slug})

    @property
    def cover_url(self):
        if self.cover:
            return getattr(self.cover, 'url', None)
            
    def __str__(self):
        return self.name        

class CustomCommentManger(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('-added')


class Comment(models.Model):
    post = models.ForeignKey(Mzalendo, on_delete=models.CASCADE, related_name='mzalendo_comments')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    comment = models.TextField()
    added = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=True)

    objects = CustomCommentManger()

    def __str__(self):
        return f"{self.user} on {self.post}"
    
    def get_delete_url(self):
        return reverse('mzalendo:delete-comment', kwargs = {'pk': self.pk})


class Verifier(models.Model):
    mzalendo = models.OneToOneField(Mzalendo, on_delete=models.CASCADE)
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="verifier_approvedby")
    approved_at = models.DateTimeField(auto_now_add=True)

    def approve(self):
        self.mzalendo.approved = True
        self.mzalendo.save()

    def __str__(self):
        return f"Verifier for {self.mzalendo.last_name}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avi = models.ImageField(default='avatar.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Image is imported from PIL
        img = Image.open(self.avi.path)
        # check file size and resize of > 150 x 150 in pixels
        if img.height > 150 or img.width > 150:
            output_size = (150, 150)
            img.thumbnail(output_size)
            img.save(self.avi.path)


#create a post signal for when a user is created a profile is created
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


    


    


