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
        "ID": 1,
        "Fname": "Ahmed",
        "Lname": "Ali",
        "Email": "ahmed.ali@example.com",
        "Mphone": "+201234567890",
        "Pass": "hashed_password_1",
        "Type": "admin",
        "Bdate": "1985-04-12",
        "Facebook_url": "https://facebook.com/ahmed.ali",
        "Country": "Egypt",
        "image_path": os.path.join(BASE_MEDIA_PATH, "user/imgs/one.jpg"),
    },
    {
        "ID": 2,
        "Fname": "Sara",
        "Lname": "Hassan",
        "Email": "sara.hassan@example.com",
        "Mphone": "+201098765432",
        "Pass": "hashed_password_2",
        "Type": "owner",
        "Bdate": "1990-08-20",
        "Facebook_url": "https://facebook.com/sara.hassan",
        "Country": "Egypt",
        "image_path": os.path.join(BASE_MEDIA_PATH, "user/imgs/two.jpg"),
    },
]

categories_data = [
    {"ID": 1, "name": "Education","description":"test description"},
    {"ID": 2, "name": "Health" ,"description":"test description"},
    {"ID": 3, "name": "Environment" ,"description":"test description"},
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
        "is_fetured": True,
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
        "is_fetured": False,
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
        "is_fetured": True,
    },
]

project_image_path = os.path.join(BASE_MEDIA_PATH, "user/imgs/one.jpg")

# إضافة Categories
for cat in categories_data:
    obj, created = Category.objects.get_or_create(ID=cat["ID"], defaults={"name": cat["name"]})
    if created:
        print(f"Category {obj.name} created.")
    else:
        print(f"Category {obj.name} already exists.")

# إضافة Users مع الصور
for u in users_data:
    user_obj, created = User.objects.get_or_create(
        ID=u["ID"],
        defaults={
            "Fname": u["Fname"],
            "Lname": u["Lname"],
            "Email": u["Email"],
            "Mphone": u["Mphone"],
            "Pass": u["Pass"],
            "Type": u["Type"],
            "Bdate": parse_datetime(u["Bdate"] + "T00:00:00Z"),
            "Facebook_url": u["Facebook_url"],
            "Country": u["Country"],
        }
    )
    # تحميل الصورة فقط إذا تم الإنشاء
    if created:
        with open(u["image_path"], "rb") as img_file:
            user_obj.image.save(os.path.basename(u["image_path"]), File(img_file))
        user_obj.save()
        print(f"User {user_obj.Fname} created with image.")
    else:
        print(f"User {user_obj.Fname} already exists.")

# إضافة Projects
# إضافة Projects
for p in projects_data:
    category_instance = Category.objects.get(ID=p["category_id"])
    user_instance = User.objects.get(ID=p["user_id"])

    project_obj, created = Project.objects.get_or_create(
        id=p["id"],  # تأكد أن هذا يتوافق مع اسم الحقل الأساسي في نموذج Project
        defaults={
            "title": p["title"],
            "details": p["details"],
            "category": category_instance,
            "target": p["target"],
            "S_time": parse_datetime(p["S_time"]),
            "E_time": parse_datetime(p["E_time"]),
            "user_id": user_instance,
            "is_fetured": p["is_fetured"],
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
