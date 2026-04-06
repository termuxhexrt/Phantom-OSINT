import os
from colorama import Fore, Style
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


def extract_metadata(filepath):
    """Extract metadata from images and documents."""
    
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"  METADATA EXTRACTION: {os.path.basename(filepath)}")
    print(f"{'='*70}{Style.RESET_ALL}")
    
    if not os.path.exists(filepath):
        print(f"\n  {Fore.RED}[!] File not found: {filepath}{Style.RESET_ALL}")
        return
    
    # File basic info
    file_size = os.path.getsize(filepath)
    file_ext = os.path.splitext(filepath)[1].lower()
    
    print(f"\n  {Fore.YELLOW}[*] File Information{Style.RESET_ALL}")
    print(f"  {'─'*50}")
    print(f"    {Fore.WHITE}{'File Name':<20}: {Fore.GREEN}{os.path.basename(filepath)}{Style.RESET_ALL}")
    print(f"    {Fore.WHITE}{'File Size':<20}: {Fore.GREEN}{_human_size(file_size)}{Style.RESET_ALL}")
    print(f"    {Fore.WHITE}{'Extension':<20}: {Fore.GREEN}{file_ext}{Style.RESET_ALL}")
    print(f"    {Fore.WHITE}{'Full Path':<20}: {Fore.GREEN}{os.path.abspath(filepath)}{Style.RESET_ALL}")
    
    # Route to the right extractor
    image_exts = [".jpg", ".jpeg", ".png", ".tiff", ".tif", ".bmp", ".gif", ".webp"]
    pdf_exts = [".pdf"]
    
    if file_ext in image_exts:
        _extract_image_metadata(filepath)
    elif file_ext in pdf_exts:
        _extract_pdf_metadata(filepath)
    else:
        print(f"\n  {Fore.YELLOW}[*] Generic file - no deep metadata extraction available for {file_ext}")
        print(f"  {Fore.WHITE}    Supported: Images (JPG/PNG/TIFF/GIF), PDF{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"  METADATA EXTRACTION COMPLETE")
    print(f"{'='*70}{Style.RESET_ALL}\n")


def _extract_image_metadata(filepath):
    """Extract EXIF data from images."""
    print(f"\n  {Fore.YELLOW}[*] Image EXIF Data{Style.RESET_ALL}")
    print(f"  {'─'*50}")
    
    try:
        img = Image.open(filepath)
        
        # Basic image info
        print(f"    {Fore.WHITE}{'Format':<20}: {Fore.GREEN}{img.format}{Style.RESET_ALL}")
        print(f"    {Fore.WHITE}{'Mode':<20}: {Fore.GREEN}{img.mode}{Style.RESET_ALL}")
        print(f"    {Fore.WHITE}{'Size':<20}: {Fore.GREEN}{img.size[0]}x{img.size[1]} pixels{Style.RESET_ALL}")
        
        if hasattr(img, "info"):
            for key, val in img.info.items():
                if isinstance(val, (str, int, float)) and key not in ["exif"]:
                    print(f"    {Fore.WHITE}{str(key):<20}: {Fore.GREEN}{str(val)[:80]}{Style.RESET_ALL}")
        
        # EXIF data
        exif_data = img._getexif()
        
        if exif_data:
            print(f"\n  {Fore.YELLOW}[*] EXIF Tags{Style.RESET_ALL}")
            print(f"  {'─'*50}")
            
            gps_info = {}
            
            for tag_id, value in exif_data.items():
                tag = TAGS.get(tag_id, tag_id)
                
                if tag == "GPSInfo":
                    for gps_tag_id, gps_value in value.items():
                        gps_tag = GPSTAGS.get(gps_tag_id, gps_tag_id)
                        gps_info[gps_tag] = gps_value
                    continue
                
                # Skip binary data
                if isinstance(value, bytes):
                    if len(value) < 50:
                        try:
                            value = value.decode("utf-8", errors="ignore")
                        except Exception:
                            value = f"<binary {len(value)} bytes>"
                    else:
                        value = f"<binary {len(value)} bytes>"
                
                # Truncate long values
                val_str = str(value)
                if len(val_str) > 100:
                    val_str = val_str[:100] + "..."
                
                print(f"    {Fore.WHITE}{str(tag):<30}: {Fore.GREEN}{val_str}{Style.RESET_ALL}")
            
            # GPS data (the juicy stuff)
            if gps_info:
                print(f"\n  {Fore.RED}[!] GPS LOCATION DATA FOUND!{Style.RESET_ALL}")
                print(f"  {'─'*50}")
                
                for key, val in gps_info.items():
                    print(f"    {Fore.WHITE}{str(key):<25}: {Fore.GREEN}{val}{Style.RESET_ALL}")
                
                # Convert GPS to decimal degrees
                lat = _gps_to_decimal(
                    gps_info.get("GPSLatitude"),
                    gps_info.get("GPSLatitudeRef")
                )
                lon = _gps_to_decimal(
                    gps_info.get("GPSLongitude"),
                    gps_info.get("GPSLongitudeRef")
                )
                
                if lat and lon:
                    print(f"\n    {Fore.RED}{'Latitude':<20}: {Fore.WHITE}{lat}{Style.RESET_ALL}")
                    print(f"    {Fore.RED}{'Longitude':<20}: {Fore.WHITE}{lon}{Style.RESET_ALL}")
                    print(f"    {Fore.YELLOW}Google Maps         : {Fore.CYAN}https://www.google.com/maps?q={lat},{lon}{Style.RESET_ALL}")
                    print(f"    {Fore.YELLOW}OpenStreetMap       : {Fore.CYAN}https://www.openstreetmap.org/?mlat={lat}&mlon={lon}&zoom=15{Style.RESET_ALL}")
            else:
                print(f"\n  {Fore.WHITE}[*] No GPS data found in this image.{Style.RESET_ALL}")
        else:
            print(f"\n  {Fore.RED}[-] No EXIF data found. Image might be stripped.{Style.RESET_ALL}")
            
    except Exception as e:
        print(f"    {Fore.RED}Image metadata extraction error: {e}{Style.RESET_ALL}")


def _extract_pdf_metadata(filepath):
    """Extract metadata from PDF files."""
    print(f"\n  {Fore.YELLOW}[*] PDF Metadata{Style.RESET_ALL}")
    print(f"  {'─'*50}")
    
    try:
        from PyPDF2 import PdfReader
        
        reader = PdfReader(filepath)
        
        print(f"    {Fore.WHITE}{'Pages':<20}: {Fore.GREEN}{len(reader.pages)}{Style.RESET_ALL}")
        print(f"    {Fore.WHITE}{'Encrypted':<20}: {Fore.GREEN}{reader.is_encrypted}{Style.RESET_ALL}")
        
        metadata = reader.metadata
        
        if metadata:
            fields = {
                "Title": metadata.title,
                "Author": metadata.author,
                "Subject": metadata.subject,
                "Creator": metadata.creator,
                "Producer": metadata.producer,
                "Creation Date": metadata.creation_date,
                "Modification Date": metadata.modification_date,
            }
            
            for key, value in fields.items():
                if value:
                    print(f"    {Fore.WHITE}{key:<20}: {Fore.GREEN}{value}{Style.RESET_ALL}")
            
            # Extra metadata keys
            for key in metadata:
                if key not in ["/Title", "/Author", "/Subject", "/Creator", 
                             "/Producer", "/CreationDate", "/ModDate"]:
                    val = metadata[key]
                    if val:
                        print(f"    {Fore.WHITE}{key:<20}: {Fore.GREEN}{str(val)[:80]}{Style.RESET_ALL}")
        else:
            print(f"    {Fore.RED}[-] No metadata found in PDF.{Style.RESET_ALL}")
            
    except ImportError:
        print(f"    {Fore.RED}PyPDF2 not installed. Install with: pip install PyPDF2{Style.RESET_ALL}")
    except Exception as e:
        print(f"    {Fore.RED}PDF metadata extraction error: {e}{Style.RESET_ALL}")


def _gps_to_decimal(gps_coords, gps_ref):
    """Convert GPS coordinates from DMS (degrees, minutes, seconds) to decimal degrees."""
    if not gps_coords or not gps_ref:
        return None
    
    try:
        degrees = float(gps_coords[0])
        minutes = float(gps_coords[1])
        seconds = float(gps_coords[2])
        
        decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
        
        if gps_ref in ["S", "W"]:
            decimal = -decimal
        
        return round(decimal, 7)
    except Exception:
        return None


def _human_size(size_bytes):
    """Convert bytes to human readable format."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"
