@router.post("/import-batch", response_model=Dict[str, Any])
async def import_papers_batch(
    papers: List[PaperCreate],
    db: Session = Depends(get_db),
):
    """
    Import multiple papers from search results.
    
    This endpoint accepts a list of paper objects and stores them in the database,
    consolidating duplicates based on DOI or title similarity.
    
    Returns:
        A dictionary containing import status, counts, and the list of successfully imported papers
        with their database IDs.
    """
    try:
        imported_count = 0
        skipped_count = 0
        errors = []
        imported_papers = []
        
        for paper_create in papers:
            try:
                # Create or update the paper in the database
                created_paper = create_paper(db, paper_create)
                
                if created_paper:
                    # Add the successfully created/found paper to our result list
                    imported_papers.append({
                        "id": created_paper.id,
                        "title": created_paper.title,
                        "doi": created_paper.doi,
                        "authors": created_paper.authors,
                        "journal": created_paper.journal,
                        "publication_date": created_paper.publication_date
                    })
                    imported_count += 1
                else:
                    skipped_count += 1
                    
            except Exception as e:
                logger.error(f"Error importing paper: {str(e)}")
                errors.append({
                    "paper": paper_create.title if hasattr(paper_create, "title") else "Unknown title",
                    "error": str(e)
                })
                skipped_count += 1
        
        return {
            "status": "success",
            "imported_count": imported_count,
            "skipped_count": skipped_count,
            "errors": errors,
            "imported_papers": imported_papers
        }
    
    except Exception as e:
        logger.error(f"Error in batch import: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error importing papers: {str(e)}")
