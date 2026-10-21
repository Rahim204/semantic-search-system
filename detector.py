import os
import PyPDF2
import docx
from sentence_transformers import SentenceTransformer, util
import numpy as np

# Load the semantic search model globally so it doesn't reload on every request
print("Loading AI Model. This might take a few seconds...")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("Model loaded successfully!")

def extract_text(file_path, filename):
    """Extracts text from PDF or DOCX files."""
    text = ""
    ext = filename.rsplit('.', 1)[1].lower()

    try:
        if ext == 'pdf':
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + " "
        elif ext == 'docx':
            doc = docx.Document(file_path)
            for para in doc.paragraphs:
                text += para.text + " "
    except Exception as e:
        print(f"Error extracting text: {e}")
        return None
        
    return text.strip()

def chunk_text(text, chunk_size=300, overlap=50):
    """Splits a massive document into overlapping word chunks."""
    words = text.split()
    chunks = []
    
    if len(words) == 0:
        return chunks

    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
        
    return chunks

def analyze_document(query, file_path, filename):
    """Orchestrates the extraction, chunking, and semantic scoring."""
    
    # 1. Extract and Chunk Text
    raw_text = extract_text(file_path, filename)
    if not raw_text:
        return {"error": "Could not extract text from the document."}
        
    chunks = chunk_text(raw_text)
    if not chunks:
        return {"error": "Document appears to be empty."}

    # 2. Vectorize the Query and Document Chunks
    query_embedding = model.encode(query, convert_to_tensor=True)
    chunk_embeddings = model.encode(chunks, convert_to_tensor=True)

    # 3. Calculate Cosine Similarity
    cosine_scores = util.cos_sim(query_embedding, chunk_embeddings)[0]
    
    # Convert PyTorch tensor back to a standard list of floats
    scores_list = cosine_scores.cpu().numpy()

    # 4. Rank the best matching chunks
    # Get indices of the top 3 scores
    top_indices = np.argsort(scores_list)[::-1][:3]
    
    top_scores = [float(scores_list[i]) for i in top_indices]
    top_chunks = [chunks[i] for i in top_indices]

    # 5. Generate Suitability Verdict based on Average Top-3 Score
    avg_top_score = sum(top_scores) / len(top_scores) if top_scores else 0
    percentage = round(avg_top_score * 100, 1)

    if percentage >= 65:
        verdict = "Highly Recommended"
    elif percentage >= 45:
        verdict = "Good for Reference"
    elif percentage >= 30:
        verdict = "Passing Mention"
    else:
        verdict = "Not Suitable"

    return {
        "score_percentage": percentage,
        "verdict": verdict,
        "evidence": [
            {"score": round(score * 100, 1), "text": chunk} 
            for score, chunk in zip(top_scores, top_chunks)
        ]
    }