import requests
import json

class MemberManagementHelper:
    def __init__(self, backend_url="https://gym-backend-kixz.onrender.com"):
        self.backend_url = backend_url
        self.members_url = f"{backend_url}/api/members"
    
    def get_all_members(self):
        """Get all members from the database"""
        try:
            response = requests.get(self.members_url)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error fetching members: {response.status_code}")
                print(response.text)
                return []
        except Exception as e:
            print(f"Error connecting to backend: {e}")
            return []
    
    def check_member_id_exists(self, member_id):
        """Check if a member ID already exists"""
        members = self.get_all_members()
        for member in members:
            if member.get('mId') == member_id:
                return True, member
        return False, None
    
    def suggest_next_member_id(self):
        """Suggest the next available member ID"""
        members = self.get_all_members()
        
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
            return f"{next_id:03d}"
        else:
            return "001"
    
    def create_member(self, member_data):
        """Create a new member"""
        try:
            response = requests.post(
                self.members_url,
                json=member_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 201:
                print("✅ Member created successfully!")
                return True, response.json()
            else:
                error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {'error': response.text}
                print(f"❌ Error creating member: {response.status_code}")
                print(f"Error: {error_data.get('error', 'Unknown error')}")
                return False, error_data
                
        except Exception as e:
            print(f"❌ Error connecting to backend: {e}")
            return False, {'error': str(e)}
    
    def display_members_summary(self):
        """Display a summary of all members"""
        members = self.get_all_members()
        if not members:
            print("No members found or error fetching members")
            return
        
        print(f"\n📋 Found {len(members)} members:")
        print("=" * 80)
        
        # Sort members by ID for easier viewing
        members.sort(key=lambda x: x.get('mId', ''))
        
        for member in members:
            print(f"ID: {member.get('mId', 'N/A'):<5} | "
                  f"Name: {member.get('name', 'N/A'):<25} | "
                  f"Mobile: {member.get('mobile', 'N/A'):<12} | "
                  f"Status: {self._get_member_status(member)}")
        
        # Show existing IDs
        existing_ids = [member.get('mId') for member in members if member.get('mId')]
        print(f"\n🔢 Existing Member IDs: {sorted(existing_ids)}")
        
        # Show suggested next ID
        next_id = self.suggest_next_member_id()
        print(f"💡 Suggested next ID: {next_id}")
    
    def _get_member_status(self, member):
        """Get member status based on expiry date"""
        try:
            from datetime import datetime
            expiry_date = datetime.strptime(member.get('expiryDate', ''), '%Y-%m-%d')
            today = datetime.now()
            days_until_expiry = (expiry_date - today).days
            
            if days_until_expiry < 0:
                return "EXPIRED"
            elif days_until_expiry <= 10:
                return "EXPIRING"
            else:
                return "ACTIVE"
        except:
            return "UNKNOWN"

def main():
    helper = MemberManagementHelper()
    
    print("🏋️  Gym Management System - Member Helper")
    print("=" * 50)
    
    while True:
        print("\nOptions:")
        print("1. View all members")
        print("2. Check if member ID exists")
        print("3. Suggest next member ID")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            helper.display_members_summary()
            
        elif choice == '2':
            member_id = input("Enter member ID to check: ").strip()
            exists, member = helper.check_member_id_exists(member_id)
            if exists:
                print(f"✅ Member ID '{member_id}' already exists:")
                print(f"   Name: {member.get('name')}")
                print(f"   Mobile: {member.get('mobile')}")
            else:
                print(f"✅ Member ID '{member_id}' is available")
                
        elif choice == '3':
            next_id = helper.suggest_next_member_id()
            print(f"💡 Suggested next member ID: {next_id}")
            
        elif choice == '4':
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()