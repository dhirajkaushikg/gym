import React, { useState, useEffect, useCallback } from 'react';
import { Plus, Download, LogOut, Dumbbell, BarChart3, Users, UserPlus, X, AlertTriangle, RefreshCw } from 'lucide-react';
import { Member } from './types/member';
import { storageUtils, initializeStorage } from './utils/storage';
import { memberUtils } from './utils/memberUtils';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import MemberForm from './components/MemberForm';
import MemberList from './components/MemberList';
import MemberModal from './components/MemberModal';
import SearchFilter from './components/SearchFilter';

type ActiveTab = 'dashboard' | 'members' | 'add-member';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [activeTab, setActiveTab] = useState<ActiveTab>('dashboard');
  const [members, setMembers] = useState<Member[]>([]);
  const [filteredMembers, setFilteredMembers] = useState<Member[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // Modals
  const [showMemberForm, setShowMemberForm] = useState(false);
  const [showMemberModal, setShowMemberModal] = useState(false);
  const [editingMember, setEditingMember] = useState<Member | undefined>();
  const [selectedMember, setSelectedMember] = useState<Member | undefined>();
  const [deleteConfirmation, setDeleteConfirmation] = useState<{ show: boolean; member: Member | null }>({
    show: false,
    member: null
  });

  useEffect(() => {
    // Initialize storage (backend or localStorage)
    const initStorage = async () => {
      await initializeStorage();
    };
    
    initStorage();
    
    setIsAuthenticated(storageUtils.isAuthenticated());
  }, []);

  // Create a memoized loadMembers function with better error handling
  const loadMembers = useCallback(async () => {
    if (!isAuthenticated) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const loadedMembers = await storageUtils.getMembers();
      setMembers(loadedMembers);
    } catch (err: any) {
      console.error('Error loading members:', err);
      setError(err.message || 'Failed to load members. Please try again.');
    } finally {
      setLoading(false);
    }
  }, [isAuthenticated]);

  useEffect(() => {
    loadMembers();
  }, [loadMembers]);

  useEffect(() => {
    const filtered = memberUtils.filterMembers(members, searchTerm, statusFilter);
    setFilteredMembers(filtered);
  }, [members, searchTerm, statusFilter]);

  const handleLogin = () => {
    storageUtils.setAuth(true);
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    storageUtils.logout();
    setIsAuthenticated(false);
    setActiveTab('dashboard');
  };

  const handleSaveMember = async (member: Member) => {
    try {
      if (editingMember) {
        await storageUtils.updateMember(member);
      } else {
        await storageUtils.addMember(member);
      }
      
      await loadMembers(); // Refresh the member list
      setShowMemberForm(false);
      setEditingMember(undefined);
      setActiveTab('members');
      setError(null); // Clear any previous errors
    } catch (error: any) {
      console.error('Error saving member:', error);
      setError(error.message || 'Failed to save member. Please check all fields are filled correctly and try again.');
    }
  };

  const handleDeleteMember = async (id: string) => {
    const member = members.find(m => m.id === id);
    if (member) {
      setDeleteConfirmation({ show: true, member });
    }
  };

  const confirmDelete = async () => {
    if (deleteConfirmation.member) {
      try {
        await storageUtils.deleteMember(deleteConfirmation.member.id);
        await loadMembers(); // Refresh the member list
        setError(null); // Clear any previous errors
      } catch (error: any) {
        console.error('Error deleting member:', error);
        setError(error.message || 'Failed to delete member. Please try again.');
      }
    }
    setDeleteConfirmation({ show: false, member: null });
  };

  const cancelDelete = () => {
    setDeleteConfirmation({ show: false, member: null });
  };

  const handleRenewMember = (member: Member) => {
    setEditingMember(member);
    setShowMemberForm(true);
  };

  const handleViewProfile = (member: Member) => {
    setSelectedMember(member);
    setShowMemberModal(true);
  };

  const handleEditMember = (member: Member) => {
    setEditingMember(member);
    setShowMemberModal(false);
    setShowMemberForm(true);
  };

  const handleAddMember = () => {
    setEditingMember(undefined);
    setShowMemberForm(true);
    // Force re-render to ensure modal opens
    setTimeout(() => {
      setActiveTab('members');
    }, 100);
  };

  const handleExportData = async () => {
    try {
      const csvData = await storageUtils.exportToCSV();
      const blob = new Blob([csvData], { type: 'text/csv' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `gym-members-${new Date().toISOString().split('T')[0]}.csv`;
      a.click();
      window.URL.revokeObjectURL(url);
      setError(null); // Clear any previous errors
    } catch (error: any) {
      console.error('Error exporting data:', error);
      setError(error.message || 'Failed to export data. Please try again.');
    }
  };

  if (!isAuthenticated) {
    return <Login onLogin={handleLogin} />;
  }

  const stats = memberUtils.getDashboardStats(members);

  const navItems = [
    { id: 'dashboard' as const, label: 'Dashboard', icon: BarChart3 },
    { id: 'members' as const, label: 'Members', icon: Users },
    { id: 'add-member' as const, label: 'Add Member', icon: UserPlus },
  ];

  return (
    <div className="min-h-screen bg-gray-50 overflow-x-hidden">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <Dumbbell className="w-8 h-8 text-blue-600" />
                <h1 className="text-xl font-bold text-gray-900">Gym Manager</h1>
              </div>
            </div>

            <div className="flex items-center space-x-2 sm:space-x-4">
              <button
                onClick={loadMembers}
                disabled={loading}
                className="flex items-center px-3 py-2 text-sm font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-100 rounded-md transition-colors disabled:opacity-50"
              >
                <RefreshCw className={`w-4 h-4 mr-1 ${loading ? 'animate-spin' : ''}`} />
                Refresh
              </button>
              <button
                onClick={handleExportData}
                className="hidden sm:flex items-center px-3 py-2 text-sm font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-100 rounded-md transition-colors"
              >
                <Download className="w-4 h-4 mr-1" />
                Export
              </button>
              <button
                onClick={handleExportData}
                className="sm:hidden flex items-center justify-center p-2 text-gray-700 hover:text-gray-900 hover:bg-gray-100 rounded-md transition-colors"
              >
                <Download className="w-4 h-4" />
              </button>
              <button
                onClick={handleLogout}
                className="hidden sm:flex items-center px-3 py-2 text-sm font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-100 rounded-md transition-colors"
              >
                <LogOut className="w-4 h-4 mr-1" />
                Logout
              </button>
              <button
                onClick={handleLogout}
                className="sm:hidden flex items-center justify-center p-2 text-gray-700 hover:text-gray-900 hover:bg-gray-100 rounded-md transition-colors"
              >
                <LogOut className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 sm:py-8">
        {/* Error Message */}
        {error && (
          <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-md">
            <div className="flex items-center">
              <AlertTriangle className="w-5 h-5 text-red-500 mr-2 flex-shrink-0" />
              <p className="text-red-700 text-sm">{error}</p>
              <button 
                onClick={() => setError(null)}
                className="ml-auto text-red-500 hover:text-red-700"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
          </div>
        )}

        {/* Navigation Tabs */}
        <div className="mb-8">
          <nav className="flex flex-col sm:flex-row sm:space-x-8 space-y-2 sm:space-y-0" aria-label="Tabs">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id)}
                  className={`flex items-center justify-center sm:justify-start px-4 sm:px-1 py-3 sm:py-4 text-sm font-medium border-b-2 sm:border-b-2 border-l-4 sm:border-l-0 rounded-md sm:rounded-none transition-colors ${
                    isActive
                      ? 'border-blue-500 text-blue-600 bg-blue-50 sm:bg-transparent'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 hover:bg-gray-50 sm:hover:bg-transparent'
                  }`}
                >
                  <Icon className="w-5 h-5 mr-2" />
                  {item.label}
                </button>
              );
            })}
          </nav>
        </div>

        {/* Content */}
        {activeTab === 'dashboard' && <Dashboard stats={stats} />}

        {activeTab === 'members' && (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <h2 className="text-2xl font-bold text-gray-900">All Members ({members.length})</h2>
              <div className="flex space-x-2">
                <button
                  onClick={loadMembers}
                  disabled={loading}
                  className="flex items-center px-3 py-2 bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200 transition-colors disabled:opacity-50"
                >
                  <RefreshCw className={`w-4 h-4 mr-1 ${loading ? 'animate-spin' : ''}`} />
                  Refresh
                </button>
                <button
                  onClick={handleAddMember}
                  className="flex items-center px-3 sm:px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors touch-manipulation text-sm sm:text-base"
                  style={{ WebkitTapHighlightColor: 'transparent' }}
                >
                  <Plus className="w-4 h-4 mr-2" />
                  Add Member
                </button>
              </div>
            </div>

            <SearchFilter
              searchTerm={searchTerm}
              onSearchChange={setSearchTerm}
              statusFilter={statusFilter}
              onStatusFilterChange={setStatusFilter}
            />

            {loading ? (
              <div className="flex justify-center items-center py-12">
                <RefreshCw className="w-8 h-8 text-blue-500 animate-spin" />
                <span className="ml-2 text-gray-600">Loading members...</span>
              </div>
            ) : (
              <MemberList
                members={filteredMembers}
                onDelete={handleDeleteMember}
                onRenew={handleRenewMember}
                onViewProfile={handleViewProfile}
              />
            )}
          </div>
        )}

        {activeTab === 'add-member' && (
          <div className="w-full max-w-4xl">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Add New Member</h2>
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <button
                onClick={handleAddMember}
                className="w-full flex items-center justify-center px-4 py-6 sm:py-8 border-2 border-dashed border-gray-300 rounded-lg hover:border-gray-400 transition-colors touch-manipulation"
                style={{ WebkitTapHighlightColor: 'transparent' }}
              >
                <div className="text-center">
                  <Plus className="w-8 h-8 sm:w-12 sm:h-12 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-base sm:text-lg font-medium text-gray-900">Add New Member</h3>
                  <p className="text-gray-500">Click to open the member registration form</p>
                </div>
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Modals */}
      {showMemberForm && (
        <MemberForm
          member={editingMember}
          onSave={handleSaveMember}
          onCancel={() => {
            setShowMemberForm(false);
            setEditingMember(undefined);
          }}
        />
      )}

      {showMemberModal && selectedMember && (
        <MemberModal
          member={selectedMember}
          onClose={() => {
            setShowMemberModal(false);
            setSelectedMember(undefined);
          }}
          onEdit={handleEditMember}
        />
      )}

      {/* Custom Delete Confirmation Modal */}
      {deleteConfirmation.show && deleteConfirmation.member && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg shadow-xl w-full max-w-md">
            <div className="p-6">
              <div className="flex items-center mb-4">
                <div className="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-red-100">
                  <AlertTriangle className="h-6 w-6 text-red-600" />
                </div>
              </div>
              <div className="text-center">
                <h3 className="text-lg font-medium text-gray-900 mb-2">
                  Delete Member
                </h3>
                <p className="text-sm text-gray-500 mb-4">
                  Are you sure you want to delete <strong>{deleteConfirmation.member.name}</strong>? 
                  This action cannot be undone.
                </p>
              </div>
            </div>
            <div className="bg-gray-50 px-6 py-3 flex flex-col sm:flex-row-reverse space-y-2 sm:space-y-0 sm:space-x-3 sm:space-x-reverse">
              <button
                onClick={confirmDelete}
                className="w-full sm:w-auto inline-flex justify-center px-4 py-2 bg-red-600 text-white text-sm font-medium rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition-colors"
              >
                Delete
              </button>
              <button
                onClick={cancelDelete}
                className="w-full sm:w-auto inline-flex justify-center px-4 py-2 bg-white text-gray-700 text-sm font-medium rounded-md border border-gray-300 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;