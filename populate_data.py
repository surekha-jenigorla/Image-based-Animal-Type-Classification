import os
import django
import random
from django.utils import timezone
from datetime import timedelta

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from breeds.models import Breed
from recognition.models import BreedScan
from notifications.models import Notification
from profiles.models import Profile

User = get_user_model()

def populate():
    print("Starting database population...")

    # 1. Create a Demo User
    user, created = User.objects.get_or_create(email="demo@farmer.com")
    if created:
        user.set_password("demo1234")
        user.save()
        Profile.objects.get_or_create(user=user, full_name="Rajesh Kumar", phone_number="+91 98765 43210", farm_location="Gujarat, India")
    
    # 2. Create Breeds (Breed Library & Management)
    breeds_data = [
        {'name': 'Gir', 'type': 'Cattle', 'desc': 'Famous milk breed from Gujarat.'},
        {'name': 'Sahiwal', 'type': 'Cattle', 'desc': 'High milk yield, heat tolerant.'},
        {'name': 'Murrah', 'type': 'Buffalo', 'desc': 'The "Black Gold" of Haryana.'},
        {'name': 'Ongole', 'type': 'Cattle', 'desc': 'Known for toughness and work power.'},
        {'name': 'Jaffarabadi', 'type': 'Buffalo', 'desc': 'Massive buffalo breed with high fat milk.'}
    ]

    for b in breeds_data:
        Breed.objects.get_or_create(
            name=b['name'], 
            category=b['type'], 
            defaults={'description': b['desc'], 'origin_location': 'India'}
        )

    # 3. Create Scan History (Dynamic Dashboard & Reports)
    breeds = Breed.objects.all()
    for i in range(25):
        selected_breed = random.choice(breeds)
        days_ago = random.randint(0, 14)
        scan_time = timezone.now() - timedelta(days=days_ago)
        
        BreedScan.objects.create(
            user=user,
            breed_name=selected_breed.name,
            cattle_type=selected_breed.category,
            confidence_score=random.randint(85, 99),
            scanned_at=scan_time
        )

    # 4. Create Notifications
    Notification.objects.create(
        user=user,
        title="Welcome to CattleBreed AI",
        message="Your account is active. Start scanning to identify breeds!",
        notification_type='success'
    )
    
    print(f"Success! Created {len(breeds_data)} breeds and 25 scan records for {user.email}.")

if __name__ == '__main__':
    populate()