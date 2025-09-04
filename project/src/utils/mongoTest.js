// Simple test to verify MongoDB integration
const { MongoClient } = require('mongodb');

async function testMongoDB() {
  const uri = process.env.MONGODB_URI || 'mongodb://localhost:27017';
  const client = new MongoClient(uri);

  try {
    // Connect to MongoDB
    await client.connect();
    console.log('Connected to MongoDB successfully!');

    // Access the database
    const database = client.db('gym_management');
    const members = database.collection('members');

    // Test inserting a document
    const testMember = {
      name: 'Test Member',
      email: 'test@example.com'
    };

    const result = await members.insertOne(testMember);
    console.log('Inserted test member with id:', result.insertedId);

    // Test retrieving documents
    const allMembers = await members.find({}).toArray();
    console.log('Found', allMembers.length, 'members in the collection');

    // Clean up - delete the test member
    await members.deleteOne({ _id: result.insertedId });
    console.log('Cleaned up test member');

    console.log('MongoDB integration test completed successfully!');
  } catch (error) {
    console.error('MongoDB test failed:', error);
  } finally {
    await client.close();
  }
}

// Run the test
testMongoDB().catch(console.error);