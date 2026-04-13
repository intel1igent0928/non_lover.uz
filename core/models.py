from django.db import models

class Banner(models.Model):
    title = models.CharField("Заголовок", max_length=200)
    subtitle = models.TextField("Подзаголовок", blank=True)
    image_1 = models.ImageField("Первое изображение", upload_to='banner/')
    image_2 = models.ImageField("Второе изображение", upload_to='banner/')

    class Meta:
        verbose_name = "Баннер (Главная)"
        verbose_name_plural = "Баннер (Главная)"

    def __str__(self):
        return self.title

class StoryCategory(models.Model):
    name = models.SlugField("Техническое имя (ID)", unique=True)
    label = models.CharField("Название категории", max_length=100)
    thumbnail = models.ImageField("Обложка", upload_to='stories/thumbs/')
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        verbose_name = "Категория историй"
        verbose_name_plural = "Категории историй"
        ordering = ['order']

    def __str__(self):
        return self.label

class StoryItem(models.Model):
    category = models.ForeignKey(StoryCategory, related_name='items', on_delete=models.CASCADE, verbose_name="Категория")
    image = models.ImageField("Изображение", upload_to='stories/')
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        verbose_name = "Слайд истории"
        verbose_name_plural = "Слайды историй"
        ordering = ['order']

class SiteContent(models.Model):
    key = models.CharField("Ключ (тех.)", max_length=100, unique=True)
    value = models.TextField("Значение (текст)")

    class Meta:
        verbose_name = "Текстовое наполнение"
        verbose_name_plural = "Текстовое наполнение"

    def __str__(self):
        return self.key

class CourseFeature(models.Model):
    title = models.CharField("Заголовок модуля", max_length=200)
    description = models.TextField("Описание")
    icon = models.ImageField("Иконка/Изображение", upload_to='course_features/', blank=True)
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        verbose_name = "Модуль курса"
        verbose_name_plural = "Модули курса"
        ordering = ['order']

class SplashLink(models.Model):
    ICON_CHOICES = [
        ('telegram', 'Telegram'),
        ('instagram', 'Instagram'),
        ('enter', 'Вход (Кнопка входа)'),
        ('link', 'Обычная ссылка'),
    ]
    title = models.CharField("Текст ссылки", max_length=100)
    url = models.CharField("URL / Ссылка", max_length=500)
    icon_type = models.CharField("Тип иконки", max_length=20, choices=ICON_CHOICES, default='telegram')
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        verbose_name = "Ссылка на заставке"
        verbose_name_plural = "Ссылки на заставке"
        ordering = ['order']

    def __str__(self):
        return self.title

class SocialLink(models.Model):
    ICON_CHOICES = [
        ('telegram', 'Telegram'),
        ('instagram', 'Instagram'),
        ('phone', 'Phone / WhatsApp'),
    ]
    url = models.CharField("URL / Ссылка", max_length=500)
    icon_type = models.CharField("Тип иконки", max_length=20, choices=ICON_CHOICES, default='telegram')
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        verbose_name = "Ссылка в футере"
        verbose_name_plural = "Ссылки в футере"
        ordering = ['order']

    def __str__(self):
        return self.icon_type
