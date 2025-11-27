from pathlib import Path
from rdflib import Graph

def merge_ttl_files(input_folder='ttl', output_file='merged_output.ttl'):
    """
    Merges all TTL files from the specified folder into a single TTL file.
    
    Args:
        input_folder: Path to folder containing TTL files (default: 'ttl')
        output_file: Name of the output merged file (default: 'merged_output.ttl')
    """
    # Create an empty graph
    merged_graph = Graph()
    
    # Get the folder path - use relative path from script location
    script_dir = Path(__file__).parent.parent  # Go up to GITHUB folder
    ttl_folder = script_dir / input_folder
    
    # Check if folder exists
    if not ttl_folder.exists():
        print(f"Error: Folder '{ttl_folder}' does not exist.")
        print(f"Script is looking in: {ttl_folder.absolute()}")
        return
    
    # Find all TTL files
    ttl_files = list(ttl_folder.glob('*.ttl'))
    
    if not ttl_files:
        print(f"No TTL files found in '{ttl_folder}'.")
        return
    
    print(f"Found {len(ttl_files)} TTL files. Merging...")
    
    # Parse and merge each TTL file
    for ttl_file in ttl_files:
        print(f"Processing: {ttl_file.name}")
        try:
            merged_graph.parse(ttl_file, format='turtle')
            print(f"  ✓ Successfully parsed {ttl_file.name}")
        except Exception as e:
            print(f"  ✗ Error parsing {ttl_file.name}: {e}")
    
    # Create output path in ttl folder
    output_path = ttl_folder / output_file
    
    # Serialize the merged graph to a new TTL file
    print(f"\nSaving merged graph to '{output_path}'...")
    try:
        merged_graph.serialize(destination=str(output_path), format='turtle')
        print(f"✓ Successfully merged {len(ttl_files)} files into '{output_file}'.")
        print(f"✓ Total triples: {len(merged_graph)}")
        print(f"✓ Output location: {output_path.absolute()}")
    except Exception as e:
        print(f"✗ Error saving merged file: {e}")

if __name__ == "__main__":
    # Use relative path from project root
    merge_ttl_files(input_folder='ttl', output_file='rrr_merged.ttl')