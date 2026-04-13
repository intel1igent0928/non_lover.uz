import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sourdough_site.settings')
django.setup()

from core.models import SiteContent, StoryCategory, StoryItem, SplashLink, Banner, CourseFeature, SocialLink
from django.core.files import File

def seed():
    print("Seeding Banner...")
    banner, created = Banner.objects.get_or_create(
        title="ЗАКВАСКАЛИ НОН",
        defaults={
            "subtitle": "Uyda zakvaska bilan haqiqiy non pishirishni o‘rganing. Mazzali va sifatli non pishirish bo'yicha onlayn darslarimiz bilan hunaringizni oshiring.",
        }
    )
    if os.path.exists("assets/xleb.png"):
        with open("assets/xleb.png", "rb") as f:
            banner.image_1.save("xleb.png", File(f), save=True)
    if os.path.exists("assets/zakvaska.png"):
        with open("assets/zakvaska.png", "rb") as f:
            banner.image_2.save("zakvaska.png", File(f), save=True)

    print("Seeding Social Links (Footer)...")
    social_links = [
        {"icon_type": "telegram", "url": "https://t.me/yourchannel", "order": 1},
        {"icon_type": "instagram", "url": "https://instagram.com/non_lover.uz", "order": 2},
        {"icon_type": "phone", "url": "tel:+998123456789", "order": 3},
    ]
    for s_link in social_links:
        SocialLink.objects.update_or_create(icon_type=s_link['icon_type'], defaults=s_link)

    print("Seeding Site Content...")
    content_map = {
        "main_title": "ЗАКВАСКАЛИ НОН",
        "curriculum_title": "Kursda nimalar o’rganasiz",
        "pricing_title": "Kurs narxi",
        "old_price": "1 000 000",
        "new_price": "800 000 so’m",
    }
    for key, value in content_map.items():
        SiteContent.objects.update_or_create(key=key, defaults={'value': value})

    print("Seeding Course Features...")
    features = [
        {"title": "Bug’doy unidan", "description": "Pshyenichnaya Zalvaska", "icon": "assets/kurs1.png", "order": 1},
        {"title": "Javdar unidan", "description": "Rzhanaya Zalvaska", "icon": "assets/kurs2.png", "order": 2},
        {"title": "Bug’doy unidan", "description": "Pshyenichnaya Zalvaska", "icon": "assets/kurs3.png", "order": 3},
        {"title": "Javdar unidan", "description": "Rzhanaya Zalvaska", "icon": "assets/kurs4.png", "order": 4},
    ]
    for f_data in features:
        feat, created = CourseFeature.objects.get_or_create(title=f_data['title'], order=f_data['order'], defaults={'description': f_data['description']})
        if os.path.exists(f_data['icon']):
            with open(f_data['icon'], 'rb') as f:
                feat.icon.save(os.path.basename(f_data['icon']), File(f), save=True)

    print("Seeding Splash Links...")
    links = [
        {"title": "Telegram Kanal", "url": "https://t.me/yourchannel", "icon_type": "telegram", "order": 1},
        {"title": "Instagram", "url": "https://instagram.com/non_lover.uz", "icon_type": "instagram", "order": 2},
        {"title": "Kurs haqida ma'lumot", "url": "#", "icon_type": "enter", "order": 3},
    ]
    for link in links:
        SplashLink.objects.update_or_create(title=link['title'], defaults=link)

    print("Seeding Gallery...")
    categories = [
        {"name": "zkvsk", "label": "Zakvaska", "thumb": "assets/zkvsk1.jpg", "order": 1},
        {"name": "bread", "label": "Nonlar", "thumb": "assets/bread5.jpg", "order": 2},
        {"name": "natija", "label": "Natijalar", "thumb": "assets/natija1.jpg", "order": 3},
    ]
    
    story_map = {
        "zkvsk": ["assets/zkvsk1.jpg", "assets/zkvsk2.jpg", "assets/zkvsk3.jpg", "assets/zkvsk4.jpg", "assets/zkvsk5.jpg", "assets/zkvsk6.jpg"],
        "bread": ["assets/bread5.jpg", "assets/bread6.jpg", "assets/bread7.jpg", "assets/bread8.jpg", "assets/bread9.jpg", "assets/bread10.jpg"],
        "natija": ["assets/natija1.jpg", "assets/natija2.jpg", "assets/natija3.jpg", "assets/natija4.jpg"],
    }

    for cat_data in categories:
        cat, created = StoryCategory.objects.get_or_create(name=cat_data['name'], defaults={
            'label': cat_data['label'],
            'order': cat_data['order']
        })
        if os.path.exists(cat_data['thumb']):
            with open(cat_data['thumb'], 'rb') as f:
                cat.thumbnail.save(os.path.basename(cat_data['thumb']), File(f), save=True)

        # To avoid MultipleObjectsReturned, we clear existing items for this category first
        cat.items.all().delete()

        # Items
        items = story_map.get(cat_data['name'], [])
        for i, img_path in enumerate(items):
            if os.path.exists(img_path):
                with open(img_path, 'rb') as f:
                    item = StoryItem.objects.create(category=cat, order=i)
                    item.image.save(os.path.basename(img_path), File(f), save=True)

    print("Done seeding!")

if __name__ == "__main__":
    seed()
