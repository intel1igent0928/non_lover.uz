from django.db import models

class SiteContent(models.Model):
    key = models.CharField(max_length=100, unique=True, help_text="Unique key for the content (e.g. hero_title)")
    value = models.TextField(help_text="The actual text content")
    
    def __str__(self):
        return f"{self.key}: {self.value[:30]}..."

    class Meta:
        verbose_name = "Matnli kontent"
        verbose_name_plural = "Matnli kontentlar"

class StoryCategory(models.Model):
    name = models.CharField(max_length=50, unique=True, help_text="e.g. zkvsk")
    label = models.CharField(max_length=100, help_text="Display label, e.g. Zakvaska")
    thumbnail = models.ImageField(upload_to='categories/', help_text="Bubble image")
    order = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.label

    class Meta:
        verbose_name = "Galereya kategoriyasi"
        verbose_name_plural = "Galereya kategoriyalari"
        ordering = ['order']

class StoryItem(models.Model):
    category = models.ForeignKey(StoryCategory, on_delete=models.CASCADE, related_name='items')
    image = models.ImageField(upload_to='stories/')
    order = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"Story for {self.category.label} - {self.id}"

    class Meta:
        verbose_name = "Storis rasm"
        verbose_name_plural = "Storis rasmlari"
        ordering = ['order']

class SplashLink(models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField()
    icon_type = models.CharField(max_length=20, choices=[('telegram', 'Telegram'), ('instagram', 'Instagram'), ('enter', 'Enter')], default='enter')
    order = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Splash havolasi"
        verbose_name_plural = "Splash havolalari"
        ordering = ['order']
