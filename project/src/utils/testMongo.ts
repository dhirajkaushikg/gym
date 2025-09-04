import { initMongoDB, closeMongoDB, addMemberToMongo, getMembersFromMongo } from './mongoService';
import { Member } from '../types/member';

/**
 * Test MongoDB integration
 */
export const testMongoDB = async (): Promise<void> => {
  try {
    console.log('Testing MongoDB integration...');
    
    // Initialize MongoDB connection
    await initMongoDB();
    
    // Create a test member
    const testMember: Member = {
      id: 'test-member-1',
      name: 'Test Member',
      mId: 'TM001',
      mobile: '9876543210',
      trainingType: 'Gym',
      address: '123 Test Street, Test City',
      idProof: 'Test ID: 1234567890',
      batch: 'Morning (6AM-10AM)',
      planType: '3 Months',
      purchaseDate: new Date().toISOString(),
      expiryDate: new Date(Date.now() + 90 * 24 * 60 * 60 * 1000).toISOString(), // 90 days from now
      totalAmount: 3000,
      amountPaid: 3000,
      dueAmount: 0,
      paymentDetails: 'Test payment',
      paymentHistory: [],
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };
    
    // Add test member to MongoDB
    console.log('Adding test member to MongoDB...');
    await addMemberToMongo(testMember);
    
    // Retrieve members from MongoDB
    console.log('Retrieving members from MongoDB...');
    const members = await getMembersFromMongo();
    console.log(`Found ${members.length} members in MongoDB`);
    
    // Close MongoDB connection
    await closeMongoDB();
    
    console.log('MongoDB integration test completed successfully!');
  } catch (error) {
    console.error('MongoDB integration test failed:', error);
  }
};

// Run the test if this file is executed directly
if (import.meta.url === new URL(import.meta.url).href) {
  testMongoDB();
}