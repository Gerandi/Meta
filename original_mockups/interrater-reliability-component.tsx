import React, { useState } from 'react';
import { Users, BarChart2, AlertTriangle, CheckCircle, RefreshCw, Clipboard, HelpCircle, Settings, Plus, UserPlus, Edit3, Eye, X, ChevronDown, ChevronUp } from 'lucide-react';

const InterraterReliability = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [expandedConflict, setExpandedConflict] = useState(null);
  
  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold">Inter-rater Reliability</h1>
          <p className="text-gray-600">Track coding agreement and resolve conflicts</p>
        </div>
        <div className="flex">
          <button className="px-4 py-2 rounded-lg border bg-white text-gray-700 hover:bg-gray-50 mr-2 flex items-center">
            <Settings size={16} className="mr-1" /> Configure
          </button>
          <button className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 flex items-center">
            <RefreshCw size={16} className="mr-1" /> Calculate Agreement
          </button>
        </div>
      </div>
      
      <div className="bg-white rounded-lg shadow-lg overflow-hidden mb-6">
        <div className="flex border-b">
          <TabButton 
            active={activeTab === 'overview'} 
            onClick={() => setActiveTab('overview')}
            icon={<BarChart2 size={18} />}
            label="Overview"
          />
          <TabButton 
            active={activeTab === 'conflicts'} 
            onClick={() => setActiveTab('conflicts')}
            icon={<AlertTriangle size={18} />}
            label="Conflicts"
            badge="12"
          />
          <TabButton 
            active={activeTab === 'assignments'} 
            onClick={() => setActiveTab('assignments')}
            icon={<Users size={18} />}
            label="Coding Assignments"
          />
          <TabButton 
            active={activeTab === 'settings'} 
            onClick={() => setActiveTab('settings')}
            icon={<Settings size={18} />}
            label="Settings"
          />
        </div>
        
        {activeTab === 'overview' && <OverviewTab />}
        {activeTab === 'conflicts' && <ConflictsTab expandedConflict={expandedConflict} setExpandedConflict={setExpandedConflict} />}
        {activeTab === 'assignments' && <AssignmentsTab />}
        {activeTab === 'settings' && <SettingsTab />}
      </div>
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

const OverviewTab = () => {
  return (
    <div className="p-6">
      <div className="grid grid-cols-3 gap-6 mb-8">
        <StatCard 
          title="Overall Agreement" 
          value="87.4%" 
          subtitle="Across all variables"
          icon={<CheckCircle className="text-green-500" />}
          trend="+2.3% from last calculation"
          trendUp={true}
        />
        <StatCard 
          title="Cohen's Kappa" 
          value="0.82" 
          subtitle="Categorical variables"
          icon={<BarChart2 className="text-indigo-500" />}
          tooltip="Cohen's Kappa measures agreement for categorical variables, correcting for chance agreement"
        />
        <StatCard 
          title="ICC" 
          value="0.91" 
          subtitle="Continuous variables"
          icon={<BarChart2 className="text-indigo-500" />}
          tooltip="Intraclass Correlation Coefficient measures agreement for continuous variables"
        />
      </div>
      
      <div className="grid grid-cols-2 gap-6 mb-8">
        <div className="bg-white rounded-lg border p-4">
          <h3 className="font-medium mb-4 flex justify-between items-center">
            <span>Agreement by Variable</span>
            <button className="text-sm text-indigo-600 hover:text-indigo-800">
              View All
            </button>
          </h3>
          <div className="space-y-4">
            <AgreementBar variable="Study Design" agreement={98} />
            <AgreementBar variable="Sample Size" agreement={95} />
            <AgreementBar variable="Effect Size" agreement={89} />
            <AgreementBar variable="Risk of Bias" agreement={76} />
            <AgreementBar variable="Moderators" agreement={72} />
          </div>
        </div>
        
        <div className="bg-white rounded-lg border p-4">
          <h3 className="font-medium mb-4 flex justify-between items-center">
            <span>Agreement by Coder Pair</span>
            <button className="text-sm text-indigo-600 hover:text-indigo-800">
              View All
            </button>
          </h3>
          <div className="space-y-4">
            <CoderPairAgreement coder1="John Doe" coder2="Jane Smith" agreement={92} studiesShared={12} />
            <CoderPairAgreement coder1="John Doe" coder2="Alex Johnson" agreement={89} studiesShared={8} />
            <CoderPairAgreement coder1="Jane Smith" coder2="Alex Johnson" agreement={84} studiesShared={7} />
            <CoderPairAgreement coder1="Jane Smith" coder2="Sarah Williams" agreement={78} studiesShared={5} />
          </div>
        </div>
      </div>
      
      <div className="bg-white rounded-lg border p-4">
        <h3 className="font-medium mb-4">Agreement History</h3>
        <div className="h-64 border rounded-lg bg-gray-50 flex items-center justify-center">
          <div className="text-center">
            <BarChart2 size={48} className="mx-auto text-gray-400 mb-2" />
            <p className="text-gray-500">Agreement trend chart would appear here</p>
            <p className="text-sm text-gray-400">Showing how agreement metrics have changed over time</p>
          </div>
        </div>
      </div>
    </div>
  );
};

const StatCard = ({ title, value, subtitle, icon, trend, trendUp, tooltip }) => {
  return (
    <div className="bg-white rounded-lg border p-6">
      <div className="flex justify-between mb-2">
        <h3 className="font-medium text-gray-700">{title}</h3>
        <div className="text-gray-400">
          {tooltip ? (
            <div className="relative group">
              <HelpCircle size={16} />
              <div className="absolute z-10 w-64 p-2 -mt-12 -ml-64 text-xs text-white bg-gray-800 rounded-lg opacity-0 pointer-events-none group-hover:opacity-100 transition-opacity duration-300">
                {tooltip}
              </div>
            </div>
          ) : icon}
        </div>
      </div>
      <div className="text-3xl font-bold mb-1">{value}</div>
      <div className="text-sm text-gray-500">{subtitle}</div>
      {trend && (
        <div className={`mt-2 text-xs ${trendUp ? 'text-green-600' : 'text-red-600'} flex items-center`}>
          {trendUp ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
          {trend}
        </div>
      )}
    </div>
  );
};

const AgreementBar = ({ variable, agreement }) => {
  let color = "bg-red-500";
  if (agreement >= 90) color = "bg-green-500";
  else if (agreement >= 80) color = "bg-green-400";
  else if (agreement >= 70) color = "bg-yellow-500";
  
  return (
    <div>
      <div className="flex justify-between mb-1">
        <span className="text-sm font-medium text-gray-700">{variable}</span>
        <span className="text-sm font-medium text-gray-700">{agreement}%</span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-2.5">
        <div
          className={`h-2.5 rounded-full ${color}`}
          style={{ width: `${agreement}%` }}
        ></div>
      </div>
    </div>
  );
};

const CoderPairAgreement = ({ coder1, coder2, agreement, studiesShared }) => {
  let color = "text-red-500";
  if (agreement >= 90) color = "text-green-500";
  else if (agreement >= 80) color = "text-green-400";
  else if (agreement >= 70) color = "text-yellow-500";
  
  return (
    <div className="flex justify-between items-center">
      <div>
        <div className="font-medium">{coder1} & {coder2}</div>
        <div className="text-xs text-gray-500">{studiesShared} studies shared</div>
      </div>
      <div className={`font-bold ${color}`}>{agreement}%</div>
    </div>
  );
};

const ConflictsTab = ({ expandedConflict, setExpandedConflict }) => {
  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-4">
        <div className="flex items-center">
          <h2 className="text-lg font-medium">Coding Conflicts</h2>
          <span className="ml-2 px-2 py-0.5 bg-red-100 text-red-800 text-xs rounded-full">
            12 Unresolved
          </span>
        </div>
        <div className="flex items-center text-sm">
          <span className="text-gray-500 mr-2">Filter by:</span>
          <select className="border rounded-md p-1">
            <option>All Variables</option>
            <option>Study Design</option>
            <option>Sample Size</option>
            <option>Effect Size</option>
            <option>Risk of Bias</option>
          </select>
        </div>
      </div>
      
      <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6 flex">
        <div className="text-red-500 mr-3 mt-0.5">
          <AlertTriangle size={20} />
        </div>
        <div>
          <h3 className="font-medium text-red-800 mb-1">Conflicts Need Resolution</h3>
          <p className="text-red-700 text-sm">
            12 coding conflicts have been identified across 7 studies. These should be resolved before finalizing data extraction.
            Conflicts can be resolved by a third reviewer or through consensus discussions.
          </p>
        </div>
      </div>
      
      <div className="bg-white rounded-lg border overflow-hidden mb-6">
        <div className="px-4 py-3 border-b bg-gray-50 font-medium">
          Studies with Coding Conflicts
        </div>
        
        <div>
          <ConflictItem 
            study="Smith et al. (2023)"
            variables={["Effect Size", "Sample Size"]}
            coders={["John Doe", "Jane Smith"]}
            severity="high"
            isExpanded={expandedConflict === 1}
            toggleExpand={() => setExpandedConflict(expandedConflict === 1 ? null : 1)}
          />
          
          <ConflictItem 
            study="Garcia et al. (2022)"
            variables={["Risk of Bias", "Effect Size", "Confidence Interval"]}
            coders={["Jane Smith", "Alex Johnson"]}
            severity="high"
            isExpanded={expandedConflict === 2}
            toggleExpand={() => setExpandedConflict(expandedConflict === 2 ? null : 2)}
          />
          
          <ConflictItem 
            study="Chen et al. (2022)"
            variables={["Study Design"]}
            coders={["John Doe", "Alex Johnson"]}
            severity="medium"
            isExpanded={expandedConflict === 3}
            toggleExpand={() => setExpandedConflict(expandedConflict === 3 ? null : 3)}
          />
          
          <ConflictItem 
            study="Kumar et al. (2021)"
            variables={["Moderators", "Follow-up Period"]}
            coders={["Jane Smith", "Sarah Williams"]}
            severity="medium"
            isExpanded={expandedConflict === 4}
            toggleExpand={() => setExpandedConflict(expandedConflict === 4 ? null : 4)}
          />
          
          <ConflictItem 
            study="Robinson et al. (2023)"
            variables={["Statistical Test", "p-value", "Sample Characteristics"]}
            coders={["John Doe", "Sarah Williams"]}
            severity="low"
            isExpanded={expandedConflict === 5}
            toggleExpand={() => setExpandedConflict(expandedConflict === 5 ? null : 5)}
          />
        </div>
      </div>
      
      <div className="bg-white rounded-lg border p-4">
        <div className="flex justify-between items-center mb-4">
          <h3 className="font-medium">Recently Resolved Conflicts</h3>
          <button className="text-sm text-indigo-600 hover:text-indigo-800">
            View All History
          </button>
        </div>
        
        <div className="space-y-3">
          <ResolvedConflictItem 
            study="Thompson et al. (2022)"
            variable="Effect Size"
            resolvedBy="Consensus"
            resolvedDate="Today"
            value="g = 0.67"
          />
          
          <ResolvedConflictItem 
            study="Wilson et al. (2021)"
            variable="Risk of Bias"
            resolvedBy="Third Reviewer (Dr. Johnson)"
            resolvedDate="Yesterday"
            value="Low Risk"
          />
          
          <ResolvedConflictItem 
            study="Anderson et al. (2023)"
            variable="Sample Size"
            resolvedBy="Consensus"
            resolvedDate="2 days ago"
            value="N = 428"
          />
        </div>
      </div>
    </div>
  );
};

const ConflictItem = ({ study, variables, coders, severity, isExpanded, toggleExpand }) => {
  let severityClass = "bg-yellow-100 text-yellow-800";
  if (severity === "high") severityClass = "bg-red-100 text-red-800";
  else if (severity === "low") severityClass = "bg-orange-100 text-orange-800";
  
  return (
    <div className="border-b last:border-b-0">
      <div 
        className="p-4 flex justify-between items-center cursor-pointer hover:bg-gray-50"
        onClick={toggleExpand}
      >
        <div className="flex-1">
          <div className="font-medium">{study}</div>
          <div className="text-sm text-gray-500">
            {variables.length} variable{variables.length !== 1 ? 's' : ''} with conflicts
          </div>
        </div>
        
        <div className="flex items-center">
          <span className={`px-2 py-1 rounded-full text-xs font-medium ${severityClass} mr-4`}>
            {severity.charAt(0).toUpperCase() + severity.slice(1)} Severity
          </span>
          <button className="text-gray-400 hover:text-gray-600 mr-2">
            {isExpanded ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
          </button>
        </div>
      </div>
      
      {isExpanded && (
        <div className="px-4 pb-4 pt-2 bg-gray-50">
          <div className="mb-4">
            <div className="text-sm font-medium text-gray-700 mb-2">Coding Conflicts</div>
            <div className="bg-white rounded-lg border">
              <table className="min-w-full divide-y divide-gray-200">
                <thead>
                  <tr className="bg-gray-50">
                    <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Variable</th>
                    <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">{coders[0]}</th>
                    <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">{coders[1]}</th>
                    <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Resolution</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {variables.map((variable, idx) => (
                    <tr key={idx}>
                      <td className="px-4 py-3 text-sm font-medium">{variable}</td>
                      <td className="px-4 py-3 text-sm">
                        {variable === "Effect Size" ? "g = 0.82" : 
                         variable === "Sample Size" ? "N = 428" :
                         variable === "Risk of Bias" ? "Low Risk" :
                         variable === "Confidence Interval" ? "[0.71, 0.93]" :
                         variable === "Study Design" ? "Meta-analysis" :
                         variable === "Moderators" ? "Treatment Format, Duration" :
                         variable === "Follow-up Period" ? "12 months" :
                         variable === "Statistical Test" ? "ANOVA" :
                         variable === "p-value" ? "p < .001" :
                         variable === "Sample Characteristics" ? "Adults (18-65)" :
                         "Value 1"}
                      </td>
                      <td className="px-4 py-3 text-sm">
                        {variable === "Effect Size" ? "g = 0.76" : 
                         variable === "Sample Size" ? "N = 412" :
                         variable === "Risk of Bias" ? "Some Concerns" :
                         variable === "Confidence Interval" ? "[0.68, 0.89]" :
                         variable === "Study Design" ? "Systematic Review" :
                         variable === "Moderators" ? "Treatment Format" :
                         variable === "Follow-up Period" ? "6 months" :
                         variable === "Statistical Test" ? "t-test" :
                         variable === "p-value" ? "p < .01" :
                         variable === "Sample Characteristics" ? "Adults (18+)" :
                         "Value 2"}
                      </td>
                      <td className="px-4 py-3 text-sm">
                        <select className="border rounded py-1 px-2 text-xs w-full">
                          <option>Select resolution...</option>
                          <option>Accept {coders[0]}'s coding</option>
                          <option>Accept {coders[1]}'s coding</option>
                          <option>Third reviewer decision</option>
                          <option>Consensus meeting</option>
                          <option>Check original source</option>
                        </select>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
          
          <div className="flex justify-between items-center">
            <button className="px-3 py-1 text-sm border rounded-md hover:bg-gray-100">
              <Eye size={14} className="inline mr-1" /> View Full Study
            </button>
            <div>
              <button className="px-3 py-1 text-sm border rounded-md hover:bg-gray-100 mr-2">
                <UserPlus size={14} className="inline mr-1" /> Assign Third Reviewer
              </button>
              <button className="px-3 py-1 text-sm bg-indigo-600 text-white rounded-md hover:bg-indigo-700">
                <CheckCircle size={14} className="inline mr-1" /> Mark as Resolved
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

const ResolvedConflictItem = ({ study, variable, resolvedBy, resolvedDate, value }) => {
  return (
    <div className="flex justify-between items-center p-3 border rounded-lg hover:bg-gray-50">
      <div>
        <div className="font-medium">{study}</div>
        <div className="text-sm text-gray-600">{variable} → <span className="font-medium">{value}</span></div>
        <div className="text-xs text-gray-500">
          Resolved by {resolvedBy} • {resolvedDate}
        </div>
      </div>
      <button className="text-gray-400 hover:text-gray-600">
        <Eye size={16} />
      </button>
    </div>
  );
};

const AssignmentsTab = () => {
  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-lg font-medium">Coding Assignments</h2>
        <button className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 flex items-center">
          <Plus size={16} className="mr-1" /> Create Assignment
        </button>
      </div>
      
      <div className="grid grid-cols-2 gap-6 mb-6">
        <div className="bg-white rounded-lg border p-4">
          <h3 className="font-medium mb-4">Team Progress</h3>
          <div className="space-y-4">
            <CoderProgress 
              name="John Doe"
              role="Primary Coder"
              assigned={42}
              completed={36}
              conflicts={5}
            />
            <CoderProgress 
              name="Jane Smith"
              role="Primary Coder"
              assigned={38}
              completed={32}
              conflicts={7}
            />
            <CoderProgress 
              name="Alex Johnson"
              role="Secondary Coder"
              assigned={32}
              completed={26}
              conflicts={4}
            />
            <CoderProgress 
              name="Sarah Williams"
              role="Secondary Coder"
              assigned={24}
              completed={18}
              conflicts={3}
            />
            <CoderProgress 
              name="Dr. Michael Brown"
              role="Conflict Resolver"
              assigned={0}
              completed={0}
              conflicts={0}
            />
          </div>
        </div>
        
        <div className="bg-white rounded-lg border p-4">
          <h3 className="font-medium mb-4">Coding Coverage</h3>
          <div className="mb-4">
            <div className="flex justify-between mb-1">
              <span className="text-sm font-medium">Overall Progress</span>
              <span className="text-sm font-medium">79%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2.5">
              <div
                className="h-2.5 rounded-full bg-green-500"
                style={{ width: "79%" }}
              ></div>
            </div>
          </div>
          
          <div className="space-y-3 mb-4">
            <div>
              <div className="text-sm font-medium mb-2">Studies by Coding Status</div>
              <div className="grid grid-cols-3 gap-2 text-center">
                <div className="border rounded-lg p-2">
                  <div className="text-2xl font-bold text-indigo-600">42</div>
                  <div className="text-xs text-gray-500">Total Studies</div>
                </div>
                <div className="border rounded-lg p-2">
                  <div className="text-2xl font-bold text-green-600">28</div>
                  <div className="text-xs text-gray-500">Fully Coded</div>
                </div>
                <div className="border rounded-lg p-2">
                  <div className="text-2xl font-bold text-orange-500">14</div>
                  <div className="text-xs text-gray-500">Partially Coded</div>
                </div>
              </div>
            </div>
            
            <div>
              <div className="text-sm font-medium mb-2">Double-coding Status</div>
              <div className="grid grid-cols-2 gap-2 text-center">
                <div className="border rounded-lg p-2">
                  <div className="text-2xl font-bold text-indigo-600">35</div>
                  <div className="text-xs text-gray-500">Double-coded</div>
                </div>
                <div className="border rounded-lg p-2">
                  <div className="text-2xl font-bold text-yellow-500">7</div>
                  <div className="text-xs text-gray-500">Single-coded</div>
                </div>
              </div>
            </div>
          </div>
          
          <button className="w-full py-2 text-sm text-indigo-600 border border-indigo-200 rounded-lg hover:bg-indigo-50">
            Generate Coverage Report
          </button>
        </div>
      </div>
      
      <div className="bg-white rounded-lg border overflow-hidden">
        <div className="px-4 py-3 border-b bg-gray-50 font-medium flex justify-between items-center">
          <span>Recent Assignments</span>
          <div className="flex items-center">
            <button className="text-sm text-gray-500 hover:text-gray-700 mr-2">Filter</button>
            <select className="text-sm border rounded py-1 px-2">
              <option>All Statuses</option>
              <option>Pending</option>
              <option>In Progress</option>
              <option>Completed</option>
            </select>
          </div>
        </div>
        
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Study</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Assigned To</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Coding Type</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Due Date</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            <AssignmentRow 
              study="Smith et al. (2023)"
              assignedTo="John Doe"
              codingType="Primary"
              dueDate="Jul 15, 2023"
              status="completed"
            />
            <AssignmentRow 
              study="Smith et al. (2023)"
              assignedTo="Jane Smith"
              codingType="Secondary"
              dueDate="Jul 15, 2023"
              status="completed"
            />
            <AssignmentRow 
              study="Garcia et al. (2022)"
              assignedTo="Jane Smith"
              codingType="Primary"
              dueDate="Jul 18, 2023"
              status="completed"
            />
            <AssignmentRow 
              study="Garcia et al. (2022)"
              assignedTo="Alex Johnson"
              codingType="Secondary"
              dueDate="Jul 18, 2023"
              status="in-progress"
            />
            <AssignmentRow 
              study="Chen et al. (2022)"
              assignedTo="John Doe"
              codingType="Primary"
              dueDate="Jul 20, 2023"
              status="completed"
            />
            <AssignmentRow 
              study="Chen et al. (2022)"
              assignedTo="Alex Johnson"
              codingType="Secondary"
              dueDate="Jul 20, 2023"
              status="in-progress"
            />
            <AssignmentRow 
              study="Smith et al. (2023)"
              assignedTo="Dr. Michael Brown"
              codingType="Conflict Resolution"
              dueDate="Jul 22, 2023"
              status="pending"
            />
          </tbody>
        </table>
        
        <div className="px-4 py-3 border-t bg-gray-50 flex justify-between items-center">
          <div className="text-sm text-gray-500">
            Showing 7 of 64 assignments
          </div>
          <div className="flex">
            <button className="px-3 py-1 border rounded-md hover:bg-gray-100 mr-2">Previous</button>
            <button className="px-3 py-1 border rounded-md hover:bg-gray-100">Next</button>
          </div>
        </div>
      </div>
    </div>
  );
};

const CoderProgress = ({ name, role, assigned, completed, conflicts }) => {
  const percentComplete = Math.round((completed / assigned) * 100) || 0;
  
  return (
    <div>
      <div className="flex justify-between items-center mb-1">
        <div>
          <span className="font-medium">{name}</span>
          <span className="text-xs text-gray-500 ml-2">{role}</span>
        </div>
        <span className="text-sm">{completed}/{assigned} completed</span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-2.5 mb-1">
        <div
          className="h-2.5 rounded-full bg-indigo-500"
          style={{ width: `${percentComplete}%` }}
        ></div>
      </div>
      <div className="flex justify-between text-xs text-gray-500">
        <span>{percentComplete}% complete</span>
        {conflicts > 0 && (
          <span className="text-orange-500">{conflicts} conflict{conflicts !== 1 ? 's' : ''}</span>
        )}
      </div>
    </div>
  );
};

const AssignmentRow = ({ study, assignedTo, codingType, dueDate, status }) => {
  let statusClass = "bg-yellow-100 text-yellow-800";
  let statusText = "Pending";
  
  if (status === "completed") {
    statusClass = "bg-green-100 text-green-800";
    statusText = "Completed";
  } else if (status === "in-progress") {
    statusClass = "bg-blue-100 text-blue-800";
    statusText = "In Progress";
  }
  
  return (
    <tr className="hover:bg-gray-50">
      <td className="px-4 py-3 whitespace-nowrap text-sm font-medium">
        {study}
      </td>
      <td className="px-4 py-3 whitespace-nowrap text-sm">
        {assignedTo}
      </td>
      <td className="px-4 py-3 whitespace-nowrap text-sm">
        {codingType}
      </td>
      <td className="px-4 py-3 whitespace-nowrap text-sm">
        {dueDate}
      </td>
      <td className="px-4 py-3 whitespace-nowrap text-sm">
        <span className={`px-2 py-1 rounded-full text-xs font-medium ${statusClass}`}>
          {statusText}
        </span>
      </td>
      <td className="px-4 py-3 whitespace-nowrap text-sm">
        <div className="flex">
          <button className="text-gray-400 hover:text-indigo-600 mr-2" title="View">
            <Eye size={16} />
          </button>
          <button className="text-gray-400 hover:text-indigo-600 mr-2" title="Edit">
            <Edit3 size={16} />
          </button>
          <button className="text-gray-400 hover:text-red-600" title="Delete">
            <X size={16} />
          </button>
        </div>
      </td>
    </tr>
  );
};

const SettingsTab = () => {
  return (
    <div className="p-6">
      <div className="mb-6">
        <h2 className="text-lg font-medium mb-4">Inter-rater Reliability Settings</h2>
        <div className="bg-white rounded-lg border p-6">
          <div className="grid grid-cols-2 gap-6">
            <div>
              <h3 className="font-medium mb-3">General Settings</h3>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Double-coding Percentage
                  </label>
                  <select className="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none">
                    <option>100% (All studies)</option>
                    <option>50% (Random selection)</option>
                    <option>30% (Random selection)</option>
                    <option>20% (Random selection)</option>
                    <option>10% (Random selection)</option>
                  </select>
                  <p className="text-xs text-gray-500 mt-1">
                    Percentage of studies that should be coded by two independent reviewers
                  </p>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Agreement Threshold
                  </label>
                  <input 
                    type="number" 
                    className="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
                    value="80"
                    min="0"
                    max="100"
                  />
                  <p className="text-xs text-gray-500 mt-1">
                    Minimum percentage agreement required (less than this will flag as conflict)
                  </p>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Kappa Threshold
                  </label>
                  <input 
                    type="number" 
                    className="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
                    value="0.7"
                    min="0"
                    max="1"
                    step="0.1"
                  />
                  <p className="text-xs text-gray-500 mt-1">
                    Minimum Cohen's Kappa required for categorical variables
                  </p>
                </div>
              </div>
            </div>
            
            <div>
              <h3 className="font-medium mb-3">Conflict Resolution</h3>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Conflict Resolution Method
                  </label>
                  <select className="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none">
                    <option>Third Reviewer Resolution</option>
                    <option>Consensus Discussion</option>
                    <option>Variable-specific Rules</option>
                    <option>Senior Researcher Decision</option>
                  </select>
                  <p className="text-xs text-gray-500 mt-1">
                    Default method for resolving coding conflicts
                  </p>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Default Conflict Resolver
                  </label>
                  <select className="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none">
                    <option>Dr. Michael Brown</option>
                    <option>None (Assign Manually)</option>
                  </select>
                  <p className="text-xs text-gray-500 mt-1">
                    Third reviewer who resolves conflicts by default
                  </p>
                </div>
                
                <div className="flex items-center">
                  <input 
                    type="checkbox" 
                    id="auto-resolve" 
                    className="mr-2"
                    checked
                  />
                  <label htmlFor="auto-resolve" className="text-sm text-gray-700">
                    Automatically assign conflicts to resolver
                  </label>
                </div>
              </div>
            </div>
          </div>
          
          <div className="mt-6 pt-6 border-t">
            <h3 className="font-medium mb-3">Variable-Specific Settings</h3>
            <p className="text-sm text-gray-600 mb-4">
              Configure how agreement is calculated for specific variable types
            </p>
            
            <div className="bg-gray-50 rounded-lg p-4 mb-4">
              <div className="flex justify-between items-center mb-3">
                <h4 className="font-medium">Categorical Variables</h4>
                <button className="text-indigo-600 hover:text-indigo-800 text-sm">
                  <Edit3 size={14} className="inline mr-1" /> Edit
                </button>
              </div>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-600">Agreement Method:</span>
                  <span>Exact Match</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Statistical Measure:</span>
                  <span>Cohen's Kappa</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Required Threshold:</span>
                  <span>0.7 (Substantial)</span>
                </div>
              </div>
            </div>
            
            <div className="bg-gray-50 rounded-lg p-4 mb-4">
              <div className="flex justify-between items-center mb-3">
                <h4 className="font-medium">Continuous Variables</h4>
                <button className="text-indigo-600 hover:text-indigo-800 text-sm">
                  <Edit3 size={14} className="inline mr-1" /> Edit
                </button>
              </div>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-600">Agreement Method:</span>
                  <span>Within 5% Tolerance</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Statistical Measure:</span>
                  <span>Intraclass Correlation (ICC)</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Required Threshold:</span>
                  <span>0.8 (Excellent)</span>
                </div>
              </div>
            </div>
            
            <div className="bg-gray-50 rounded-lg p-4">
              <div className="flex justify-between items-center mb-3">
                <h4 className="font-medium">Text Fields</h4>
                <button className="text-indigo-600 hover:text-indigo-800 text-sm">
                  <Edit3 size={14} className="inline mr-1" /> Edit
                </button>
              </div>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-600">Agreement Method:</span>
                  <span>Manual Review</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Statistical Measure:</span>
                  <span>Percentage Agreement</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Required Threshold:</span>
                  <span>80%</span>
                </div>
              </div>
            </div>
          </div>
          
          <div className="mt-6 flex justify-end">
            <button className="px-4 py-2 border rounded-lg text-gray-700 hover:bg-gray-50 mr-2">
              Cancel
            </button>
            <button className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700">
              Save Settings
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default InterraterReliability;
