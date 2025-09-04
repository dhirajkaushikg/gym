import React from 'react';
import { X, User, Phone, MapPin, CreditCard, Calendar, DollarSign, FileText } from 'lucide-react';
import { Member } from '../types/member';
import { memberUtils } from '../utils/memberUtils';

interface MemberModalProps {
  member: Member;
  onClose: () => void;
  onEdit: (member: Member) => void;
}

export default function MemberModal({ member, onClose, onEdit }: MemberModalProps) {
  const status = memberUtils.getMemberStatus(member.expiryDate);
  const badgeColor = memberUtils.getStatusBadgeColor(status);

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-start justify-center p-2 sm:p-4 z-50 overflow-y-auto">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-2xl min-h-screen sm:min-h-0 sm:my-4">
        <div className="sticky top-0 bg-white border-b px-6 py-4 flex items-center justify-between">
          <h2 className="text-xl font-semibold text-gray-900">Member Profile</h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-full transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="max-h-[calc(100vh-80px)] sm:max-h-[80vh] overflow-y-auto">
          <div className="p-4 sm:p-6">
          {/* Header with Photo and Status */}
          <div className="flex flex-col sm:flex-row items-center sm:space-x-4 space-y-4 sm:space-y-0 mb-6">
            {member.profilePicture ? (
              <img
                src={member.profilePicture}
                alt={member.name}
                className="w-16 h-16 sm:w-20 sm:h-20 rounded-full object-cover border-4 border-gray-200"
              />
            ) : (
              <div className="w-16 h-16 sm:w-20 sm:h-20 bg-gray-200 rounded-full flex items-center justify-center">
                <User className="w-8 h-8 sm:w-10 sm:h-10 text-gray-400" />
              </div>
            )}
            <div className="text-center sm:text-left">
              <h3 className="text-xl sm:text-2xl font-bold text-gray-900">{member.name}</h3>
              <p className="text-gray-600 text-sm sm:text-base">Member ID: {member.mId}</p>
              <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium mt-2 ${badgeColor}`}>
                {status.charAt(0).toUpperCase() + status.slice(1)}
              </span>
            </div>
          </div>

          {/* Member Details */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div className="space-y-4">
              <div className="flex items-center space-x-3">
                <Phone className="w-5 h-5 text-gray-400" />
                <div>
                  <p className="text-sm text-gray-500">Mobile Number</p>
                  <p className="font-medium">{member.mobile}</p>
                </div>
              </div>

              <div className="flex items-start space-x-3">
                <MapPin className="w-5 h-5 text-gray-400 mt-1" />
                <div>
                  <p className="text-sm text-gray-500">Address</p>
                  <p className="font-medium">{member.address}</p>
                </div>
              </div>

              <div className="flex items-center space-x-3">
                <FileText className="w-5 h-5 text-gray-400" />
                <div>
                  <p className="text-sm text-gray-500">ID Proof</p>
                  <p className="font-medium">{member.idProof}</p>
                </div>
              </div>

              <div className="flex items-center space-x-3">
                <CreditCard className="w-5 h-5 text-gray-400" />
                <div>
                  <p className="text-sm text-gray-500">Training Type</p>
                  <p className="font-medium">{member.trainingType}</p>
                </div>
              </div>
            </div>

            <div className="space-y-4">
              <div className="flex items-center space-x-3">
                <Calendar className="w-5 h-5 text-gray-400" />
                <div>
                  <p className="text-sm text-gray-500">Batch</p>
                  <p className="font-medium">{member.batch}</p>
                </div>
              </div>

              <div className="flex items-center space-x-3">
                <CreditCard className="w-5 h-5 text-gray-400" />
                <div>
                  <p className="text-sm text-gray-500">Plan Type</p>
                  <p className="font-medium">{member.planType}</p>
                </div>
              </div>

              <div className="flex items-center space-x-3">
                <Calendar className="w-5 h-5 text-gray-400" />
                <div>
                  <p className="text-sm text-gray-500">Purchase Date</p>
                  <p className="font-medium">{memberUtils.formatDate(member.purchaseDate)}</p>
                </div>
              </div>

              <div className="flex items-center space-x-3">
                <Calendar className="w-5 h-5 text-gray-400" />
                <div>
                  <p className="text-sm text-gray-500">Expiry Date</p>
                  <p className="font-medium">{memberUtils.formatDate(member.expiryDate)}</p>
                </div>
              </div>
            </div>
          </div>

          {/* Payment Information */}
          <div className="bg-gray-50 rounded-lg p-4 mb-6">
            <h4 className="font-semibold text-gray-900 mb-3 flex items-center">
              <DollarSign className="w-5 h-5 mr-2" />
              Payment Information
            </h4>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div>
                <p className="text-sm text-gray-500">Total Amount</p>
                <p className="font-semibold text-base sm:text-lg">{memberUtils.formatCurrency(member.totalAmount)}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Amount Paid</p>
                <p className="font-semibold text-base sm:text-lg text-green-600">{memberUtils.formatCurrency(member.amountPaid)}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Due Amount</p>
                <p className={`font-semibold text-base sm:text-lg ${member.dueAmount > 0 ? 'text-red-600' : 'text-green-600'}`}>
                  {memberUtils.formatCurrency(member.dueAmount)}
                </p>
              </div>
            </div>
            {member.paymentDetails && (
              <div className="mt-3">
                <p className="text-sm text-gray-500">Payment Details</p>
                <p className="font-medium">{member.paymentDetails}</p>
              </div>
            )}
          </div>

          {/* Actions */}
          <div className="flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-3">
            <button
              onClick={() => onEdit(member)}
              className="w-full sm:flex-1 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
            >
              Edit Profile
            </button>
            <button
              onClick={onClose}
              className="w-full sm:w-auto px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 transition-colors"
            >
              Close
            </button>
          </div>
          </div>
        </div>
      </div>
    </div>
  );
}