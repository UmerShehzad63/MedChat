import os
import re
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Load explicitly to ensure we have the API key
load_dotenv()

# We import the functions from our existing LLM architecture
try:
    from connect_llm_with_memory import answer_question, embedding_model, db
except ImportError as e:
    print(f"Error importing LLM modules: {e}")
    # Provide dummy implementations for testing UI if needed
    def answer_question(q): return "Mock response due to missing imports."

app = Flask(__name__)

def format_ai_response(text):
    """
    Parses the raw text response from the LLM and formats it
    into the HTML structure required by the premium UI.
    """
    # 1. Extract Confidence
    confidence_match = re.search(r'\*\*Confidence:\*\*\s*(High|Medium|Low)', text, re.IGNORECASE)
    confidence = confidence_match.group(1) if confidence_match else "Medium"
    confidence_class = f"conf-{confidence.lower()}"
    
    # 2. Extract Sources
    sources_match = re.search(r'\*\*Sources:\*\*(.*?)(?=\*\*|$)', text, re.IGNORECASE | re.DOTALL)
    sources_html = ""
    if sources_match:
        sources_text = sources_match.group(1).strip()
        # Find individual sources (usually bullet points)
        source_items = re.findall(r'- (.*?)(?:\n|$)', sources_text)
        
        sources_html += '<div class="ai-section-label">SOURCES</div>'
        sources_html += '<div class="sources-container">'
        
        if not source_items:
            # Maybe they aren't bulleted, just split by newline
            source_items = [s.strip() for s in sources_text.split('\n') if s.strip()]
            
        for source in source_items:
            # Clean up the source string to look like "filename - Page X"
            clean_source = source.replace('**', '').replace('Source:', '').strip()
            # Try to format nice chips
            sources_html += f'''
                <div class="source-chip">
                    <svg viewBox="0 0 24 24"><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg>
                    {clean_source}
                </div>
            '''
        sources_html += '</div>'
    
    # 3. Extract main content (everything before "**Sources:**" or "**Confidence:**")
    main_content = text
    if '**Sources:**' in main_content:
        main_content = main_content.split('**Sources:**')[0]
    if '**Confidence:**' in main_content:
        main_content = main_content.split('**Confidence:**')[0]
        
    main_content = main_content.strip()
    
    # 4. Process main content into Clinical Answer and Supporting Evidence
    # The LLM often prefixes its output with these headers
    clinical_answer = []
    evidence_blocks = []
    
    # Split by double newline to get distinct paragraphs/blocks
    paragraphs = main_content.split('\n\n')
    
    current_section = "clinical"  # default
    
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
            
        # Detect section headers
        if p.startswith('Clinical Answer:'):
            p = p.replace('Clinical Answer:', '').strip()
            current_section = "clinical"
        elif p.startswith('Supporting Evidence:'):
            p = p.replace('Supporting Evidence:', '').strip()
            current_section = "evidence"
            
        # Very basic formatting of bold text
        p = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', p)
        
        if not p:
            continue
            
        if current_section == "evidence":
            # Clean up leading hyphens for evidence blocks
            if p.startswith('- '):
                p = p[2:].strip()
            # If multiple evidence points are packed in one string separated by "- "
            evidence_points = [x.strip() for x in p.split('- ') if x.strip()]
            for point in evidence_points:
                # Filter out lines that are just the LLM repeating its prompt structure
                point_lower = point.lower()
                if any(x in point_lower for x in ["limitations:", "confidence:", "sources:", "source:"]):
                    continue
                    
                # Add quotes around it if it's not already quoted, as it's meant to be evidence
                if not point.startswith('"') and not point.endswith('"'):
                    evidence_blocks.append(f'"{point}"')
                else:
                    evidence_blocks.append(point)
        else:
            # Clinical answer section
            if p.startswith('- '):
                # Format lists
                list_items = re.findall(r'- (.*?)(?:\n|$)', p)
                if list_items:
                    ul = "<ul>" + "".join([f"<li>{item}</li>" for item in list_items]) + "</ul>"
                    clinical_answer.append(ul)
                else:
                    clinical_answer.append(f"<p>{p}</p>")
            else:
                clinical_answer.append(f"<p>{p}</p>")

    # Assemble final HTML
    html = f'''
        {"".join(clinical_answer)}
    '''
    
    if evidence_blocks:
        html += '<div class="ai-section-label">SUPPORTING EVIDENCE</div>'
        for block in evidence_blocks:
            html += f'<div class="ai-evidence-block">{block}</div>'
            
    # Add Limitations (Disclaimer)
    html += '''
        <div class="ai-section-label ai-limits-label">LIMITATIONS</div>
        <div class="ai-limits-text">
            This information is extracted from available medical literature for educational purposes. 
            It does not constitute a medical diagnosis or treatment plan.
        </div>
    '''
    
    # Add Confidence Badge
    html += f'''
        <div style="margin-top: 24px;">
            <span style="font-size: 11px; color: var(--text-secondary);">CONFIDENCE SCORE:</span>
            <span class="confidence-badge {confidence_class}">{confidence}</span>
        </div>
    '''
    
    # Add Sources
    html += sources_html
    
    return html

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_query = data.get('query')
        
        if not user_query:
            return jsonify({'error': 'No query provided'}), 400
            
        # Call the LangChain RAG pipeline
        raw_response = answer_question(user_query)
        
        # Format the raw markdown response into our premium HTML structure
        formatted_html = format_ai_response(raw_response)
        
        return jsonify({
            'html': formatted_html,
            'raw': raw_response
        })
        
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify({
            'error': str(e),
            'html': f'<p style="color: var(--danger)">An error occurred: {str(e)}</p>'
        }), 500

@app.route('/clear', methods=['POST'])
def clear():
    # In a real app with sessions, we'd clear memory here.
    # Currently connect_llm_with_memory manages its own state
    # or creates a new chain, so this is just a placeholder for UI reset.
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    print("Starting MedChat Flask API...")
    app.run(host='0.0.0.0', port=5000, debug=True)
