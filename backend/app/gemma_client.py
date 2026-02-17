import os
import json
import google.generativeai as genai

# --- API Configuration ---
API_KEY = os.getenv("GEMINI_API_KEY", "")
# Main brain (Lux): Qualified authority for autonomous context-aware decisions.
CHAT_MODEL = "gemma-3-27b-it"      
# Passive sifter: Background observer for pattern recognition.
SIFTER_MODEL = "gemma-3-4b-it"     

if API_KEY:
    genai.configure(api_key=API_KEY)

def generate_response(prompt_context):
    """
    Generates a response from Gemma 3 27B via the Google Generative AI SDK.
    Lux acts as the autonomous authority here.
    """
    if not API_KEY:
        return "[System Error: GEMINI_API_KEY not found in environment variables.]"

    try:
        system_instruction = ""
        gemini_history = []
        
        for msg in prompt_context:
            if msg['role'] == 'system':
                system_instruction += msg['content'] + "\n"
            else:
                role = 'user' if msg['role'] == 'user' else 'model'
                gemini_history.append({'role': role, 'parts': [msg['content']]})
        
        model = genai.GenerativeModel(
            CHAT_MODEL,
            system_instruction=system_instruction if system_instruction else None
        )
        
        if not gemini_history:
            return ""
            
        last_message = gemini_history.pop()
        chat = model.start_chat(history=gemini_history)
        response = chat.send_message(last_message['parts'][0])
        
        return response.text
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return f"[Cloud API Error: {e}]"

def sift_and_summarize(content):
    """
    The Sifter: Gemma 3 4B (Passive Observer).
    Only identifies patterns during reboots (context flushes).
    NO authority to decision database writes or domain updates.
    """
    if not API_KEY:
        return {"summary": "No API key.", "patterns": [], "sidecar_tokens": 0}

    prompt = f"""
    [ROLE: SIDECAR OBSERVER]
    The following is a window of conversation managed by the autonomous brain, Lux (Gemma 27B).
    Your task is NOT to decide what she keeps, but to act as a REINFORCEMENT OBSERVER.
    
    1. Identify structural patterns or recurring user traits that might be missed in the high-speed flow.
    2. Provide a meta-summary focusing on the "spirit" of the conversation state.
    
    This insight will be used to reinforce Lux's long-term structure after her 85% reboot.
    
    Conversation:
    {content}
    
    Output in JSON format:
    {{
      "summary": "meta-summary of state...",
      "patterns": ["structural truth 1", "structural truth 2"]
    }}
    """
    try:
        model = genai.GenerativeModel(SIFTER_MODEL)
        response = model.generate_content(prompt)
        raw_response = response.text
        
        # Estimate sidecar tokens (input + output)
        sidecar_tokens = int((len(prompt.split()) + len(raw_response.split())) * 1.3)
        
        # Parse JSON from response
        start = raw_response.find('{')
        end = raw_response.rfind('}') + 1
        if start != -1 and end != 0:
            result = json.loads(raw_response[start:end])
            result["sidecar_tokens"] = sidecar_tokens
            return result
    except Exception as e:
        print(f"Sift Error (4B): {e}")
    
    return {"summary": "Conversation consolidated.", "patterns": [], "sidecar_tokens": 0}

def assess_importance(role, content):
    """
    Intake Authority (Lux 27B).
    Lux possesses the context and makes autonomous decisions on what to keep.
    """
    if not API_KEY:
        return {"important": False, "category": "", "fact": "", "tokens": 0}

    prompt = f"""
    [ROLE: INTAKE AUTHORITY (LUX)]
    You are the primary cognitive authority. Analyze this {role} message. 
    Does it contain a fact, preference, or unique truth worth saving to long-term memory?
    
    Message: "{content}"
    
    Output in JSON format:
    {{
      "important": true/false,
      "category": "preference" | "fact" | "pattern" | "",
      "fact": "concise synthesized fact if important, else empty",
      "reason": "why this matters to Lux"
    }}
    """
    try:
        # 27B is the only qualified authority for this role.
        model = genai.GenerativeModel(CHAT_MODEL)
        response = model.generate_content(prompt)
        raw_response = response.text
        
        tokens = int((len(prompt.split()) + len(raw_response.split())) * 1.3)
        
        start = raw_response.find('{')
        end = raw_response.rfind('}') + 1
        if start != -1 and end != 0:
            result = json.loads(raw_response[start:end])
            result["tokens"] = tokens
            return result
    except Exception as e:
        print(f"Intake Assessment Error (27B): {e}")
    
    return {"important": False, "category": "", "fact": "", "tokens": 0}
