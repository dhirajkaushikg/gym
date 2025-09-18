export interface Member {
  id: string;
  _id?: string; // MongoDB _id field
  profilePicture?: string;
  name: string;
  mId: string;
  mobile: string;
  trainingType: string;
  address: string;
  idProof: string;
  batch: string;
  planType: string;
  purchaseDate: string;
  expiryDate: string;
  totalAmount: number;
  amountPaid: number;
  dueAmount: number;
  paymentDetails: string;
}

export interface PaymentRecord {
  id: string;
  date: string;
  amount: number;
  method: string;
  notes?: string;
}

export type MemberStatus = 'active' | 'expiring' | 'expired';

export interface DashboardStats {
  totalMembers: number;
  activeMembers: number;
  expiringMembers: number;
  expiredMembers: number;
  totalIncome: number;
}