import React from 'react';
import { Member } from '../types/member';
import MemberCard from './MemberCard';

interface MemberListProps {
  members: Member[];
  onDelete: (id: string) => void;
  onRenew: (member: Member) => void;
  onViewProfile: (member: Member) => void;
}

export default function MemberList({ members, onDelete, onRenew, onViewProfile }: MemberListProps) {
  if (members.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="max-w-md mx-auto">
          <div className="mx-auto w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mb-4">
            <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">No members found</h3>
          <p className="text-gray-500">Add your first member or adjust your search filters.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {members.map((member) => (
        <MemberCard
          key={member.id}
          member={member}
          onDelete={onDelete}
          onRenew={onRenew}
          onViewProfile={onViewProfile}
        />
      ))}
    </div>
  );
}