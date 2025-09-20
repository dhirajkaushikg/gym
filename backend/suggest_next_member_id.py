import requests

def suggest_next_member_id():
    """
    Suggest the next available member ID based on existing members
    """
    url = "https://gym-backend-kixz.onrender.com/api/members"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            members = response.json()
            
            # Extract existing numeric IDs
            existing_ids = []
            for member in members:
                mid = member.get('mId')
                if mid and mid.isdigit():
                    existing_ids.append(int(mid))
            
            # Sort the IDs
            existing_ids.sort()
            
            # Find the next available ID
            if existing_ids:
                next_id = max(existing_ids) + 1
                # Format to match the existing pattern (3 digits with leading zeros)
                suggested_id = f"{next_id:03d}"
            else:
                suggested_id = "001"
            
            print(f"Existing member IDs: {sorted(existing_ids)}")
            print(f"Suggested next member ID: {suggested_id}")
            
            return suggested_id
        else:
            print(f"Error fetching members: {response.status_code}")
            return "001"
    except Exception as e:
        print(f"Error connecting to backend: {e}")
        return "001"

if __name__ == "__main__":
    suggest_next_member_id()