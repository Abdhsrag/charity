from user.models import User
from category.models import Category
from project.models import Project
from project_image.models import Project_image
from datetime import datetime
from django.utils.timezone import make_aware
from django.core.files import File
import os

def parse_datetime(dt_str):
    dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
    # إذا التاريخ aware بالفعل، ارجعه كما هو
    if dt.tzinfo is not None and dt.tzinfo.utcoffset(dt) is not None:
        return dt
    # إذا كان naive، اجعله aware
    return make_aware(dt)

BASE_MEDIA_PATH = 'media/'  # عدل المسار هنا لمجلد media عندك

users_data = [
    {
        "id": 1,
        "fname": "Ahmed",
        "lname": "Ali",
        "email": "ahmed.ali@example.com",
        "mphone": "+201234567890",
        "password": "hashed_password_1",
        "type": "admin",
        "bdate": "1985-04-12",
        "facebook_url": "https://facebook.com/ahmed.ali",
        "country": "Egypt",
        "image_path": os.path.join(BASE_MEDIA_PATH, "user/imgs/one.jpg"),
    },
    {
        "id": 2,
        "fname": "Sara",
        "lname": "Hassan",
        "email": "sara.hassan@example.com",
        "mphone": "+201098765432",
        "password": "hashed_password_2",
        "type": "owner",
        "bdate": "1990-08-20",
        "facebook_url": "https://facebook.com/sara.hassan",
        "country": "Egypt",
        "image_path": os.path.join(BASE_MEDIA_PATH, "user/imgs/two.jpg"),
    },
]

categories_data = [
    {"id": 1, "name": "Education","description":"test description"},
    {"id": 2, "name": "Health" ,"description":"test description"},
    {"id": 3, "name": "Environment" ,"description":"test description"},
]

projects_data = [
    {
        "id": 1,
        "title": "Clean Water Initiative",
        "details": "Project aims to provide clean drinking water in rural areas.",
        "category_id": 2,
        "target": "10000 USD",
        "S_time": "2025-06-01T08:00:00Z",
        "E_time": "2025-12-31T23:59:59Z",
        "user_id": 2,
        "is_featured": True,
    },
    {
        "id": 2,
        "title": "School Supplies for Kids",
        "details": "Providing school supplies for underprivileged children.",
        "category_id": 1,
        "target": "5000 USD",
        "S_time": "2025-05-15T08:00:00Z",
        "E_time": "2025-11-15T23:59:59Z",
        "user_id": 2,
        "is_featured": False,
    },
    {
        "id": 3,
        "title": "Tree Planting Campaign",
        "details": "Planting trees to combat deforestation.",
        "category_id": 3,
        "target": "3000 USD",
        "S_time": "2025-07-01T08:00:00Z",
        "E_time": "2025-10-31T23:59:59Z",
        "user_id": 1,
        "is_featured": True,
    },
]

project_image_path = os.path.join(BASE_MEDIA_PATH, "user/imgs/one.jpg")

# إضافة Categories
for cat in categories_data:
    obj, created = Category.objects.get_or_create(id=cat["id"], defaults={"name": cat["name"]})
    if created:
        print(f"Category {obj.name} created.")
    else:
        print(f"Category {obj.name} already exists.")

# إضافة Users مع الصور
for u in users_data:
    user_obj, created = User.objects.get_or_create(
        id=u["id"],
        defaults={
            "fname": u["fname"],
            "lname": u["lname"],
            "email": u["email"],
            "mphone": u["mphone"],
            "password": u["password"],
            "type": u["type"],
            "bdate": parse_datetime(u["bdate"] + "T00:00:00Z"),
            "facebook_url": u["facebook_url"],
            "country": u["country"],
        }
    )
    # تحميل الصورة فقط إذا تم الإنشاء
    if created:
        with open(u["image_path"], "rb") as img_file:
            user_obj.image.save(os.path.basename(u["image_path"]), File(img_file))
        user_obj.save()
        print(f"User {user_obj.fname} created with image.")
    else:
        print(f"User {user_obj.fname} already exists.")

# إضافة Projects
# إضافة Projects
for p in projects_data:
    category_instance = Category.objects.get(id=p["category_id"])
    user_instance = User.objects.get(id=p["user_id"])

    project_obj, created = Project.objects.get_or_create(
        id=p["id"],  # تأكد أن هذا يتوافق مع اسم الحقل الأساسي في نموذج Project
        defaults={
            "title": p["title"],
            "details": p["details"],
            "category_id": category_instance,
            "target": p["target"],
            "S_time": parse_datetime(p["S_time"]),
            "E_time": parse_datetime(p["E_time"]),
            "user_id": user_instance,
            "is_featured": p["is_featured"],
        }
    )
    if created:
        print(f"Project {project_obj.title} created.")
    else:
        print(f"Project {project_obj.title} already exists.")

    # إضافة صورة لكل مشروع
    with open(project_image_path, "rb") as img_file:
        # أنشئ كائن Project_image واحفظه في متغير
        image_obj = Project_image.objects.create(
            project_id=project_obj,  # استخدم الاسم الصحيح للحقل كما في الموديل
            url=File(img_file)
        )

        # احفظ الصورة في الحقل url باستخدام اسم الملف الأصلي
        image_obj.url.save(os.path.basename(project_image_path), File(img_file))
        image_obj.save()

        print(f"Image for project {project_obj.title} added.")
