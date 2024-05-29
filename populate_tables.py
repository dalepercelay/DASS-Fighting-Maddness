import sqlalchemy
import os
import dotenv
from faker import Faker
import numpy as np

def database_connection_url():
    dotenv.load_dotenv()
    DB_USER: str = os.environ.get("POSTGRES_USER")
    DB_PASSWD = os.environ.get("POSTGRES_PASSWORD")
    DB_SERVER: str = os.environ.get("POSTGRES_SERVER")
    DB_PORT: str = os.environ.get("POSTGRES_PORT")
    DB_NAME: str = os.environ.get("POSTGRES_DB")
    return f"postgresql://{DB_USER}:{DB_PASSWD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"

# Create a new DB engine based on our connection string
engine = sqlalchemy.create_engine(database_connection_url(), use_insertmanyvalues=True)
categories = ['News', 'Sports', 'Politics', 'Entertainment', 'Technology', 'Science', 'Health', 'Business', 'Travel', 'Food']

with engine.begin() as conn:
    conn.execute(sqlalchemy.text("""
    DROP TABLE IF EXISTS likes;
    DROP TABLE IF EXISTS posts;
    DROP TABLE IF EXISTS users;
    DROP TABLE IF EXISTS category;

    CREATE TABLE 
        category (
            id int generated always as identity not null PRIMARY KEY,
            category_name text not null
        );

    CREATE TABLE
    users (
        id int generated always as identity not null PRIMARY KEY,
        username text unique not null,
        full_name text not null,
        birthday date not null,
        device_type text not null
    );    
        
    CREATE TABLE
    posts (
        id int generated always as identity not null PRIMARY KEY,
        title text not null, 
        content text not null,
        created_at timestamp not null,
        visible boolean not null,
        poster_id int not null references users(id),
        category_id int  not null references category(id),
        likes int default 0,
        nsfw boolean default false
    );
    """))
    
    # populate initial posting categories
    for category in categories:    
        conn.execute(sqlalchemy.text("""
        INSERT INTO category (category_name) VALUES (:category_name);
        """), {"category_name": category})

num_users = 200000
fake = Faker()
posts_sample_distribution = np.random.default_rng().negative_binomial(0.04, 0.01, num_users)
category_sample_distribution = np.random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                                                 num_users,
                                                p=[0.1, 0.05, 0.1, 0.3, 0.05, 0.05, 0.05, 0.05, 0.15, 0.1])
total_posts = 0

# create fake posters with fake names and birthdays
with engine.begin() as conn:
    print("creating fake posters...")
    posts = []
    for i in range(num_users):
        if (i % 10 == 0):
            print(i)
        
        profile = fake.profile()
        username = fake.unique.email()
        device_type = fake.random_element(elements=('Android', 'iOS', 'Web'))

        poster_id = conn.execute(sqlalchemy.text("""
        INSERT INTO users (username, full_name, birthday, device_type) VALUES (:username, :name, :birthday, :device_type) RETURNING id;
        """), {"username": username, "name": profile['name'], "birthday": profile['birthdate'], "device_type": device_type}).scalar_one();

        num_posts = posts_sample_distribution[i]
        likes_sample_distribution = np.random.default_rng().negative_binomial(0.8, 0.0001, num_posts)  
        for j in range(num_posts):
            total_posts += 1
            posts.append({
                "title": fake.sentence(),
                "content": fake.text(),
                "poster_id": poster_id,
                "category_id": category_sample_distribution[i].item(),
                "visible": fake.boolean(75),
                "created_at": fake.date_time_between(start_date='-5y', end_date='now', tzinfo=None),
                "likes": likes_sample_distribution[j].item(),
                "nsfw": fake.boolean(10)
            })

    if posts:
        conn.execute(sqlalchemy.text("""
        INSERT INTO posts (title, content, poster_id, category_id, visible, created_at) 
        VALUES (:title, :content, :poster_id, :category_id, :visible, :created_at);
        """), posts)

    print("total posts: ", total_posts)