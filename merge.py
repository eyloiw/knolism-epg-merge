import requests
import xml.etree.ElementTree as ET

urls = [
    "https://raw.githubusercontent.com/Animenosekai/japanterebi-xmltv/main/guide.xml",
    "https://raw.githubusercontent.com/karenda-jp/etc/refs/heads/main/guides.xml"
]

tv_root = ET.Element("tv")
seen_channels = set()

for url in urls:
    try:
        print(f"Downloading: {url}")

        response = requests.get(url, timeout=60)
        response.raise_for_status()

        root = ET.fromstring(response.text)

        for child in root:
            if child.tag == "channel":
                cid = child.attrib.get("id")
                if cid not in seen_channels:
                    seen_channels.add(cid)
                    tv_root.append(child)

            elif child.tag == "programme":
                tv_root.append(child)

        print(f"Successfully merged: {url}")

    except Exception as e:
        print(f"Failed to process {url}")
        print(e)

ET.ElementTree(tv_root).write(
    "combined.xml",
    encoding="utf-8",
    xml_declaration=True
)