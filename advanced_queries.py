# Assignment 2

from gym_database import GymDatabase
from mysql.connector import Error

class AdvancedGymQueries(GymDatabase):
    def get_members_in_age_range(self, start_age, end_age):
        """
        Task 1: Retrieve members within a specific age range
        
        Args:
            start_age (int): Lower bound of age range (inclusive)
            end_age (int): Upper bound of age range (inclusive)
            
        Returns:
            list: List of tuples containing member details
        """
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            query = """
                SELECT id, name, age 
                FROM Members 
                WHERE age BETWEEN %s AND %s 
                ORDER BY age
            """
            
            cursor.execute(query, (start_age, end_age))
            members = cursor.fetchall()
            
            if not members:
                print(f"No members found between ages {start_age} and {end_age}")
                return []
            
            print(f"\nMembers between ages {start_age} and {end_age}:")
            print("-" * 40)
            print(f"{'ID':<5} {'Name':<20} {'Age':<5}")
            print("-" * 40)
            
            for member in members:
                print(f"{member['id']:<5} {member['name']:<20} {member['age']:<5}")
            
            cursor.close()
            return members
            
        except Error as e:
            print(f"Error retrieving members in age range: {e}")
            return []

def test_advanced_queries():
    """Test the advanced query functionality"""
    
    gym_db = AdvancedGymQueries(
        host="localhost",
        user="root",
        password="Pikapika07$",
        database="gym_db"
    )
    
    test_members = [
        (1, "Riley Thompson", 28),
        (2, "Tiberius Hans", 35),
        (3, "Morgan Chen", 25),
        (4, "Zara Ahmed", 29),
        (5, "Lucas Santos", 27)
    ]
    
    cursor = gym_db.connection.cursor()
    for member in test_members:
        try:
            cursor.execute(
                "INSERT IGNORE INTO Members (id, name, age) VALUES (%s, %s, %s)",
                member
            )
        except Error as e:
            print(f"Error inserting member {member[1]}: {e}")
    
    gym_db.connection.commit()
    cursor.close()
    
    print("\nTesting age range query (25-30):")
    gym_db.get_members_in_age_range(25, 30)
    
    gym_db.close_connection()

if __name__ == "__main__":
    test_advanced_queries()