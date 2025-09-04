#!/usr/bin/env python3
"""
Data validation utilities for Editorial Assistant
Simple helper functions to ensure data integrity
"""

import json
import os
from typing import Dict, List, Any


def validate_catalog_structure(catalog_data: List[Dict]) -> bool:
    """Validate catalog data structure"""
    required_fields = ['title', 'author', 'publisher', 'release_date']
    
    for book in catalog_data:
        if not all(field in book for field in required_fields):
            return False
    return True


def validate_ticket_structure(ticket_data: List[Dict]) -> bool:
    """Validate ticket data structure"""
    required_fields = ['id', 'message', 'status']
    
    for ticket in ticket_data:
        if not all(field in ticket for field in required_fields):
            return False
    return True


def check_file_exists(file_path: str) -> bool:
    """Check if required data file exists"""
    return os.path.exists(file_path)


def validate_json_file(file_path: str) -> bool:
    """Validate JSON file format"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            json.load(f)
        return True
    except (json.JSONDecodeError, FileNotFoundError):
        return False


def run_data_validation() -> Dict[str, bool]:
    """Run complete data validation suite"""
    results = {
        'catalog_exists': check_file_exists('mock_catalog.json'),
        'tickets_exists': check_file_exists('mock_tickets.json'),
        'catalog_valid_json': validate_json_file('mock_catalog.json'),
        'tickets_valid_json': validate_json_file('mock_tickets.json')
    }
    
    if results['catalog_valid_json']:
        with open('mock_catalog.json', 'r', encoding='utf-8') as f:
            catalog = json.load(f)
        results['catalog_structure'] = validate_catalog_structure(catalog)
    
    if results['tickets_valid_json']:
        with open('mock_tickets.json', 'r', encoding='utf-8') as f:
            tickets = json.load(f)
        results['tickets_structure'] = validate_ticket_structure(tickets)
    
    return results


if __name__ == "__main__":
    print("🔍 Running data validation...")
    results = run_data_validation()
    
    for test, passed in results.items():
        status = "✅" if passed else "❌"
        print(f"{status} {test}")
    
    all_passed = all(results.values())
    print(f"\n{'✅ All validations passed!' if all_passed else '⚠️ Some validations failed'}")
