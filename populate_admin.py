import os
import django
import random
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from breeds.models import Breed
from recognition.models import BreedScan
from profiles.models import Profile

User = get_user_model()

def populate_admin_data():
    print("🚀 Populating Admin & Global System Data...")

    # 1. Create Multiple Users (to fill 'Total Users' metric)
    user_data = [
        ("farmer_rajesh@gmail.com", "Rajesh Kumar", "Gujarat"),
        ("amit_dairy@yahoo.com", "Amit Patel", "Punjab"),
        ("sunita_farms@gmail.com", "Sunita Devi", "Haryana"),
        ("kerala_livestock@outlook.com", "Manoj Nair", "Kerala")
    ]

    all_users = []
    for email, name, loc in user_data:
        u, created = User.objects.get_or_create(email=email)
        if created:
            u.set_password("pass1234")
            u.save()
            Profile.objects.update_or_create(
                user=u, 
                defaults={'full_name': name, 'farm_location': loc}
            )
        all_users.append(u)

    # 2. Add More Detailed Breeds (to fill 'Breed DB Size')
    breeds_list = [
        ('Gir', 'Cattle', 'Gujarat'),
        ('Sahiwal', 'Cattle', 'Punjab'),
        ('Murrah', 'Buffalo', 'Haryana'),
        ('Tharparkar', 'Cattle', 'Rajasthan'),
        ('Surti', 'Buffalo', 'Gujarat'),
        ('Red Sindhi', 'Cattle', 'Sindh Region'),
        ('Mehsana', 'Buffalo', 'Gujarat'),
    ]

    for b_name, b_type, b_loc in breeds_list:
        Breed.objects.update_or_create(
            name=b_name, 
            category=b_type, 
            defaults={'origin_location': b_loc, 'description': f"Traditional {b_type} breed from {b_loc}."}
        )

    # 3. Create Global Scan Activity (to fill 'Recent Global Scans' table)
    # This creates a "Live Feed" effect on your admin dashboard
    all_breeds = Breed.objects.all()
    for _ in range(40):
        u = random.choice(all_users)
        b = random.choice(all_breeds)
        
        # Randomly distribute scans over the last 30 days
        days_ago = random.randint(0, 30)
        BreedScan.objects.create(
            user=u,
            breed_name=b.name,
            cattle_type=b.category,
            confidence_score=random.randint(75, 99),
            scanned_at=timezone.now() - timedelta(days=days_ago)
        )

    print(f"✅ Success: System now has {User.objects.count()} Users, {Breed.objects.count()} Breeds, and {BreedScan.objects.count()} Total Scans.")

if __name__ == '__main__':
    populate_admin_data()