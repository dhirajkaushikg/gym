import React, { useState, useEffect } from 'react';
import { X, Upload, Save } from 'lucide-react';
import { Member, PaymentRecord } from '../types/member';
import { memberUtils } from '../utils/memberUtils';

interface MemberFormProps {
  member?: Member;
  onSave: (member: Member) => void;
  onCancel: () => void;
}

export default function MemberForm({ member, onSave, onCancel }: MemberFormProps) {
  const [formData, setFormData] = useState({
    name: '',
    mId: '',
    mobile: '',
    trainingType: '',
    address: '',
    idProof: '',
    batch: '',
    planType: '',
    purchaseDate: '',
    expiryDate: '',
    totalAmount: 0,
    amountPaid: 0,
    paymentDetails: '',
    profilePicture: ''
  });

  const [imagePreview, setImagePreview] = useState<string>('');
  const [errors, setErrors] = useState<Record<string, string>>({});

  useEffect(() => {
    if (member) {
      // Ensure values are properly rounded when editing existing member using more precise method
      const roundedTotalAmount = Math.round((member.totalAmount + Number.EPSILON) * 100) / 100;
      const roundedAmountPaid = Math.round((member.amountPaid + Number.EPSILON) * 100) / 100;

      setFormData({
        name: member.name,
        mId: member.mId,
        mobile: member.mobile,
        trainingType: member.trainingType,
        address: member.address,
        idProof: member.idProof,
        batch: member.batch,
        planType: member.planType,
        purchaseDate: member.purchaseDate,
        expiryDate: member.expiryDate,
        totalAmount: roundedTotalAmount,
        amountPaid: roundedAmountPaid,
        paymentDetails: member.paymentDetails,
        profilePicture: member.profilePicture || ''
      });
      if (member.profilePicture) {
        setImagePreview(member.profilePicture);
      }
    }
  }, [member]);

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        const result = e.target?.result as string;
        setImagePreview(result);
        setFormData(prev => ({ ...prev, profilePicture: result }));
      };
      reader.readAsDataURL(file);
    }
  };

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!formData.name.trim()) newErrors.name = 'Name is required';
    if (!formData.mId.trim()) newErrors.mId = 'Member ID is required';
    if (!formData.mobile.trim()) newErrors.mobile = 'Mobile number is required';
    if (!/^\d{10}$/.test(formData.mobile)) newErrors.mobile = 'Mobile number must be 10 digits';
    if (!formData.trainingType) newErrors.trainingType = 'Training type is required';
    if (!formData.address.trim()) newErrors.address = 'Address is required';
    if (!formData.idProof.trim()) newErrors.idProof = 'ID proof is required';
    if (!formData.batch) newErrors.batch = 'Batch is required';
    if (!formData.planType) newErrors.planType = 'Plan type is required';
    if (!formData.purchaseDate) newErrors.purchaseDate = 'Purchase date is required';
    if (!formData.expiryDate) newErrors.expiryDate = 'Expiry date is required';
    if (formData.totalAmount <= 0) newErrors.totalAmount = 'Total amount must be greater than 0';
    if (formData.amountPaid < 0) newErrors.amountPaid = 'Amount paid cannot be negative';
    if (formData.amountPaid > formData.totalAmount) newErrors.amountPaid = 'Amount paid cannot exceed total amount';

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) return;

    // Ensure values are properly handled as numbers
    const totalAmount = parseFloat(formData.totalAmount.toString()) || 0;
    const amountPaid = parseFloat(formData.amountPaid.toString()) || 0;
    const dueAmount = memberUtils.calculateDueAmount(totalAmount, amountPaid);

    const memberData: Member = {
      id: member?.id || memberUtils.generateId(),
      ...formData,
      totalAmount,
      amountPaid,
      dueAmount
    };

    onSave(memberData);
  };

  const trainingTypes = ['Personal Training', 'General Training', 'Weight Training', 'Cardio Training'];
  const batches = ['Morning(5AM-10AM)', 'Evening(5PM-10PM)'];
  const planTypes = ['1 month', '2 month', '4 month', '6 month', 'Annual'];
  const paymentMethods = ['Cash', 'UPI', 'Net Banking', 'Check', 'Card'];

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-start justify-center p-2 sm:p-4 z-50 overflow-y-auto">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-4xl min-h-screen sm:min-h-0 sm:my-4">
        <div className="sticky top-0 bg-white border-b px-6 py-4 flex items-center justify-between">
          <h2 className="text-xl font-semibold text-gray-900">
            {member ? 'Edit Member' : 'Add New Member'}
          </h2>
          <button
            onClick={onCancel}
            className="p-2 hover:bg-gray-100 rounded-full transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="max-h-[calc(100vh-80px)] sm:max-h-[80vh] overflow-y-auto">
          <form onSubmit={handleSubmit} className="p-4 sm:p-6">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 sm:gap-6">
              {/* Profile Picture */}
              <div className="lg:col-span-1">
                <div className="text-center">
                  <div className="mb-4">
                    {imagePreview ? (
                      <img
                        src={imagePreview}
                        alt="Profile"
                        className="w-24 h-24 sm:w-32 sm:h-32 mx-auto rounded-full object-cover border-4 border-gray-200"
                      />
                    ) : (
                      <div className="w-24 h-24 sm:w-32 sm:h-32 mx-auto bg-gray-200 rounded-full flex items-center justify-center">
                        <Upload className="w-6 h-6 sm:w-8 sm:h-8 text-gray-400" />
                      </div>
                    )}
                  </div>
                  <label htmlFor="profilePicture" className="inline-flex items-center px-3 py-2 sm:px-4 sm:py-2 bg-blue-50 border border-blue-200 rounded-md cursor-pointer hover:bg-blue-100 transition-colors text-sm">
                    <Upload className="w-4 h-4 mr-1 sm:mr-2" />
                    Upload Photo
                  </label>
                  <input
                    type="file"
                    id="profilePicture"
                    accept="image/*"
                    onChange={handleImageChange}
                    className="hidden"
                  />
                </div>
              </div>

              {/* Form Fields */}
              <div className="lg:col-span-2 grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4">
                <div>
                  <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">
                    Full Name *
                  </label>
                  <input
                    type="text"
                    id="name"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-base ${errors.name ? 'border-red-500' : 'border-gray-300'}`}
                  />
                  {errors.name && <p className="text-red-500 text-sm mt-1">{errors.name}</p>}
                </div>

                <div>
                  <label htmlFor="mId" className="block text-sm font-medium text-gray-700 mb-1">
                    Member ID *
                  </label>
                  <input
                    type="text"
                    id="mId"
                    value={formData.mId}
                    onChange={(e) => setFormData({ ...formData, mId: e.target.value })}
                    className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-base ${errors.mId ? 'border-red-500' : 'border-gray-300'}`}
                  />
                  {errors.mId && <p className="text-red-500 text-sm mt-1">{errors.mId}</p>}
                </div>

                <div>
                  <label htmlFor="mobile" className="block text-sm font-medium text-gray-700 mb-1">
                    Mobile Number *
                  </label>
                  <input
                    type="tel"
                    id="mobile"
                    value={formData.mobile}
                    onChange={(e) => setFormData({ ...formData, mobile: e.target.value })}
                    className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-base ${errors.mobile ? 'border-red-500' : 'border-gray-300'}`}
                  />
                  {errors.mobile && <p className="text-red-500 text-sm mt-1">{errors.mobile}</p>}
                </div>

                <div>
                  <label htmlFor="trainingType" className="block text-sm font-medium text-gray-700 mb-1">
                    Training Type *
                  </label>
                  <select
                    id="trainingType"
                    value={formData.trainingType}
                    onChange={(e) => setFormData({ ...formData, trainingType: e.target.value })}
                    className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-base ${errors.trainingType ? 'border-red-500' : 'border-gray-300'}`}
                  >
                    <option value="">Select Training Type</option>
                    {trainingTypes.map(type => (
                      <option key={type} value={type}>{type}</option>
                    ))}
                  </select>
                  {errors.trainingType && <p className="text-red-500 text-sm mt-1">{errors.trainingType}</p>}
                </div>

                <div className="sm:col-span-2">
                  <label htmlFor="address" className="block text-sm font-medium text-gray-700 mb-1">
                    Address *
                  </label>
                  <textarea
                    id="address"
                    rows={2}
                    value={formData.address}
                    onChange={(e) => setFormData({ ...formData, address: e.target.value })}
                    className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-base ${errors.address ? 'border-red-500' : 'border-gray-300'}`}
                  />
                  {errors.address && <p className="text-red-500 text-sm mt-1">{errors.address}</p>}
                </div>

                <div>
                  <label htmlFor="idProof" className="block text-sm font-medium text-gray-700 mb-1">
                    ID Proof *
                  </label>
                  <input
                    type="text"
                    id="idProof"
                    value={formData.idProof}
                    onChange={(e) => setFormData({ ...formData, idProof: e.target.value })}
                    placeholder="e.g., Aadhar: 1234567890"
                    className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-base ${errors.idProof ? 'border-red-500' : 'border-gray-300'}`}
                  />
                  {errors.idProof && <p className="text-red-500 text-sm mt-1">{errors.idProof}</p>}
                </div>

                <div>
                  <label htmlFor="batch" className="block text-sm font-medium text-gray-700 mb-1">
                    Batch *
                  </label>
                  <select
                    id="batch"
                    value={formData.batch}
                    onChange={(e) => setFormData({ ...formData, batch: e.target.value })}
                    className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-base ${errors.batch ? 'border-red-500' : 'border-gray-300'}`}
                  >
                    <option value="">Select Batch</option>
                    {batches.map(batch => (
                      <option key={batch} value={batch}>{batch}</option>
                    ))}
                  </select>
                  {errors.batch && <p className="text-red-500 text-sm mt-1">{errors.batch}</p>}
                </div>

                <div>
                  <label htmlFor="planType" className="block text-sm font-medium text-gray-700 mb-1">
                    Plan Type *
                  </label>
                  <select
                    id="planType"
                    value={formData.planType}
                    onChange={(e) => setFormData({ ...formData, planType: e.target.value })}
                    className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-base ${errors.planType ? 'border-red-500' : 'border-gray-300'}`}
                  >
                    <option value="">Select Plan</option>
                    {planTypes.map(plan => (
                      <option key={plan} value={plan}>{plan}</option>
                    ))}
                  </select>
                  {errors.planType && <p className="text-red-500 text-sm mt-1">{errors.planType}</p>}
                </div>

                <div>
                  <label htmlFor="purchaseDate" className="block text-sm font-medium text-gray-700 mb-1">
                    Purchase Date *
                  </label>
                  <input
                    type="date"
                    id="purchaseDate"
                    value={formData.purchaseDate}
                    onChange={(e) => setFormData({ ...formData, purchaseDate: e.target.value })}
                    className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-base ${errors.purchaseDate ? 'border-red-500' : 'border-gray-300'}`}
                  />
                  {errors.purchaseDate && <p className="text-red-500 text-sm mt-1">{errors.purchaseDate}</p>}
                </div>

                <div>
                  <label htmlFor="expiryDate" className="block text-sm font-medium text-gray-700 mb-1">
                    Expiry Date *
                  </label>
                  <input
                    type="date"
                    id="expiryDate"
                    value={formData.expiryDate}
                    onChange={(e) => setFormData({ ...formData, expiryDate: e.target.value })}
                    className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-base ${errors.expiryDate ? 'border-red-500' : 'border-gray-300'}`}
                  />
                  {errors.expiryDate && <p className="text-red-500 text-sm mt-1">{errors.expiryDate}</p>}
                </div>

                <div>
                  <label htmlFor="totalAmount" className="block text-sm font-medium text-gray-700 mb-1">
                    Total Amount (₹) *
                  </label>
                  <input
                    type="number"
                    id="totalAmount"
                    value={formData.totalAmount}
                    onChange={(e) => setFormData({ ...formData, totalAmount: parseFloat(e.target.value) || 0 })}
                    className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-base ${errors.totalAmount ? 'border-red-500' : 'border-gray-300'}`}
                  />
                  {errors.totalAmount && <p className="text-red-500 text-sm mt-1">{errors.totalAmount}</p>}
                </div>

                <div>
                  <label htmlFor="amountPaid" className="block text-sm font-medium text-gray-700 mb-1">
                    Amount Paid (₹) *
                  </label>
                  <input
                    type="number"
                    id="amountPaid"
                    value={formData.amountPaid}
                    onChange={(e) => setFormData({ ...formData, amountPaid: parseFloat(e.target.value) || 0 })}
                    className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-base ${errors.amountPaid ? 'border-red-500' : 'border-gray-300'}`}
                  />
                  {errors.amountPaid && <p className="text-red-500 text-sm mt-1">{errors.amountPaid}</p>}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Due Amount (₹)
                  </label>
                  <input
                    type="number"
                    value={Math.round((memberUtils.calculateDueAmount(formData.totalAmount, formData.amountPaid) + Number.EPSILON) * 100) / 100}
                    readOnly
                    className="w-full px-3 py-2 border border-gray-300 rounded-md bg-gray-50 text-gray-600 text-base"
                  />
                </div>

                <div className="sm:col-span-2">
                  <label htmlFor="paymentDetails" className="block text-sm font-medium text-gray-700 mb-1">
                    Payment Details
                  </label>
                  <select
                    id="paymentDetails"
                    value={formData.paymentDetails}
                    onChange={(e) => setFormData({ ...formData, paymentDetails: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-base"
                  >
                    <option value="">Select Payment Method</option>
                    {paymentMethods.map(method => (
                      <option key={method} value={method}>{method}</option>
                    ))}
                  </select>
                </div>
              </div>

              <div className="sticky bottom-0 bg-white border-t pt-4 mt-6 flex flex-col sm:flex-row justify-end space-y-2 sm:space-y-0 sm:space-x-3">
                <button
                  type="button"
                  onClick={onCancel}
                  className="w-full sm:w-auto px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="w-full sm:w-auto px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors flex items-center justify-center"
                >
                  <Save className="w-4 h-4 mr-2" />
                  {member ? 'Update Member' : 'Save Member'}
                </button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
