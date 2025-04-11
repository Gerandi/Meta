import React, { useState } from 'react';
import { Users, UserPlus, Settings, Mail, Shield, Key, LogOut, AlertTriangle, Bell, CheckCircle, User, X, Edit3, Trash2, Copy, PlusCircle } from 'lucide-react';

const UserManagement = () => {
  const [activeTab, setActiveTab] = useState('team');
  const [showInviteModal, setShowInviteModal] = useState(false);
  const [showProfileModal, setShowProfileModal] = useState(false);
  
  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold">Team & Collaboration</h1>
          <p className="text-gray-600">Manage team members and collaboration settings</p>
        </div>
        <div className="flex">
          <button 
            className="px-4 py-2 rounded-lg border bg-white text-gray-700 hover:bg-gray-50 mr-2 flex items-center"
            onClick={() => setActiveTab('settings')}
          >
            <Settings size={16} className="mr-1" /> Team Settings
          </button>
          <button 
            className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 flex items-center"
            onClick={() => setShowInviteModal(true)}
          >
            <UserPlus size={16} className="mr-1" /> Invite Member
          </button>
        </div>
      </div>
      
      <div className="bg-white rounded-lg shadow-lg overflow-hidden mb-6">
        <div className="flex border-b">
          <TabButton 
            active={activeTab === 'team'} 
            onClick={() => setActiveTab('team')}
            icon={<Users size={18} />}
            label="Team Members"
          />
          <TabButton 
            active={activeTab === 'roles'} 
            onClick={() => setActiveTab('roles')}
            icon={<Shield size={18} />}
            label="Roles & Permissions"
          />
          <TabButton 
            active={activeTab === 'invitations'} 
            onClick={() => setActiveTab('invitations')}
            icon={<Mail size={18} />}
            label="Invitations"
            badge="3"
          />
          <TabButton 
            active={activeTab === 'settings'} 
            onClick={() => setActiveTab('settings')}
            icon={<Settings size={18} />}
            label="Team Settings"
          />
        </div>
        
        {activeTab === 'team' && <TeamMembersTab setShowProfileModal={setShowProfileModal} />}
        {activeTab === 'roles' && <RolesTab />}
        {activeTab === 'invitations' && <InvitationsTab />}
        {activeTab === 'settings' && <SettingsTab />}
      </div>
      
      {showInviteModal && <InviteModal onClose={() => setShowInviteModal(false)} />}
      {showProfileModal && <ProfileModal onClose={() => setShowProfileModal(false)} />}
    </div>
  );
};

const TabButton = ({ active, onClick, icon, label, badge }) => {
  return (
    <button 
      className={`py-4 px-6 font-medium flex items-center ${
        active 
          ? 'text-indigo-600 border-b-2 border-indigo-600' 
          : 'text-gray-500 hover:text-gray-700'
      }`}
      onClick={onClick}
    >
      <span className="mr-2">{icon}</span>
      {label}
      {badge && (
        <span className="ml-2 px-2 py-0.5 bg-red-100 text-red-800 text-xs rounded-full">
          {badge}
        </span>
      )}
    </button>
  );
};

const TeamMembersTab = ({ setShowProfileModal }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [filterRole, setFilterRole] = useState('all');
  
  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <div className="text-xl font-medium">Team Members (12)</div>
        <div className="flex">
          <div className="relative mr-2">
            <input 
              type="text" 
              placeholder="Search members..." 
              className="w-64 pl-4 pr-10 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
            <button className="absolute right-3 top-2 text-gray-400">
              <X size={16} onClick={() => setSearchQuery('')} />
            </button>
          </div>
          <select 
            className="border rounded-lg py-2 px-3 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            value={filterRole}
            onChange={(e) => setFilterRole(e.target.value)}
          >
            <option value="all">All Roles</option>
            <option value="admin">Administrators</option>
            <option value="researcher">Researchers</option>
            <option value="coder">Coders</option>
            <option value="analyst">Analysts</option>
            <option value="viewer">Viewers</option>
          </select>
        </div>
      </div>
      
      <div className="bg-gray-50 rounded-lg p-4 mb-6 flex items-center justify-between">
        <div className="flex items-center">
          <div className="w-10 h-10 rounded-full bg-green-100 text-green-700 flex items-center justify-center mr-3">
            <Users size={20} />
          </div>
          <div>
            <h3 className="font-medium">Your Team Organization</h3>
            <p className="text-sm text-gray-600">MetaReview Research Group • 12 members • 8 active projects</p>
          </div>
        </div>
        <div>
          <button className="text-sm text-indigo-600 hover:text-indigo-800">
            Organization Settings
          </button>
        </div>
      </div>
      
      <div className="bg-white border rounded-lg overflow-hidden mb-6">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                User
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Role
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Projects
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Last Active
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Status
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            <TeamMemberRow 
              name="John Doe" 
              email="john.doe@example.com"
              avatar="JD"
              role="Administrator"
              projects={8}
              lastActive="Today"
              status="active"
              showActions={true}
              onViewProfile={() => setShowProfileModal(true)}
            />
            <TeamMemberRow 
              name="Jane Smith" 
              email="jane.smith@example.com"
              avatar="JS"
              role="Primary Researcher"
              projects={6}
              lastActive="Yesterday"
              status="active"
              showActions={true}
              onViewProfile={() => setShowProfileModal(true)}
            />
            <TeamMemberRow 
              name="Alex Johnson" 
              email="alex.j@example.com"
              avatar="AJ"
              role="Statistical Analyst"
              projects={5}
              lastActive="2 days ago"
              status="active"
              showActions={true}
              onViewProfile={() => setShowProfileModal(true)}
            />
            <TeamMemberRow 
              name="Sarah Williams" 
              email="s.williams@example.com"
              avatar="SW"
              role="Secondary Coder"
              projects={4}
              lastActive="3 days ago"
              status="active"
              showActions={true}
              onViewProfile={() => setShowProfileModal(true)}
            />
            <TeamMemberRow 
              name="Michael Brown" 
              email="m.brown@example.com"
              avatar="MB"
              role="Data Reviewer"
              projects={3}
              lastActive="5 days ago"
              status="active"
              showActions={true}
              onViewProfile={() => setShowProfileModal(true)}
            />
            <TeamMemberRow 
              name="Lisa Garcia" 
              email="l.garcia@example.com"
              avatar="LG"
              role="Viewer"
              projects={2}
              lastActive="2 weeks ago"
              status="inactive"
              showActions={true}
              onViewProfile={() => setShowProfileModal(true)}
            />
          </tbody>
        </table>
      </div>
      
      <div className="flex justify-between items-center">
        <div className="text-sm text-gray-500">
          Showing 6 of 12 team members
        </div>
        <div className="flex">
          <button className="px-3 py-1 border rounded hover:bg-gray-50 mr-2">Previous</button>
          <button className="px-3 py-1 border rounded hover:bg-gray-50">Next</button>
        </div>
      </div>
    </div>
  );
};

const TeamMemberRow = ({ name, email, avatar, role, projects, lastActive, status, showActions, onViewProfile }) => {
  const [showOptions, setShowOptions] = useState(false);
  
  const getStatusColor = (status) => {
    switch(status) {
      case 'active': return 'bg-green-100 text-green-800';
      case 'inactive': return 'bg-gray-100 text-gray-800';
      case 'pending': return 'bg-yellow-100 text-yellow-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };
  
  return (
    <tr className="hover:bg-gray-50">
      <td className="px-6 py-4 whitespace-nowrap">
        <div className="flex items-center">
          <div className="h-10 w-10 rounded-full bg-indigo-100 text-indigo-800 flex items-center justify-center mr-3">
            {avatar}
          </div>
          <div>
            <div className="font-medium text-gray-900">{name}</div>
            <div className="text-sm text-gray-500">{email}</div>
          </div>
        </div>
      </td>
      <td className="px-6 py-4 whitespace-nowrap">
        <span className="text-sm text-gray-900">{role}</span>
      </td>
      <td className="px-6 py-4 whitespace-nowrap">
        <span className="text-sm text-gray-900">{projects}</span>
      </td>
      <td className="px-6 py-4 whitespace-nowrap">
        <span className="text-sm text-gray-500">{lastActive}</span>
      </td>
      <td className="px-6 py-4 whitespace-nowrap">
        <span className={`px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${getStatusColor(status)}`}>
          {status.charAt(0).toUpperCase() + status.slice(1)}
        </span>
      </td>
      <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
        {showActions && (
          <div className="flex justify-end">
            <button 
              className="text-indigo-600 hover:text-indigo-900 mr-3"
              onClick={onViewProfile}
            >
              Profile
            </button>
            <div className="relative">
              <button 
                className="text-gray-400 hover:text-gray-600"
                onClick={() => setShowOptions(!showOptions)}
              >
                <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z" />
                </svg>
              </button>
              
              {showOptions && (
                <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg z-10 border">
                  <div className="py-1">
                    <button className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                      Assign Projects
                    </button>
                    <button className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                      Change Role
                    </button>
                    <button className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                      Reset Password
                    </button>
                    <button className="block w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50">
                      Remove from Team
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </td>
    </tr>
  );
};

const RolesTab = () => {
  const [showEditModal, setShowEditModal] = useState(false);
  const [showCreateModal, setShowCreateModal] = useState(false);
  
  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <div className="text-xl font-medium">Roles & Permissions</div>
        <button 
          className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 flex items-center"
          onClick={() => setShowCreateModal(true)}
        >
          <PlusCircle size={16} className="mr-1" /> Create Role
        </button>
      </div>
      
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6 flex">
        <div className="text-yellow-500 mr-3 mt-0.5">
          <AlertTriangle size={20} />
        </div>
        <div>
          <h3 className="font-medium text-yellow-800 mb-1">About Roles & Permissions</h3>
          <p className="text-yellow-700 text-sm">
            Roles define what team members can do within the system. Each role has specific permissions for viewing, editing, and managing 
            projects and organizational data. Changes to roles affect all users assigned to those roles.
          </p>
        </div>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <RoleCard 
          name="Administrator" 
          description="Full access to all features, user management, and organization settings"
          members={2}
          isDefault={false}
          permissions={[
            "Full system access",
            "Manage users and roles",
            "Create and delete projects",
            "Configure organization settings"
          ]}
          onEdit={() => setShowEditModal(true)}
        />
        
        <RoleCard 
          name="Primary Researcher" 
          description="Can create projects, manage project settings, and assign team members"
          members={3}
          isDefault={true}
          permissions={[
            "Create new projects",
            "Configure project settings",
            "Add/remove team members to projects",
            "Full analysis capabilities"
          ]}
          onEdit={() => setShowEditModal(true)}
        />
        
        <RoleCard 
          name="Statistical Analyst" 
          description="Can perform statistical analyses, but limited project management"
          members={2}
          isDefault={false}
          permissions={[
            "View all papers and data",
            "Configure statistical settings",
            "Run and save analyses",
            "Cannot modify project structure"
          ]}
          onEdit={() => setShowEditModal(true)}
        />
        
        <RoleCard 
          name="Secondary Coder" 
          description="Focused on data extraction and coding, limited analysis capabilities"
          members={3}
          isDefault={false}
          permissions={[
            "View assigned papers",
            "Extract and code data",
            "View summary statistics",
            "Cannot modify project settings"
          ]}
          onEdit={() => setShowEditModal(true)}
        />
        
        <RoleCard 
          name="Data Reviewer" 
          description="Reviews coding decisions and resolves conflicts"
          members={1}
          isDefault={false}
          permissions={[
            "View all papers and coding",
            "Resolve coding conflicts",
            "Provide feedback on coding",
            "Limited analysis capabilities"
          ]}
          onEdit={() => setShowEditModal(true)}
        />
        
        <RoleCard 
          name="Viewer" 
          description="Read-only access to projects and results"
          members={1}
          isDefault={false}
          permissions={[
            "View projects and papers",
            "View results and analyses",
            "Cannot modify any data",
            "Cannot create new projects"
          ]}
          onEdit={() => setShowEditModal(true)}
        />
      </div>
      
      {showEditModal && <EditRoleModal onClose={() => setShowEditModal(false)} />}
      {showCreateModal && <CreateRoleModal onClose={() => setShowCreateModal(false)} />}
    </div>
  );
};

const RoleCard = ({ name, description, members, isDefault, permissions, onEdit }) => {
  const [expanded, setExpanded] = useState(false);
  
  return (
    <div className="bg-white border rounded-lg overflow-hidden hover:shadow-md transition-shadow">
      <div className="p-4 border-b flex justify-between items-center">
        <div className="flex items-center">
          <div className="font-medium">{name}</div>
          {isDefault && (
            <span className="ml-2 text-xs bg-blue-100 text-blue-800 px-2 py-0.5 rounded-full">
              Default
            </span>
          )}
        </div>
        <button 
          className="text-gray-400 hover:text-gray-600"
          onClick={() => setExpanded(!expanded)}
        >
          {expanded ? (
            <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 15l7-7 7 7" />
            </svg>
          ) : (
            <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          )}
        </button>
      </div>
      
      <div className="p-4">
        <p className="text-sm text-gray-600 mb-3">{description}</p>
        <div className="text-sm text-gray-500">{members} {members === 1 ? 'member' : 'members'}</div>
        
        {expanded && (
          <div className="mt-4 pt-4 border-t">
            <h4 className="text-sm font-medium mb-2">Permissions</h4>
            <ul className="space-y-1 text-sm text-gray-600">
              {permissions.map((permission, idx) => (
                <li key={idx} className="flex items-center">
                  <svg className="h-4 w-4 text-green-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  {permission}
                </li>
              ))}
            </ul>
            
            <div className="flex justify-end mt-4">
              <button 
                className="text-indigo-600 hover:text-indigo-800 text-sm mr-2"
                onClick={() => {}}
              >
                View Members
              </button>
              <button 
                className="text-indigo-600 hover:text-indigo-800 text-sm"
                onClick={onEdit}
              >
                Edit Role
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

const InvitationsTab = () => {
  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <div className="text-xl font-medium">Invitations</div>
        <div className="flex">
          <button className="px-4 py-2 rounded-lg border bg-white text-gray-700 hover:bg-gray-50 mr-2">
            View Invitation History
          </button>
          <button className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 flex items-center">
            <UserPlus size={16} className="mr-1" /> Send New Invitation
          </button>
        </div>
      </div>
      
      <div className="bg-white border rounded-lg overflow-hidden mb-6">
        <div className="bg-gray-50 py-3 px-4 border-b">
          <div className="font-medium">Pending Invitations (3)</div>
        </div>
        
        <div className="divide-y">
          <InvitationItem 
            email="robert.wilson@example.com"
            role="Statistical Analyst"
            projects={["CBT Meta-Analysis", "Remote Work Study"]}
            sentBy="John Doe"
            sentDate="2 days ago"
            expiresIn="5 days"
          />
          <InvitationItem 
            email="emily.johnson@example.com"
            role="Secondary Coder"
            projects={["CBT Meta-Analysis"]}
            sentBy="Jane Smith"
            sentDate="3 days ago"
            expiresIn="4 days"
          />
          <InvitationItem 
            email="david.martinez@example.com"
            role="Viewer"
            projects={["Vaccine Efficacy Comparison"]}
            sentBy="John Doe"
            sentDate="1 week ago"
            expiresIn="Today"
          />
        </div>
      </div>
      
      <div className="bg-white border rounded-lg overflow-hidden">
        <div className="bg-gray-50 py-3 px-4 border-b">
          <div className="font-medium">Recently Joined (4)</div>
        </div>
        
        <div className="divide-y">
          <NewMemberItem 
            name="Thomas Lee"
            email="thomas.lee@example.com"
            avatar="TL"
            role="Secondary Coder"
            joinedDate="Today"
            projects={["Remote Work Study"]}
          />
          <NewMemberItem 
            name="Rachel Kim"
            email="rachel.kim@example.com"
            avatar="RK"
            role="Data Reviewer"
            joinedDate="Yesterday"
            projects={["CBT Meta-Analysis"]}
          />
          <NewMemberItem 
            name="Paul Garcia"
            email="p.garcia@example.com"
            avatar="PG"
            role="Statistical Analyst"
            joinedDate="3 days ago"
            projects={["Exercise for Depression Meta-Analysis"]}
          />
          <NewMemberItem 
            name="Olivia Chen"
            email="o.chen@example.com"
            avatar="OC"
            role="Viewer"
            joinedDate="1 week ago"
            projects={["CBT Meta-Analysis", "Vaccine Efficacy Comparison"]}
          />
        </div>
      </div>
    </div>
  );
};

const InvitationItem = ({ email, role, projects, sentBy, sentDate, expiresIn }) => {
  return (
    <div className="py-4 px-6 hover:bg-gray-50">
      <div className="flex justify-between items-start mb-2">
        <div>
          <div className="font-medium">{email}</div>
          <div className="text-sm text-gray-500">Role: {role}</div>
        </div>
        <div className="flex">
          <button className="px-3 py-1 bg-indigo-100 text-indigo-700 rounded-lg text-sm mr-2 hover:bg-indigo-200">
            Resend
          </button>
          <button className="px-3 py-1 bg-red-100 text-red-700 rounded-lg text-sm hover:bg-red-200">
            Cancel
          </button>
        </div>
      </div>
      
      <div className="flex items-center text-sm text-gray-500 mb-2">
        <span className="mr-3">Sent by {sentBy} • {sentDate}</span>
        <span className={`${expiresIn === 'Today' ? 'text-red-500' : ''}`}>Expires {expiresIn}</span>
      </div>
      
      <div className="mt-2">
        <div className="text-xs text-gray-500 mb-1">Invited to projects:</div>
        <div className="flex flex-wrap">
          {projects.map((project, idx) => (
            <span 
              key={idx} 
              className="text-xs bg-gray-100 text-gray-600 rounded-full px-2 py-1 mr-1 mb-1"
            >
              {project}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
};

const NewMemberItem = ({ name, email, avatar, role, joinedDate, projects }) => {
  return (
    <div className="py-4 px-6 hover:bg-gray-50">
      <div className="flex items-center mb-2">
        <div className="h-10 w-10 rounded-full bg-indigo-100 text-indigo-800 flex items-center justify-center mr-3">
          {avatar}
        </div>
        <div>
          <div className="font-medium">{name}</div>
          <div className="text-sm text-gray-500">{email}</div>
        </div>
        <div className="ml-auto">
          <span className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded-full">
            Joined {joinedDate}
          </span>
        </div>
      </div>
      
      <div className="flex justify-between items-center">
        <div>
          <div className="text-xs text-gray-500 mb-1">Assigned role: {role}</div>
          <div className="flex flex-wrap">
            {projects.map((project, idx) => (
              <span 
                key={idx} 
                className="text-xs bg-gray-100 text-gray-600 rounded-full px-2 py-1 mr-1 mb-1"
              >
                {project}
              </span>
            ))}
          </div>
        </div>
        <button className="text-indigo-600 hover:text-indigo-800 text-sm">
          View Profile
        </button>
      </div>
    </div>
  );
};

const SettingsTab = () => {
  return (
    <div className="p-6">
      <div className="text-xl font-medium mb-6">Team Settings</div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white border rounded-lg overflow-hidden">
          <div className="p-4 border-b">
            <h3 className="font-medium">Organization Information</h3>
          </div>
          <div className="p-4">
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Team Name
              </label>
              <input 
                type="text" 
                className="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
                value="MetaReview Research Group"
              />
            </div>
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Team Description
              </label>
              <textarea 
                className="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
                rows="3"
                value="Collaborative research team focused on meta-analyses and systematic reviews in psychology and health sciences."
              ></textarea>
            </div>
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Website (optional)
              </label>
              <input 
                type="url" 
                className="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
                value="https://metareview-research.org"
              />
            </div>
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Primary Contact Email
              </label>
              <input 
                type="email" 
                className="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
                value="contact@metareview-research.org"
              />
            </div>
            
            <button className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700">
              Save Changes
            </button>
          </div>
        </div>
        
        <div className="bg-white border rounded-lg overflow-hidden">
          <div className="p-4 border-b">
            <h3 className="font-medium">General Settings</h3>
          </div>
          <div className="p-4">
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Default Role for New Members
              </label>
              <select className="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none">
                <option>Primary Researcher</option>
                <option>Secondary Coder</option>
                <option>Statistical Analyst</option>
                <option>Data Reviewer</option>
                <option>Viewer</option>
              </select>
              <p className="text-xs text-gray-500 mt-1">
                The default role assigned to new team members when invited without specifying a role
              </p>
            </div>
            
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Invitation Expiration
              </label>
              <select className="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none">
                <option>7 days</option>
                <option>14 days</option>
                <option>30 days</option>
                <option>Never</option>
              </select>
              <p className="text-xs text-gray-500 mt-1">
                How long invitations remain valid before they expire and need to be resent
              </p>
            </div>
            
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Project Visibility
              </label>
              <select className="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none">
                <option>Team Only - All projects visible to all team members</option>
                <option>Project-Based - Only visible to assigned members</option>
              </select>
              <p className="text-xs text-gray-500 mt-1">
                Controls default visibility of projects across the team
              </p>
            </div>
            
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Activity Tracking
              </label>
              <div className="space-y-2">
                <div className="flex items-center">
                  <input id="track-logins" type="checkbox" className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded" checked />
                  <label htmlFor="track-logins" className="ml-2 text-sm text-gray-700">
                    Track user logins and activities
                  </label>
                </div>
                <div className="flex items-center">
                  <input id="track-coding" type="checkbox" className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded" checked />
                  <label htmlFor="track-coding" className="ml-2 text-sm text-gray-700">
                    Track coding time and productivity
                  </label>
                </div>
              </div>
            </div>
            
            <button className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700">
              Save Settings
            </button>
          </div>
        </div>
        
        <div className="bg-white border rounded-lg overflow-hidden">
          <div className="p-4 border-b">
            <h3 className="font-medium">Security Settings</h3>
          </div>
          <div className="p-4">
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Session Timeout
              </label>
              <select className="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none">
                <option>30 minutes</option>
                <option>1 hour</option>
                <option>2 hours</option>
                <option>4 hours</option>
                <option>8 hours</option>
              </select>
              <p className="text-xs text-gray-500 mt-1">
                How long users remain logged in during inactivity
              </p>
            </div>
            
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Password Policy
              </label>
              <div className="space-y-2">
                <div className="flex items-center">
                  <input id="complex-password" type="checkbox" className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded" checked />
                  <label htmlFor="complex-password" className="ml-2 text-sm text-gray-700">
                    Require complex passwords (min. 8 chars, uppercase, number, symbol)
                  </label>
                </div>
                <div className="flex items-center">
                  <input id="password-expiry" type="checkbox" className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded" />
                  <label htmlFor="password-expiry" className="ml-2 text-sm text-gray-700">
                    Password expires after 90 days
                  </label>
                </div>
                <div className="flex items-center">
                  <input id="2fa" type="checkbox" className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded" checked />
                  <label htmlFor="2fa" className="ml-2 text-sm text-gray-700">
                    Allow two-factor authentication
                  </label>
                </div>
              </div>
            </div>
            
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Login Restrictions
              </label>
              <div className="space-y-2">
                <div className="flex items-center">
                  <input id="ip-restrict" type="checkbox" className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded" />
                  <label htmlFor="ip-restrict" className="ml-2 text-sm text-gray-700">
                    Restrict access to specific IP addresses
                  </label>
                </div>
                <div className="flex items-center">
                  <input id="failed-attempts" type="checkbox" className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded" checked />
                  <label htmlFor="failed-attempts" className="ml-2 text-sm text-gray-700">
                    Lock account after 5 failed login attempts
                  </label>
                </div>
              </div>
            </div>
            
            <button className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700">
              Save Security Settings
            </button>
          </div>
        </div>
        
        <div className="bg-white border rounded-lg overflow-hidden">
          <div className="p-4 border-b">
            <h3 className="font-medium">Notification Settings</h3>
          </div>
          <div className="p-4">
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Team Email Notifications
              </label>
              <div className="space-y-2">
                <div className="flex items-center">
                  <input id="new-member" type="checkbox" className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded" checked />
                  <label htmlFor="new-member" className="ml-2 text-sm text-gray-700">
                    New member joins
                  </label>
                </div>
                <div className="flex items-center">
                  <input id="role-changes" type="checkbox" className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded" checked />
                  <label htmlFor="role-changes" className="ml-2 text-sm text-gray-700">
                    Role changes
                  </label>
                </div>
                <div className="flex items-center">
                  <input id="project-created" type="checkbox" className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded" checked />
                  <label htmlFor="project-created" className="ml-2 text-sm text-gray-700">
                    New project created
                  </label>
                </div>
                <div className="flex items-center">
                  <input id="weekly-summary" type="checkbox" className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded" />
                  <label htmlFor="weekly-summary" className="ml-2 text-sm text-gray-700">
                    Weekly team activity summary
                  </label>
                </div>
              </div>
            </div>
            
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Project Notifications
              </label>
              <div className="space-y-2">
                <div className="flex items-center">
                  <input id="assignment" type="checkbox" className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded" checked />
                  <label htmlFor="assignment" className="ml-2 text-sm text-gray-700">
                    New assignments
                  </label>
                </div>
                <div className="flex items-center">
                  <input id="approaching-deadline" type="checkbox" className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded" checked />
                  <label htmlFor="approaching-deadline" className="ml-2 text-sm text-gray-700">
                    Approaching deadlines
                  </label>
                </div>
                <div className="flex items-center">
                  <input id="coding-conflicts" type="checkbox" className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded" checked />
                  <label htmlFor="coding-conflicts" className="ml-2 text-sm text-gray-700">
                    Coding conflicts
                  </label>
                </div>
                <div className="flex items-center">
                  <input id="project-completion" type="checkbox" className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded" checked />
                  <label htmlFor="project-completion" className="ml-2 text-sm text-gray-700">
                    Project milestones
                  </label>
                </div>
              </div>
            </div>
            
            <button className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700">
              Save Notification Settings
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

const InviteModal = ({ onClose }) => {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-md">
        <div className="p-4 border-b flex justify-between items-center">
          <h3 className="font-medium text-lg">Invite Team Member</h3>
          <button 
            className="text-gray-400 hover:text-gray-600"
            onClick={onClose}
          >
            <X size={18} />
          </button>
        </div>
        
        <div className="p-6">
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Email Address
            </label>
            <input 
              type="email" 
              className="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
              placeholder="colleague@example.com"
            />
          </div>
          
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Role
            </label>
            <select className="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none">
              <option>Primary Researcher</option>
              <option>Secondary Coder</option>
              <option>Statistical Analyst</option>
              <option>Data Reviewer</option>
              <option>Viewer</option>
            </select>
          </div>
          
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Assign to Projects
            </label>
            <div className="border rounded-lg p-3 max-h-40 overflow-y-auto">
              <div className="space-y-2">
                <div className="flex items-center">
                  <input id="project1" type="checkbox" className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded" checked />
                  <label htmlFor="project1" className="ml-2 text-sm text-gray-700">
                    Effectiveness of CBT for Anxiety Disorders
                  </label>
                </div>
                <div className="flex items-center">
                  <input id="project2" type="checkbox" className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded" />
                  <label htmlFor="project2" className="ml-2 text-sm text-gray-700">
                    Meta-analysis of Remote Work Productivity
                  </label>
                </div>
                <div className="flex items-center">
                  <input id="project3" type="checkbox" className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded" checked />
                  <label htmlFor="project3" className="ml-2 text-sm text-gray-700">
                    Vaccine Efficacy Comparison
                  </label>
                </div>
                <div className="flex items-center">
                  <input id="project4" type="checkbox" className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded" />
                  <label htmlFor="project4" className="ml-2 text-sm text-gray-700">
                    Effects of Mindfulness Meditation
                  </label>
                </div>
                <div className="flex items-center">
                  <input id="project5" type="checkbox" className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded" />
                  <label htmlFor="project5" className="ml-2 text-sm text-gray-700">
                    Exercise for Depression Meta-Analysis
                  </label>
                </div>
              </div>
            </div>
          </div>
          
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Personalized Message (Optional)
            </label>
            <textarea 
              className="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
              rows="3"
              placeholder="Add a personal note to your invitation..."
            ></textarea>
          </div>
        </div>
        
        <div className="p-4 border-t flex justify-end bg-gray-50 rounded-b-lg">
          <button 
            className="px-4 py-2 border rounded-lg text-gray-700 hover:bg-gray-100 mr-2"
            onClick={onClose}
          >
            Cancel
          </button>
          <button 
            className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
            onClick={onClose}
          >
            Send Invitation
          </button>
        </div>
      </div>
    </div>
  );
};

const ProfileModal = ({ onClose }) => {
  const [activeTab, setActiveTab] = useState('overview');
  
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-3xl max-h-[90vh] flex flex-col">
        <div className="p-4 border-b flex justify-between items-center">
          <h3 className="font-medium text-lg">User Profile</h3>
          <button 
            className="text-gray-400 hover:text-gray-600"
            onClick={onClose}
          >
            <X size={18} />
          </button>
        </div>
        
        <div className="p-6 overflow-y-auto flex-1">
          <div className="flex mb-6">
            <div className="mr-6">
              <div className="h-24 w-24 rounded-full bg-indigo-100 text-indigo-800 flex items-center justify-center text-2xl font-bold">
                JD
              </div>
            </div>
            <div className="flex-1">
              <h3 className="text-xl font-medium mb-1">John Doe</h3>
              <p className="text-gray-500 mb-2">john.doe@example.com</p>
              <div className="flex items-center mb-3">
                <span className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full mr-2">
                  Administrator
                </span>
                <span className="text-sm text-gray-500">
                  Joined March 2023
                </span>
              </div>
              <div className="flex">
                <button className="text-indigo-600 hover:text-indigo-800 text-sm mr-3">
                  Reset Password
                </button>
                <button className="text-indigo-600 hover:text-indigo-800 text-sm mr-3">
                  Change Role
                </button>
                <button className="text-red-600 hover:text-red-800 text-sm">
                  Deactivate Account
                </button>
              </div>
            </div>
          </div>
          
          <div className="border-b mb-4">
            <div className="flex">
              <button 
                className={`py-2 px-4 font-medium text-sm ${activeTab === 'overview' ? 'text-indigo-600 border-b-2 border-indigo-600' : 'text-gray-500 hover:text-gray-700'}`}
                onClick={() => setActiveTab('overview')}
              >
                Overview
              </button>
              <button 
                className={`py-2 px-4 font-medium text-sm ${activeTab === 'projects' ? 'text-indigo-600 border-b-2 border-indigo-600' : 'text-gray-500 hover:text-gray-700'}`}
                onClick={() => setActiveTab('projects')}
              >
                Projects
              </button>
              <button 
                className={`py-2 px-4 font-medium text-sm ${activeTab === 'activity' ? 'text-indigo-600 border-b-2 border-indigo-600' : 'text-gray-500 hover:text-gray-700'}`}
                onClick={() => setActiveTab('activity')}
              >
                Activity
              </button>
              <button 
                className={`py-2 px-4 font-medium text-sm ${activeTab === 'settings' ? 'text-indigo-600 border-b-2 border-indigo-600' : 'text-gray-500 hover:text-gray-700'}`}
                onClick={() => setActiveTab('settings')}
              >
                Settings
              </button>
            </div>
          </div>
          
          {activeTab === 'overview' && (
            <div>
              <div className="grid grid-cols-2 gap-6 mb-6">
                <div>
                  <h4 className="font-medium text-sm mb-2">Contact Information</h4>
                  <div className="space-y-1 text-sm">
                    <div className="flex justify-between border-b pb-1">
                      <span className="text-gray-500">Email</span>
                      <span>john.doe@example.com</span>
                    </div>
                    <div className="flex justify-between border-b pb-1">
                      <span className="text-gray-500">Phone</span>
                      <span>+1 (555) 123-4567</span>
                    </div>
                    <div className="flex justify-between border-b pb-1">
                      <span className="text-gray-500">Department</span>
                      <span>Research Methods</span>
                    </div>
                    <div className="flex justify-between border-b pb-1">
                      <span className="text-gray-500">Institution</span>
                      <span>University of Research</span>
                    </div>
                  </div>
                </div>
                
                <div>
                  <h4 className="font-medium text-sm mb-2">System Information</h4>
                  <div className="space-y-1 text-sm">
                    <div className="flex justify-between border-b pb-1">
                      <span className="text-gray-500">User ID</span>
                      <span>UR12345</span>
                    </div>
                    <div className="flex justify-between border-b pb-1">
                      <span className="text-gray-500">Account Status</span>
                      <span className="text-green-600">Active</span>
                    </div>
                    <div className="flex justify-between border-b pb-1">
                      <span className="text-gray-500">2FA Enabled</span>
                      <span>Yes</span>
                    </div>
                    <div className="flex justify-between border-b pb-1">
                      <span className="text-gray-500">Last Login</span>
                      <span>Today, 9:45 AM</span>
                    </div>
                  </div>
                </div>
              </div>
              
              <div className="mb-6">
                <h4 className="font-medium text-sm mb-2">Team Role & Permissions</h4>
                <div className="bg-gray-50 rounded-lg p-4 mb-2">
                  <div className="flex justify-between mb-1">
                    <div className="font-medium">Administrator</div>
                    <button className="text-indigo-600 hover:text-indigo-800 text-sm">
                      Change Role
                    </button>
                  </div>
                  <p className="text-sm text-gray-500 mb-3">
                    Full access to all features, user management, and organization settings
                  </p>
                  <div className="text-sm text-gray-600">
                    <div className="font-medium mb-1">Key Permissions:</div>
                    <ul className="list-disc pl-5 space-y-1">
                      <li>Manage users and roles</li>
                      <li>Create and delete projects</li>
                      <li>Configure organization settings</li>
                      <li>Access all projects and data</li>
                    </ul>
                  </div>
                </div>
              </div>
              
              <div>
                <h4 className="font-medium text-sm mb-2">Project Statistics</h4>
                <div className="grid grid-cols-3 gap-4">
                  <div className="bg-gray-50 rounded-lg p-3 text-center">
                    <div className="text-2xl font-bold text-indigo-600">8</div>
                    <div className="text-xs text-gray-500">Active Projects</div>
                  </div>
                  <div className="bg-gray-50 rounded-lg p-3 text-center">
                    <div className="text-2xl font-bold text-indigo-600">142</div>
                    <div className="text-xs text-gray-500">Papers Coded</div>
                  </div>
                  <div className="bg-gray-50 rounded-lg p-3 text-center">
                    <div className="text-2xl font-bold text-indigo-600">36</div>
                    <div className="text-xs text-gray-500">Hours Active This Month</div>
                  </div>
                </div>
              </div>
            </div>
          )}
          
          {activeTab === 'projects' && (
            <div>
              <div className="flex justify-between items-center mb-4">
                <h4 className="font-medium">Assigned Projects (8)</h4>
                <button className="text-sm text-indigo-600 hover:text-indigo-800 flex items-center">
                  <PlusCircle size={14} className="mr-1" /> Add to Project
                </button>
              </div>
              
              <div className="bg-white border rounded-lg overflow-hidden">
                <div className="bg-gray-50 py-3 px-4 border-b flex">
                  <div className="w-1/2 font-medium text-gray-700 text-sm">Project</div>
                  <div className="w-1/4 font-medium text-gray-700 text-sm">Role</div>
                  <div className="w-1/4 font-medium text-gray-700 text-sm">Status</div>
                </div>
                
                <div className="divide-y">
                  <UserProjectItem 
                    name="Effectiveness of CBT for Anxiety Disorders"
                    role="Project Lead"
                    status="In Progress"
                  />
                  <UserProjectItem 
                    name="Meta-analysis of Remote Work Productivity"
                    role="Statistical Analyst"
                    status="Analysis"
                  />
                  <UserProjectItem 
                    name="Vaccine Efficacy Comparison"
                    role="Project Lead"
                    status="Screening"
                  />
                  <UserProjectItem 
                    name="Effects of Mindfulness Meditation"
                    role="Secondary Coder"
                    status="Data Extraction"
                  />
                  <UserProjectItem 
                    name="Exercise for Depression Meta-Analysis"
                    role="Statistical Analyst"
                    status="Complete"
                  />
                </div>
              </div>
            </div>
          )}
          
          {activeTab === 'activity' && (
            <div>
              <div className="flex justify-between items-center mb-4">
                <h4 className="font-medium">Recent Activity</h4>
                <div className="flex items-center text-sm">
                  <span className="text-gray-500 mr-2">Filter by:</span>
                  <select className="border rounded-md p-1">
                    <option>All Activity</option>
                    <option>Projects</option>
                    <option>Coding</option>
                    <option>Analysis</option>
                    <option>Team</option>
                  </select>
                </div>
              </div>
              
              <div className="space-y-4">
                <ActivityTimelineItem 
                  action="Added 3 papers to"
                  project="Effectiveness of CBT for Anxiety Disorders"
                  time="Today, 2:30 PM"
                  type="papers"
                />
                <ActivityTimelineItem 
                  action="Completed coding of Chen et al. (2022) in"
                  project="Vaccine Efficacy Comparison"
                  time="Today, 11:15 AM"
                  type="coding"
                />
                <ActivityTimelineItem 
                  action="Ran meta-regression analysis for"
                  project="Meta-analysis of Remote Work Productivity"
                  time="Yesterday, 4:45 PM"
                  type="analysis"
                />
                <ActivityTimelineItem 
                  action="Invited Robert Wilson to"
                  project="Effectiveness of CBT for Anxiety Disorders"
                  time="Yesterday, 10:20 AM"
                  type="team"
                />
                <ActivityTimelineItem 
                  action="Created project"
                  project="Exercise for Depression Meta-Analysis"
                  time="March 15, 2023"
                  type="projects"
                />
              </div>
              
              <div className="mt-4 text-center">
                <button className="text-sm text-indigo-600 hover:text-indigo-800">
                  Load More Activity
                </button>
              </div>
            </div>
          )}
          
          {activeTab === 'settings' && (
            <div>
              <div className="mb-6">
                <h4 className="font-medium mb-3">Account Settings</h4>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Full Name
                    </label>
                    <input 
                      type="text" 
                      className="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
                      value="John Doe"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Email Address
                    </label>
                    <input 
                      type="email" 
                      className="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
                      value="john.doe@example.com"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Phone Number
                    </label>
                    <input 
                      type="tel" 
                      className="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
                      value="+1 (555) 123-4567"
                    />
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Department
                      </label>
                      <input 
                        type="text" 
                        className="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
                        value="Research Methods"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Institution
                      </label>
                      <input 
                        type="text" 
                        className="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
                        value="University of Research"
                      />
                    </div>
                  </div>
                </div>
              </div>
              
              <div className="mb-6">
                <h4 className="font-medium mb-3">Notification Preferences</h4>
                <div className="space-y-2">
                  <div className="flex items-center">
                    <input id="email-assign" type="checkbox" className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded" checked />
                    <label htmlFor="email-assign" className="ml-2 text-sm text-gray-700">
                      Email notifications for new assignments
                    </label>
                  </div>
                  <div className="flex items-center">
                    <input id="email-comments" type="checkbox" className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded" checked />
                    <label htmlFor="email-comments" className="ml-2 text-sm text-gray-700">
                      Email notifications for comments and feedback
                    </label>
                  </div>
                  <div className="flex items-center">
                    <input id="email-conflicts" type="checkbox" className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded" checked />
                    <label htmlFor="email-conflicts" className="ml-2 text-sm text-gray-700">
                      Email notifications for coding conflicts
                    </label>
                  </div>
                  <div className="flex items-center">
                    <input id="email-team" type="checkbox" className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded" />
                    <label htmlFor="email-team" className="ml-2 text-sm text-gray-700">
                      Email notifications for team changes
                    </label>
                  </div>
                  <div className="flex items-center">
                    <input id="email-digest" type="checkbox" className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded" checked />
                    <label htmlFor="email-digest" className="ml-2 text-sm text-gray-700">
                      Weekly digest of project activity
                    </label>
                  </div>
                </div>
              </div>
              
              <div className="mb-6">
                <h4 className="font-medium mb-3">Security</h4>
                <div className="space-y-4">
                  <div>
                    <button className="px-4 py-2 border rounded-lg text-gray-700 hover:bg-gray-50 flex items-center">
                      <Key size={16} className="mr-1" /> Change Password
                    </button>
                  </div>
                  <div>
                    <button className="px-4 py-2 border rounded-lg text-gray-700 hover:bg-gray-50 flex items-center">
                      <Shield size={16} className="mr-1" /> Set Up Two-Factor Authentication
                    </button>
                  </div>
                  <div>
                    <button className="px-4 py-2 border rounded-lg text-gray-700 hover:bg-gray-50 flex items-center">
                      <LogOut size={16} className="mr-1" /> Log Out of All Devices
                    </button>
                  </div>
                </div>
              </div>
              
              <div className="mt-6 flex justify-end">
                <button className="px-4 py-2 border rounded-lg text-gray-700 hover:bg-gray-100 mr-2">
                  Cancel
                </button>
                <button className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700">
                  Save Changes
                </button>
              </div>
            </div>
          )}
        </div>
        
        <div className="p-4 border-t flex justify-end bg-gray-50 rounded-b-lg">
          <button 
            className="px-4 py-2 border rounded-lg text-gray-700 hover:bg-gray-100 mr-2"
            onClick={onClose}
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

const EditRoleModal = ({ onClose }) => {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-2xl">
        <div className="p-4 border-b flex justify-between items-center">
          <h3 className="font-medium text-lg">Edit Role</h3>
          <button 
            className="text-gray-400 hover:text-gray-600"
            onClick={onClose}
          >
            <X size={18} />
          </button>
        </div>
        
        <div className="p-6">
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Role Name
            </label>
            <input 
              type="text" 
              className="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
              value="Primary Researcher"
            />
          </div>
          
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Description
            </label>
            <textarea 
              className="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
              rows="2"
              value="Can create projects, manage project settings, and assign team members"
            ></textarea>
          </div>
          
          <div className="mb-4">
            <div className="flex items-center mb-1">
              <input id="default-role" type="checkbox" className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded" checked />
              <label htmlFor="default-role" className="ml-2 text-sm text-gray-700">
                Set as default role for new members
              </label>
            </div>
            <p className="text-xs text-gray-500">
              New team members will automatically be assigned this role when invited without specifying a role
            </p>
          </div>
          
          <div className="mb-4">
            <h4 className="font-medium text-sm mb-3">Permissions</h4>
            
            <div className="space-y-6">
              <PermissionSection 
                title="Project Permissions" 
                permissions={[
                  { id: 'create-project', label: 'Create new projects', checked: true },
                  { id: 'delete-project', label: 'Delete projects', checked: true },
                  { id: 'edit-project', label: 'Edit project settings', checked: true },
                  { id: 'view-all-projects', label: 'View all team projects', checked: true }
                ]}
              />
              
              <PermissionSection 
                title="Team & Collaboration" 
                permissions={[
                  { id: 'add-members', label: 'Add members to projects', checked: true },
                  { id: 'remove-members', label: 'Remove members from projects', checked: true },
                  { id: 'assign-roles', label: 'Assign roles within projects', checked: true },
                  { id: 'manage-roles', label: 'Manage and create roles', checked: false }
                ]}
              />
              
              <PermissionSection 
                title="Data Management" 
                permissions={[
                  { id: 'add-papers', label: 'Add/remove papers', checked: true },
                  { id: 'code-papers', label: 'Code and extract data', checked: true },
                  { id: 'edit-coding', label: 'Edit coding sheets', checked: true },
                  { id: 'resolve-conflicts', label: 'Resolve coding conflicts', checked: true }
                ]}
              />
              
              <PermissionSection 
                title="Analysis & Results" 
                permissions={[
                  { id: 'run-analysis', label: 'Run analyses', checked: true },
                  { id: 'edit-analysis', label: 'Edit analysis settings', checked: true },
                  { id: 'export-results', label: 'Export results and reports', checked: true },
                  { id: 'publish-results', label: 'Publish results internally', checked: true }
                ]}
              />
              
              <PermissionSection 
                title="Administration" 
                permissions={[
                  { id: 'system-settings', label: 'Change system settings', checked: false },
                  { id: 'manage-users', label: 'Manage all users', checked: false },
                  { id: 'billing-access', label: 'Access billing and subscription', checked: false },
                  { id: 'audit-logs', label: 'View audit logs', checked: false }
                ]}
              />
            </div>
          </div>
        </div>
        
        <div className="p-4 border-t flex justify-end bg-gray-50 rounded-b-lg">
          <button 
            className="px-4 py-2 border rounded-lg text-gray-700 hover:bg-gray-100 mr-2"
            onClick={onClose}
          >
            Cancel
          </button>
          <button 
            className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
            onClick={onClose}
          >
            Save Changes
          </button>
        </div>
      </div>
    </div>
  );
};

const CreateRoleModal = ({ onClose }) => {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-2xl">
        <div className="p-4 border-b flex justify-between items-center">
          <h3 className="font-medium text-lg">Create New Role</h3>
          <button 
            className="text-gray-400 hover:text-gray-600"
            onClick={onClose}
          >
            <X size={18} />
          </button>
        </div>
        
        <div className="p-6">
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Role Name
            </label>
            <input 
              type="text" 
              className="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
              placeholder="Enter role name..."
            />
          </div>
          
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Description
            </label>
            <textarea 
              className="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
              rows="2"
              placeholder="Describe the role's purpose and responsibilities..."
            ></textarea>
          </div>
          
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Base Role Template
            </label>
            <select className="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none">
              <option>Start from scratch</option>
              <option>Copy from Administrator</option>
              <option>Copy from Primary Researcher</option>
              <option>Copy from Statistical Analyst</option>
              <option>Copy from Secondary Coder</option>
              <option>Copy from Viewer</option>
            </select>
            <p className="text-xs text-gray-500 mt-1">
              Start with permissions from an existing role or create from scratch
            </p>
          </div>
          
          <div className="mb-4">
            <div className="flex items-center mb-1">
              <input id="default-role-new" type="checkbox" className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded" />
              <label htmlFor="default-role-new" className="ml-2 text-sm text-gray-700">
                Set as default role for new members
              </label>
            </div>
          </div>
          
          <div className="mb-4">
            <h4 className="font-medium text-sm mb-3">Permissions</h4>
            
            <div className="space-y-6">
              <PermissionSection 
                title="Project Permissions" 
                permissions={[
                  { id: 'create-project-new', label: 'Create new projects', checked: false },
                  { id: 'delete-project-new', label: 'Delete projects', checked: false },
                  { id: 'edit-project-new', label: 'Edit project settings', checked: false },
                  { id: 'view-all-projects-new', label: 'View all team projects', checked: true }
                ]}
              />
              
              <PermissionSection 
                title="Team & Collaboration" 
                permissions={[
                  { id: 'add-members-new', label: 'Add members to projects', checked: false },
                  { id: 'remove-members-new', label: 'Remove members from projects', checked: false },
                  { id: 'assign-roles-new', label: 'Assign roles within projects', checked: false },
                  { id: 'manage-roles-new', label: 'Manage and create roles', checked: false }
                ]}
              />
              
              <PermissionSection 
                title="Data Management" 
                permissions={[
                  { id: 'add-papers-new', label: 'Add/remove papers', checked: false },
                  { id: 'code-papers-new', label: 'Code and extract data', checked: true },
                  { id: 'edit-coding-new', label: 'Edit coding sheets', checked: false },
                  { id: 'resolve-conflicts-new', label: 'Resolve coding conflicts', checked: false }
                ]}
              />
            </div>
            
            <div className="mt-3 pl-2">
              <button className="text-sm text-indigo-600 hover:text-indigo-800">
                Show all permission categories...
              </button>
            </div>
          </div>
        </div>
        
        <div className="p-4 border-t flex justify-end bg-gray-50 rounded-b-lg">
          <button 
            className="px-4 py-2 border rounded-lg text-gray-700 hover:bg-gray-100 mr-2"
            onClick={onClose}
          >
            Cancel
          </button>
          <button 
            className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
            onClick={onClose}
          >
            Create Role
          </button>
        </div>
      </div>
    </div>
  );
};

const PermissionSection = ({ title, permissions }) => {
  const [expanded, setExpanded] = useState(true);
  
  return (
    <div className="border rounded-lg overflow-hidden">
      <div 
        className="p-3 bg-gray-50 flex justify-between items-center cursor-pointer"
        onClick={() => setExpanded(!expanded)}
      >
        <h5 className="font-medium text-sm">{title}</h5>
        <button className="text-gray-400">
          {expanded ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
        </button>
      </div>
      
      {expanded && (
        <div className="p-3 grid grid-cols-2 gap-y-2 gap-x-4">
          {permissions.map((permission) => (
            <div key={permission.id} className="flex items-center">
              <input 
                id={permission.id} 
                type="checkbox" 
                className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded" 
                checked={permission.checked}
              />
              <label htmlFor={permission.id} className="ml-2 text-sm text-gray-700">
                {permission.label}
              </label>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

const UserProjectItem = ({ name, role, status }) => {
  const getStatusColor = (status) => {
    switch(status) {
      case 'Planning': return 'bg-gray-100 text-gray-800';
      case 'Screening': return 'bg-blue-100 text-blue-800';
      case 'Data Extraction': return 'bg-yellow-100 text-yellow-800';
      case 'Analysis': return 'bg-purple-100 text-purple-800';
      case 'In Progress': return 'bg-indigo-100 text-indigo-800';
      case 'Complete': return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };
  
  return (
    <div className="py-3 px-4 flex items-center hover:bg-gray-50">
      <div className="w-1/2">
        <div className="font-medium text-indigo-600 hover:text-indigo-800 cursor-pointer">{name}</div>
      </div>
      <div className="w-1/4 text-sm text-gray-600">{role}</div>
      <div className="w-1/4">
        <span className={`text-xs px-2 py-1 rounded-full ${getStatusColor(status)}`}>
          {status}
        </span>
      </div>
    </div>
  );
};

const ActivityTimelineItem = ({ action, project, time, type }) => {
  const getTypeIcon = (type) => {
    switch(type) {
      case 'papers': return <FileText size={16} className="text-blue-500" />;
      case 'coding': return <Edit3 size={16} className="text-purple-500" />;
      case 'analysis': return <BarChart2 size={16} className="text-green-500" />;
      case 'team': return <Users size={16} className="text-orange-500" />;
      case 'projects': return <Folder size={16} className="text-indigo-500" />;
      default: return <Bell size={16} className="text-gray-500" />;
    }
  };
  
  return (
    <div className="flex">
      <div className="mr-3 mt-1">
        <div className="h-8 w-8 rounded-full bg-gray-100 flex items-center justify-center">
          {getTypeIcon(type)}
        </div>
      </div>
      <div className="flex-1 pb-5 border-l border-gray-200 pl-4 relative">
        <div className="absolute -left-1.5 mt-1.5 h-3 w-3 rounded-full border-2 border-white bg-gray-200"></div>
        <div className="text-sm">
          <span>{action} </span>
          <span className="font-medium text-indigo-600">{project}</span>
        </div>
        <div className="text-xs text-gray-500 mt-1">{time}</div>
      </div>
    </div>
  );
};

export default UserManagement;
