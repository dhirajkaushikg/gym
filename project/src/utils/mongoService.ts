import mongodb from 'mongodb';
import { Member } from '../types/member';

// MongoDB connection configuration
const MONGODB_URI = process.env.MONGODB_URI || 'mongodb://localhost:27017';
const DATABASE_NAME = process.env.DATABASE_NAME || 'gym_management';
const COLLECTION_NAME = 'members';

// Global variables to store database connection
let client: mongodb.MongoClient | null = null;
let db: mongodb.Db | null = null;
let membersCollection: mongodb.Collection<Member> | null = null;

/**
 * Initialize MongoDB connection
 */
export const initMongoDB = async (): Promise<void> => {
  try {
    if (client) {
      console.log('MongoDB client already initialized');
      return;
    }

    client = new mongodb.MongoClient(MONGODB_URI);
    await client.connect();
    db = client.db(DATABASE_NAME);
    membersCollection = db.collection<Member>(COLLECTION_NAME);
    
    // Create indexes for better query performance
    await membersCollection.createIndex({ mId: 1 }, { unique: true });
    await membersCollection.createIndex({ mobile: 1 });
    await membersCollection.createIndex({ name: 1 });
    await membersCollection.createIndex({ expiryDate: 1 });
    
    console.log('Connected to MongoDB successfully');
  } catch (error) {
    console.error('Failed to connect to MongoDB:', error);
    throw error;
  }
};

/**
 * Get all members from MongoDB
 */
export const getMembersFromMongo = async (): Promise<Member[]> => {
  try {
    if (!membersCollection) {
      throw new Error('MongoDB not initialized');
    }
    
    const members = await membersCollection.find({}).toArray();
    console.log(`Retrieved ${members.length} members from MongoDB`);
    return members;
  } catch (error) {
    console.error('Error retrieving members from MongoDB:', error);
    throw error;
  }
};

/**
 * Save all members to MongoDB (bulk operation)
 */
export const saveMembersToMongo = async (members: Member[]): Promise<void> => {
  try {
    if (!membersCollection) {
      throw new Error('MongoDB not initialized');
    }
    
    // Clear existing members and insert all new ones
    await membersCollection.deleteMany({});
    if (members.length > 0) {
      await membersCollection.insertMany(members);
    }
    
    console.log(`Saved ${members.length} members to MongoDB`);
  } catch (error) {
    console.error('Error saving members to MongoDB:', error);
    throw error;
  }
};

/**
 * Add a new member to MongoDB
 */
export const addMemberToMongo = async (member: Member): Promise<void> => {
  try {
    if (!membersCollection) {
      throw new Error('MongoDB not initialized');
    }
    
    await membersCollection.insertOne(member);
    console.log('Added member to MongoDB:', member.name);
  } catch (error) {
    console.error('Error adding member to MongoDB:', error);
    throw error;
  }
};

/**
 * Update an existing member in MongoDB
 */
export const updateMemberInMongo = async (member: Member): Promise<void> => {
  try {
    if (!membersCollection) {
      throw new Error('MongoDB not initialized');
    }
    
    const result = await membersCollection.updateOne(
      { id: member.id },
      { $set: member }
    );
    
    if (result.matchedCount === 0) {
      throw new Error(`Member with id ${member.id} not found`);
    }
    
    console.log('Updated member in MongoDB:', member.name);
  } catch (error) {
    console.error('Error updating member in MongoDB:', error);
    throw error;
  }
};

/**
 * Delete a member from MongoDB
 */
export const deleteMemberFromMongo = async (id: string): Promise<void> => {
  try {
    if (!membersCollection) {
      throw new Error('MongoDB not initialized');
    }
    
    const result = await membersCollection.deleteOne({ id });
    
    if (result.deletedCount === 0) {
      throw new Error(`Member with id ${id} not found`);
    }
    
    console.log('Deleted member from MongoDB with id:', id);
  } catch (error) {
    console.error('Error deleting member from MongoDB:', error);
    throw error;
  }
};

/**
 * Close MongoDB connection
 */
export const closeMongoDB = async (): Promise<void> => {
  try {
    if (client) {
      await client.close();
      client = null;
      db = null;
      membersCollection = null;
      console.log('Closed MongoDB connection');
    }
  } catch (error) {
    console.error('Error closing MongoDB connection:', error);
  }
};