import React, { useState } from 'react';
import { 
  Download, Upload, X, Check, AlertTriangle, Filter, Trash2, 
  Search, RefreshCw, FileText, ChevronDown, Link, ExternalLink,
  Edit3, Copy, CheckCircle, RotateCw, Clock, HelpCircle
} from 'lucide-react';

const PaperProcessing = () => {
  const [activeTab, setActiveTab] = useState('cleanup');
  const [selectedPapers, setSelectedPapers] = useState([]);
  const [showUploadModal, setShowUploadModal] = useState(false);
  
  const selectAllPapers = () => {
    // Logic to select all papers
  };
  
  const deselectAllPapers = () => {
    setSelectedPapers([]);
  };
  
  const removeDuplicates = () => {
    // Logic to remove duplicate papers
  };
  
  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold">Process Papers</h1>
          <p className="text-gray-600">Clean up your paper collection and retrieve full texts</p>
        </div>
        <div className="flex">
          <button className="px-4 py-2 border bg-white text-gray-700 hover:bg-gray-50 rounded-lg mr-2 flex items-center">
            <Filter size={16} className="mr-1" /> Filter
          </button>
          <button 
            className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 flex items-center"
            onClick={() => {}}
          >
            <CheckCircle size={16} className="mr-1" /> Continue to Coding
          </button>
        </div>
      </div>
      
      <div className="bg-white rounded-lg shadow-lg mb-6">
        <div className="flex border-b">
          <TabButton 
            label="Clean up Collection" 
            icon={<FileText size={18} />}
            active={activeTab === 'cleanup'} 
            onClick={() => setActiveTab('cleanup')}
          />
          <TabButton 
            label="Retrieve Full Texts" 
            icon={<Download size={18} />}
            active={activeTab === 'retrieve'} 
            onClick={() => setActiveTab('retrieve')}
          />
        </div>
        
        {activeTab === 'cleanup' && (
          <CleanupTab 
            selectedPapers={selectedPapers} 
            setSelectedPapers={setSelectedPapers}
            selectAllPapers={selectAllPapers}
            deselectAllPapers={deselectAllPapers}
            removeDuplicates={removeDuplicates}
          />
        )}
        {activeTab === 'retrieve' && (
          <RetrieveTab 
            setShowUploadModal={setShowUploadModal}
          />
        )}
      </div>
      
      {showUploadModal && <PdfUploadModal onClose={() => setShowUploadModal(false)} />}
    </div>
  );
};

const TabButton = ({ label, icon, active, onClick }) => {
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
    </button>
  );
};

const CleanupTab = ({ 
  selectedPapers, 
  setSelectedPapers,
  selectAllPapers,
  deselectAllPapers,
  removeDuplicates
}) => {
  const [activeFilter, setActiveFilter] = useState('all');
  
  const handleSelectPaper = (paperId) => {
    if (selectedPapers.includes(paperId)) {
      setSelectedPapers(selectedPapers.filter(id => id !== paperId));
    } else {
      setSelectedPapers([...selectedPapers, paperId]);
    }
  };
  
  return (
    <div className="p-6">
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6 flex">
        <div className="text-blue-500 mr-3 mt-0.5">
          <HelpCircle size={20} />
        </div>
        <div>
          <h3 className="font-medium text-blue-800 mb-1">Paper Collection Clean-up</h3>
          <p className="text-blue-700 text-sm">
            Review your imported papers to remove duplicates, irrelevant papers, or papers with incomplete metadata.
            Use the duplicate detection tool to automatically identify potential duplicates.
          </p>
        </div>
      </div>
      
      <div className="flex justify-between items-center mb-4">
        <div className="flex">
          <div className="relative mr-2">
            <Search size={18} className="absolute left-3 top-2.5 text-gray-400" />
            <input 
              type="text" 
              placeholder="Search papers..."
              className="pl-10 pr-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none w-64"
            />
          </div>
          <select className="border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none">
            <option>Sort by Title</option>
            <option>Sort by Author</option>
            <option>Sort by Year</option>
            <option>Sort by Journal</option>
          </select>
        </div>
        <div className="flex">
          <button 
            className="px-3 py-2 border rounded-lg text-gray-700 hover:bg-gray-50 mr-2 flex items-center text-sm"
            onClick={removeDuplicates}
          >
            <RotateCw size={14} className="mr-1" /> Find Duplicates
          </button>
          <button className="px-3 py-2 border rounded-lg text-gray-700 hover:bg-gray-50 mr-2 flex items-center text-sm">
            <Trash2 size={14} className="mr-1" /> Remove Selected
          </button>
          <button className="px-3 py-2 border rounded-lg text-gray-700 hover:bg-gray-50 flex items-center text-sm">
            <Download size={14} className="mr-1" /> Export List
          </button>
        </div>
      </div>
      
      <div className="flex mb-4">
        <div 
          className={`px-4 py-2 rounded-lg mr-2 text-sm cursor-pointer ${
            activeFilter === 'all' ? 'bg-indigo-100 text-indigo-800' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }`}
          onClick={() => setActiveFilter('all')}
        >
          All Papers (42)
        </div>
        <div 
          className={`px-4 py-2 rounded-lg mr-2 text-sm cursor-pointer ${
            activeFilter === 'duplicates' ? 'bg-indigo-100 text-indigo-800' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }`}
          onClick={() => setActiveFilter('duplicates')}
        >
          Potential Duplicates (5)
        </div>
        <div 
          className={`px-4 py-2 rounded-lg mr-2 text-sm cursor-pointer ${
            activeFilter === 'incomplete' ? 'bg-indigo-100 text-indigo-800' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }`}
          onClick={() => setActiveFilter('incomplete')}
        >
          Incomplete Metadata (8)
        </div>
        <div 
          className={`px-4 py-2 rounded-lg text-sm cursor-pointer ${
            activeFilter === 'flagged' ? 'bg-indigo-100 text-indigo-800' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }`}
          onClick={() => setActiveFilter('flagged')}
        >
          Flagged (3)
        </div>
      </div>
      
      <div className="bg-white border rounded-lg overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th scope="col" className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                <input 
                  type="checkbox" 
                  className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                  onChange={(e) => e.target.checked ? selectAllPapers() : deselectAllPapers()}
                />
              </th>
              <th scope="col" className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Title & Authors
              </th>
              <th scope="col" className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Journal & Year
              </th>
              <th scope="col" className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                PDF Status
              </th>
              <th scope="col" className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Status
              </th>
              <th scope="col" className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            <PaperRow 
              id="paper1"
              title="Effectiveness of Cognitive Behavioral Therapy for Anxiety Disorders: A Meta-Analytic Review"
              authors="Smith J, Johnson A, Williams B"
              journal="Journal of Clinical Psychology"
              year="2023"
              pdfStatus="available"
              status="clean"
              selected={selectedPapers.includes('paper1')}
              onSelect={() => handleSelectPaper('paper1')}
            />
            
            <PaperRow 
              id="paper2"
              title="A Systematic Review and Meta-analysis of Remote Work Productivity During the COVID-19 Pandemic"
              authors="Garcia M, Lee S, Thompson P"
              journal="Journal of Organizational Behavior"
              year="2022"
              pdfStatus="missing"
              status="clean"
              selected={selectedPapers.includes('paper2')}
              onSelect={() => handleSelectPaper('paper2')}
            />
            
            <PaperRow 
              id="paper3"
              title="Comparative Efficacy and Safety of COVID-19 Vaccines: A Systematic Review and Network Meta-analysis"
              authors="Chen H, Patel R, Nguyen T"
              journal="The Lancet Infectious Diseases"
              year="2022"
              pdfStatus="available"
              status="clean"
              selected={selectedPapers.includes('paper3')}
              onSelect={() => handleSelectPaper('paper3')}
            />
            
            <PaperRow 
              id="paper4"
              title="Cognitive Behavioral Therapy for Anxiety: A Comprehensive Meta-Analysis of Outcomes"
              authors="Johnson A, Smith J, Davis R"
              journal="Clinical Psychology Review"
              year="2023"
              pdfStatus="available"
              status="duplicate"
              flagged="Potential duplicate of Smith et al. (2023)"
              selected={selectedPapers.includes('paper4')}
              onSelect={() => handleSelectPaper('paper4')}
            />
            
            <PaperRow 
              id="paper5"
              title="Effects of Mindfulness-Based Interventions on Anxiety Symptoms: A Meta-Analysis"
              authors="Wilson T, Garcia M"
              journal=""
              year="2021"
              pdfStatus="missing"
              status="incomplete"
              flagged="Missing journal information"
              selected={selectedPapers.includes('paper5')}
              onSelect={() => handleSelectPaper('paper5')}
            />
          </tbody>
        </table>
        
        <div className="px-6 py-4 border-t flex justify-between items-center bg-gray-50">
          <div className="text-sm text-gray-700">
            Showing 5 of 42 papers
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

const PaperRow = ({ 
  id, 
  title, 
  authors, 
  journal, 
  year, 
  pdfStatus, 
  status, 
  flagged,
  selected,
  onSelect 
}) => {
  const getPdfStatusDisplay = (status) => {
    switch(status) {
      case 'available':
        return (
          <div className="flex items-center text-green-600">
            <CheckCircle size={16} className="mr-1" /> Available
          </div>
        );
      case 'missing':
        return (
          <div className="flex items-center text-orange-500">
            <AlertTriangle size={16} className="mr-1" /> Missing
          </div>
        );
      case 'pending':
        return (
          <div className="flex items-center text-blue-500">
            <Clock size={16} className="mr-1" /> Pending
          </div>
        );
      default:
        return null;
    }
  };
  
  const getStatusDisplay = (status, flagged) => {
    if (flagged) {
      return (
        <div className="flex items-center text-yellow-600" title={flagged}>
          <AlertTriangle size={16} className="mr-1" /> {status.charAt(0).toUpperCase() + status.slice(1)}
        </div>
      );
    }
    
    switch(status) {
      case 'clean':
        return (
          <div className="flex items-center text-green-600">
            <Check size={16} className="mr-1" /> Clean
          </div>
        );
      case 'duplicate':
        return (
          <div className="flex items-center text-yellow-600">
            <Copy size={16} className="mr-1" /> Duplicate
          </div>
        );
      case 'incomplete':
        return (
          <div className="flex items-center text-orange-500">
            <AlertTriangle size={16} className="mr-1" /> Incomplete
          </div>
        );
      default:
        return null;
    }
  };
  
  return (
    <tr className={`${selected ? 'bg-indigo-50' : 'hover:bg-gray-50'}`}>
      <td className="px-4 py-4 whitespace-nowrap">
        <input 
          type="checkbox" 
          className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
          checked={selected}
          onChange={onSelect}
        />
      </td>
      <td className="px-4 py-4">
        <div className="font-medium text-gray-900">{title}</div>
        <div className="text-sm text-gray-500">{authors}</div>
      </td>
      <td className="px-4 py-4 whitespace-nowrap">
        <div className="text-sm text-gray-900">{journal || "—"}</div>
        <div className="text-sm text-gray-500">{year}</div>
      </td>
      <td className="px-4 py-4 whitespace-nowrap text-sm">
        {getPdfStatusDisplay(pdfStatus)}
      </td>
      <td className="px-4 py-4 whitespace-nowrap text-sm">
        {getStatusDisplay(status, flagged)}
      </td>
      <td className="px-4 py-4 whitespace-nowrap text-right text-sm font-medium">
        <button className="text-indigo-600 hover:text-indigo-900 mr-3">
          Edit
        </button>
        <button className="text-red-600 hover:text-red-900">
          Remove
        </button>
      </td>
    </tr>
  );
};

const RetrieveTab = ({ setShowUploadModal }) => {
  const [activeFilter, setActiveFilter] = useState('missing');
  
  return (
    <div className="p-6">
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6 flex">
        <div className="text-blue-500 mr-3 mt-0.5">
          <HelpCircle size={20} />
        </div>
        <div>
          <h3 className="font-medium text-blue-800 mb-1">Retrieving Full Text PDFs</h3>
          <p className="text-blue-700 text-sm">
            Retrieve full text PDFs for your papers using automatic retrieval APIs, manual upload, or by providing links.
            PDFs are required for the data extraction and coding phase.
          </p>
        </div>
      </div>
      
      <div className="grid grid-cols-3 gap-6 mb-6">
        <div className="bg-white rounded-lg border p-6 text-center hover:shadow-md transition-shadow">
          <div className="inline-flex items-center justify-center h-12 w-12 rounded-full bg-indigo-100 text-indigo-600 mb-4">
            <Download size={24} />
          </div>
          <h3 className="text-lg font-medium mb-2">Automatic Retrieval</h3>
          <p className="text-gray-600 text-sm mb-4">
            Try to automatically retrieve PDFs from open access sources and databases
          </p>
          <button className="w-full px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700">
            Retrieve All Missing PDFs
          </button>
        </div>
        
        <div className="bg-white rounded-lg border p-6 text-center hover:shadow-md transition-shadow">
          <div className="inline-flex items-center justify-center h-12 w-12 rounded-full bg-indigo-100 text-indigo-600 mb-4">
            <Upload size={24} />
          </div>
          <h3 className="text-lg font-medium mb-2">Manual Upload</h3>
          <p className="text-gray-600 text-sm mb-4">
            Manually upload PDFs from your computer and match them to papers
          </p>
          <button 
            className="w-full px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
            onClick={() => setShowUploadModal(true)}
          >
            Upload PDFs
          </button>
        </div>
        
        <div className="bg-white rounded-lg border p-6 text-center hover:shadow-md transition-shadow">
          <div className="inline-flex items-center justify-center h-12 w-12 rounded-full bg-indigo-100 text-indigo-600 mb-4">
            <Link size={24} />
          </div>
          <h3 className="text-lg font-medium mb-2">Provide URLs</h3>
          <p className="text-gray-600 text-sm mb-4">
            Add direct URLs to PDFs or pages where PDFs can be found
          </p>
          <button className="w-full px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700">
            Add PDF URLs
          </button>
        </div>
      </div>
      
      <div className="flex mb-4">
        <div 
          className={`px-4 py-2 rounded-lg mr-2 text-sm cursor-pointer ${
            activeFilter === 'all' ? 'bg-indigo-100 text-indigo-800' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }`}
          onClick={() => setActiveFilter('all')}
        >
          All Papers (42)
        </div>
        <div 
          className={`px-4 py-2 rounded-lg mr-2 text-sm cursor-pointer ${
            activeFilter === 'missing' ? 'bg-indigo-100 text-indigo-800' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }`}
          onClick={() => setActiveFilter('missing')}
        >
          Missing PDFs (14)
        </div>
        <div 
          className={`px-4 py-2 rounded-lg mr-2 text-sm cursor-pointer ${
            activeFilter === 'available' ? 'bg-indigo-100 text-indigo-800' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }`}
          onClick={() => setActiveFilter('available')}
        >
          Available PDFs (28)
        </div>
      </div>
      
      <div className="bg-white border rounded-lg overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th scope="col" className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Title & Authors
              </th>
              <th scope="col" className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Source
              </th>
              <th scope="col" className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                PDF Status
              </th>
              <th scope="col" className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            <PdfRow 
              title="A Systematic Review and Meta-analysis of Remote Work Productivity"
              authors="Garcia M, Lee S, Thompson P"
              journal="Journal of Organizational Behavior"
              year="2022"
              source="—"
              status="missing"
            />
            
            <PdfRow 
              title="Effects of Mindfulness-Based Interventions on Anxiety Symptoms"
              authors="Wilson T, Garcia M"
              journal="Psychological Bulletin"
              year="2021"
              source="—"
              status="missing"
            />
            
            <PdfRow 
              title="Effectiveness of Cognitive Behavioral Therapy for Anxiety Disorders"
              authors="Smith J, Johnson A, Williams B"
              journal="Journal of Clinical Psychology"
              year="2023"
              source="PubMed Central"
              status="available"
            />
            
            <PdfRow 
              title="Comparative Efficacy and Safety of COVID-19 Vaccines"
              authors="Chen H, Patel R, Nguyen T"
              journal="The Lancet Infectious Diseases"
              year="2022"
              source="Manual Upload"
              status="available"
            />
            
            <PdfRow 
              title="Exercise Interventions for Mental Health: A Meta-Analysis"
              authors="Martinez K, Roberts J"
              journal="Sports Medicine"
              year="2022"
              source="—"
              status="pending"
            />
          </tbody>
        </table>
        
        <div className="px-6 py-4 border-t flex justify-between items-center bg-gray-50">
          <div className="text-sm text-gray-700">
            Showing 5 of 42 papers
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

const PdfRow = ({ 
  title, 
  authors, 
  journal, 
  year, 
  source, 
  status 
}) => {
  const getStatusDisplay = (status) => {
    switch(status) {
      case 'available':
        return (
          <div className="flex items-center text-green-600">
            <CheckCircle size={16} className="mr-1" /> Available
          </div>
        );
      case 'missing':
        return (
          <div className="flex items-center text-orange-500">
            <AlertTriangle size={16} className="mr-1" /> Missing
          </div>
        );
      case 'pending':
        return (
          <div className="flex items-center text-blue-500">
            <Clock size={16} className="mr-1" /> Retrieving...
          </div>
        );
      default:
        return null;
    }
  };
  
  return (
    <tr className="hover:bg-gray-50">
      <td className="px-4 py-4">
        <div className="font-medium text-gray-900">{title}</div>
        <div className="text-sm text-gray-500">{authors}</div>
        <div className="text-xs text-gray-400">{journal} ({year})</div>
      </td>
      <td className="px-4 py-4 whitespace-nowrap">
        <div className="text-sm text-gray-900">{source}</div>
      </td>
      <td className="px-4 py-4 whitespace-nowrap text-sm">
        {getStatusDisplay(status)}
      </td>
      <td className="px-4 py-4 whitespace-nowrap text-right text-sm font-medium">
        {status === 'missing' && (
          <>
            <button className="text-indigo-600 hover:text-indigo-900 mr-3">
              Retrieve
            </button>
            <button className="text-indigo-600 hover:text-indigo-900 mr-3">
              Upload
            </button>
            <button className="text-indigo-600 hover:text-indigo-900">
              Add URL
            </button>
          </>
        )}
        {status === 'available' && (
          <>
            <button className="text-indigo-600 hover:text-indigo-900 mr-3">
              View
            </button>
            <button className="text-indigo-600 hover:text-indigo-900">
              Replace
            </button>
          </>
        )}
        {status === 'pending' && (
          <button className="text-gray-600 hover:text-gray-900">
            Cancel
          </button>
        )}
      </td>
    </tr>
  );
};

const PdfUploadModal = ({ onClose }) => {
  const [activeTab, setActiveTab] = useState('upload');
  const [files, setFiles] = useState([]);
  
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-3xl max-h-[90vh] overflow-hidden flex flex-col">
        <div className="p-4 border-b flex justify-between items-center">
          <h3 className="font-medium text-lg">Upload and Match PDFs</h3>
          <button 
            className="text-gray-400 hover:text-gray-600"
            onClick={onClose}
          >
            <X size={18} />
          </button>
        </div>
        
        <div className="border-b">
          <div className="flex">
            <button 
              className={`py-3 px-4 font-medium ${activeTab === 'upload' ? 'text-indigo-600 border-b-2 border-indigo-600' : 'text-gray-500 hover:text-gray-700'}`}
              onClick={() => setActiveTab('upload')}
            >
              Upload PDFs
            </button>
            <button 
              className={`py-3 px-4 font-medium ${activeTab === 'match' ? 'text-indigo-600 border-b-2 border-indigo-600' : 'text-gray-500 hover:text-gray-700'}`}
              onClick={() => setActiveTab('match')}
            >
              Match to Papers
            </button>
          </div>
        </div>
        
        <div className="flex-1 overflow-y-auto p-6">
          {activeTab === 'upload' && (
            <div>
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center mb-6">
                <div className="mx-auto w-16 h-16 bg-indigo-100 rounded-full flex items-center justify-center mb-4">
                  <Upload size={32} className="text-indigo-600" />
                </div>
                <h3 className="text-lg font-medium mb-2">Drop PDF files here</h3>
                <p className="text-gray-500 mb-4">or click to browse your computer</p>
                <button className="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700">
                  Select Files
                </button>
                <p className="text-xs text-gray-500 mt-4">
                  Supported formats: PDF only. Maximum file size: 50MB.
                </p>
              </div>
              
              <div className="mb-4">
                <h4 className="font-medium mb-2">Uploaded Files (3)</h4>
                <div className="space-y-3">
                  <FileUploadItem 
                    name="Smith_et_al_2023.pdf" 
                    size="2.8 MB"
                    progress={100}
                    status="complete"
                  />
                  <FileUploadItem 
                    name="Chen_COVID_Vaccines_2022.pdf" 
                    size="4.2 MB"
                    progress={100}
                    status="complete"
                  />
                  <FileUploadItem 
                    name="Martinez_Exercise_2022.pdf" 
                    size="3.1 MB"
                    progress={45}
                    status="uploading"
                  />
                </div>
              </div>
              
              <div className="flex items-center border rounded-lg p-4 bg-indigo-50 text-indigo-800">
                <CheckCircle size={20} className="mr-2" />
                <span>2 files uploaded successfully. Continue to match these files with your papers.</span>
                <button 
                  className="ml-auto px-4 py-1 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 text-sm"
                  onClick={() => setActiveTab('match')}
                >
                  Continue
                </button>
              </div>
            </div>
          )}
          
          {activeTab === 'match' && (
            <div>
              <div className="mb-6">
                <h4 className="font-medium mb-2">Match PDFs to Papers</h4>
                <p className="text-gray-600 text-sm mb-4">
                  We'll try to automatically match PDFs to papers based on the filename and content.
                  You can manually adjust the matches if needed.
                </p>
                
                <button className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 flex items-center mr-2">
                  <RotateCw size={16} className="mr-1" /> Auto-Match PDFs
                </button>
              </div>
              
              <div className="space-y-4">
                <PdfMatchItem 
                  filename="Smith_et_al_2023.pdf"
                  filesize="2.8 MB"
                  matchStatus="matched"
                  matchedPaper="Effectiveness of Cognitive Behavioral Therapy for Anxiety Disorders"
                  confidence={95}
                />
                
                <PdfMatchItem 
                  filename="Chen_COVID_Vaccines_2022.pdf"
                  filesize="4.2 MB"
                  matchStatus="matched"
                  matchedPaper="Comparative Efficacy and Safety of COVID-19 Vaccines"
                  confidence={98}
                />
                
                <PdfMatchItem 
                  filename="Martinez_Exercise_2022.pdf"
                  filesize="3.1 MB"
                  matchStatus="unmatched"
                  suggestions={[
                    "Exercise Interventions for Mental Health: A Meta-Analysis",
                    "Physical Activity and Depression: A Meta-Analytic Review"
                  ]}
                />
              </div>
            </div>
          )}
        </div>
        
        <div className="p-4 border-t flex justify-end bg-gray-50">
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
            Save and Continue
          </button>
        </div>
      </div>
    </div>
  );
};

const FileUploadItem = ({ name, size, progress, status }) => {
  return (
    <div className="bg-white p-3 rounded border shadow-sm">
      <div className="flex justify-between items-center mb-2">
        <div className="font-medium flex items-center">
          <FileText size={16} className="text-gray-500 mr-2" />
          {name}
        </div>
        <div className="text-sm text-gray-500">{size}</div>
      </div>
      
      <div className="w-full bg-gray-200 rounded-full h-2 mb-1">
        <div 
          className={`h-2 rounded-full ${status === 'complete' ? 'bg-green-500' : 'bg-indigo-600'}`} 
          style={{ width: `${progress}%` }}
        ></div>
      </div>
      
      <div className="flex justify-between items-center">
        <div className="text-xs text-gray-500">
          {status === 'complete' ? 'Upload complete' : `Uploading... ${progress}%`}
        </div>
        {status === 'uploading' && (
          <button className="text-gray-400 hover:text-gray-600">
            <X size={16} />
          </button>
        )}
        {status === 'complete' && (
          <button className="text-red-500 hover:text-red-700 text-xs">
            Remove
          </button>
        )}
      </div>
    </div>
  );
};

const PdfMatchItem = ({ 
  filename, 
  filesize, 
  matchStatus, 
  matchedPaper, 
  confidence, 
  suggestions 
}) => {
  const [showSuggestions, setShowSuggestions] = useState(false);
  
  return (
    <div className={`border rounded-lg p-4 ${matchStatus === 'matched' ? 'bg-green-50 border-green-200' : 'bg-yellow-50 border-yellow-200'}`}>
      <div className="flex items-start">
        <div className="h-10 w-10 rounded-full bg-white border flex items-center justify-center mr-3">
          <FileText size={20} className="text-gray-500" />
        </div>
        
        <div className="flex-1">
          <div className="font-medium">{filename}</div>
          <div className="text-sm text-gray-500">{filesize}</div>
          
          {matchStatus === 'matched' && (
            <div className="mt-2">
              <div className="text-sm text-gray-700">Matched with:</div>
              <div className="flex items-center mt-1">
                <div className="flex-1">
                  <div className="font-medium text-green-800">{matchedPaper}</div>
                  <div className="text-xs text-green-600">Match confidence: {confidence}%</div>
                </div>
                <button className="text-indigo-600 hover:text-indigo-800 text-sm">
                  Change
                </button>
              </div>
            </div>
          )}
          
          {matchStatus === 'unmatched' && (
            <div className="mt-2">
              <div className="flex justify-between items-center">
                <div className="text-sm text-yellow-700">This PDF couldn't be automatically matched</div>
                <button 
                  className="text-indigo-600 hover:text-indigo-800 text-sm flex items-center"
                  onClick={() => setShowSuggestions(!showSuggestions)}
                >
                  View Suggestions
                  <ChevronDown size={14} className={`ml-1 transition-transform ${showSuggestions ? 'rotate-180' : ''}`} />
                </button>
              </div>
              
              {showSuggestions && (
                <div className="mt-2 space-y-2">
                  <div className="text-sm text-gray-700">Possible matches:</div>
                  {suggestions.map((suggestion, index) => (
                    <div key={index} className="flex items-center justify-between bg-white p-2 rounded border">
                      <div className="font-medium text-sm">{suggestion}</div>
                      <button className="text-indigo-600 hover:text-indigo-800 text-xs">
                        Select
                      </button>
                    </div>
                  ))}
                  <button className="mt-1 text-sm text-indigo-600 hover:text-indigo-800 flex items-center">
                    <Plus size={14} className="mr-1" /> Match to another paper
                  </button>
                </div>
              )}
              
              {!showSuggestions && (
                <div className="mt-2 flex">
                  <select className="flex-1 border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none mr-2">
                    <option>Select a paper to match...</option>
                    {suggestions.map((suggestion, index) => (
                      <option key={index}>{suggestion}</option>
                    ))}
                  </select>
                  <button className="px-3 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 text-sm">
                    Match
                  </button>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default PaperProcessing;
