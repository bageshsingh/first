import json
import xml.etree.ElementTree as ET
from typing import Any, Dict


def xml_to_dict(elem: ET.Element) -> Dict[str, Any]:
    # Convert an XML element and its children into a dictionary
    children = list(elem)
    if not children:
        return {elem.tag: elem.text}
    result = {}
    for child in children:
        result.update(xml_to_dict(child))
    return {elem.tag: result}


def parse_input(data: str) -> Dict[str, Any]:
    data = data.strip()
    if not data:
        raise ValueError("No input data provided")
    # Detect JSON
    if data.startswith('{') or data.startswith('['):
        return json.loads(data)
    # Treat everything else as XML/SOAP
    root = ET.fromstring(data)
    return xml_to_dict(root)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Convert XML/SOAP/JSON to a dictionary")
    parser.add_argument('file', help="Path to input file")
    args = parser.parse_args()
    with open(args.file, 'r', encoding='utf-8') as f:
        data = f.read()
    result = parse_input(data)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
