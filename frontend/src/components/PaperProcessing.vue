
<template>
  <div class="p-6 bg-gray-100 min-h-screen">
    <div class="flex justify-between items-center mb-6">
      <div>
        <h1 class="text-2xl font-bold">Process Papers</h1>
        <p class="text-gray-600">Clean up your paper collection and retrieve full texts</p>
      </div>
      <div class="flex">
        <button class="px-4 py-2 border bg-white text-gray-700 hover:bg-gray-50 rounded-lg mr-2 flex items-center"
        @click="toggleFilters">
          <Filter class="mr-1" size="16" /> Filter
        </button>
        <button class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 flex items-center"
          @click="goToCoding">
          <CheckCircle class="mr-1" size="16" /> Continue to Coding
        </button>
      </div>
    </div>
    
    <div class="bg-white rounded-lg shadow-lg mb-6">
      <div class="flex border-b">
        <TabButton 
          label="Clean up Collection" 
          :icon="'file-text'"
          :active="activeTab === 'cleanup'" 
          @click="activeTab = 'cleanup'"
        />
        <TabButton 
          label="Retrieve Full Texts" 
          :icon="'download'"
          :active="activeTab === 'retrieve'" 
          @click="activeTab = 'retrieve'"
        />
      </div>
      
      <div v-if="activeTab === 'cleanup'" class="p-6">
        <div class="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6 flex">
          <div class="text-blue-500 mr-3 mt-0.5">
            <HelpCircle size="24" />
          </div>
          <div>
            <h3 class="font-medium text-blue-800 mb-1">Paper Collection Clean-up</h3>
            <p class="text-blue-700 text-sm">
              Review your imported papers to remove duplicates, irrelevant papers, or papers with incomplete metadata.
              Use the duplicate detection tool to automatically identify potential duplicates.
            </p>
          </div>
        </div>
        
        <div class="flex justify-between items-center mb-4">
          <div class="flex">
            <div class="relative mr-2">
              <Search class="absolute left-3 top-2.5 text-gray-400" size="18" />
              <input 
                v-model="searchQuery"
                type="text" 
                placeholder="Search papers..."
                class="pl-10 pr-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none w-64"
                @keyup.enter="searchPapers"
              />
            </div>
            <select 
              v-model="sortBy"
              class="border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
              @change="fetchPapers"
            >
              <option value="title">Sort by Title</option>
              <option value="authors">Sort by Author</option>
              <option value="year">Sort by Year</option>
              <option value="journal">Sort by Journal</option>
            </select>
          </div>
          <div class="flex">
            <button 
              class="px-3 py-2 border rounded-lg text-gray-700 hover:bg-gray-50 mr-2 flex items-center text-sm"
              @click="findDuplicates"
              :disabled="isLoading"
            >
              <RefreshCw class="mr-1" size="16" v-if="isLoading" /> 
              <RotateCw class="mr-1" size="16" v-else /> 
              Find Duplicates
            </button>
            <button 
              class="px-3 py-2 border rounded-lg text-gray-700 hover:bg-gray-50 mr-2 flex items-center text-sm"
              @click="removeSelectedPapers"
              :disabled="selectedPapers.length === 0"
            >
              <Trash2 class="mr-1" size="16" /> Remove Selected
            </button>
            <button 
              class="px-3 py-2 border rounded-lg text-gray-700 hover:bg-gray-50 flex items-center text-sm"
              @click="exportPaperList"
            >
              <Download class="mr-1" size="16" /> Export List
            </button>
          </div>
        </div>
        
        <div class="flex mb-4">
          <div 
            class="px-4 py-2 rounded-lg mr-2 text-sm cursor-pointer"
            :class="filterType === 'all' ? 'bg-indigo-100 text-indigo-800' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'"
            @click="setFilterType('all')"
          >
            All Papers ({{ totalPapers }})
          </div>
          <div 
            class="px-4 py-2 rounded-lg mr-2 text-sm cursor-pointer"
            :class="filterType === 'duplicates' ? 'bg-indigo-100 text-indigo-800' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'"
            @click="setFilterType('duplicates')"
          >
            Potential Duplicates ({{ duplicateCount }})
          </div>
          <div 
            class="px-4 py-2 rounded-lg mr-2 text-sm cursor-pointer"
            :class="filterType === 'incomplete' ? 'bg-indigo-100 text-indigo-800' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'"
            @click="setFilterType('incomplete')"
          >
            Incomplete Metadata ({{ incompleteCount }})
          </div>
        </div>
        
        <div v-if="isLoading" class="text-center py-12">
          <div class="spinner mb-4"></div>
          <p class="text-gray-500">Loading papers...</p>
        </div>
        
        <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 p-4 rounded-lg mb-6">
          <h3 class="font-medium mb-1">Error loading papers</h3>
          <p>{{ error }}</p>
        </div>
        
        <div v-else-if="papers.length === 0" class="text-center py-12">
          <FolderOpen class="text-gray-400 mx-auto mb-4" size="48" />
          <h3 class="text-xl font-medium mb-2">No Papers Found</h3>
          <p class="text-gray-600 mb-4">Try adjusting your filters or search terms.</p>
        </div>
        
        <div v-else class="bg-white border rounded-lg overflow-hidden">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  <input 
                    type="checkbox" 
                    class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                    :checked="allSelected"
                    @change="toggleSelectAll"
                  />
                </th>
                <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Title & Authors
                </th>
                <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Journal & Year
                </th>
                <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  PDF Status
                </th>
                <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th scope="col" class="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="paper in papers" :key="paper.id" :class="isSelected(paper.id) ? 'bg-indigo-50' : 'hover:bg-gray-50'">
                <td class="px-4 py-4 whitespace-nowrap">
                  <input 
                    type="checkbox" 
                    class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                    :checked="isSelected(paper.id)"
                    @change="toggleSelection(paper.id)"
                  />
                </td>
                <td class="px-4 py-4">
                  <div class="font-medium text-gray-900">{{ paper.title }}</div>
                  <div class="text-sm text-gray-500">{{ formatAuthors(paper.authors) }}</div>
                </td>
                <td class="px-4 py-4 whitespace-nowrap">
                  <div class="text-sm text-gray-900">{{ paper.journal || "—" }}</div>
                  <div class="text-sm text-gray-500">{{ paper.year || "Unknown Year" }}</div>
                </td>
                <td class="px-4 py-4 whitespace-nowrap text-sm">
                  <div v-if="paper.pdfStatus === 'available'" class="flex items-center text-green-600">
                    <CheckCircle class="mr-1" size="16" /> Available
                  </div>
                  <div v-else-if="paper.pdfStatus === 'missing'" class="flex items-center text-orange-500">
                    <AlertTriangle class="mr-1" size="16" /> Missing
                  </div>
                  <div v-else class="flex items-center text-blue-500">
                    <Clock class="mr-1" size="16" /> Pending
                  </div>
                </td>
                <td class="px-4 py-4 whitespace-nowrap text-sm">
                  <div v-if="paper.flagged" class="flex items-center text-yellow-600" :title="paper.flagged">
                    <AlertTriangle class="mr-1" size="16" /> {{ paper.status.charAt(0).toUpperCase() + paper.status.slice(1) }}
                  </div>
                  <div v-else-if="paper.status === 'clean'" class="flex items-center text-green-600">
                    <Check class="mr-1" size="16" /> Clean
                  </div>
                  <div v-else-if="paper.status === 'duplicate'" class="flex items-center text-yellow-600">
                    <Copy class="mr-1" size="16" /> Duplicate
                  </div>
                  <div v-else-if="paper.status === 'incomplete'" class="flex items-center text-orange-500">
                    <AlertTriangle class="mr-1" size="16" /> Incomplete
                  </div>
                </td>
                <td class="px-4 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <button class="text-indigo-600 hover:text-indigo-900 mr-3" @click="editPaper(paper)">
                    Edit
                  </button>
                  <button class="text-red-600 hover:text-red-900" @click="confirmRemove(paper)">
                    Remove
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
          
          <div class="px-6 py-4 border-t flex justify-between items-center bg-gray-50">
            <div class="text-sm text-gray-700">
              Showing {{ papers.length }} of {{ totalPapers }} papers
            </div>
            <div class="flex">
              <button 
                class="px-3 py-1 border rounded-md hover:bg-gray-100 mr-2"
                :disabled="currentPage === 1"
                @click="prevPage"
              >Previous</button>
              <button 
                class="px-3 py-1 border rounded-md hover:bg-gray-100"
                :disabled="currentPage === totalPages"
                @click="nextPage"
              >Next</button>
            </div>
          </div>
        </div>
      </div>
      
      <div v-if="activeTab === 'retrieve'" class="p-6">
        <div class="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6 flex">
          <div class="text-blue-500 mr-3 mt-0.5">
            <HelpCircle size="24" />
          </div>
          <div>
            <h3 class="font-medium text-blue-800 mb-1">Retrieving Full Text PDFs</h3>
            <p class="text-blue-700 text-sm">
              Retrieve full text PDFs for your papers using automatic retrieval APIs, manual upload, or by providing links.
              PDFs are required for the data extraction and coding phase.
            </p>
          </div>
        </div>
        
        <div class="grid grid-cols-3 gap-6 mb-6">
          <div class="bg-white rounded-lg border p-6 text-center hover:shadow-md transition-shadow">
            <div class="inline-flex items-center justify-center h-12 w-12 rounded-full bg-indigo-100 text-indigo-600 mb-4">
              <Download size="24" />
            </div>
            <h3 class="text-lg font-medium mb-2">Automatic Retrieval</h3>
            <p class="text-gray-600 text-sm mb-4">
              Try to automatically retrieve PDFs from open access sources and databases
            </p>
            <button 
              class="w-full px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
              @click="retrieveAllMissingPDFs"
              :disabled="isRetrieving"
            >
              <span v-if="isRetrieving">
                <Loader2 class="mr-1 inline-block animate-spin" size="16" /> 
                Retrieving...
              </span>
              <span v-else>Retrieve All Missing PDFs</span>
            </button>
          </div>
          
          <div class="bg-white rounded-lg border p-6 text-center hover:shadow-md transition-shadow">
            <div class="inline-flex items-center justify-center h-12 w-12 rounded-full bg-indigo-100 text-indigo-600 mb-4">
              <UploadCloud size="24" />
            </div>
            <h3 class="text-lg font-medium mb-2">Manual Upload</h3>
            <p class="text-gray-600 text-sm mb-4">
              Manually upload PDFs from your computer and match them to papers
            </p>
            <button 
              class="w-full px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
              @click="showUploadModal = true"
            >
              Upload PDFs
            </button>
          </div>
          
          <div class="bg-white rounded-lg border p-6 text-center hover:shadow-md transition-shadow">
            <div class="inline-flex items-center justify-center h-12 w-12 rounded-full bg-indigo-100 text-indigo-600 mb-4">
              <Link size="24" />
            </div>
            <h3 class="text-lg font-medium mb-2">Provide URLs</h3>
            <p class="text-gray-600 text-sm mb-4">
              Add direct URLs to PDFs or pages where PDFs can be found
            </p>
            <button 
              class="w-full px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
              @click="showUrlModal = true"
            >
              Add PDF URLs
            </button>
          </div>
        </div>
        
        <div class="flex mb-4">
          <div 
            class="px-4 py-2 rounded-lg mr-2 text-sm cursor-pointer"
            :class="pdfFilterType === 'all' ? 'bg-indigo-100 text-indigo-800' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'"
            @click="setPdfFilterType('all')"
          >
            All Papers ({{ totalPapers }})
          </div>
          <div 
            class="px-4 py-2 rounded-lg mr-2 text-sm cursor-pointer"
            :class="pdfFilterType === 'missing' ? 'bg-indigo-100 text-indigo-800' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'"
            @click="setPdfFilterType('missing')"
          >
            Missing PDFs ({{ missingPdfCount }})
          </div>
          <div 
            class="px-4 py-2 rounded-lg mr-2 text-sm cursor-pointer"
            :class="pdfFilterType === 'available' ? 'bg-indigo-100 text-indigo-800' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'"
            @click="setPdfFilterType('available')"
          >
            Available PDFs ({{ availablePdfCount }})
          </div>
        </div>
        
        <div v-if="isLoading" class="text-center py-12">
          <div class="spinner mb-4"></div>
          <p class="text-gray-500">Loading papers...</p>
        </div>
        
        <div v-else-if="papers.length === 0" class="text-center py-12">
          <FolderOpen class="text-gray-400 mx-auto mb-4" size="48" />
          <h3 class="text-xl font-medium mb-2">No Papers Found</h3>
          <p class="text-gray-600 mb-4">Try adjusting your filters or search terms.</p>
        </div>
        
        <div v-else class="bg-white border rounded-lg overflow-hidden">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Title & Authors
                </th>
                <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Source
                </th>
                <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  PDF Status
                </th>
                <th scope="col" class="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="paper in papers" :key="paper.id" class="hover:bg-gray-50">
                <td class="px-4 py-4">
                  <div class="font-medium text-gray-900">{{ paper.title }}</div>
                  <div class="text-sm text-gray-500">{{ formatAuthors(paper.authors) }}</div>
                  <div class="text-xs text-gray-400">{{ paper.journal }} ({{ paper.year || 'Unknown Year' }})</div>
                </td>
                <td class="px-4 py-4 whitespace-nowrap">
                  <div class="text-sm text-gray-900">{{ paper.source || "—" }}</div>
                </td>
                <td class="px-4 py-4 whitespace-nowrap text-sm">
                  <div v-if="paper.pdfStatus === 'available'" class="flex items-center text-green-600">
                    <CheckCircle class="mr-1" size="16" /> Available
                  </div>
                  <div v-else-if="paper.pdfStatus === 'missing'" class="flex items-center text-orange-500">
                    <AlertTriangle class="mr-1" size="16" /> Missing
                  </div>
                  <div v-else class="flex items-center text-blue-500">
                    <Clock class="mr-1" size="16" /> Retrieving...
                  </div>
                </td>
                <td class="px-4 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <template v-if="paper.pdfStatus === 'missing'">
                    <button class="text-indigo-600 hover:text-indigo-900 mr-3" @click="retrievePdf(paper)">
                      Retrieve
                    </button>
                    <button class="text-indigo-600 hover:text-indigo-900 mr-3" @click="uploadPdf(paper)">
                      Upload
                    </button>
                    <button class="text-indigo-600 hover:text-indigo-900" @click="markPaperReady(paper)">
                      Mark Ready
                    </button>
                  </template>
                  <template v-else-if="paper.pdfStatus === 'available'">
                    <button class="text-indigo-600 hover:text-indigo-900 mr-3" @click="viewPdf(paper)">
                      View
                    </button>
                    <button class="text-indigo-600 hover:text-indigo-900" @click="replacePdf(paper)">
                      Replace
                    </button>
                  </template>
                  <template v-else>
                    <button class="text-gray-600 hover:text-gray-900" @click="cancelRetrieval(paper)">
                      Cancel
                    </button>
                  </template>
                </td>
              </tr>
            </tbody>
          </table>
          
          <div class="px-6 py-4 border-t flex justify-between items-center bg-gray-50">
            <div class="text-sm text-gray-700">
              Showing {{ papers.length }} of {{ totalPapers }} papers
            </div>
            <div class="flex">
              <button 
                class="px-3 py-1 border rounded-md hover:bg-gray-100 mr-2"
                :disabled="currentPage === 1"
                @click="prevPage"
              >Previous</button>
              <button 
                class="px-3 py-1 border rounded-md hover:bg-gray-100"
                :disabled="currentPage === totalPages"
                @click="nextPage"
              >Next</button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Edit Paper Modal -->
    <div v-if="showEditModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg shadow-lg p-6 w-full max-w-md">
        <h2 class="text-xl font-bold mb-4">Edit Paper Metadata</h2>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Title</label>
          <input 
            v-model="editForm.title"
            type="text" 
            class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            placeholder="Paper title"
          />
        </div>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Journal</label>
          <input 
            v-model="editForm.journal"
            type="text" 
            class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            placeholder="Journal name"
          />
        </div>
        
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Publication Year</label>
          <input 
            v-model="editForm.year"
            type="number" 
            class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            placeholder="YYYY"
          />
        </div>
        
        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 mb-1">Authors (comma separated)</label>
          <input 
            v-model="editForm.authors"
            type="text" 
            class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            placeholder="Author names separated by commas"
          />
        </div>
        
        <div class="flex justify-end">
          <button 
            class="text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-100 mr-2"
            @click="showEditModal = false"
          >
            Cancel
          </button>
          <button 
            class="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700"
            @click="updatePaperMetadata"
            :disabled="!editForm.title"
          >
            Save Changes
          </button>
        </div>
      </div>
    </div>
    
    <!-- PDF Upload Modal -->
    <div v-if="showUploadModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg shadow-xl w-full max-w-3xl max-h-[90vh] overflow-hidden flex flex-col">
        <div class="p-4 border-b flex justify-between items-center">
          <h3 class="font-medium text-lg">Upload and Match PDFs</h3>
          <button 
            class="text-gray-400 hover:text-gray-600"
            @click="showUploadModal = false"
          >
            <X size="18" />
          </button>
        </div>
        
        <div class="border-b">
          <div class="flex">
            <button 
              class="py-3 px-4 font-medium"
              :class="uploadTab === 'upload' ? 'text-indigo-600 border-b-2 border-indigo-600' : 'text-gray-500 hover:text-gray-700'"
              @click="uploadTab = 'upload'"
            >
              Upload PDFs
            </button>
            <button 
              class="py-3 px-4 font-medium"
              :class="uploadTab === 'match' ? 'text-indigo-600 border-b-2 border-indigo-600' : 'text-gray-500 hover:text-gray-700'"
              @click="uploadTab = 'match'"
            >
              Match to Papers
            </button>
          </div>
        </div>
        
        <div class="flex-1 overflow-y-auto p-6">
          <div v-if="uploadTab === 'upload'">
            <div class="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center mb-6">
              <div class="mx-auto w-16 h-16 bg-indigo-100 rounded-full flex items-center justify-center mb-4">
                <UploadCloud size="24" class="text-indigo-600" />
              </div>
              <h3 class="text-lg font-medium mb-2">Drop PDF files here</h3>
              <p class="text-gray-500 mb-4">or click to browse your computer</p>
              <input 
                type="file" 
                ref="fileInput"
                accept=".pdf"
                multiple
                class="hidden"
                @change="handleFileUpload"
              />
              <button 
                class="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700"
                @click="$refs.fileInput.click()"
              >
                Select Files
              </button>
              <p class="text-xs text-gray-500 mt-4">
                Supported formats: PDF only. Maximum file size: 50MB.
              </p>
            </div>
            
            <div v-if="uploadedFiles.length > 0" class="mb-4">
              <h4 class="font-medium mb-2">Uploaded Files ({{ uploadedFiles.length }})</h4>
              <div class="space-y-3">
                <div 
                  v-for="(file, index) in uploadedFiles" 
                  :key="index"
                  class="bg-white p-3 rounded border shadow-sm"
                >
                  <div class="flex justify-between items-center mb-2">
                    <div class="font-medium flex items-center">
                      <font-awesome-icon icon="file-pdf" class="text-gray-500 mr-2" />
                      {{ file.name }}
                    </div>
                    <div class="text-sm text-gray-500">{{ formatFileSize(file.size) }}</div>
                  </div>
                  
                  <div class="w-full bg-gray-200 rounded-full h-2 mb-1">
                    <div 
                      class="h-2 rounded-full"
                      :class="file.status === 'complete' ? 'bg-green-500' : 'bg-indigo-600'"
                      :style="{ width: `${file.progress}%` }"
                    ></div>
                  </div>
                  
                  <div class="flex justify-between items-center">
                    <div class="text-xs text-gray-500">
                      {{ file.status === 'complete' ? 'Upload complete' : `Uploading... ${file.progress}%` }}
                    </div>
                    <button class="text-red-500 hover:text-red-700 text-xs" @click="removeFile(index)">
                      Remove
                    </button>
                  </div>
                </div>
              </div>
            </div>
            
            <div v-if="uploadedFiles.length > 0 && uploadedFiles.some(f => f.status === 'complete')" class="flex items-center border rounded-lg p-4 bg-indigo-50 text-indigo-800">
              <font-awesome-icon icon="check-circle" class="mr-2" />
              <span>{{ uploadedFiles.filter(f => f.status === 'complete').length }} files uploaded successfully. Continue to match these files with your papers.</span>
              <button 
                class="ml-auto px-4 py-1 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 text-sm"
                @click="uploadTab = 'match'"
              >
                Continue
              </button>
            </div>
          </div>
          
          <div v-if="uploadTab === 'match'" class="space-y-4">
            <div class="mb-6">
              <h4 class="font-medium mb-2">Match PDFs to Papers</h4>
              <p class="text-gray-600 text-sm mb-4">
                We'll try to automatically match PDFs to papers based on the filename and content.
                You can manually adjust the matches if needed.
              </p>
              
              <button 
                class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 flex items-center mr-2"
                @click="autoMatchPdfs"
              >
                <font-awesome-icon icon="rotate-right" class="mr-1" /> Auto-Match PDFs
              </button>
            </div>
            
            <div v-for="(file, index) in uploadedFiles.filter(f => f.status === 'complete')" :key="index" class="border rounded-lg p-4" :class="file.matched ? 'bg-green-50 border-green-200' : 'bg-yellow-50 border-yellow-200'">
              <div class="flex items-start">
                <div class="h-10 w-10 rounded-full bg-white border flex items-center justify-center mr-3">
                  <font-awesome-icon icon="file-pdf" class="text-gray-500" />
                </div>
                
                <div class="flex-1">
                  <div class="font-medium">{{ file.name }}</div>
                  <div class="text-sm text-gray-500">{{ formatFileSize(file.size) }}</div>
                  
                  <div v-if="file.matched" class="mt-2">
                    <div class="text-sm text-gray-700">Matched with:</div>
                    <div class="flex items-center mt-1">
                      <div class="flex-1">
                        <div class="font-medium text-green-800">{{ file.matchedPaper.title }}</div>
                        <div class="text-xs text-green-600">Match confidence: {{ file.confidence }}%</div>
                      </div>
                      <button class="text-indigo-600 hover:text-indigo-800 text-sm" @click="file.matched = false">
                        Change
                      </button>
                    </div>
                  </div>
                  
                  <div v-else class="mt-2">
                    <div class="mt-2 flex">
                      <select 
                        v-model="file.selectedPaperId"
                        class="flex-1 border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none mr-2"
                      >
                        <option value="">Select a paper to match...</option>
                        <option v-for="paper in papers" :key="paper.id" :value="paper.id">
                          {{ paper.title }}
                        </option>
                      </select>
                      <button 
                        class="px-3 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 text-sm"
                        @click="matchFileToPaper(file)"
                        :disabled="!file.selectedPaperId"
                      >
                        Match
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="p-4 border-t flex justify-end bg-gray-50">
          <button 
            class="px-4 py-2 border rounded-lg text-gray-700 hover:bg-gray-100 mr-2"
            @click="showUploadModal = false"
          >
            Cancel
          </button>
          <button 
            class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
            @click="finishPdfUpload"
          >
            Save and Continue
          </button>
        </div>
      </div>
    </div>
    
    <!-- Add PDF URL Modal -->
    <div v-if="showUrlModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg shadow-lg p-6 w-full max-w-md">
        <h2 class="text-xl font-bold mb-4">Add PDF URL</h2>
        
        <div v-if="selectedPaperForUrl" class="mb-4 p-3 bg-gray-50 rounded-lg">
          <div class="font-medium">{{ selectedPaperForUrl.title }}</div>
          <div class="text-sm text-gray-500">{{ formatAuthors(selectedPaperForUrl.authors) }}</div>
        </div>
        
        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 mb-1">PDF URL</label>
          <input 
            v-model="pdfUrl"
            type="text" 
            class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            placeholder="https://example.com/paper.pdf"
          />
          <p class="text-xs text-gray-500 mt-1">
            Enter a direct URL to the PDF file. The URL must end with .pdf
          </p>
        </div>
        
        <div class="flex justify-end">
          <button 
            class="text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-100 mr-2"
            @click="closeUrlModal"
          >
            Cancel
          </button>
          <button 
            class="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700"
            @click="savePdfUrl"
            :disabled="!pdfUrl || !pdfUrl.trim().toLowerCase().endsWith('.pdf')"
          >
            Save URL
          </button>
        </div>
      </div>
    </div>
    
    <!-- Confirmation Modal -->
    <div v-if="showConfirmationModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg shadow-lg p-6 w-full max-w-md">
        <h2 class="text-xl font-bold mb-4">{{ confirmationTitle }}</h2>
        <p class="mb-6">{{ confirmationMessage }}</p>
        
        <div class="flex justify-end">
          <button 
            class="text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-100 mr-2"
            @click="showConfirmationModal = false"
          >
            Cancel
          </button>
          <button 
            class="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700"
            @click="confirmationAction"
          >
            {{ confirmationButtonText }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { API_ROUTES } from '../config.js';
import { paperService, processingService } from '../services/api.js';

export default {
  name: 'PaperProcessing',
  components: {
    TabButton: {
      props: {
        label: String,
        icon: String,
        active: Boolean
      },
      template: `
        <button 
          :class="[
            'py-4 px-6 font-medium flex items-center', 
            active 
              ? 'text-indigo-600 border-b-2 border-indigo-600' 
              : 'text-gray-500 hover:text-gray-700'
          ]"
          @click="$emit('click')"
        >
          <span class="mr-2"><font-awesome-icon :icon="icon" /></span>
          {{ label }}
        </button>
      `
    }
  },
  props: {
    selectedPapers: {
      type: Array,
      default: () => []
    },
    activeProject: {
      type: Object,
      required: true,
      validator: (project) => {
        // Validate that the project has an id
        return project && project.id;
      }
    }
  },
  data() {
    return {
      activeTab: 'cleanup',
      filterType: 'all',
      pdfFilterType: 'all',
      papers: [],
      totalPapers: 0,
      duplicateCount: 0,
      incompleteCount: 0,
      missingPdfCount: 0,
      availablePdfCount: 0,
      currentPage: 1,
      itemsPerPage: 10,
      totalPages: 1,
      localSelectedPapers: [],
      searchQuery: '',
      sortBy: 'title',
      isLoading: false,
      isRetrieving: false,
      error: null,
      
      // Modals
      showEditModal: false,
      showUploadModal: false,
      showUrlModal: false,
      showConfirmationModal: false,
      
      // Edit form
      editForm: {
        id: null,
        title: '',
        journal: '',
        year: null,
        authors: ''
      },
      
      // PDF Upload
      uploadTab: 'upload',
      uploadedFiles: [],
      
      // PDF URL
      selectedPaperForUrl: null,
      pdfUrl: '',
      
      // Confirmation
      confirmationTitle: '',
      confirmationMessage: '',
      confirmationButtonText: 'Confirm',
      confirmationAction: () => {},
      
      // Keep track of papers being retrieved
      retrievingPapers: new Set()
    }
  },
  computed: {
    allSelected() {
      return this.papers.length > 0 && this.localSelectedPapers.length === this.papers.length;
    }
  },
  watch: {
    selectedPapers: {
      immediate: true,
      handler(newVal) {
        if (newVal && newVal.length) {
          // Initialize our local selected papers with the ones passed from parent
          this.localSelectedPapers = [...newVal];
        }
      }
    },
    activeProject: {
      immediate: true,
      handler(newProject, oldProject) {
        // When the active project changes, refresh the data
        if (newProject && newProject.id) {
          if (!oldProject || newProject.id !== oldProject.id) {
            console.log(`Active project changed to ${newProject.name} (${newProject.id}), refreshing data...`);
            this.fetchPapers();
            this.fetchPaperCounts();
          }
        } else {
          console.warn('Active project is undefined or missing ID');
          this.papers = [];
          this.totalPapers = 0;
          this.error = "No active project selected. Please select a project first.";
        }
      }
    }
  },
  mounted() {
    this.fetchPapers();
    this.fetchPaperCounts();
  },
  methods: {
    async fetchPapers() {
      this.isLoading = true;
      this.error = null;
      
      try {
        if (!this.activeProject || !this.activeProject.id) {
          this.papers = []; // Clear papers if no active project
          this.totalPapers = 0;
          this.totalPages = 1;
          console.warn("PaperProcessing: No active project ID available.");
          this.error = "No active project selected. Please select a project first.";
          return; // Exit if no active project
        }

        // Build filters object
        const filters = {};
        if (this.searchQuery) filters.search = this.searchQuery;
        if (this.sortBy) filters.sort_by = this.sortBy;
        
        // Add PDF status filter
        if (this.activeTab === 'retrieve' && this.pdfFilterType !== 'all') {
          filters.pdf_status = this.pdfFilterType;
        }
        
        // Add paper status filter
        if (this.activeTab === 'cleanup' && this.filterType !== 'all') {
          filters.status = this.filterType;
        }
        
        // Log the active project being used
        console.log(`Fetching papers for project ${this.activeProject.id} (${this.activeProject.name})`);
        
        // Use the processing service with active project ID
        const data = await processingService.getPapersForProcessing(
          this.activeProject.id,
          (this.currentPage - 1) * this.itemsPerPage,
          this.itemsPerPage,
          filters
        );
        
        this.papers = data; // Assuming the endpoint returns the list directly
        this.totalPapers = data.length; // Will be improved when API returns total count
        this.totalPages = Math.ceil(this.totalPapers / this.itemsPerPage);
        
        // Update counts for different PDF statuses
        this.missingPdfCount = this.papers.filter(p => p.pdfStatus === 'missing').length;
        this.availablePdfCount = this.papers.filter(p => p.pdfStatus === 'available').length;
        
      } catch (err) {
        this.error = err.message;
        console.error('Error fetching papers for processing:', err);
      } finally {
        this.isLoading = false;
      }
    },
    
    async fetchPaperCounts() {
      try {
        if (!this.activeProject || !this.activeProject.id) {
          // Reset counts if no active project
          this.totalPapers = 0;
          this.duplicateCount = 0;
          this.incompleteCount = 0;
          this.missingPdfCount = 0;
          this.availablePdfCount = 0;
          this.totalPages = 1;
          return;
        }
        
        // Fetch total counts with project ID as query parameter
        const response = await fetch(`${API_ROUTES.PROCESSING.COUNTS}?project_id=${this.activeProject.id}`);
        
        if (response.ok) {
          const data = await response.json();
          this.totalPapers = data.total || 0;
          this.duplicateCount = data.duplicates || 0;
          this.incompleteCount = data.incomplete || 0;
          this.missingPdfCount = data.missing_pdf || 0;
          this.availablePdfCount = data.available_pdf || 0;
          
          // Calculate total pages
          this.totalPages = Math.ceil(this.totalPapers / this.itemsPerPage);
        }
      } catch (err) {
        console.error('Error fetching paper counts:', err);
      }
    },
    
    async findDuplicates() {
      this.isLoading = true;
      this.error = null;
      
      try {
        if (!this.activeProject || !this.activeProject.id) {
          alert('Please select an active project first.');
          return;
        }
        
        console.log(`Finding duplicates for project ${this.activeProject.id}`);
        
        // Use the processing service with project ID
        const data = await processingService.findProjectDuplicates(this.activeProject.id);
        
        console.log(`Duplicate detection complete. Found ${data.length} potential duplicate groups`);
        
        if (data.length > 0) {
          // Set filter to duplicates to show the results
          this.filterType = 'duplicates';
          await this.fetchPapers();
          
          // Show confirmation with results
          alert(`Found ${data.length} potential duplicate groups.`);
        } else {
          alert('No duplicates found.');
        }
        
      } catch (err) {
        this.error = err.message;
        console.error('Error finding duplicates:', err);
      } finally {
        this.isLoading = false;
      }
    },
    
    // PDF retrieval functions
    async retrieveAllMissingPDFs() {
      if (this.isRetrieving) return;
      
      if (!this.activeProject || !this.activeProject.id) {
        alert('Please select an active project first.');
        return;
      }
      
      this.isRetrieving = true;
      
      try {
        // Fetch all papers with missing PDFs for this project
        const filters = {
          pdf_status: 'missing',
          limit: 100 // Retrieve up to 100 papers to process
        };
        
        // Use the processing service
        const papers = await processingService.getPapersForProcessing(
          this.activeProject.id,
          0, // Start from the first paper
          100, // Get up to 100 papers
          filters
        );
        
        if (papers.length === 0) {
          alert('No papers with missing PDFs found in this project.');
          return;
        }
        
        // Process each paper sequentially
        let successCount = 0;
        let failCount = 0;
        
        for (const paper of papers) {
          if (!paper.doi) {
            failCount++;
            continue;
          }
          
          try {
            // Add to retrieving set
            this.retrievingPapers.add(paper.id);
            
            // Use the processing service
            const result = await processingService.retrievePdfForPaper(paper.id);
            
            if (result.success) {
              successCount++;
            } else {
              failCount++;
            }
          } catch (e) {
            console.error(`Error retrieving PDF for paper ${paper.id}:`, e);
            failCount++;
          } finally {
            // Remove from retrieving set
            this.retrievingPapers.delete(paper.id);
          }
        }
        
        // Refresh the papers list
        await this.fetchPapers();
        await this.fetchPaperCounts();
        
        alert(`PDF retrieval complete: ${successCount} PDFs retrieved successfully, ${failCount} failed.`);
        
      } catch (err) {
        console.error('Error retrieving PDFs:', err);
        alert(`Error retrieving PDFs: ${err.message}`);
      } finally {
        this.isRetrieving = false;
      }
    },
    
    async retrievePdf(paper) {
      if (!paper.doi) {
        alert('This paper has no DOI. Cannot automatically retrieve PDF.');
        return;
      }
      
      // Add to retrieving set
      this.retrievingPapers.add(paper.id);
      
      try {
        console.log(`Retrieving PDF for paper ID: ${paper.id}, DOI: ${paper.doi}`);
        
        // Use the processing service
        const result = await processingService.retrievePdfForPaper(paper.id);
        
        if (result.success) {
          // Refresh the papers list (status changed to ready_to_code)
          await this.fetchPapers();
          alert('PDF retrieved successfully and paper marked as ready for coding.');
        } else {
          alert('No open access PDF found for this paper.');
        }
        
      } catch (err) {
        console.error('Error retrieving PDF:', err);
        alert(`Error retrieving PDF: ${err.message}`);
      } finally {
        // Remove from retrieving set
        this.retrievingPapers.delete(paper.id);
      }
    },

    // Mark paper as ready for coding (when PDF isn't available but coding can proceed)
    async markPaperReady(paper) {
      try {
        console.log(`Marking paper ID: ${paper.id} as ready for coding`);
        
        // Use the processing service
        await processingService.markPaperReady(paper.id);
        
        alert('Paper marked as ready for coding.');
        // Refresh the papers list since status changed
        await this.fetchPapers();
        
        // If paper was marked ready, its status should be set to 'ready_to_code'
        // This means it will appear in the coding view
        console.log(`Paper ${paper.id} status updated to ready_to_code`);
        
      } catch (err) {
        console.error('Error marking paper as ready:', err);
        alert(`Error marking paper as ready: ${err.message}`);
      }
    },
    
    // Selection functions
    isSelected(paperId) {
      return this.localSelectedPapers.includes(paperId);
    },
    
    toggleSelection(paperId) {
      const index = this.localSelectedPapers.indexOf(paperId);
      if (index === -1) {
        this.localSelectedPapers.push(paperId);
      } else {
        this.localSelectedPapers.splice(index, 1);
      }
    },
    
    toggleSelectAll() {
      if (this.allSelected) {
        this.localSelectedPapers = [];
      } else {
        this.localSelectedPapers = this.papers.map(p => p.id);
      }
    },
    
    // Filter and navigation
    setFilterType(type) {
      this.filterType = type;
      this.currentPage = 1;
      this.fetchPapers();
    },
    
    setPdfFilterType(type) {
      this.pdfFilterType = type;
      this.currentPage = 1;
      this.fetchPapers();
    },
    
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
        this.fetchPapers();
      }
    },
    
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
        this.fetchPapers();
      }
    },
    
    searchPapers() {
      this.currentPage = 1;
      this.fetchPapers();
    },
    
    // Edit paper
    editPaper(paper) {
      this.editForm = {
        id: paper.id,
        title: paper.title,
        journal: paper.journal || '',
        year: paper.year || null,
        authors: Array.isArray(paper.authors) 
          ? paper.authors.join(', ') 
          : paper.authors
      };
      
      this.showEditModal = true;
    },
    
    async updatePaperMetadata() {
      try {
        const formData = new FormData();
        formData.append('title', this.editForm.title);
        formData.append('journal', this.editForm.journal);
        
        if (this.editForm.year) {
          formData.append('year', this.editForm.year.toString());
        }
        
        if (this.editForm.authors) {
          // Convert comma-separated authors to JSON array
          const authorNames = this.editForm.authors.split(',').map(a => a.trim());
          const authors = authorNames.map(name => ({ name }));
          formData.append('authors', JSON.stringify(authors));
        }
        
        const response = await fetch(API_ROUTES.PROCESSING.UPDATE_METADATA(this.editForm.id), {
          method: 'PUT',
          body: formData
        });
        
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || 'Failed to update paper metadata');
        }
        
        // Refresh the papers list
        await this.fetchPapers();
        
        // Close modal
        this.showEditModal = false;
        
        alert('Paper metadata updated successfully.');
        
      } catch (err) {
        console.error('Error updating paper metadata:', err);
        alert(`Error updating paper metadata: ${err.message}`);
      }
    },
    
    // Remove papers
    confirmRemove(paper) {
      this.confirmationTitle = 'Remove Paper';
      this.confirmationMessage = `Are you sure you want to remove "${paper.title}"? This will remove the paper from all projects.`;
      this.confirmationButtonText = 'Remove';
      this.confirmationAction = () => this.removePaper(paper.id);
      this.showConfirmationModal = true;
    },
    
    async removePaper(paperId) {
      try {
        const response = await fetch(`${API_ROUTES.PAPERS.GET_BY_ID(paperId)}`, {
          method: 'DELETE'
        });
        
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || 'Failed to remove paper');
        }
        
        // Remove from selected papers if selected
        const index = this.localSelectedPapers.indexOf(paperId);
        if (index !== -1) {
          this.localSelectedPapers.splice(index, 1);
        }
        
        // Refresh papers and counts
        await this.fetchPapers();
        await this.fetchPaperCounts();
        
        // Close confirmation modal
        this.showConfirmationModal = false;
        
      } catch (err) {
        console.error('Error removing paper:', err);
        alert(`Error removing paper: ${err.message}`);
      }
    },
    
    removeSelectedPapers() {
      if (this.localSelectedPapers.length === 0) return;
      
      this.confirmationTitle = 'Remove Selected Papers';
      this.confirmationMessage = `Are you sure you want to remove ${this.localSelectedPapers.length} selected papers? This will remove them from all collections.`;
      this.confirmationButtonText = 'Remove All';
      this.confirmationAction = this.removeMultiplePapers;
      this.showConfirmationModal = true;
    },
    
    async removeMultiplePapers() {
      try {
        let successCount = 0;
        
        for (const paperId of this.localSelectedPapers) {
          try {
            const response = await fetch(`${API_ROUTES.PAPERS.GET_BY_ID(paperId)}`, {
              method: 'DELETE'
            });
            
            if (response.ok) {
              successCount++;
            }
          } catch (e) {
            console.error(`Error removing paper ${paperId}:`, e);
          }
        }
        
        // Clear selected papers
        this.localSelectedPapers = [];
        
        // Refresh papers and counts
        await this.fetchPapers();
        await this.fetchPaperCounts();
        
        // Close confirmation modal
        this.showConfirmationModal = false;
        
        alert(`${successCount} papers removed successfully.`);
        
      } catch (err) {
        console.error('Error removing papers:', err);
        alert(`Error removing papers: ${err.message}`);
      }
    },
    
    // PDF Upload functions
    handleFileUpload(event) {
      const files = event.target.files;
      if (!files || files.length === 0) return;
      
      // Add files to uploadedFiles array
      Array.from(files).forEach(file => {
        if (file.type === 'application/pdf') {
          this.uploadedFiles.push({
            file,
            name: file.name,
            size: file.size,
            progress: 100, // Mock progress for now
            status: 'complete', // Mock status for now
            matched: false,
            selectedPaperId: null,
            matchedPaper: null,
            confidence: 0
          });
        }
      });
    },
    
    removeFile(index) {
      this.uploadedFiles.splice(index, 1);
    },
    
    formatFileSize(bytes) {
      const sizes = ['Bytes', 'KB', 'MB', 'GB'];
      if (bytes === 0) return '0 Bytes';
      const i = Math.floor(Math.log(bytes) / Math.log(1024));
      return parseFloat((bytes / Math.pow(1024, i)).toFixed(2)) + ' ' + sizes[i];
    },
    
    autoMatchPdfs() {
      // Simple matching algorithm based on filenames
      const unmatchedFiles = this.uploadedFiles.filter(f => !f.matched && f.status === 'complete');
      
      for (const file of unmatchedFiles) {
        // Extract potential title from filename
        let filename = file.name.toLowerCase().replace('.pdf', '');
        
        // Find best matching paper based on title similarity
        let bestMatch = null;
        let highestScore = 0;
        
        for (const paper of this.papers) {
          const paperTitle = paper.title.toLowerCase();
          
          // Skip papers that already have PDFs
          if (paper.pdfStatus === 'available') {
            continue;
          }
          
          // Calculate simple similarity score
          let score = 0;
          const words = paperTitle.split(/\s+/);
          
          for (const word of words) {
            if (word.length > 3 && filename.includes(word)) {
              score += 10;
            }
          }
          
          if (score > highestScore) {
            highestScore = score;
            bestMatch = paper;
          }
        }
        
        // If good enough match found
        if (bestMatch && highestScore > 30) {
          file.matched = true;
          file.matchedPaper = bestMatch;
          file.confidence = Math.min(95, Math.floor(highestScore / 2));
        }
      }
    },
    
    matchFileToPaper(file) {
      if (!file.selectedPaperId) return;
      
      const selectedPaper = this.papers.find(p => p.id === file.selectedPaperId);
      if (selectedPaper) {
        file.matched = true;
        file.matchedPaper = selectedPaper;
        file.confidence = 100; // User-selected match
      }
    },
    
    finishPdfUpload() {
      // In a real implementation, we would upload the PDFs to the server
      // and associate them with the matched papers
      
      const matchedFiles = this.uploadedFiles.filter(f => f.matched);
      if (matchedFiles.length === 0) {
        alert('No files have been matched to papers.');
        return;
      }
      
      // For this mock, we'll just update the UI
      for (const file of matchedFiles) {
        const paperId = file.matchedPaper.id;
        const paperIndex = this.papers.findIndex(p => p.id === paperId);
        
        if (paperIndex !== -1) {
          this.papers[paperIndex].pdfStatus = 'available';
        }
      }
      
      // Update counts
      this.availablePdfCount += matchedFiles.length;
      this.missingPdfCount = Math.max(0, this.missingPdfCount - matchedFiles.length);
      
      // Close modal and clear uploads
      this.showUploadModal = false;
      this.uploadedFiles = [];
      
      alert(`${matchedFiles.length} PDFs successfully matched and uploaded.`);
    },
    
    // PDF URL functions
    addPdfUrl(paper) {
      this.selectedPaperForUrl = paper;
      this.pdfUrl = '';
      this.showUrlModal = true;
    },
    
    async savePdfUrl() {
      if (!this.selectedPaperForUrl || !this.pdfUrl) return;
      
      try {
        // In a real implementation, we'd call an API endpoint
        // For now, just update the UI
        const paperId = this.selectedPaperForUrl.id;
        const paperIndex = this.papers.findIndex(p => p.id === paperId);
        
        if (paperIndex !== -1) {
          this.papers[paperIndex].pdfStatus = 'available';
        }
        
        // Update counts
        this.availablePdfCount++;
        this.missingPdfCount = Math.max(0, this.missingPdfCount - 1);
        
        this.closeUrlModal();
        
        alert('PDF URL saved successfully.');
        
      } catch (err) {
        console.error('Error saving PDF URL:', err);
        alert(`Error saving PDF URL: ${err.message}`);
      }
    },
    
    closeUrlModal() {
      this.showUrlModal = false;
      this.selectedPaperForUrl = null;
      this.pdfUrl = '';
    },
    
    // PDF actions
    viewPdf(paper) {
      alert(`Viewing PDF for "${paper.title}"`);
      // In a real implementation, this would open the PDF viewer
    },
    
    uploadPdf(paper) {
      this.selectedPaperForUrl = paper;
      this.showUploadModal = true;
      this.uploadTab = 'upload';
    },
    
    replacePdf(paper) {
      this.selectedPaperForUrl = paper;
      this.showUploadModal = true;
      this.uploadTab = 'upload';
    },
    
    cancelRetrieval(paper) {
      // In a real implementation, this would cancel the retrieval process
      this.retrievingPapers.delete(paper.id);
      alert('PDF retrieval cancelled.');
    },
    
    // Helper functions
    formatAuthors(authors) {
      if (!authors || authors.length === 0) {
        return 'Unknown Authors';
      }
      
      if (typeof authors === 'string') {
        return authors;
      }
      
      if (authors.length <= 3) {
        return authors.join(', ');
      } else {
        return `${authors[0]}, et al.`;
      }
    },
    
    exportPaperList() {
      // In a real implementation, this would export the paper list as CSV
      alert('Paper list exported.');
    },
    
    goToCoding() {
      // Check if any papers are ready for coding
      const readyPapers = this.papers.filter(p => 
        p.pdfStatus === 'available' || 
        p.status === 'ready_to_code'
      );
      
      if (readyPapers.length === 0) {
        alert('No papers are ready for coding. Please process at least one paper first.');
        return;
      }
      
      // Emit event to parent to change view, passing the active project
      this.$emit('change-view', 'coding', this.activeProject.id);
      console.log(`Navigating to coding view for project ${this.activeProject.id}`);
    },
    
    toggleFilters() {
      // This would show/hide additional filters
      alert('Additional filters would be shown here.');
    }
  }
}
</script>

<style scoped>
.spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border-left-color: #4f46e5;
  animation: spin 1s linear infinite;
  margin: 0 auto;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
