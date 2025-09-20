import requests

def check_existing_members():
    """
    Check what members currently exist in the database to identify taken IDs
    """
    url = "https://gym-backend-kixz.onrender.com/api/members"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            members = response.json()
            print(f"Found {len(members)} existing members:")
            print("=" * 50)
            
            # Sort members by ID for easier viewing
            members.sort(key=lambda x: x.get('mId', ''))
            
            for member in members:
                print(f"ID: {member.get('mId', 'N/A')} | Name: {member.get('name', 'N/A')} | Mobile: {member.get('mobile', 'N/A')}")
            
            # Show all existing IDs
            existing_ids = [member.get('mId') for member in members if member.get('mId')]
            print(f"\nExisting Member IDs: {sorted(existing_ids)}")
            
            return members
        else:
            print(f"Error fetching members: {response.status_code}")
            print(response.text)
            return []
    except Exception as e:
        print(f"Error connecting to backend: {e}")
        return []

if __name__ == "__main__":
    check_existing_members()