import React, { useState } from 'react';
import { Search, Upload, PlusCircle, Filter, Download, Book, FileText, Grid, Settings, Trash2, Save, Edit3, Check, X } from 'lucide-react';

const MetaAnalysisTool = () => {
  const [activeView, setActiveView] = useState('dashboard');

  const renderView = () => {
    switch(activeView) {
      case 'dashboard':
        return <Dashboard setActiveView={setActiveView} />;
      case 'search':
        return <SearchView setActiveView={setActiveView} />;
      case 'viewer':
        return <PdfViewer setActiveView={setActiveView} />;
      case 'codingSheet':
        return <CodingSheetConfig setActiveView={setActiveView} />;
      case 'resultsTable':
        return <ResultsTable setActiveView={setActiveView} />;
      default:
        return <Dashboard setActiveView={setActiveView} />;
    }
  };

  return (
    <div className="flex h-screen bg-gray-100">
      <Sidebar activeView={activeView} setActiveView={setActiveView} />
      <div className="flex-1 overflow-auto">
        {renderView()}
      </div>
    </div>
  );
};

const Sidebar = ({ activeView, setActiveView }) => {
  return (
    <div className="w-64 bg-indigo-800 text-white p-4">
      <div className="text-xl font-bold mb-8 pl-2">MetaReview</div>
      <nav>
        <SidebarItem 
          icon={<Grid size={20} />} 
          text="Dashboard" 
          active={activeView === 'dashboard'} 
          onClick={() => setActiveView('dashboard')} 
        />
        <SidebarItem 
          icon={<Search size={20} />} 
          text="Find Papers" 
          active={activeView === 'search'} 
          onClick={() => setActiveView('search')} 
        />
        <SidebarItem 
          icon={<FileText size={20} />} 
          text="PDF Viewer" 
          active={activeView === 'viewer'} 
          onClick={() => setActiveView('viewer')} 
        />
        <SidebarItem 
          icon={<Edit3 size={20} />} 
          text="Coding Sheet" 
          active={activeView === 'codingSheet'} 
          onClick={() => setActiveView('codingSheet')} 
        />
        <SidebarItem 
          icon={<FileText size={20} />} 
          text="Results Table" 
          active={activeView === 'resultsTable'} 
          onClick={() => setActiveView('resultsTable')} 
        />
        <SidebarItem 
          icon={<Settings size={20} />} 
          text="Settings" 
          active={activeView === 'settings'} 
          onClick={() => {}} 
        />
      </nav>
      <div className="mt-auto pt-4 border-t border-indigo-700 mt-8">
        <div className="flex items-center p-2 rounded hover:bg-indigo-700 cursor-pointer">
          <div className="w-8 h-8 rounded-full bg-indigo-600 flex items-center justify-center mr-2">
            JD
          </div>
          <div>
            <div className="text-sm font-semibold">John Doe</div>
            <div className="text-xs text-indigo-300">Researcher</div>
          </div>
        </div>
      </div>
    </div>
  );
};

const SidebarItem = ({ icon, text, active, onClick }) => {
  return (
    <div 
      className={`flex items-center p-2 my-1 rounded cursor-pointer ${active ? 'bg-indigo-700' : 'hover:bg-indigo-700'}`}
      onClick={onClick}
    >
      <div className="mr-3">{icon}</div>
      <div>{text}</div>
    </div>
  );
};

const Dashboard = ({ setActiveView }) => {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Dashboard</h1>
      
      <div className="grid grid-cols-3 gap-6 mb-8">
        <StatCard title="Papers Collected" value="42" />
        <StatCard title="Papers Coded" value="28" />
        <StatCard title="Data Points Extracted" value="364" />
      </div>
      
      <div className="grid grid-cols-2 gap-6">
        <div className="bg-white rounded-lg p-6 shadow">
          <h2 className="text-lg font-semibold mb-4">Recent Projects</h2>
          <div className="space-y-3">
            <ProjectItem 
              title="Effectiveness of CBT for Anxiety Disorders" 
              papers="42" 
              lastUpdated="Today" 
              onClick={() => {}}
            />
            <ProjectItem 
              title="Meta-analysis of Remote Work Productivity" 
              papers="28" 
              lastUpdated="Yesterday" 
              onClick={() => {}}
            />
            <ProjectItem 
              title="Vaccine Efficacy Comparison" 
              papers="35" 
              lastUpdated="3 days ago" 
              onClick={() => {}}
            />
          </div>
          <button className="mt-4 flex items-center text-indigo-600 hover:text-indigo-800">
            <PlusCircle size={16} className="mr-1" /> New Project
          </button>
        </div>
        
        <div className="bg-white rounded-lg p-6 shadow">
          <h2 className="text-lg font-semibold mb-4">Quick Actions</h2>
          <div className="grid grid-cols-2 gap-4">
            <ActionCard 
              icon={<Search size={24} />} 
              title="Find Papers" 
              description="Search databases for relevant papers" 
              onClick={() => setActiveView('search')}
            />
            <ActionCard 
              icon={<Upload size={24} />} 
              title="Import PDFs" 
              description="Upload PDFs from your computer" 
              onClick={() => {}}
            />
            <ActionCard 
              icon={<Edit3 size={24} />} 
              title="Edit Coding Sheet" 
              description="Configure your data extraction variables" 
              onClick={() => setActiveView('codingSheet')}
            />
            <ActionCard 
              icon={<FileText size={24} />} 
              title="View Results" 
              description="See your extracted data" 
              onClick={() => setActiveView('resultsTable')}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

const StatCard = ({ title, value }) => {
  return (
    <div className="bg-white rounded-lg p-6 shadow">
      <div className="text-sm text-gray-500 mb-1">{title}</div>
      <div className="text-3xl font-bold">{value}</div>
    </div>
  );
};

const ProjectItem = ({ title, papers, lastUpdated, onClick }) => {
  return (
    <div className="border-b border-gray-100 pb-2 cursor-pointer hover:bg-gray-50 -mx-4 px-4" onClick={onClick}>
      <div className="font-medium text-gray-800">{title}</div>
      <div className="flex text-sm text-gray-500">
        <span>{papers} papers</span>
        <span className="mx-2">•</span>
        <span>Updated {lastUpdated}</span>
      </div>
    </div>
  );
};

const ActionCard = ({ icon, title, description, onClick }) => {
  return (
    <div 
      className="border rounded-lg p-4 hover:bg-gray-50 cursor-pointer transition-colors"
      onClick={onClick}
    >
      <div className="text-indigo-600 mb-2">{icon}</div>
      <div className="font-medium mb-1">{title}</div>
      <div className="text-sm text-gray-500">{description}</div>
    </div>
  );
};

const SearchView = ({ setActiveView }) => {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Find Papers</h1>
      
      <div className="bg-white rounded-lg p-6 shadow mb-6">
        <div className="flex mb-4">
          <div className="relative flex-1 mr-4">
            <Search size={20} className="absolute left-3 top-2.5 text-gray-400" />
            <input 
              type="text" 
              placeholder="Search by title, author, keywords..."
              className="w-full pl-10 pr-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            />
          </div>
          <button className="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700">
            Search
          </button>
        </div>
        
        <div className="flex flex-wrap -mx-2">
          <div className="px-2 w-1/4">
            <div className="mb-2 text-sm font-medium">Databases</div>
            <select className="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none">
              <option>All Databases</option>
              <option>PubMed</option>
              <option>Scopus</option>
              <option>Web of Science</option>
              <option>Google Scholar</option>
            </select>
          </div>
          <div className="px-2 w-1/4">
            <div className="mb-2 text-sm font-medium">Year Range</div>
            <div className="flex">
              <input 
                type="number" 
                placeholder="From"
                className="w-1/2 mr-2 border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
              />
              <input 
                type="number" 
                placeholder="To" 
                className="w-1/2 border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
              />
            </div>
          </div>
          <div className="px-2 w-1/4">
            <div className="mb-2 text-sm font-medium">Study Type</div>
            <select className="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none">
              <option>All Types</option>
              <option>RCT</option>
              <option>Cohort</option>
              <option>Case Control</option>
              <option>Meta-Analysis</option>
            </select>
          </div>
          <div className="px-2 w-1/4">
            <div className="mb-2 text-sm font-medium">Sort By</div>
            <select className="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none">
              <option>Relevance</option>
              <option>Most Recent</option>
              <option>Most Cited</option>
              <option>Title (A-Z)</option>
            </select>
          </div>
        </div>
        
        <div className="flex justify-end mt-4">
          <button className="flex items-center text-indigo-600 mr-4 hover:text-indigo-800">
            <Filter size={16} className="mr-1" /> More Filters
          </button>
          <button className="flex items-center text-gray-600 hover:text-gray-800">
            Clear All
          </button>
        </div>
      </div>
      
      <div className="bg-white rounded-lg shadow">
        <div className="p-4 border-b flex justify-between items-center">
          <div className="font-medium">28 Results</div>
          <div className="flex items-center text-sm">
            <span>Page 1 of 3</span>
            <button className="ml-4 px-2 py-1 border rounded-md hover:bg-gray-50">Previous</button>
            <button className="ml-2 px-2 py-1 border rounded-md hover:bg-gray-50">Next</button>
          </div>
        </div>
        
        <div>
          <SearchResultItem 
            title="Effectiveness of Cognitive Behavioral Therapy for Anxiety Disorders: A Meta-Analytic Review"
            authors="Smith J, Johnson A, Williams B"
            journal="Journal of Clinical Psychology"
            year="2023"
            abstract="This meta-analysis examined the efficacy of cognitive behavioral therapy (CBT) for anxiety disorders across 42 randomized controlled trials..."
            onClick={() => setActiveView('viewer')}
          />
          <SearchResultItem 
            title="A Systematic Review and Meta-analysis of Remote Work Productivity During the COVID-19 Pandemic"
            authors="Garcia M, Lee S, Thompson P"
            journal="Journal of Organizational Behavior"
            year="2022"
            abstract="This systematic review synthesized findings from 28 studies examining the impact of remote work arrangements on employee productivity..."
            onClick={() => {}}
          />
          <SearchResultItem 
            title="Comparative Efficacy and Safety of COVID-19 Vaccines: A Systematic Review and Network Meta-analysis"
            authors="Chen H, Patel R, Nguyen T"
            journal="The Lancet Infectious Diseases"
            year="2022"
            abstract="This network meta-analysis compared the efficacy and safety profiles of available COVID-19 vaccines based on data from 35 clinical trials..."
            onClick={() => {}}
          />
        </div>
      </div>
    </div>
  );
};

const SearchResultItem = ({ title, authors, journal, year, abstract, onClick }) => {
  return (
    <div className="p-4 border-b hover:bg-gray-50 cursor-pointer" onClick={onClick}>
      <div className="font-medium text-indigo-600 mb-1">{title}</div>
      <div className="text-sm text-gray-700 mb-1">{authors}</div>
      <div className="text-sm text-gray-500 mb-2">{journal} • {year}</div>
      <div className="text-sm text-gray-600">{abstract}</div>
      <div className="flex mt-3 text-sm">
        <button className="flex items-center text-indigo-600 mr-4 hover:text-indigo-800">
          <Download size={16} className="mr-1" /> Download PDF
        </button>
        <button className="flex items-center text-indigo-600 mr-4 hover:text-indigo-800">
          <PlusCircle size={16} className="mr-1" /> Add to Collection
        </button>
        <button className="flex items-center text-indigo-600 hover:text-indigo-800">
          <Book size={16} className="mr-1" /> View Details
        </button>
      </div>
    </div>
  );
};

const PdfViewer = ({ setActiveView }) => {
  const [showCodingPanel, setShowCodingPanel] = useState(true);
  
  return (
    <div className="flex h-full">
      <div className={`${showCodingPanel ? 'w-2/3' : 'w-full'} bg-gray-100 border-r flex flex-col h-full`}>
        <div className="p-4 bg-white border-b flex justify-between items-center">
          <div>
            <h2 className="font-medium">Effectiveness of Cognitive Behavioral Therapy for Anxiety Disorders</h2>
            <div className="text-sm text-gray-500">Smith J, et al. • Journal of Clinical Psychology • 2023</div>
          </div>
          <div className="flex">
            <button className="px-3 py-1 rounded border mr-2 hover:bg-gray-50">
              <Download size={16} />
            </button>
            <button 
              className="px-3 py-1 rounded border hover:bg-gray-50"
              onClick={() => setShowCodingPanel(!showCodingPanel)}
            >
              {showCodingPanel ? <X size={16} /> : <Edit3 size={16} />}
            </button>
          </div>
        </div>
        
        <div className="flex-1 p-6 overflow-auto">
          {/* This would be the PDF viewer */}
          <div className="bg-white rounded-lg shadow p-6">
            <div className="border-b pb-4 mb-4">
              <h1 className="text-xl font-bold mb-2">Effectiveness of Cognitive Behavioral Therapy for Anxiety Disorders: A Meta-Analytic Review</h1>
              <p className="text-sm text-gray-700 mb-4">Smith J, Johnson A, Williams B • Journal of Clinical Psychology • 2023</p>
              <p className="font-medium mb-1">Abstract</p>
              <p className="text-gray-700">
                This meta-analysis examined the efficacy of cognitive behavioral therapy (CBT) for anxiety disorders across 42 randomized controlled trials. Results indicated that CBT produced significant reductions in anxiety symptoms compared to control conditions (g = 0.82, 95% CI [0.71, 0.93], p &lt; .001). Treatment effects were maintained at follow-up assessments. Moderator analyses revealed that treatment format (individual vs. group) and treatment duration influenced outcomes. These findings provide robust evidence supporting CBT as a first-line treatment for anxiety disorders.
              </p>
            </div>
            
            <div className="mb-6">
              <h2 className="text-lg font-medium mb-3">1. Introduction</h2>
              <p className="mb-3">
                Anxiety disorders represent one of the most prevalent categories of mental health conditions worldwide, affecting approximately 275 million people globally (WHO, 2021). These disorders, including generalized anxiety disorder, social anxiety disorder, panic disorder, and specific phobias, are characterized by excessive fear, anxiety, and related behavioral disturbances that significantly impair functioning.
              </p>
              <p className="mb-3">
                Cognitive behavioral therapy (CBT) has emerged as one of the most extensively researched psychological interventions for anxiety disorders. CBT encompasses a range of techniques that target both the cognitive and behavioral aspects of anxiety, including cognitive restructuring, exposure therapy, relaxation training, and skills development.
              </p>
              <p>
                While numerous studies support the efficacy of CBT for anxiety disorders, there is considerable variability in reported effect sizes across trials. Previous meta-analyses have typically focused on specific anxiety disorders or limited aspects of treatment. A comprehensive synthesis of the literature examining CBT across anxiety disorders would provide valuable information for clinicians and researchers.
              </p>
            </div>
            
            <div>
              <h2 className="text-lg font-medium mb-3">2. Methods</h2>
              <h3 className="font-medium mb-2">2.1 Study Selection</h3>
              <p className="mb-3">
                We conducted a systematic search of electronic databases including PubMed, PsycINFO, and CENTRAL from inception through December 2022. Search terms included combinations of "cognitive behavioral therapy," "cognitive therapy," "behavioral therapy," "anxiety disorders," and specific anxiety disorder diagnoses.
              </p>
              <h3 className="font-medium mb-2">2.2 Inclusion Criteria</h3>
              <p className="mb-3">
                Studies were included if they: (1) were randomized controlled trials; (2) included adult participants with a primary diagnosis of an anxiety disorder; (3) compared CBT to a control condition (waitlist, treatment as usual, or psychological placebo); (4) reported outcomes using validated measures of anxiety symptoms; and (5) provided sufficient data to calculate effect sizes.
              </p>
              <h3 className="font-medium mb-2">2.3 Data Extraction</h3>
              <p>
                Two independent reviewers extracted data using a standardized form. Extracted information included sample characteristics, intervention details (format, duration, components), outcome measures, and statistical data necessary for effect size calculation.
              </p>
            </div>
          </div>
        </div>
      </div>
      
      {showCodingPanel && (
        <div className="w-1/3 bg-white flex flex-col h-full">
          <div className="p-4 border-b">
            <h2 className="font-medium mb-2">Coding Sheet</h2>
            <p className="text-sm text-gray-500">Extract data from the paper using the form below</p>
          </div>
          
          <div className="flex-1 p-4 overflow-auto">
            <div className="mb-6">
              <h3 className="font-medium mb-3">Study Information</h3>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Authors
                </label>
                <input 
                  type="text" 
                  className="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
                  value="Smith J, Johnson A, Williams B"
                />
              </div>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Publication Year
                </label>
                <input 
                  type="text" 
                  className="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
                  value="2023"
                />
              </div>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Journal
                </label>
                <input 
                  type="text" 
                  className="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
                  value="Journal of Clinical Psychology"
                />
              </div>
            </div>
            
            <div className="mb-6">
              <h3 className="font-medium mb-3">Methodology</h3>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Study Design
                </label>
                <select className="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none">
                  <option>Meta-Analysis</option>
                  <option>RCT</option>
                  <option>Cohort Study</option>
                  <option>Case-Control</option>
                  <option>Systematic Review</option>
                </select>
              </div>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Number of Studies
                </label>
                <input 
                  type="number" 
                  className="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
                  value="42"
                />
              </div>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Total Sample Size
                </label>
                <input 
                  type="number" 
                  className="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
                />
              </div>
            </div>
            
            <div className="mb-6">
              <h3 className="font-medium mb-3">Study Findings</h3>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Overall Effect Size
                </label>
                <input 
                  type="text" 
                  className="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
                  placeholder="e.g., g = 0.82"
                  value="g = 0.82"
                />
              </div>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Confidence Interval
                </label>
                <input 
                  type="text" 
                  className="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
                  placeholder="e.g., 95% CI [0.71, 0.93]"
                  value="95% CI [0.71, 0.93]"
                />
              </div>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Statistical Significance
                </label>
                <input 
                  type="text" 
                  className="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
                  placeholder="e.g., p < .001"
                  value="p < .001"
                />
              </div>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Moderators Identified
                </label>
                <textarea 
                  className="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
                  rows="3"
                  value="Treatment format (individual vs. group), Treatment duration"
                />
              </div>
            </div>
            
            <div className="mb-6">
              <h3 className="font-medium mb-3">Quality Assessment</h3>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Risk of Bias
                </label>
                <select className="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none">
                  <option>Low</option>
                  <option>Moderate</option>
                  <option>High</option>
                  <option>Unclear</option>
                </select>
              </div>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  PRISMA Adherence
                </label>
                <select className="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none">
                  <option>Complete</option>
                  <option>Partial</option>
                  <option>Minimal</option>
                  <option>Not Reported</option>
                </select>
              </div>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Notes on Quality
                </label>
                <textarea 
                  className="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
                  rows="3"
                />
              </div>
            </div>
          </div>
          
          <div className="p-4 border-t flex justify-end">
            <button className="px-4 py-2 rounded-lg bg-gray-200 text-gray-800 mr-2 hover:bg-gray-300">
              Cancel
            </button>
            <button className="px-4 py-2 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 flex items-center">
              <Save size={16} className="mr-1" /> Save Data
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

const CodingSheetConfig = ({ setActiveView }) => {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Coding Sheet Configuration</h1>
      
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <div className="flex justify-between items-center mb-4">
          <div>
            <h2 className="font-medium">Basic Information</h2>
            <p className="text-sm text-gray-500">Configure fields for study identification and basic metadata</p>
          </div>
        </div>
        
        <div className="space-y-4">
          <div className="flex items-center p-3 border rounded-lg">
            <div className="flex-1">
              <div className="font-medium">Authors</div>
              <div className="text-sm text-gray-500">Text field for paper authors</div>
            </div>
            <div className="flex">
              <button className="p-1 text-gray-400 hover:text-gray-600 mr-1">
                <Edit3 size={16} />
              </button>
              <button className="p-1 text-gray-400 hover:text-red-600">
                <Trash2 size={16} />
              </button>
            </div>
          </div>
          
          <div className="flex items-center p-3 border rounded-lg">
            <div className="flex-1">
              <div className="font-medium">Publication Year</div>
              <div className="text-sm text-gray-500">Numeric field for publication year</div>
            </div>
            <div className="flex">
              <button className="p-1 text-gray-400 hover:text-gray-600 mr-1">
                <Edit3 size={16} />
              </button>
              <button className="p-1 text-gray-400 hover:text-red-600">
                <Trash2 size={16} />
              </button>
            </div>
          </div>
          
          <div className="flex items-center p-3 border rounded-lg">
            <div className="flex-1">
              <div className="font-medium">Journal</div>
              <div className="text-sm text-gray-500">Text field for journal name</div>
            </div>
            <div className="flex">
              <button className="p-1 text-gray-400 hover:text-gray-600 mr-1">
                <Edit3 size={16} />
              </button>
              <button className="p-1 text-gray-400 hover:text-red-600">
                <Trash2 size={16} />
              </button>
            </div>
          </div>
          
          <button className="flex items-center text-indigo-600 hover:text-indigo-800 mt-2">
            <PlusCircle size={16} className="mr-1" /> Add Field
          </button>
        </div>
      </div>
      
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <div className="flex justify-between items-center mb-4">
          <div>
            <h2 className="font-medium">Methodology Fields</h2>
            <p className="text-sm text-gray-500">Configure fields for methodological information</p>
          </div>
        </div>
        
        <div className="space-y-4">
          <div className="flex items-center p-3 border rounded-lg">
            <div className="flex-1">
              <div className="font-medium">Study Design</div>
              <div className="text-sm text-gray-500">Dropdown with study design options</div>
            </div>
            <div className="flex">
              <button className="p-1 text-gray-400 hover:text-gray-600 mr-1">
                <Edit3 size={16} />
              </button>
              <button className="p-1 text-gray-400 hover:text-red-600">
                <Trash2 size={16} />
              </button>
            </div>
          </div>
          
          <div className="flex items-center p-3 border rounded-lg">
            <div className="flex-1">
              <div className="font-medium">Number of Studies</div>
              <div className="text-sm text-gray-500">Numeric field for number of included studies</div>
            </div>
            <div className="flex">
              <button className="p-1 text-gray-400 hover:text-gray-600 mr-1">
                <Edit3 size={16} />
              </button>
              <button className="p-1 text-gray-400 hover:text-red-600">
                <Trash2 size={16} />
              </button>
            </div>
          </div>
          
          <div className="flex items-center p-3 border rounded-lg">
            <div className="flex-1">
              <div className="font-medium">Total Sample Size</div>
              <div className="text-sm text-gray-500">Numeric field for total participants</div>
            </div>
            <div className="flex">
              <button className="p-1 text-gray-400 hover:text-gray-600 mr-1">
                <Edit3 size={16} />
              </button>
              <button className="p-1 text-gray-400 hover:text-red-600">
                <Trash2 size={16} />
              </button>
            </div>
          </div>
          
          <button className="flex items-center text-indigo-600 hover:text-indigo-800 mt-2">
            <PlusCircle size={16} className="mr-1" /> Add Field
          </button>
        </div>
      </div>
      
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex justify-between items-center mb-4">
          <div>
            <h2 className="font-medium">Results Fields</h2>
            <p className="text-sm text-gray-500">Configure fields for study findings and results</p>
          </div>
        </div>
        
        <div className="space-y-4">
          <div className="flex items-center p-3 border rounded-lg">
            <div className="flex-1">
              <div className="font-medium">Overall Effect Size</div>
              <div className="text-sm text-gray-500">Text field for effect size measures</div>
            </div>
            <div className="flex">
              <button className="p-1 text-gray-400 hover:text-gray-600 mr-1">
                <Edit3 size={16} />
              </button>
              <button className="p-1 text-gray-400 hover:text-red-600">
                <Trash2 size={16} />
              </button>
            </div>
          </div>
          
          <div className="flex items-center p-3 border rounded-lg">
            <div className="flex-1">
              <div className="font-medium">Confidence Interval</div>
              <div className="text-sm text-gray-500">Text field for confidence intervals</div>
            </div>
            <div className="flex">
              <button className="p-1 text-gray-400 hover:text-gray-600 mr-1">
                <Edit3 size={16} />
              </button>
              <button className="p-1 text-gray-400 hover:text-red-600">
                <Trash2 size={16} />
              </button>
            </div>
          </div>
          
          <div className="flex items-center p-3 border rounded-lg">
            <div className="flex-1">
              <div className="font-medium">Statistical Significance</div>
              <div className="text-sm text-gray-500">Text field for p-values</div>
            </div>
            <div className="flex">
              <button className="p-1 text-gray-400 hover:text-gray-600 mr-1">
                <Edit3 size={16} />
              </button>
              <button className="p-1 text-gray-400 hover:text-red-600">
                <Trash2 size={16} />
              </button>
            </div>
          </div>
          
          <div className="flex items-center p-3 border rounded-lg">
            <div className="flex-1">
              <div className="font-medium">Moderators Identified</div>
              <div className="text-sm text-gray-500">Text area for moderating variables</div>
            </div>
            <div className="flex">
              <button className="p-1 text-gray-400 hover:text-gray-600 mr-1">
                <Edit3 size={16} />
              </button>
              <button className="p-1 text-gray-400 hover:text-red-600">
                <Trash2 size={16} />
              </button>
            </div>
          </div>
          
          <button className="flex items-center text-indigo-600 hover:text-indigo-800 mt-2">
            <PlusCircle size={16} className="mr-1" /> Add Field
          </button>
        </div>
      </div>
      
      <div className="mt-6 flex justify-end">
        <button 
          className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
          onClick={() => setActiveView('viewer')}
        >
          Save Configuration
        </button>
      </div>
    </div>
  );
};

const ResultsTable = ({ setActiveView }) => {
  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Results Table</h1>
        <div className="flex">
          <button className="flex items-center px-3 py-2 rounded-lg border bg-white mr-2 hover:bg-gray-50">
            <Filter size={16} className="mr-1" /> Filter
          </button>
          <button className="flex items-center px-3 py-2 rounded-lg border bg-white hover:bg-gray-50">
            <Download size={16} className="mr-1" /> Export
          </button>
        </div>
      </div>
      
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="p-4 border-b">
          <div className="flex justify-between items-center">
            <div className="text-lg font-medium">Extracted Data</div>
            <div className="text-sm text-gray-500">28 Papers • 364 Data Points</div>
          </div>
        </div>
        
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Authors
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Year
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Journal
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Study Design
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  N Studies
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Effect Size
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  95% CI
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  p-value
                </th>
                <th scope="col" className="relative px-6 py-3">
                  <span className="sr-only">Edit</span>
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              <tr>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  Smith J, et al.
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  2023
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  J Clin Psychol
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  Meta-Analysis
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  42
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  g = 0.82
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  [0.71, 0.93]
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  &lt; .001
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <button className="text-indigo-600 hover:text-indigo-900">Edit</button>
                </td>
              </tr>
              <tr>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  Garcia M, et al.
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  2022
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  J Org Behav
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  Meta-Analysis
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  28
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  d = 0.35
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  [0.22, 0.48]
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  &lt; .01
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <button className="text-indigo-600 hover:text-indigo-900">Edit</button>
                </td>
              </tr>
              <tr>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  Chen H, et al.
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  2022
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  Lancet Infect Dis
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  Network Meta
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  35
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  RR = 0.76
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  [0.65, 0.89]
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  &lt; .001
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <button className="text-indigo-600 hover:text-indigo-900">Edit</button>
                </td>
              </tr>
              <tr>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  Kumar A, et al.
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  2021
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  JAMA Psychiatry
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  Meta-Analysis
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  18
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  SMD = 0.54
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  [0.39, 0.69]
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  &lt; .001
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <button className="text-indigo-600 hover:text-indigo-900">Edit</button>
                </td>
              </tr>
              <tr>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  Robinson T, et al.
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  2023
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  Psychol Med
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  Meta-Analysis
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  24
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  g = 0.67
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  [0.51, 0.83]
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  &lt; .01
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <button className="text-indigo-600 hover:text-indigo-900">Edit</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <div className="px-6 py-4 border-t flex justify-between items-center">
          <div className="text-sm text-gray-500">
            Showing 5 of 28 studies
          </div>
          <div className="flex">
            <button className="px-3 py-1 border rounded-md hover:bg-gray-50 mr-2">Previous</button>
            <button className="px-3 py-1 border rounded-md hover:bg-gray-50">Next</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MetaAnalysisTool;
