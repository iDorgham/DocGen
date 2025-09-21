#!/usr/bin/env python3
"""
Document Generation Script for DocGen CLI
Generate documentation using Jinja2 templates
"""

import os
import sys
import yaml
from pathlib import Path
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape

def load_project_data(data_file):
    """Load project data from YAML file."""
    with open(data_file, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def setup_jinja_environment():
    """Set up Jinja2 environment with custom filters."""
    env = Environment(
        loader=FileSystemLoader('src/templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    
    # Add custom filters
    def format_date(date_str):
        """Format date string for display."""
        if isinstance(date_str, str):
            try:
                dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                return dt.strftime('%B %d, %Y')
            except:
                return date_str
        return date_str
    
    env.filters['format_date'] = format_date
    return env

def generate_document(template_name, project_data, output_file):
    """Generate a document using the specified template."""
    env = setup_jinja_environment()
    
    # Load template
    template = env.get_template(f'{template_name}.j2')
    
    # Prepare template context
    risks_data = project_data.get('risks', {})
    all_risks = []
    if 'technical' in risks_data:
        for risk in risks_data['technical']:
            # Ensure all required fields are present
            risk_dict = {
                'title': risk.get('title', ''),
                'description': risk.get('description', ''),
                'impact': risk.get('impact', ''),
                'impact_score': risk.get('impact_score', 5),
                'probability': risk.get('probability', ''),
                'probability_score': risk.get('probability_score', 5),
                'mitigation': risk.get('mitigation', ''),
                'owner': risk.get('owner', ''),
                'status': risk.get('status', ''),
                'category': risk.get('category', 'Technical')
            }
            all_risks.append(risk_dict)
    if 'business' in risks_data:
        for risk in risks_data['business']:
            # Ensure all required fields are present
            risk_dict = {
                'title': risk.get('title', ''),
                'description': risk.get('description', ''),
                'impact': risk.get('impact', ''),
                'impact_score': risk.get('impact_score', 5),
                'probability': risk.get('probability', ''),
                'probability_score': risk.get('probability_score', 5),
                'mitigation': risk.get('mitigation', ''),
                'owner': risk.get('owner', ''),
                'status': risk.get('status', ''),
                'category': risk.get('category', 'Business')
            }
            all_risks.append(risk_dict)
    
    context = {
        'project': project_data.get('project', {}),
        'team': project_data.get('team', {}),
        'requirements': project_data.get('requirements', {}),
        'timeline': project_data.get('timeline', {}),
        'marketing': project_data.get('marketing', {}),
        'technical': project_data.get('technical', {}),
        'data_model': project_data.get('data_model', {}),
        'development': project_data.get('development', {}),
        'risks': all_risks,
        'glossary': project_data.get('glossary', {}),
        'references': project_data.get('references', []),
        'resources': project_data.get('resources', {}),
        'budget': project_data.get('budget', {}),
        'contingency_plans': project_data.get('contingency_plans', []),
        'quality': project_data.get('quality', {}),
        'communication': project_data.get('communication', {}),
        'change_management': project_data.get('change_management', {}),
        'closure': project_data.get('closure', {}),
        'appendices': project_data.get('appendices', {}),
        '_template': {
            'generated_at': datetime.now().isoformat(),
            'template_name': template_name
        },
        '_metadata': {
            'project_path': str(Path.cwd()),
            'generated_by': 'DocGen CLI v2.0.0'
        }
    }
    
    # Render template
    try:
        content = template.render(**context)
    except Exception as e:
        print(f"Template rendering error for {template_name}: {e}")
        print(f"Context keys: {list(context.keys())}")
        if template_name == 'project_plan':
            print(f"Risks data: {context.get('risks', [])}")
        elif template_name == 'marketing':
            print(f"Marketing data keys: {list(context.get('marketing', {}).keys())}")
        raise
    
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Generated {output_file}")
    return content

def main():
    """Main function to generate all documents."""
    print("DocGen Document Generation")
    print("=" * 40)
    
    # Load project data
    data_file = 'assets/data/samples/sample_project_data.yaml'
    if not Path(data_file).exists():
        print(f"Error: {data_file} not found!")
        sys.exit(1)
    
    print(f"Loading project data from {data_file}...")
    project_data = load_project_data(data_file)
    
    # Create output directory
    output_dir = Path('assets/docs/generated')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate documents
    templates = [
        ('technical_spec', 'Technical Specification'),
        ('project_plan', 'Project Plan'),
        ('marketing', 'Marketing Materials')
    ]
    
    print(f"\nGenerating documents in {output_dir}/...")
    
    for template_name, doc_name in templates:
        output_file = output_dir / f'{template_name}.md'
        try:
            content = generate_document(template_name, project_data, output_file)
            print(f"  {doc_name}: {len(content)} characters")
        except Exception as e:
            print(f"  Error generating {doc_name}: {e}")
    
    print(f"\n✓ All documents generated successfully!")
    print(f"📁 Output directory: {output_dir.absolute()}")
    
    # Show file sizes
    print(f"\nGenerated files:")
    for file_path in output_dir.glob('*.md'):
        size = file_path.stat().st_size
        print(f"  {file_path.name}: {size:,} bytes")

if __name__ == '__main__':
    main()
