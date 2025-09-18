import { Member } from '../types/member';

// Use environment variable for backend URL with fallback to localhost
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:5000';

// Cache for member data with timestamp
let membersCache: { data: Member[]; timestamp: number } | null = null;
const CACHE_DURATION = 1000; // 1 second cache

console.log('Backend URL being used:', BACKEND_URL); // Debug log

// Clear any existing localStorage data on application start
// This ensures we don't have any leftover data from previous versions
try {
  localStorage.removeItem('gym_members');
} catch (e) {
  // Ignore errors if localStorage is not available
}

// Initialize storage - test backend connection
export const initializeStorage = async (): Promise<void> => {
  // In this version, we always use the backend
  // No need to test connection as we assume it's available
  console.log('Using MongoDB backend for storage');
};

// Function to invalidate cache when data changes
const invalidateCache = (): void => {
  membersCache = null;
};

export const storageUtils = {
  getMembers: async (): Promise<Member[]> => {
    // Check if we have valid cached data
    const now = Date.now();
    if (membersCache && (now - membersCache.timestamp) < CACHE_DURATION) {
      console.log('Returning cached members data');
      return membersCache.data;
    }

    try {
      console.log('Attempting to fetch from:', `${BACKEND_URL}/api/members`); // Debug log
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 5000); // 5 second timeout
      
      const response = await fetch(`${BACKEND_URL}/api/members`, {
        signal: controller.signal
      });
      
      clearTimeout(timeoutId);
      
      console.log('Response status:', response.status); // Debug log
      
      // Check if response is HTML (error page) instead of JSON
      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('text/html')) {
        const errorText = await response.text();
        console.error('Received HTML response instead of JSON:', errorText.substring(0, 200) + '...');
        throw new Error(`Backend returned HTML instead of JSON. Server may be down or endpoint not found. Status: ${response.status}`);
      }
      
      if (response.ok) {
        const members = await response.json();
        console.log('Loading members from backend:', members.length);
        
        // Process members to ensure they have the correct structure
        const processedMembers = members.map((member: any) => {
          // If the member has a MongoDB _id, store it in both _id and id fields
          // This ensures compatibility with both backend and frontend operations
          if (member._id && !member.id) {
            return {
              ...member,
              id: member._id
            };
          }
          // If the member already has both _id and id, make sure they're the same
          if (member._id && member.id) {
            return {
              ...member,
              id: member._id // Always use _id as the primary ID
            };
          }
          return member;
        });
        
        // Cache the data
        membersCache = {
          data: processedMembers,
          timestamp: now
        };
        
        return processedMembers;
      } else {
        const errorText = await response.text();
        console.error('Backend error response:', errorText); // Debug log
        throw new Error(`Backend returned status ${response.status}: ${errorText}`);
      }
    } catch (error: any) {
      if (error.name === 'AbortError') {
        console.error('Request timeout while loading members from backend');
        throw new Error('Request timeout - backend is taking too long to respond');
      }
      console.error('Error loading members from backend:', error);
      // Return empty array - no localStorage fallback
      throw error; // Re-throw the error so the UI can handle it properly
    }
  },

  // Invalidate cache when data changes
  invalidateCache: (): void => {
    membersCache = null;
  },

  saveMembers: async (members: Member[]): Promise<void> => {
    // Bulk save is not implemented for backend
    console.log('Bulk save not implemented for backend - use individual operations');
    return;
  },

  addMember: async (member: Member): Promise<void> => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/members`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(member),
      });
      
      // Check if response is HTML (error page) instead of JSON
      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('text/html')) {
        const errorText = await response.text();
        console.error('Received HTML response instead of JSON:', errorText.substring(0, 200) + '...');
        throw new Error(`Backend returned HTML instead of JSON. Server may be down or endpoint not found. Status: ${response.status}`);
      }
      
      if (!response.ok) {
        const errorText = await response.text();
        const errorMessage = `Backend returned status ${response.status}: ${errorText}`;
        console.error('Error adding member to backend:', errorMessage);
        throw new Error(errorMessage);
      }
      
      console.log('Added member to backend:', member.name);
      // Invalidate cache after adding member
      invalidateCache();
    } catch (error) {
      console.error('Error adding member to backend:', error);
      throw error;
    }
  },

  updateMember: async (updatedMember: Member): Promise<void> => {
    try {
      // Extract the MongoDB _id from the member object
      // When members are retrieved from backend, they have both id and _id
      // The _id is what we need for MongoDB operations
      let memberId = (updatedMember as any)._id;
      
      // If _id is not directly available, try to use id
      // This handles cases where the member might not have been retrieved from backend yet
      if (!memberId) {
        memberId = updatedMember.id;
      }
      
      // If we still don't have a member ID, we can't update
      if (!memberId) {
        throw new Error('Member ID not found for update');
      }
      
      // Prepare the member data for update
      // Remove the _id from the updated member data to avoid conflicts
      const memberData = { ...updatedMember };
      delete (memberData as any)._id;
      
      const response = await fetch(`${BACKEND_URL}/api/members/${memberId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(memberData),
      });
      
      // Check if response is HTML (error page) instead of JSON
      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('text/html')) {
        const errorText = await response.text();
        console.error('Received HTML response instead of JSON:', errorText.substring(0, 200) + '...');
        throw new Error(`Backend returned HTML instead of JSON. Server may be down or endpoint not found. Status: ${response.status}`);
      }
      
      if (!response.ok) {
        const errorText = await response.text();
        const errorMessage = `Backend returned status ${response.status}: ${errorText}`;
        console.error('Error updating member in backend:', errorMessage);
        throw new Error(errorMessage);
      }
      
      console.log('Updated member in backend:', updatedMember.name);
      // Invalidate cache after updating member
      invalidateCache();
    } catch (error) {
      console.error('Error updating member in backend:', error);
      throw error;
    }
  },

  deleteMember: async (id: string): Promise<void> => {
    try {
      // Use the id parameter directly for deletion
      // The backend expects the MongoDB _id in the URL
      const response = await fetch(`${BACKEND_URL}/api/members/${id}`, {
        method: 'DELETE',
      });
      
      // Check if response is HTML (error page) instead of JSON
      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('text/html')) {
        const errorText = await response.text();
        console.error('Received HTML response instead of JSON:', errorText.substring(0, 200) + '...');
        throw new Error(`Backend returned HTML instead of JSON. Server may be down or endpoint not found. Status: ${response.status}`);
      }
      
      if (!response.ok) {
        const errorText = await response.text();
        const errorMessage = `Backend returned status ${response.status}: ${errorText}`;
        console.error('Error deleting member from backend:', errorMessage);
        throw new Error(errorMessage);
      }
      
      console.log('Deleted member from backend with id:', id);
      // Invalidate cache after deleting member
      invalidateCache();
    } catch (error) {
      console.error('Error deleting member from backend:', error);
      throw error;
    }
  },

  // Authentication functions - still using localStorage for authentication state
  // but this is separate from member data storage
  isAuthenticated: (): boolean => {
    const authData = localStorage.getItem('gym_auth');
    return authData === 'true';
  },

  setAuth: (authenticated: boolean): void => {
    localStorage.setItem('gym_auth', authenticated.toString());
  },

  logout: (): void => {
    localStorage.removeItem('gym_auth');
  },

  exportToJSON: async (): Promise<string> => {
    const members = await storageUtils.getMembers();
    return JSON.stringify(members, null, 2);
  },

  exportToCSV: async (): Promise<string> => {
    const members = await storageUtils.getMembers();
    if (members.length === 0) return '';

    const headers = [
      'Name', 'Member ID', 'Mobile', 'Training Type', 'Address', 
      'ID Proof', 'Batch', 'Plan Type', 'Purchase Date', 'Expiry Date',
      'Total Amount', 'Amount Paid', 'Due Amount', 'Payment Details'
    ];

    const csvContent = [
      headers.join(','),
      ...members.map(member => [
        `"${member.name}"`,
        `"${member.mId}"`,
        `"${member.mobile}"`,
        `"${member.trainingType}"`,
        `"${member.address}"`,
        `"${member.idProof}"`,
        `"${member.batch}"`,
        `"${member.planType}"`,
        `"${member.purchaseDate}"`,
        `"${member.expiryDate}"`,
        member.totalAmount,
        member.amountPaid,
        member.dueAmount,
        `"${member.paymentDetails}"`
      ].join(','))
    ].join('\n');

    return csvContent;
  }
};