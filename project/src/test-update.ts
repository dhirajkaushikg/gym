import { storageUtils, initializeStorage } from './utils/storage';
import { Member } from './types/member';

// Test the update functionality
async function testUpdate() {
  try {
    // Initialize storage
    await initializeStorage();
    
    // Get all members
    const members = await storageUtils.getMembers();
    console.log('Total members:', members.length);
    
    if (members.length > 0) {
      // Get the first member
      const member = members[0];
      console.log('Original member:', member);
      
      // Update the member's name
      const updatedMember = {
        ...member,
        name: member.name + ' - Updated',
      };
      
      console.log('Updating member with:', updatedMember);
      
      // Try to update the member
      await storageUtils.updateMember(updatedMember);
      console.log('Member updated successfully!');
      
      // Verify the update
      const updatedMembers = await storageUtils.getMembers();
      const updatedMemberFromStorage = updatedMembers.find(m => m.id === member.id);
      console.log('Updated member from storage:', updatedMemberFromStorage);
    } else {
      console.log('No members found to update');
    }
  } catch (error) {
    console.error('Error testing update:', error);
  }
}

testUpdate();