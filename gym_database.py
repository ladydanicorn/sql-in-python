# Assignment 1
import mysql.connector
from datetime import datetime
from mysql.connector import Error

class GymDatabase:
    def __init__(self, host='localhost', user='your_username', password='your_password', database='gym_db'):
        """Initialize database connection"""
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Pikapika07$",
                database="gym_db"
            )
            print("Successfully connected to the database")
        except Error as e:
            print(f"Error connecting to MySQL: {e}")

    def setup_database(self):
        """Create tables if they don't exist"""
        try:
            cursor = self.connection.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Members (
                    id INT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    age INT CHECK (age > 0)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS WorkoutSessions (
                    session_id INT AUTO_INCREMENT PRIMARY KEY,
                    member_id INT,
                    date DATE,
                    duration_minutes INT,
                    calories_burned INT,
                    FOREIGN KEY (member_id) REFERENCES Members(id)
                )
            ''')
            
            self.connection.commit()
            cursor.close()
            print("Tables created successfully")
            
        except Error as e:
            print(f"Error setting up database: {e}")

    def add_member(self, id, name, age):
        """
        Task 1: Add a new member to the database
        """
        try:
            cursor = self.connection.cursor()
            
            cursor.execute("SELECT id FROM Members WHERE id = %s", (id,))
            if cursor.fetchone():
                print(f"Error: Member ID {id} already exists")
                cursor.close()
                return False
            
            cursor.execute(
                "INSERT INTO Members (id, name, age) VALUES (%s, %s, %s)",
                (id, name, age)
            )
            
            self.connection.commit()
            cursor.close()
            print(f"Successfully added member: {name}")
            return True
            
        except Error as e:
            print(f"Error adding member: {e}")
            return False

    def add_workout_session(self, member_id, date, duration_minutes, calories_burned):
        """
        Task 2: Add a new workout session
        """
        try:
            cursor = self.connection.cursor()
            
            cursor.execute("SELECT id FROM Members WHERE id = %s", (member_id,))
            if not cursor.fetchone():
                print(f"Error: Member ID {member_id} does not exist")
                cursor.close()
                return False
            
            cursor.execute('''
                INSERT INTO WorkoutSessions 
                (member_id, date, duration_minutes, calories_burned)
                VALUES (%s, %s, %s, %s)
            ''', (member_id, date, duration_minutes, calories_burned))
            
            self.connection.commit()
            cursor.close()
            print(f"Successfully added workout session for member {member_id}")
            return True
            
        except Error as e:
            print(f"Error adding workout session: {e}")
            return False

    def update_member_age(self, member_id, new_age):
        """
        Task 3: Update member age
        """
        try:
            cursor = self.connection.cursor()
            
            cursor.execute("SELECT id FROM Members WHERE id = %s", (member_id,))
            if not cursor.fetchone():
                print(f"Error: Member ID {member_id} does not exist")
                cursor.close()
                return False
            
            cursor.execute(
                "UPDATE Members SET age = %s WHERE id = %s",
                (new_age, member_id)
            )
            
            self.connection.commit()
            cursor.close()
            print(f"Successfully updated age for member {member_id}")
            return True
            
        except Error as e:
            print(f"Error updating member age: {e}")
            return False

    def delete_workout_session(self, session_id):
        """
        Task 4: Delete a workout session
        """
        try:
            cursor = self.connection.cursor()
            
            cursor.execute("SELECT session_id FROM WorkoutSessions WHERE session_id = %s", (session_id,))
            if not cursor.fetchone():
                print(f"Error: Session ID {session_id} does not exist")
                cursor.close()
                return False
            
            cursor.execute("DELETE FROM WorkoutSessions WHERE session_id = %s", (session_id,))
            
            self.connection.commit()
            cursor.close()
            print(f"Successfully deleted workout session {session_id}")
            return True
            
        except Error as e:
            print(f"Error deleting workout session: {e}")
            return False

    def close_connection(self):
        """Close the database connection"""
        if self.connection.is_connected():
            self.connection.close()
            print("Database connection closed.")

def test_gym_database():
    """Test all functionality of the GymDatabase class"""
    gym_db = GymDatabase(
        host='localhost',
        user='your_username',
        password='your_password',
        database='gym_db'
    )
    
    gym_db.setup_database()
    
    gym_db.add_member(1, "Riley Thompson", 28)
    gym_db.add_member(2, "Tiberius Hans", 35)
    
    gym_db.add_workout_session(1, "2024-04-16", 60, 500)
    gym_db.add_workout_session(2, "2024-03-15", 45, 350)
    
    gym_db.update_member_age(1, 26)
    
    gym_db.delete_workout_session(1)
    
    gym_db.close_connection()

if __name__ == "__main__":
    test_gym_database()