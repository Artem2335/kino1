"""Seed database with 50 real movies and reviews for v2.0.0

Note: As of v2.0.0, the ratings table has been removed.
Rating functionality is now part of the review model.
Each review has an optional rating field (1-5).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app import db

# 10 viewer users
viewers_data = [
    {"email": "ivanov@mail.ru", "username": "Иванов Игорь", "password": "viewer123"},
    {"email": "petrov@mail.ru", "username": "Петров Петр", "password": "viewer123"},
    {"email": "smirnov@mail.ru", "username": "Смирнов Сергей", "password": "viewer123"},
    {"email": "sokolov@mail.ru", "username": "Соколов Сергей", "password": "viewer123"},
    {"email": "lebedev@mail.ru", "username": "Лебедев Лев", "password": "viewer123"},
    {"email": "novikov@mail.ru", "username": "Новиков Николай", "password": "viewer123"},
    {"email": "volkov@mail.ru", "username": "Волков Виктор", "password": "viewer123"},
    {"email": "solovyev@mail.ru", "username": "Соловьев Станислав", "password": "viewer123"},
    {"email": "antonov@mail.ru", "username": "Антонов Андрей", "password": "viewer123"},
    {"email": "pavlov@mail.ru", "username": "Павлов Павел", "password": "viewer123"},
]

# Moderator and admin users
admin_user = {"email": "moderator@kinovzor.ru", "username": "moderator", "password": "admin123", "is_moderator": True}

# Real movies with posters
movies_data = [
    {"title": "Шоу Трумэна", "year": 1998, "genre": "Драма", "poster": "https://images.tmdb.org/t/p/w500/wcZAHMq0dHW0yVSiXG3wk9T8NuS.jpg", "desc": "История человека, жизнь которого - один огромный телевизионный спектакль"},
    {"title": "Жизнь прекрасна", "year": 1997, "genre": "Драма", "poster": "https://images.tmdb.org/t/p/w500/a8Q0gKwXL4sTY4e2JRqJJe0R9Uf.jpg", "desc": "Отец защищает своего сына от ужасов войны через игру и воображение"},
    {"title": "Форрест Гамп", "year": 1994, "genre": "Драма", "poster": "https://images.tmdb.org/t/p/w500/h5oK4pZKTBbzYWh5f5GR6nUyJGX.jpg", "desc": "История простого человека, который достиг невероятных высот"},
    {"title": "Зелёная миля", "year": 1999, "genre": "Драма", "poster": "https://images.tmdb.org/t/p/w500/radBbkxJuMCIgDmH6sIJ3xOIw5N.jpg", "desc": "Исправительная камера и чудо в виде сверхъестественных способностей"},
    {"title": "Спасение рядового Райана", "year": 1998, "genre": "Боевик", "poster": "https://images.tmdb.org/t/p/w500/3mQm4l3Fb9xP6R8vNPSu6s4RbVq.jpg", "desc": "Эпическая история о спасении солдата во время Второй мировой войны"},
    {"title": "Бойцовский клуб", "year": 1999, "genre": "Триллер", "poster": "https://images.tmdb.org/t/p/w500/hEv2ovsKl5p3itLVeKyUaO0d04o.jpg", "desc": "Психологический триллер о подпольном клубе бойцов"},
    {"title": "Матрица", "year": 1999, "genre": "Фантастика", "poster": "https://images.tmdb.org/t/p/w500/vgpXmVaVSUdzqkAcg1aWZbB0Bsb.jpg", "desc": "Революционный фантастический боевик о реальности и иллюзии"},
    {"title": "Список Шиндлера", "year": 1993, "genre": "Драма", "poster": "https://images.tmdb.org/t/p/w500/sF1U4EUQS8YHUPAzM9QFGpDQi23.jpg", "desc": "История немецкого бизнесмена, спасившего тысячи евреев"},
    {"title": "Звёздные войны: Эпизод I", "year": 1999, "genre": "Фантастика", "poster": "https://images.tmdb.org/t/p/w500/sblJQR6dYLmA4iZM3fZ8QZKnqFi.jpg", "desc": "Новое начало саги о войне галактик"},
    {"title": "Титаник", "year": 1997, "genre": "Мелодрама", "poster": "https://images.tmdb.org/t/p/w500/9xjZS2rlWxYGEARQbIcRswroIDe.jpg", "desc": "Эпическая романтическая драма о гибели лайнера"},
    {"title": "Красота по-американски", "year": 1999, "genre": "Драма", "poster": "https://images.tmdb.org/t/p/w500/lj03JWZVYDRmXQDwCYf3LST6zKE.jpg", "desc": "Тёмная комедия о мечтах и идеалах в пригороде"},
    {"title": "Хороший, плохой, злой", "year": 1966, "genre": "Боевик", "poster": "https://images.tmdb.org/t/p/w500/kGLuv0OWeSYXaDn7tDLwQF24xNr.jpg", "desc": "Культовый вестерн про три стрелка в поисках сокровища"},
    {"title": "Пульп Фикшн", "year": 1994, "genre": "Триллер", "poster": "https://images.tmdb.org/t/p/w500/d8duYyyC9J5T3OMsDNxoXy7AzM2.jpg", "desc": "Нелинейное повествование о криминальной жизни Лос-Анджелеса"},
    {"title": "Молчание ягнят", "year": 1991, "genre": "Триллер", "poster": "https://images.tmdb.org/t/p/w500/lqnkQg27xzj5zEMWIGDyamCs78V.jpg", "desc": "Психологический триллер про охоту на серийного убийцу"},
    {"title": "Назад в будущее", "year": 1985, "genre": "Комедия", "poster": "https://images.tmdb.org/t/p/w500/w0OMwQ67BC2I3yxn91jMmqKGP2D.jpg", "desc": "Приключенческая комедия о путешествиях во времени"},
    {"title": "Пираты Карибского моря", "year": 2003, "genre": "Приключения", "poster": "https://images.tmdb.org/t/p/w500/tkt7b9G3MC2j0FkyMb1dBG6MxPf.jpg", "desc": "Веселое приключение капитана Джека Воробья"},
    {"title": "Великий Гэтсби", "year": 2013, "genre": "Драма", "poster": "https://images.tmdb.org/t/p/w500/fpVcjqoKXRVHlWpbiKLEeA6XC7S.jpg", "desc": "Роман о любви, амбициях и американской мечте"},
    {"title": "Интерстеллар", "year": 2014, "genre": "Фантастика", "poster": "https://images.tmdb.org/t/p/w500/nv5yFk2kZo6jjc2gc3umaGmel8Z.jpg", "desc": "Космическая эпопея о спасении человечества"},
    {"title": "Темный рыцарь", "year": 2008, "genre": "Боевик", "poster": "https://images.tmdb.org/t/p/w500/1hCw8kSUIKd9yb1PLV2yAGG7vIY.jpg", "desc": "Второй фильм о Бэтмене с легендарным Джокером"},
    {"title": "Социальная сеть", "year": 2010, "genre": "Драма", "poster": "https://images.tmdb.org/t/p/w500/gzJnMEMnWay6UWuKvnEfM9VZeI9.jpg", "desc": "История создания Facebook и его основателя"},
    {"title": "Лучший стрелок", "year": 1986, "genre": "Боевик", "poster": "https://images.tmdb.org/t/p/w500/xGKNcXc0M8cVERYV7tVrVgkn5ZL.jpg", "desc": "История летчика истребителя и его романтичного пути"},
    {"title": "Джанго освобожденный", "year": 2012, "genre": "Боевик", "poster": "https://images.tmdb.org/t/p/w500/v8ZaC0QrMLKqHSi2X0HMXVK5X9M.jpg", "desc": "Западный боевик о борьбе с рабством"},
    {"title": "Мёртвые поэты общества", "year": 1989, "genre": "Драма", "poster": "https://images.tmdb.org/t/p/w500/2l8Rgc2V7o81GKD8dMD9dHmcbJh.jpg", "desc": "Вдохновляющая история учителя и его учеников"},
    {"title": "Выцветший гвоздик", "year": 1992, "genre": "Боевик", "poster": "https://images.tmdb.org/t/p/w500/7bnJAyGxNRWZ8YxqgQkuOI3ZTzi.jpg", "desc": "Мрачный вестерн про старого стрелка"},
    {"title": "Холодная гора", "year": 2003, "genre": "Драма", "poster": "https://images.tmdb.org/t/p/w500/aJyJDNz79B4w5r8QVLpIozY7Ppf.jpg", "desc": "История любви и войны в период Гражданской войны"},
    {"title": "Один дома", "year": 1990, "genre": "Комедия", "poster": "https://images.tmdb.org/t/p/w500/r1bKEBUgJDJ6dIwBN2L6oG8BYtX.jpg", "desc": "Семейная комедия о мальчике, оставшемся защищать дом"},
    {"title": "Ловушка для мамы", "year": 1998, "genre": "Комедия", "poster": "https://images.tmdb.org/t/p/w500/6K5yJvHVLk2p6dVBOHlzJ1tqMnl.jpg", "desc": "Комедия про близнецов, разлученных при рождении"},
    {"title": "Город грехов", "year": 2005, "genre": "Боевик", "poster": "https://images.tmdb.org/t/p/w500/jJJqVjvJStvVb9eoSQxP4S3K3Vy.jpg", "desc": "Нуаровский боевик про преступный город"},
    {"title": "Люди в чёрном", "year": 1997, "genre": "Комедия", "poster": "https://images.tmdb.org/t/p/w500/z1p34vh_XGMElephic263GDwHu4.jpg", "desc": "Весёлая комедия про инопланетян и секретных агентов"},
    {"title": "Парк Юрского периода", "year": 1993, "genre": "Приключения", "poster": "https://images.tmdb.org/t/p/w500/WXZ1O0nYL9T2AehM8YGOmtEj2Ov.jpg", "desc": "Культовая фантастика про парк динозавров"},
]

reviews_templates = {
    "Драма": [
        {"text": "Глубокий фильм, который трогает за душу. Актёры играют великолепно!", "rating": 5},
        {"text": "Эмоциональная история, не могу оторваться от экрана.", "rating": 5},
        {"text": "Хорошая драма, но местами медленновато.", "rating": 4},
        {"text": "Интересный сюжет, но концовка предсказуема.", "rating": 3},
        {"text": "Мощная история, оставляет впечатление.", "rating": 5},
        {"text": "Неплохо, но мне кажется, лучше читать книгу.", "rating": 3},
    ],
    "Боевик": [
        {"text": "Динамичный и захватывающий боевик! Отличные трюки!", "rating": 5},
        {"text": "Супер! Не скучал ни секунды, экшена на всё 100%", "rating": 5},
        {"text": "Хороший боевик, но сюжет немного слабый.", "rating": 4},
        {"text": "Много взрывов и стрельбы, без особого смысла.", "rating": 3},
        {"text": "Классический боевик! Есть всё - действие, герой, девушка!", "rating": 5},
        {"text": "Предсказуемо, но развлечения ради годится.", "rating": 3},
    ],
    "Фантастика": [
        {"text": "Поражающий воображение фильм! Великолепная визуализация!", "rating": 5},
        {"text": "Научная фантастика на высшем уровне. Просто восхитительно!", "rating": 5},
        {"text": "Интересные идеи, но реализация могла быть лучше.", "rating": 4},
        {"text": "Слишком много компьютерной графики, мало сюжета.", "rating": 3},
        {"text": "Инновационный и захватывающий фильм!", "rating": 5},
        {"text": "Хорошая фантастика, но местами скучновато.", "rating": 3},
    ],
    "Комедия": [
        {"text": "Очень смешная и весёлая! Перенеслась в прекрасное настроение!", "rating": 5},
        {"text": "Отличная комедия! Смеялась весь фильм!", "rating": 5},
        {"text": "Забавная комедия, хорошо помогает расслабиться.", "rating": 4},
        {"text": "Юмор не очень, но что-то смешное есть.", "rating": 3},
        {"text": "Гениальная комедия! Просто шедевр юмора!", "rating": 5},
        {"text": "Попытка комедии, но юмор странноват.", "rating": 2},
    ],
    "Триллер": [
        {"text": "Напряженный и захватывающий триллер! На краю кресла!", "rating": 5},
        {"text": "Держит в напряжении всё время. Отличный триллер!", "rating": 5},
        {"text": "Хороший триллер, но предсказуем в некоторых местах.", "rating": 4},
        {"text": "Ничего особенного, стандартный триллер.", "rating": 3},
        {"text": "Невероятно напряженный и интересный фильм!", "rating": 5},
        {"text": "Можно посмотреть, но лучше есть.", "rating": 3},
    ],
    "Мелодрама": [
        {"text": "Трогательная история любви. Со слезами на глазах!", "rating": 5},
        {"text": "Красивая любовная история. Очень романтично!", "rating": 5},
        {"text": "Мелодрама хороша, но местами слишком сладкая.", "rating": 4},
        {"text": "Стандартная история любви, ничего нового.", "rating": 3},
        {"text": "Волшебный фильм про вечную любовь!", "rating": 5},
        {"text": "Слишком много слёз, мало действия.", "rating": 2},
    ],
    "Приключения": [
        {"text": "Захватывающее приключение! Магия и чудеса!", "rating": 5},
        {"text": "Веселое путешествие полное сюрпризов!", "rating": 5},
        {"text": "Хороший фильм про приключения, развлечение гарантировано.", "rating": 4},
        {"text": "Неплохо для семейного просмотра.", "rating": 3},
        {"text": "Шикарный фильм про путешествия и дружбу!", "rating": 5},
        {"text": "Неплохо, но могло быть ещё лучше.", "rating": 3},
    ],
}

def seed_movies_and_reviews():
    """Load all movies with reviews and users into database
    
    v2.0.0 Changes:
    - Removed ratings table (ratings are now part of reviews)
    - Passwords are automatically hashed in create_user()
    - Each review can have an optional rating field (1-5)
    """
    print("\n🎬 Loading movies, reviews, and users for v2.0.0...\n")
    
    # Create users first
    print("👥 Creating users...")
    user_ids = []
    
    # Create 10 viewers
    # Passwords are automatically hashed in create_user()
    for viewer in viewers_data:
        user = db.create_user(
            email=viewer["email"],
            username=viewer["username"],
            password=viewer["password"]  # Will be auto-hashed
        )
        user_ids.append(user['id'])
        print(f"   ✅ Created viewer: {viewer['username']}")
    
    # Create moderator
    # Password will be auto-hashed
    admin = db.create_user(
        email=admin_user["email"],
        username=admin_user["username"],
        password=admin_user["password"],  # Will be auto-hashed
        is_moderator=admin_user["is_moderator"]
    )
    print(f"   ✅ Created moderator: {admin_user['username']}")
    
    print(f"\n🎬 Creating {len(movies_data)} movies with reviews...\n")
    
    total_reviews = 0
    
    for i, movie_info in enumerate(movies_data):
        # Create movie
        movie = db.create_movie(
            title=movie_info["title"],
            description=movie_info["desc"],
            genre=movie_info["genre"],
            year=movie_info["year"],
            poster_url=movie_info["poster"]
        )
        movie_id = movie['id']
        
        # Get reviews for this genre
        genre_reviews = reviews_templates.get(movie_info["genre"], reviews_templates["Драма"])
        
        # Add 4-7 reviews per movie from different users
        review_count = 4 + (i % 4)  # 4-7 reviews
        for j in range(review_count):
            review = genre_reviews[j % len(genre_reviews)]
            # Assign to different user (cycle through user_ids)
            user_id = user_ids[j % len(user_ids)]
            
            # Create review with rating
            # v2.0.0: Ratings are part of review, not separate table
            db.create_review(
                movie_id=movie_id,
                user_id=user_id,
                text=review["text"],
                rating=review["rating"]
            )
            total_reviews += 1
        
        # Print progress
        if (i + 1) % 10 == 0:
            print(f"  ✅ {i + 1}/{len(movies_data)} movies loaded")
    
    print("\n✅ All data loaded successfully!")
    print("\n📊 Database Summary:")
    print(f"   🎬 {len(movies_data)} movies")
    print(f"   👥 {len(user_ids)} viewers + 1 moderator")
    print(f"   🗣️  {total_reviews} reviews with ratings")
    print(f"\n🔐 Test Accounts:")
    print(f"   Moderator:")
    print(f"   • Email: {admin_user['email']}")
    print(f"   • Password: {admin_user['password']}")
    print(f"\n   Viewer Example (Иванов Игорь):")
    print(f"   • Email: {viewers_data[0]['email']}")
    print(f"   • Password: {viewers_data[0]['password']}")
    print(f"\n📁 Database: kinovzor.db")
    print(f"\n💡 v2.0.0 Changes:")
    print(f"   ✅ Ratings table removed (ratings are in reviews)")
    print(f"   ✅ Passwords automatically hashed with bcrypt")
    print(f"   ✅ Each review can have rating 1-5\n")

if __name__ == "__main__":
    seed_movies_and_reviews()
