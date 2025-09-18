// Test script to verify connection improvements
import { storageUtils } from './utils/storage';

async function testConnectionPerformance() {
  console.log('Testing connection performance improvements...');
  
  // Test 1: Multiple rapid requests to check caching
  console.time('Multiple requests');
  try {
    const results = await Promise.all([
      storageUtils.getMembers(),
      storageUtils.getMembers(),
      storageUtils.getMembers()
    ]);
    console.timeEnd('Multiple requests');
    console.log(`Received ${results[0].length} members in each request`);
    
    // Test 2: Check if caching is working
    console.time('Cached request');
    const cachedResult = await storageUtils.getMembers();
    console.timeEnd('Cached request');
    console.log(`Cached request returned ${cachedResult.length} members`);
    
    console.log('Connection performance test completed successfully!');
  } catch (error) {
    console.error('Connection performance test failed:', error);
  }
}

// Run the test
testConnectionPerformance();