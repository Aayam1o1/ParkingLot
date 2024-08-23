import fitz  # PyMuPDF

def extract_text_and_images(pdf_path):
    doc = fitz.open(pdf_path)
    text_positions = []
    image_positions = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text("dict")

        for block in text["blocks"]:
            if block["type"] == 0: 
                for line in block["lines"]:
                    for span in line["spans"]:
                        text_positions.append({
                            "text": span["text"],
                            "bbox": span["bbox"],  
                            "page": page_num
                        })
            elif block["type"] == 1: 
                for img in block["images"]:
                    bbox = img["bbox"]  
                    image_positions.append({
                        "bbox": bbox,
                        "page": page_num
                    })

    return text_positions, image_positions

def add_comment_to_pdf(pdf_path, output_path, comments):
    doc = fitz.open(pdf_path)
    
    for comment in comments:
        page = doc.load_page(comment["page"])
        rect = fitz.Rect(comment["bbox"])
        annot = page.add_freetext_annot(rect, comment["text"], fontsize=12)
        annot.set_colors(stroke=(1, 0, 0))  # Set text color to red
        annot.update()
    
    doc.save(output_path)

def find_bbox_for_coordinates(pdf_path, page_num, coordinates):
    text_positions, image_positions = extract_text_and_images(pdf_path)
    
    for position in text_positions + image_positions:
        if position["page"] == page_num:
            bbox = position["bbox"]
            if (bbox[0] <= coordinates[0] <= bbox[2] and
                bbox[1] <= coordinates[1] <= bbox[3]):
                return bbox
    return None