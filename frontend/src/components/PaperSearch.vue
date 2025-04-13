    async importExtractedPapers() {
      // Import papers with extracted metadata
      try {
        const papersToImport = this.uploadQueue
          .filter(item => item.status === 'complete' && item.metadata)
          .map(item => ({
            title: item.metadata.title || item.name,
            abstract: item.metadata.abstract,
            authors: item.metadata.authors || [],
            publication_date: item.metadata.year ? new Date(item.metadata.year, 0, 1).toISOString() : null,
            journal: item.metadata.journal,
            doi: item.metadata.doi,
            file_path: item.metadata.file_path,
            file_name: item.name,
            source: 'PDF Upload'
          }));
        
        if (papersToImport.length === 0) {
          console.log('No papers with metadata to import');
          return;
        }
        
        console.log('Importing papers from uploads:', papersToImport);
        
        const response = await fetch(API_ROUTES.PAPERS.IMPORT_BATCH, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          // FIX: Send the array directly, not wrapped in an object
          body: JSON.stringify(papersToImport)
        });
        
        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}));
          throw new Error(errorData.detail || 'Failed to import papers');
        }
        
        const result = await response.json();
        console.log('Import result:', result);
        
        if (result.imported_count > 0) {
          alert(`${result.imported_count} paper(s) imported successfully.`);
          // Refresh imported papers list with real data
          await this.fetchImportedPapers();
          // Clear upload queue for successfully imported papers
          this.uploadQueue = this.uploadQueue.filter(item => {
            return item.status !== 'complete' || !item.metadata;
          });
        }
        
      } catch (error) {
        console.error('Error importing papers from uploads:', error);
        alert('There was a problem importing the papers: ' + error.message);
      }
    }