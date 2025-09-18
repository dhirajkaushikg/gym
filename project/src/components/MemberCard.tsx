import React from 'react';
import { Phone, Trash2, RefreshCw, Eye, User, Calendar, DollarSign } from 'lucide-react';
import { Member } from '../types/member';
import { memberUtils } from '../utils/memberUtils';

interface MemberCardProps {
  member: Member;
  onDelete: (id: string) => void;
  onRenew: (member: Member) => void;
  onViewProfile: (member: Member) => void;
}

export default function MemberCard({ member, onDelete, onRenew, onViewProfile }: MemberCardProps) {
  const status = memberUtils.getMemberStatus(member.expiryDate);
  const borderColor = memberUtils.getStatusColor(status);
  const badgeColor = memberUtils.getStatusBadgeColor(status);

  const handleCall = () => {
    window.open(`tel:${member.mobile}`, '_self');
  };

  const handleDelete = () => {
    onDelete(member.id);
  };

  return (
    <div className={`bg-white rounded-lg shadow-md border-l-4 ${borderColor} p-6 hover:shadow-lg transition-shadow`}>
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center space-x-3">
          {member.profilePicture ? (
            <img
              src={member.profilePicture}
              alt={member.name}
              className="w-12 h-12 rounded-full object-cover border-2 border-gray-200"
            />
          ) : (
            <div className="w-12 h-12 bg-gray-200 rounded-full flex items-center justify-center">
              <User className="w-6 h-6 text-gray-400" />
            </div>
          )}
          <div>
            <h3 className="font-semibold text-gray-900">{member.name}</h3>
            <p className="text-sm text-gray-500">ID: {member.mId}</p>
          </div>
        </div>
        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${badgeColor}`}>
          {status.charAt(0).toUpperCase() + status.slice(1)}
        </span>
      </div>

      <div className="space-y-2 mb-4">
        <div className="flex items-center text-sm text-gray-600">
          <Phone className="w-4 h-4 mr-2" />
          <span>{member.mobile}</span>
        </div>
        <div className="flex items-center text-sm text-gray-600">
          <Calendar className="w-4 h-4 mr-2" />
          <span>Expires: {memberUtils.formatDate(member.expiryDate)}</span>
        </div>
        <div className="flex items-center text-sm text-gray-600">
          <DollarSign className="w-4 h-4 mr-2" />
          <span>Due: {memberUtils.formatCurrency(member.dueAmount)}</span>
        </div>
      </div>

      <div className="flex space-x-2">
        <button
          onClick={handleCall}
          className="flex-1 flex items-center justify-center px-3 py-2 bg-green-600 text-white text-sm rounded-md hover:bg-green-700 transition-colors touch-manipulation"
          style={{ WebkitTapHighlightColor: 'transparent' }}
        >
          <Phone className="w-4 h-4 mr-1" />
          Call
        </button>
        <button
          onClick={() => onRenew(member)}
          className="flex-1 flex items-center justify-center px-3 py-2 bg-blue-600 text-white text-sm rounded-md hover:bg-blue-700 transition-colors touch-manipulation"
          style={{ WebkitTapHighlightColor: 'transparent' }}
        >
          <RefreshCw className="w-4 h-4 mr-1" />
          Renew
        </button>
        <button
          onClick={() => onViewProfile(member)}
          className="flex items-center justify-center px-3 py-2 bg-gray-600 text-white text-sm rounded-md hover:bg-gray-700 transition-colors touch-manipulation"
          style={{ WebkitTapHighlightColor: 'transparent' }}
        >
          <Eye className="w-4 h-4" />
        </button>
        <button
          onClick={handleDelete}
          className="flex items-center justify-center px-3 py-2 bg-red-600 text-white text-sm rounded-md hover:bg-red-700 transition-colors touch-manipulation"
          style={{ WebkitTapHighlightColor: 'transparent' }}
        >
          <Trash2 className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}