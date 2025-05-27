import json
import os
import requests
from typing import List, Dict, Optional

def ensure_data_directory():
    """Ensure the data directory exists."""
    if not os.path.exists("data"):
        os.makedirs("data")

def load_prompts() -> List[Dict]:
    """Load prompt-response pairs from the JSON file."""
    ensure_data_directory()
    prompts_file = "data/prompts.json"
    
    try:
        if os.path.exists(prompts_file):
            with open(prompts_file, 'r', encoding='utf-8') as f:
                prompts = json.load(f)
                return prompts if isinstance(prompts, list) else []
        else:
            # Create default prompts file if it doesn't exist
            default_prompts = create_default_prompts()
            with open(prompts_file, 'w', encoding='utf-8') as f:
                json.dump(default_prompts, f, indent=2, ensure_ascii=False)
            return default_prompts
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading prompts: {e}")
        return []

def load_evaluations() -> List[Dict]:
    """Load existing evaluations from the JSON file."""
    ensure_data_directory()
    evaluations_file = "data/evaluations.json"
    
    try:
        if os.path.exists(evaluations_file):
            with open(evaluations_file, 'r', encoding='utf-8') as f:
                evaluations = json.load(f)
                return evaluations if isinstance(evaluations, list) else []
        else:
            # Create empty evaluations file if it doesn't exist
            with open(evaluations_file, 'w', encoding='utf-8') as f:
                json.dump([], f)
            return []
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading evaluations: {e}")
        return []

def save_evaluation(evaluation: Dict) -> bool:
    """Save a new evaluation to the JSON file."""
    ensure_data_directory()
    evaluations_file = "data/evaluations.json"
    
    try:
        # Load existing evaluations
        evaluations = load_evaluations()
        
        # Add new evaluation
        evaluations.append(evaluation)
        
        # Save back to file
        with open(evaluations_file, 'w', encoding='utf-8') as f:
            json.dump(evaluations, f, indent=2, ensure_ascii=False)
        
        return True
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error saving evaluation: {e}")
        return False

def get_completion_from_hf(prompt: str) -> Optional[str]:
    """
    Generate a completion using Hugging Face Inference API.
    Requires HF_API_KEY environment variable to be set.
    """
    api_key = os.getenv("HF_API_KEY")
    
    if not api_key:
        print("HF_API_KEY not found in environment variables")
        return None
    
    # Using a popular text generation model
    model_id = "microsoft/DialoGPT-medium"
    api_url = f"https://api-inference.huggingface.co/models/{model_id}"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_length": 200,
            "temperature": 0.7,
            "do_sample": True
        }
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get("generated_text", "").strip()
            return None
        else:
            print(f"HF API Error: {response.status_code} - {response.text}")
            return None
            
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return None

def create_default_prompts() -> List[Dict]:
    """Create default prompt-response pairs for the system."""
    return [
        {
            "prompt": "Explain the concept of machine learning in simple terms.",
            "response": "Machine learning is a type of artificial intelligence where computers learn to make predictions or decisions by finding patterns in data, rather than being explicitly programmed for every possible scenario. Think of it like teaching a child to recognize animals - instead of describing every feature of every animal, you show them many pictures of different animals with labels, and they learn to identify new animals they haven't seen before."
        },
        {
            "prompt": "What are the benefits of renewable energy sources?",
            "response": "Renewable energy sources offer several key benefits: 1) Environmental - they produce little to no greenhouse gas emissions, helping combat climate change, 2) Economic - they provide long-term cost savings and energy independence, 3) Sustainability - they won't run out like fossil fuels, 4) Health - they reduce air pollution and related health problems, 5) Job creation - the renewable energy sector creates many new employment opportunities."
        },
        {
            "prompt": "How do I cook a perfect scrambled egg?",
            "response": "To make perfect scrambled eggs: 1) Crack 2-3 eggs into a bowl, add a pinch of salt and pepper, 2) Whisk thoroughly until well combined, 3) Heat a non-stick pan over low-medium heat with a little butter, 4) Pour in eggs and let them sit for 20 seconds, 5) Gently stir with a spatula, pushing from edges to center, 6) Continue stirring gently every 20 seconds, 7) Remove from heat while still slightly wet - they'll finish cooking from residual heat. The key is low heat and patience!"
        },
        {
            "prompt": "What is the capital of Australia?",
            "response": "The capital of Australia is Canberra. It's located in the Australian Capital Territory (ACT) between Sydney and Melbourne. Canberra was specifically planned and built to be the national capital, with construction beginning in 1913. Many people mistakenly think Sydney or Melbourne is the capital because they are much larger and more well-known cities."
        },
        {
            "prompt": "Explain the water cycle.",
            "response": "The water cycle is the continuous movement of water on, above, and below Earth's surface. It works in several stages: 1) Evaporation - heat from the sun turns water from oceans, lakes, and rivers into water vapor, 2) Transpiration - plants release water vapor through their leaves, 3) Condensation - water vapor cools and forms clouds, 4) Precipitation - water falls as rain, snow, or hail, 5) Collection - water flows back to bodies of water or soaks into the ground. This cycle repeats continuously, recycling Earth's water supply."
        },
        {
            "prompt": "What are some effective study techniques?",
            "response": "Here are proven study techniques: 1) Active recall - test yourself frequently instead of just re-reading, 2) Spaced repetition - review material at increasing intervals, 3) Pomodoro Technique - study in 25-minute focused sessions with breaks, 4) Elaborative interrogation - ask yourself 'why' and 'how' questions, 5) Dual coding - combine visual and verbal information, 6) Interleaving - mix different topics rather than studying one subject for hours, 7) Practice testing - take practice exams, 8) Teaching others - explain concepts to someone else."
        },
        {
            "prompt": "How does photosynthesis work?",
            "response": "Photosynthesis is how plants make food using sunlight. The process occurs mainly in leaves and involves: 1) Light absorption - chlorophyll in leaves captures sunlight, 2) Water uptake - roots absorb water from soil, 3) CO2 intake - leaves take in carbon dioxide from air through stomata, 4) Chemical reaction - using light energy, plants combine CO2 and water to create glucose (sugar) and release oxygen as a byproduct. The simple equation is: 6CO2 + 6H2O + light energy → C6H12O6 + 6O2. This process is crucial for life on Earth as it produces the oxygen we breathe."
        },
        {
            "prompt": "What are the health benefits of regular exercise?",
            "response": "Regular exercise provides numerous health benefits: 1) Cardiovascular health - strengthens heart, lowers blood pressure and cholesterol, 2) Weight management - burns calories and builds muscle, 3) Mental health - reduces stress, anxiety, and depression while boosting mood, 4) Bone health - increases bone density and reduces osteoporosis risk, 5) Immune system - strengthens immune function, 6) Sleep quality - improves sleep patterns, 7) Brain function - enhances memory and cognitive abilities, 8) Longevity - increases life expectancy and reduces chronic disease risk, 9) Energy levels - boosts daily energy and reduces fatigue."
        },
        {
            "prompt": "Explain the difference between weather and climate.",
            "response": "Weather and climate are related but distinct concepts: Weather refers to short-term atmospheric conditions in a specific place at a specific time - like today's temperature, rainfall, or wind. It can change from hour to hour or day to day. Climate, on the other hand, refers to long-term patterns of weather in a region over many years (typically 30+ years). Climate tells us what to generally expect (like 'this area is usually hot and dry in summer'), while weather tells us what's actually happening right now (like 'it's 85°F and sunny today')."
        },
        {
            "prompt": "What is artificial intelligence and how is it used today?",
            "response": "Artificial Intelligence (AI) is technology that enables machines to perform tasks that typically require human intelligence, such as learning, reasoning, and problem-solving. Today, AI is used in: 1) Virtual assistants (Siri, Alexa), 2) Recommendation systems (Netflix, Amazon), 3) Healthcare (medical diagnosis, drug discovery), 4) Transportation (self-driving cars, traffic optimization), 5) Finance (fraud detection, algorithmic trading), 6) Social media (content filtering, targeted ads), 7) Search engines (Google's search algorithms), 8) Language translation, 9) Image and speech recognition, 10) Smart home devices. AI is becoming increasingly integrated into daily life, making systems more efficient and personalized."
        },
        {
            "prompt": "How do I start learning a new programming language?",
            "response": "To start learning a new programming language effectively: 1) Choose your first language based on your goals (Python for beginners/data science, JavaScript for web development), 2) Set up your development environment (code editor, compiler/interpreter), 3) Start with basics - syntax, variables, data types, 4) Practice with small programs and exercises, 5) Use interactive learning platforms (Codecademy, freeCodeCamp), 6) Build simple projects to apply what you learn, 7) Read other people's code on GitHub, 8) Join programming communities and forums, 9) Be consistent - practice a little every day, 10) Don't rush - focus on understanding concepts rather than memorizing syntax."
        },
        {
            "prompt": "What causes earthquakes?",
            "response": "Earthquakes are caused by the sudden release of energy in Earth's crust, creating seismic waves. The main causes include: 1) Tectonic plate movement - most earthquakes occur when massive plates of Earth's crust move against each other at fault lines, 2) Volcanic activity - magma movement can trigger earthquakes, 3) Human activities - mining, fracking, or large construction projects can sometimes cause minor earthquakes, 4) Fault rupture - when stress builds up along fault lines and suddenly releases. The point where the earthquake starts underground is called the hypocenter, while the point directly above it on the surface is the epicenter. The strength is measured using the Richter scale."
        }
    ]
