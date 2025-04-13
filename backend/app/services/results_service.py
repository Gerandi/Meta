from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from fastapi import HTTPException

from app.models.paper import Paper
from app.models.coding import CodingSheet, CodingData
from app.schemas.results import ResultsTable, ResultColumn, ResultRow
from app.services.coding_service import get_coding_sheet_by_project_service

def get_results_table_service(db: Session, project_id: int) -> ResultsTable:
    """
    Generate a formatted results table for a project.
    
    Args:
        db: Database session
        project_id: ID of the project
        
    Returns:
        ResultsTable object containing columns and rows of coded data
    """
    # Step 1: Get the coding sheet for this project
    coding_sheet = get_coding_sheet_by_project_service(db, project_id)
    if not coding_sheet:
        # If no coding sheet exists for this project, return an empty results table
        return ResultsTable(columns=[], rows=[], total_rows=0, page=1, page_size=50)
    
    # Step 2: Get all papers in this project
    papers = db.query(Paper).filter(Paper.projects.any(id=project_id)).all()
    
    # Step 3: Define columns
    columns = []
    
    # Basic paper info columns
    columns.append(ResultColumn(name="title", label="Title", data_type="text"))
    columns.append(ResultColumn(name="authors", label="Authors", data_type="text"))
    columns.append(ResultColumn(name="publication_date", label="Publication Date", data_type="date"))
    columns.append(ResultColumn(name="journal", label="Journal", data_type="text"))
    
    # Add columns from coding sheet
    for section in coding_sheet.sections:
        for field in section.fields:
            columns.append(ResultColumn(
                name=field.get('name'),
                label=field.get('label'),
                data_type=field.get('type', 'text'),
                description=field.get('description')
            ))
    
    # Step 4: Build rows
    rows = []
    for paper in papers:
        # Get coding data for this paper
        coding_data = db.query(CodingData).filter(
            CodingData.paper_id == paper.id,
            CodingData.sheet_id == coding_sheet.id
        ).first()
        
        # Initialize with paper metadata
        values = {
            "title": paper.title,
            "authors": format_authors(paper.authors),
            "publication_date": paper.publication_date,
            "journal": paper.journal
        }
        
        # Add coded data if available
        if coding_data and coding_data.data:
            values.update(coding_data.data)
        
        # Add row
        rows.append(ResultRow(
            paper_id=paper.id,
            values=values
        ))
    
    # Step 5: Return formatted results table
    return ResultsTable(
        columns=columns,
        rows=rows,
        total_rows=len(rows),
        page=1,
        page_size=50
    )

def format_authors(authors_list: List[Dict[str, Any]]) -> str:
    """Format authors list into a string."""
    if not authors_list:
        return "Unknown Authors"
    
    if len(authors_list) <= 3:
        return ", ".join([a.get("name", "Unknown") for a in authors_list])
    else:
        return f"{authors_list[0].get('name', 'Unknown')} et al."
