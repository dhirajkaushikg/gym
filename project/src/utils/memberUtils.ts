import { Member, MemberStatus, DashboardStats } from '../types/member';

// Cache for member status calculations
const statusCache = new Map<string, { status: MemberStatus; timestamp: number }>();
const CACHE_DURATION = 60000; // 1 minute

export const memberUtils = {
  generateId: (): string => {
    return Date.now().toString(36) + Math.random().toString(36).substr(2);
  },

  calculateDueAmount: (totalAmount: number, amountPaid: number): number => {
    // Use a more precise method to handle decimal inputs
    const roundedTotal = Math.round((totalAmount + Number.EPSILON) * 100) / 100;
    const roundedPaid = Math.round((amountPaid + Number.EPSILON) * 100) / 100;
    
    // Calculate and round the result
    const due = roundedTotal - roundedPaid;
    return Math.max(0, Math.round((due + Number.EPSILON) * 100) / 100);
  },

  getMemberStatus: (expiryDate: string): MemberStatus => {
    // Check cache first
    const cached = statusCache.get(expiryDate);
    const now = Date.now();
    
    if (cached && (now - cached.timestamp) < CACHE_DURATION) {
      return cached.status;
    }
    
    const today = new Date();
    const expiry = new Date(expiryDate);
    const daysUntilExpiry = Math.ceil((expiry.getTime() - today.getTime()) / (1000 * 60 * 60 * 24));

    let status: MemberStatus;
    if (daysUntilExpiry < 0) {
      status = 'expired';
    } else if (daysUntilExpiry <= 10) {
      status = 'expiring';
    } else {
      status = 'active';
    }
    
    // Cache the result
    statusCache.set(expiryDate, { status, timestamp: now });
    
    return status;
  },

  getStatusColor: (status: MemberStatus): string => {
    switch (status) {
      case 'active': return 'border-green-500';
      case 'expiring': return 'border-yellow-500';
      case 'expired': return 'border-red-500';
    }
  },

  getStatusBadgeColor: (status: MemberStatus): string => {
    switch (status) {
      case 'active': return 'bg-green-100 text-green-800';
      case 'expiring': return 'bg-yellow-100 text-yellow-800';
      case 'expired': return 'bg-red-100 text-red-800';
    }
  },

  getDashboardStats: (members: Member[]): DashboardStats => {
    // Clear expired cache entries
    const now = Date.now();
    for (const [key, value] of statusCache.entries()) {
      if ((now - value.timestamp) >= CACHE_DURATION) {
        statusCache.delete(key);
      }
    }
    
    const stats = members.reduce((acc, member) => {
      const status = memberUtils.getMemberStatus(member.expiryDate);
      
      acc.totalMembers++;
      acc.totalIncome += member.amountPaid;

      switch (status) {
        case 'active':
          acc.activeMembers++;
          break;
        case 'expiring':
          acc.expiringMembers++;
          break;
        case 'expired':
          acc.expiredMembers++;
          break;
      }

      return acc;
    }, {
      totalMembers: 0,
      activeMembers: 0,
      expiringMembers: 0,
      expiredMembers: 0,
      totalIncome: 0
    });

    return stats;
  },

  sortMembersByExpiry: (members: Member[]): Member[] => {
    return [...members].sort((a, b) => {
      const dateA = new Date(a.expiryDate);
      const dateB = new Date(b.expiryDate);
      return dateA.getTime() - dateB.getTime();
    });
  },

  filterMembers: (members: Member[], searchTerm: string, statusFilter: string): Member[] => {
    let filtered = members;

    // Apply search filter
    if (searchTerm) {
      const term = searchTerm.toLowerCase().trim();
      if (term) {
        filtered = filtered.filter(member =>
          member.name.toLowerCase().includes(term) ||
          member.mobile.includes(term) ||
          member.mId.toLowerCase().includes(term)
        );
      }
    }

    // Apply status filter
    if (statusFilter && statusFilter !== 'all') {
      filtered = filtered.filter(member =>
        memberUtils.getMemberStatus(member.expiryDate) === statusFilter
      );
    }

    return memberUtils.sortMembersByExpiry(filtered);
  },

  formatCurrency: (amount: number): string => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
    }).format(amount);
  },

  formatDate: (dateString: string): string => {
    return new Date(dateString).toLocaleDateString('en-IN');
  }
};

// Function to validate if a member ID is available
export const isMemberIdAvailable = async (memberId: string): Promise<boolean> => {
  try {
    const response = await fetch(`${import.meta.env.VITE_BACKEND_URL || 'http://localhost:5000'}/api/members`);
    if (response.ok) {
      const members = await response.json();
      const existingMember = members.find((member: any) => member.mId === memberId);
      return !existingMember;
    }
    return true; // If we can't fetch members, assume ID is available
  } catch (error) {
    console.error('Error checking member ID availability:', error);
    return true; // If there's an error, assume ID is available
  }
};

// Function to suggest the next available member ID
export const suggestNextMemberId = async (): Promise<string> => {
  try {
    const response = await fetch(`${import.meta.env.VITE_BACKEND_URL || 'http://localhost:5000'}/api/members`);
    if (response.ok) {
      const members = await response.json();
      
      // Extract existing numeric IDs
      const existingIds = members
        .map((member: any) => member.mId)
        .filter((id: string) => id && /^\d+$/.test(id))
        .map((id: string) => parseInt(id, 10))
        .sort((a: number, b: number) => a - b);
      
      // Find the next available ID
      if (existingIds.length > 0) {
        const nextId = Math.max(...existingIds) + 1;
        return nextId.toString().padStart(3, '0'); // Format as 3-digit number with leading zeros
      } else {
        return '001';
      }
    }
    return '001'; // Default if we can't fetch members
  } catch (error) {
    console.error('Error suggesting next member ID:', error);
    return '001'; // Default if there's an error
  }
};
