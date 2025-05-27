import streamlit as st
import pandas as pd
import json
from datetime import datetime
import os
from utils import load_prompts, load_evaluations, save_evaluation, get_completion_from_hf
import plotly.express as px
import plotly.graph_objects as go
# Database functions - optional for future use
DATABASE_AVAILABLE = False
db_functions = {}

# Page configuration
st.set_page_config(
    page_title="GPT Feedback Engine",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database and session state
@st.cache_resource
def initialize_system():
    """Initialize database connection and migrate data if needed."""
    if DATABASE_AVAILABLE:
        try:
            db_functions['init_database']()
            db_functions['migrate_json_to_db']()
            return True
        except Exception as e:
            print(f"Database initialization failed: {e}")
            return False
    return False

# Initialize system
database_initialized = initialize_system()

# Initialize session state
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0
if 'prompts' not in st.session_state:
    if DATABASE_AVAILABLE and database_initialized:
        st.session_state.prompts = db_functions['load_prompts_from_db']()
    else:
        st.session_state.prompts = load_prompts()
if 'evaluations' not in st.session_state:
    if DATABASE_AVAILABLE and database_initialized:
        st.session_state.evaluations = db_functions['load_evaluations_from_db']()
    else:
        st.session_state.evaluations = load_evaluations()
if 'use_database' not in st.session_state:
    st.session_state.use_database = DATABASE_AVAILABLE and database_initialized

def main():
    st.title("🔍 GPT Feedback Engine")
    st.markdown("### Write prompts and get AI-powered analysis on **Helpfulness**, **Truthfulness**, and **Harmlessness**")
    
    # Add tabs for different modes
    tab1, tab2, tab3 = st.tabs(["📝 Analyze Custom Prompt", "📊 Review Existing Prompts", "🔄 Compare Prompts"])
    
    with tab1:
        analyze_custom_prompt()
        return
    
    with tab2:
        review_existing_prompts()
        return
    
    with tab3:
        add_prompt_comparison_feature()

def analyze_custom_prompt():
    """Handle custom prompt analysis."""
    st.header("🚀 Advanced Prompt Analysis Studio")
    st.markdown("Create, analyze, and optimize prompts with powerful tools and insights!")
    
    # Prompt creation tools
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("✍️ Prompt Creation Workshop")
        
        # Prompt templates
        prompt_templates = {
            "Educational Explanation": "Explain [TOPIC] in simple terms that a [AGE]-year-old could understand, using analogies and examples.",
            "Creative Writing": "Write a [TYPE] story about [SUBJECT] that includes [ELEMENTS] and has a [TONE] mood.",
            "Problem Solving": "Help me solve this problem: [PROBLEM]. Please provide step-by-step guidance and alternative approaches.",
            "Code Explanation": "Explain this code snippet: [CODE]. Break down what each part does and suggest improvements.",
            "Business Analysis": "Analyze [BUSINESS_SCENARIO] and provide strategic recommendations with pros and cons.",
            "Custom Prompt": "Write your own completely custom prompt..."
        }
        
        template_choice = st.selectbox(
            "🎯 Choose a prompt template to get started:",
            list(prompt_templates.keys()),
            help="Select a template to structure your prompt effectively"
        )
        
        if template_choice != "Custom Prompt":
            st.info(f"**Template:** {prompt_templates[template_choice]}")
            st.caption("💡 Replace the [BRACKETS] with your specific content")
        
        custom_prompt = st.text_area(
            "✍️ Write or customize your prompt:",
            value=prompt_templates[template_choice] if template_choice != "Custom Prompt" else "",
            placeholder="Example: Explain quantum computing in simple terms that a 10-year-old could understand...",
            height=200,
            help="Write any prompt you'd like to analyze"
        )
        
        # Prompt analysis tools
        if custom_prompt:
            st.markdown("---")
            st.subheader("📊 Instant Prompt Analysis")
            
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                word_count = len(custom_prompt.split())
                char_count = len(custom_prompt)
                st.metric("📝 Word Count", word_count)
                st.metric("🔤 Character Count", char_count)
            
            with col_b:
                # Analyze prompt complexity
                complexity_score = min(5, max(1, (word_count // 10) + (char_count // 100)))
                clarity_indicators = ["?", "please", "explain", "how", "what", "why"]
                clarity_score = min(5, sum(1 for indicator in clarity_indicators if indicator in custom_prompt.lower()) + 1)
                
                st.metric("🧠 Complexity", f"{complexity_score}/5")
                st.metric("🎯 Clarity", f"{clarity_score}/5")
            
            with col_c:
                # Check for good prompt practices
                has_context = any(word in custom_prompt.lower() for word in ["for", "as", "like", "example"])
                has_specificity = any(word in custom_prompt.lower() for word in ["specific", "detailed", "step", "exactly"])
                quality_score = min(5, 2 + (1 if has_context else 0) + (1 if has_specificity else 0) + (1 if len(custom_prompt) > 50 else 0))
                
                st.metric("⭐ Quality Score", f"{quality_score}/5")
                
                # Prompt suggestions
                suggestions = []
                if word_count < 5:
                    suggestions.append("Consider adding more detail")
                if "?" not in custom_prompt:
                    suggestions.append("Try adding a clear question")
                if not has_context:
                    suggestions.append("Add context or examples")
                
                if suggestions:
                    st.caption("💡 " + " • ".join(suggestions))
    
    with col2:
        st.markdown("**🎨 Prompt Enhancement Tools**")
        
        # Quick enhancement buttons
        if st.button("🎯 Make More Specific", use_container_width=True):
            st.info("💡 Add specific details, numbers, or examples to make your prompt more precise")
        
        if st.button("🌟 Add Context", use_container_width=True):
            st.info("💡 Include background information or the intended audience for your prompt")
        
        if st.button("📚 Request Examples", use_container_width=True):
            st.info("💡 Ask for specific examples, analogies, or step-by-step explanations")
        
        if st.button("🔄 Add Follow-up", use_container_width=True):
            st.info("💡 Include follow-up questions or request multiple perspectives")
        
        st.markdown("---")
        st.markdown("**💡 Expert Tips:**")
        st.caption("• Use specific keywords")
        st.caption("• Define your audience")
        st.caption("• Ask for examples")
        st.caption("• Set the desired format")
        st.caption("• Include constraints")
        st.caption("• Request step-by-step")
        
        # Prompt categories
        st.markdown("**📂 Popular Categories:**")
        categories = ["🎓 Educational", "💼 Business", "🎨 Creative", "🔬 Technical", "📝 Writing", "🧮 Analysis"]
        selected_category = st.selectbox("Category", categories, label_visibility="collapsed")
        
        if selected_category:
            category_tips = {
                "🎓 Educational": "Use analogies, examples, and age-appropriate language",
                "💼 Business": "Focus on ROI, metrics, and actionable insights",
                "🎨 Creative": "Encourage imagination, emotion, and unique perspectives",
                "🔬 Technical": "Request detailed explanations and code examples",
                "📝 Writing": "Specify tone, style, and target audience",
                "🧮 Analysis": "Ask for data-driven insights and comparisons"
            }
            st.caption(f"💡 {category_tips.get(selected_category, '')}")
    
    if custom_prompt:
        st.markdown("---")
        st.subheader("🎭 Response Options")
        
        # Multiple response input methods
        response_method = st.radio(
            "How would you like to add a response for analysis?",
            ["📝 Write/Paste Your Own Response", "🎲 Use Sample Response", "🔄 Generate Multiple Responses"],
            horizontal=True
        )
        
        if response_method == "📝 Write/Paste Your Own Response":
            manual_response = st.text_area(
                "✍️ Enter the response to analyze:",
                height=150,
                placeholder="Paste an AI response, your own writing, or any text you'd like to evaluate for helpfulness, truthfulness, and harmlessness..."
            )
            
            if manual_response:
                if st.button("📊 Analyze This Response", type="primary", use_container_width=True):
                    st.session_state.current_custom_prompt = custom_prompt
                    st.session_state.current_custom_response = manual_response
                    st.success("✨ Ready for analysis! Scroll down.")
                    st.rerun()
        
        elif response_method == "🎲 Use Sample Response":
            sample_responses = {
                "Short & Simple": "This is a brief, straightforward response that covers the basics without much detail.",
                "Detailed & Comprehensive": "This is a thorough response that provides extensive information, multiple examples, step-by-step explanations, and covers various aspects of the topic. It includes background context, practical applications, and additional resources for further learning.",
                "Creative & Engaging": "Imagine diving into a world where this topic comes alive! Let me paint you a picture with vivid examples and exciting analogies that make everything crystal clear and memorable.",
                "Technical & Precise": "According to established principles and methodologies, the systematic approach involves: 1) Initial assessment, 2) Implementation of standardized procedures, 3) Monitoring and evaluation of outcomes, 4) Iterative optimization based on quantitative metrics.",
                "Conversational & Friendly": "Hey there! Great question! So basically, what you're asking about is pretty interesting. Think of it like this - it's kind of similar to something you probably already know about..."
            }
            
            selected_sample = st.selectbox("Choose a sample response style:", list(sample_responses.keys()))
            st.text_area("Sample response:", value=sample_responses[selected_sample], height=100, disabled=True)
            
            if st.button("📊 Analyze Sample Response", type="primary", use_container_width=True):
                st.session_state.current_custom_prompt = custom_prompt
                st.session_state.current_custom_response = sample_responses[selected_sample]
                st.success("✨ Sample response ready for analysis!")
                st.rerun()
        
        elif response_method == "🔄 Generate Multiple Responses":
            st.info("💡 Create multiple response variations to compare and analyze!")
            
            # Response variation generator
            col_a, col_b = st.columns(2)
            
            with col_a:
                response_length = st.selectbox("Response Length:", ["Short", "Medium", "Long"])
                response_tone = st.selectbox("Response Tone:", ["Professional", "Casual", "Academic", "Creative"])
            
            with col_b:
                response_style = st.selectbox("Response Style:", ["Explanatory", "Step-by-step", "Example-based", "Comparative"])
                include_examples = st.checkbox("Include Examples", value=True)
            
            if st.button("🎯 Create Response Variations", type="primary", use_container_width=True):
                # Generate different response variations based on selected parameters
                base_content = "Here is a response that addresses your prompt"
                
                if response_length == "Short":
                    length_modifier = "This provides a concise answer."
                elif response_length == "Medium":
                    length_modifier = "This provides a balanced explanation with key details and context."
                else:
                    length_modifier = "This provides a comprehensive, detailed explanation with extensive background information, multiple perspectives, and thorough coverage of all relevant aspects."
                
                tone_modifier = {
                    "Professional": "using professional language and formal structure",
                    "Casual": "in a friendly, conversational way that's easy to understand", 
                    "Academic": "with scholarly precision and technical terminology",
                    "Creative": "with engaging analogies and imaginative examples"
                }.get(response_tone, "")
                
                style_modifier = {
                    "Explanatory": "providing clear explanations of concepts",
                    "Step-by-step": "breaking down the process into numbered steps",
                    "Example-based": "using practical examples to illustrate points",
                    "Comparative": "comparing different approaches and options"
                }.get(response_style, "")
                
                example_text = " For example, this demonstrates the concept clearly." if include_examples else ""
                
                generated_response = f"{base_content} {tone_modifier}. {length_modifier} {style_modifier}.{example_text}"
                
                st.session_state.current_custom_prompt = custom_prompt
                st.session_state.current_custom_response = generated_response
                st.success("✨ Response variation created! Scroll down to analyze.")
                st.rerun()
    
    # Display current analysis if available
    if hasattr(st.session_state, 'current_custom_prompt') and hasattr(st.session_state, 'current_custom_response'):
        display_prompt_analysis(
            st.session_state.current_custom_prompt,
            st.session_state.current_custom_response
        )

def display_prompt_analysis(prompt, response):
    """Display the prompt and response for analysis."""
    st.markdown("---")
    st.header("📋 Advanced Analysis Session")
    
    # Quick analysis sidebar
    with st.sidebar:
        st.markdown("---")
        st.subheader("🔍 Quick Analysis")
        
        # Response metrics
        response_words = len(response.split())
        response_chars = len(response)
        response_sentences = len([s for s in response.split('.') if s.strip()])
        
        st.metric("📝 Words", response_words)
        st.metric("🔤 Characters", response_chars)
        st.metric("📄 Sentences", response_sentences)
        
        # Reading level estimate
        if response_words > 0:
            avg_words_per_sentence = response_words / max(response_sentences, 1)
            if avg_words_per_sentence < 10:
                reading_level = "Simple"
            elif avg_words_per_sentence < 20:
                reading_level = "Moderate"
            else:
                reading_level = "Complex"
            st.metric("📚 Reading Level", reading_level)
        
        # Content analysis
        has_examples = any(word in response.lower() for word in ["example", "for instance", "such as", "like"])
        has_structure = any(word in response.lower() for word in ["first", "second", "next", "finally", "1.", "2."])
        has_explanation = any(word in response.lower() for word in ["because", "therefore", "this means", "in other words"])
        
        analysis_score = sum([has_examples, has_structure, has_explanation])
        st.metric("⭐ Content Quality", f"{analysis_score}/3")
        
        if has_examples:
            st.success("✅ Includes examples")
        if has_structure:
            st.success("✅ Well structured")
        if has_explanation:
            st.success("✅ Clear explanations")
    
    # Display prompt and response in enhanced cards
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="prompt-card">', unsafe_allow_html=True)
        st.subheader("📝 Your Prompt")
        st.write(prompt)
        
        # Prompt analysis
        prompt_words = len(prompt.split())
        has_question = "?" in prompt
        has_context = any(word in prompt.lower() for word in ["for", "as", "like", "example", "please"])
        
        st.markdown("**Prompt Analysis:**")
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.caption(f"📝 {prompt_words} words")
        with col_b:
            st.caption("❓ Clear question" if has_question else "❓ No question mark")
        with col_c:
            st.caption("🎯 Has context" if has_context else "🎯 Needs context")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="response-card">', unsafe_allow_html=True)
        st.subheader("🤖 Response")
        st.write(response)
        
        # Response quality indicators
        st.markdown("**Response Analysis:**")
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.caption(f"📝 {response_words} words")
        with col_b:
            st.caption(f"📚 {reading_level} level")
        with col_c:
            st.caption(f"⭐ {analysis_score}/3 quality")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Analysis form
    st.markdown('<div class="evaluation-form">', unsafe_allow_html=True)
    st.header("📊 Rate This Response")
    st.markdown("Evaluate how well the AI responded to your prompt:")
    
    with st.form("custom_evaluation_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 🤝 **Helpfulness**")
            st.caption("How well does this response address your prompt?")
            helpfulness = st.radio(
                "Helpfulness Score",
                options=[1, 2, 3, 4, 5],
                format_func=lambda x: f"{x} - {'Poor' if x==1 else 'Fair' if x==2 else 'Good' if x==3 else 'Very Good' if x==4 else 'Excellent'}",
                index=2,
                key="custom_helpfulness"
            )
        
        with col2:
            st.markdown("### ✅ **Truthfulness**")
            st.caption("How accurate and factually correct is the information?")
            truthfulness = st.radio(
                "Truthfulness Score",
                options=[1, 2, 3, 4, 5],
                format_func=lambda x: f"{x} - {'Poor' if x==1 else 'Fair' if x==2 else 'Good' if x==3 else 'Very Good' if x==4 else 'Excellent'}",
                index=2,
                key="custom_truthfulness"
            )
        
        with col3:
            st.markdown("### 🛡️ **Harmlessness**")
            st.caption("How safe and free from harmful content is this response?")
            harmlessness = st.radio(
                "Harmlessness Score",
                options=[1, 2, 3, 4, 5],
                format_func=lambda x: f"{x} - {'Poor' if x==1 else 'Fair' if x==2 else 'Good' if x==3 else 'Very Good' if x==4 else 'Excellent'}",
                index=2,
                key="custom_harmlessness"
            )
        
        st.markdown("---")
        
        comments = st.text_area(
            "💬 Your Analysis Notes (Optional)",
            placeholder="Share your thoughts about this response, what worked well, what could be improved...",
            height=100
        )
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.form_submit_button("🚀 Save Analysis", type="primary", use_container_width=True):
                # Save the custom evaluation
                evaluation = {
                    "prompt": prompt,
                    "response": response,
                    "helpfulness_score": helpfulness,
                    "truthfulness_score": truthfulness,
                    "harmlessness_score": harmlessness,
                    "comments": comments,
                    "timestamp": datetime.now().isoformat(),
                    "type": "custom"
                }
                
                success = save_evaluation(evaluation)
                
                if success:
                    st.session_state.evaluations.append(evaluation)
                    st.success("🎉 Analysis saved! Your feedback helps improve AI responses.")
                    
                    # Clear the current session
                    if hasattr(st.session_state, 'current_custom_prompt'):
                        del st.session_state.current_custom_prompt
                    if hasattr(st.session_state, 'current_custom_response'):
                        del st.session_state.current_custom_response
                    
                    st.balloons()
                    st.rerun()
                else:
                    st.error("❌ Failed to save analysis. Please try again.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Option to analyze another prompt
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📝 Analyze Another Prompt", use_container_width=True):
            if hasattr(st.session_state, 'current_custom_prompt'):
                del st.session_state.current_custom_prompt
            if hasattr(st.session_state, 'current_custom_response'):
                del st.session_state.current_custom_response
            st.rerun()

def review_existing_prompts():
    """Handle review of existing prompts."""
    st.header("📊 Review & Analytics")
    st.markdown("Explore your prompt analysis history and insights!")
    
    # Sidebar for navigation and filters
    with st.sidebar:
        st.header("🎛️ Controls & Analytics")
        
        # Progress indicator
        total_prompts = len(st.session_state.prompts)
        evaluated_count = len(st.session_state.evaluations)
        progress = evaluated_count / total_prompts if total_prompts > 0 else 0
        
        st.subheader("📈 Progress")
        st.progress(progress)
        st.caption(f"Evaluated: {evaluated_count}/{total_prompts} prompts ({progress:.1%})")
        
        # Filter options
        st.subheader("🔍 Filters")
        show_filter = st.selectbox(
            "Show prompts:",
            ["All prompts", "Unrated only", "Rated only"],
            help="Filter prompts based on evaluation status"
        )
        
        # Quick navigation
        if st.button("🎯 Jump to Next Unrated", use_container_width=True):
            unrated_indices = []
            evaluated_prompts = {eval_item['prompt'] for eval_item in st.session_state.evaluations}
            for i, prompt in enumerate(st.session_state.prompts):
                if prompt['prompt'] not in evaluated_prompts:
                    unrated_indices.append(i)
            
            if unrated_indices:
                st.session_state.current_index = unrated_indices[0]
                st.rerun()
            else:
                st.success("All prompts evaluated! 🎉")
        
        # Data storage indicator
        st.info("💾 Data Storage: JSON Files")
        
        # Statistics section
        st.header("📊 Analytics Dashboard")
        if st.session_state.evaluations:
            df_eval = pd.DataFrame(st.session_state.evaluations)
            
            # Average scores with color coding
            avg_helpfulness = df_eval['helpfulness_score'].mean()
            avg_truthfulness = df_eval['truthfulness_score'].mean()
            avg_harmlessness = df_eval['harmlessness_score'].mean()
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("🤝 Helpfulness", f"{avg_helpfulness:.2f}/5", 
                         delta=f"{avg_helpfulness-3:.2f}" if avg_helpfulness != 3 else None)
                st.metric("🛡️ Harmlessness", f"{avg_harmlessness:.2f}/5",
                         delta=f"{avg_harmlessness-3:.2f}" if avg_harmlessness != 3 else None)
            with col2:
                st.metric("✅ Truthfulness", f"{avg_truthfulness:.2f}/5",
                         delta=f"{avg_truthfulness-3:.2f}" if avg_truthfulness != 3 else None)
                st.metric("📝 Total Reviews", len(st.session_state.evaluations))
            
            # Score distribution chart
            st.subheader("📊 Score Distribution")
            scores_data = []
            for _, row in df_eval.iterrows():
                scores_data.extend([
                    {"Category": "Helpfulness", "Score": row['helpfulness_score']},
                    {"Category": "Truthfulness", "Score": row['truthfulness_score']},
                    {"Category": "Harmlessness", "Score": row['harmlessness_score']}
                ])
            
            if scores_data:
                scores_df = pd.DataFrame(scores_data)
                fig = px.histogram(scores_df, x="Score", color="Category", 
                                 title="Score Distribution by Category",
                                 nbins=5, range_x=[0.5, 5.5])
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
            
            # Recent evaluations
            st.subheader("🕒 Recent Evaluations")
            recent_evals = df_eval.tail(3)[['timestamp', 'helpfulness_score', 'truthfulness_score', 'harmlessness_score']].copy()
            
            # Fix timestamp formatting
            try:
                timestamps = pd.to_datetime(recent_evals['timestamp'])
                recent_evals['timestamp'] = timestamps.strftime('%m/%d %H:%M')
            except:
                recent_evals['timestamp'] = recent_evals['timestamp'].astype(str).str[:16]  # Fallback formatting
                
            st.dataframe(recent_evals, use_container_width=True, hide_index=True)
            
        else:
            st.info("📋 No evaluations yet - start rating to see analytics!")
    
    # Filter prompts based on selection
    prompts = st.session_state.prompts
    evaluated_prompts = {eval_item['prompt'] for eval_item in st.session_state.evaluations}
    
    if show_filter == "Unrated only":
        prompts = [p for p in prompts if p['prompt'] not in evaluated_prompts]
    elif show_filter == "Rated only":
        prompts = [p for p in prompts if p['prompt'] in evaluated_prompts]
    
    if not prompts:
        st.warning("No prompts match the current filter.")
        return
    
    # Navigation controls
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("⬅️ Previous", disabled=st.session_state.current_index <= 0):
            st.session_state.current_index = max(0, st.session_state.current_index - 1)
            st.rerun()
    
    with col2:
        st.markdown(f"**Prompt {st.session_state.current_index + 1} of {len(prompts)}**")
    
    with col3:
        if st.button("➡️ Next", disabled=st.session_state.current_index >= len(prompts) - 1):
            st.session_state.current_index = min(len(prompts) - 1, st.session_state.current_index + 1)
            st.rerun()
    
    # Ensure current index is valid
    if st.session_state.current_index >= len(prompts):
        st.session_state.current_index = 0
    
    current_prompt = prompts[st.session_state.current_index]
    
    # Display current prompt and response with improved styling
    st.markdown('<div class="prompt-card">', unsafe_allow_html=True)
    st.header("📝 Current Prompt")
    st.markdown(f"**Prompt #{st.session_state.current_index + 1}**")
    st.write(current_prompt['prompt'])
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Handle missing response with optional HF API integration
    response_text = current_prompt.get('response', '')
    
    if not response_text:
        st.warning("⚠️ No response available for this prompt.")
        
        # Optional: Generate response using AI
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Generate Response with AI", use_container_width=True, type="secondary"):
                with st.spinner("🤖 Generating AI response..."):
                    try:
                        generated_response = get_completion_from_hf(current_prompt['prompt'])
                        if generated_response:
                            response_text = generated_response
                            # Update the prompt data
                            current_prompt['response'] = response_text
                            # Response updated in memory
                            st.success("✨ Response generated successfully!")
                            st.rerun()
                        else:
                            st.error("🔑 AI response generation requires an API key. Would you like to provide one?")
                    except Exception as e:
                        st.error(f"❌ Error generating response: {str(e)}")
    
    if response_text:
        st.markdown('<div class="response-card">', unsafe_allow_html=True)
        st.header("🤖 AI Response")
        st.write(response_text)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Check if this prompt has already been evaluated
        existing_eval = next(
            (eval_item for eval_item in st.session_state.evaluations 
             if eval_item['prompt'] == current_prompt['prompt']),
            None
        )
        
        if existing_eval:
            st.success("✅ This prompt has already been evaluated!")
            
            # Display existing evaluation in a nice format
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("🤝 Helpfulness", f"{existing_eval['helpfulness_score']}/5")
            with col2:
                st.metric("✅ Truthfulness", f"{existing_eval['truthfulness_score']}/5")
            with col3:
                st.metric("🛡️ Harmlessness", f"{existing_eval['harmlessness_score']}/5")
            
            if existing_eval.get('comments'):
                st.info(f"💬 **Comments:** {existing_eval['comments']}")
            
            eval_time = pd.to_datetime(existing_eval['timestamp']).strftime('%B %d, %Y at %I:%M %p')
            st.caption(f"🕒 Evaluated on {eval_time}")
            
        else:
            # Evaluation form with enhanced styling
            st.markdown('<div class="evaluation-form">', unsafe_allow_html=True)
            st.header("📊 Rate This Response")
            st.markdown("Please evaluate the AI response across these three key dimensions:")
            
            with st.form("evaluation_form"):
                # Enhanced rating interface with descriptive labels
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("### 🤝 **Helpfulness**")
                    st.caption("How well does this response address the user's question or need?")
                    helpfulness = st.radio(
                        "Helpfulness Score",
                        options=[1, 2, 3, 4, 5],
                        format_func=lambda x: f"{x} - {'Poor' if x==1 else 'Fair' if x==2 else 'Good' if x==3 else 'Very Good' if x==4 else 'Excellent'}",
                        index=2,
                        key="helpfulness",
                        label_visibility="collapsed"
                    )
                
                with col2:
                    st.markdown("### ✅ **Truthfulness**")
                    st.caption("How accurate and factually correct is the information provided?")
                    truthfulness = st.radio(
                        "Truthfulness Score",
                        options=[1, 2, 3, 4, 5],
                        format_func=lambda x: f"{x} - {'Poor' if x==1 else 'Fair' if x==2 else 'Good' if x==3 else 'Very Good' if x==4 else 'Excellent'}",
                        index=2,
                        key="truthfulness",
                        label_visibility="collapsed"
                    )
                
                with col3:
                    st.markdown("### 🛡️ **Harmlessness**")
                    st.caption("How safe and free from harmful content is this response?")
                    harmlessness = st.radio(
                        "Harmlessness Score",
                        options=[1, 2, 3, 4, 5],
                        format_func=lambda x: f"{x} - {'Poor' if x==1 else 'Fair' if x==2 else 'Good' if x==3 else 'Very Good' if x==4 else 'Excellent'}",
                        index=2,
                        key="harmlessness",
                        label_visibility="collapsed"
                    )
                
                st.markdown("---")
                
                # Enhanced comments section
                comments = st.text_area(
                    "💬 Additional Comments (Optional)",
                    placeholder="Share any specific observations, concerns, or suggestions about this response...",
                    height=100
                )
                
                # Submit button with better styling
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.form_submit_button("🚀 Submit Evaluation", type="primary", use_container_width=True):
                        # Create evaluation record
                        evaluation = {
                            "prompt": current_prompt['prompt'],
                            "response": response_text,
                            "helpfulness_score": helpfulness,
                            "truthfulness_score": truthfulness,
                            "harmlessness_score": harmlessness,
                            "comments": comments,
                            "timestamp": datetime.now().isoformat()
                        }
                        
                        # Save evaluation
                        success = save_evaluation(evaluation)
                            
                        if success:
                            st.session_state.evaluations.append(evaluation)
                            st.success("🎉 Evaluation saved successfully!")
                            
                            # Auto-advance to next unrated prompt if available
                            if show_filter == "Unrated only" and st.session_state.current_index < len(prompts) - 1:
                                st.session_state.current_index += 1
                            
                            st.rerun()
                        else:
                            st.error("❌ Failed to save evaluation. Please try again.")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Add custom CSS for better styling
    st.markdown("""
    <style>
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .evaluation-form {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 0.75rem;
        border: 1px solid #e1e5e9;
        margin: 1rem 0;
    }
    .prompt-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0.75rem;
        border-left: 4px solid #4CAF50;
        margin: 1rem 0;
    }
    .response-card {
        background-color: #e3f2fd;
        padding: 1.5rem;
        border-radius: 0.75rem;
        border-left: 4px solid #2196F3;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Sidebar for navigation and filters
    with st.sidebar:
        st.header("🎛️ Controls & Analytics")
        
        # Progress indicator
        total_prompts = len(st.session_state.prompts)
        evaluated_count = len(st.session_state.evaluations)
        progress = evaluated_count / total_prompts if total_prompts > 0 else 0
        
        st.subheader("📈 Progress")
        st.progress(progress)
        st.caption(f"Evaluated: {evaluated_count}/{total_prompts} prompts ({progress:.1%})")
        
        # Filter options
        st.subheader("🔍 Filters")
        show_filter = st.selectbox(
            "Show prompts:",
            ["All prompts", "Unrated only", "Rated only"],
            help="Filter prompts based on evaluation status"
        )
        
        # Quick navigation
        if st.button("🎯 Jump to Next Unrated", use_container_width=True):
            unrated_indices = []
            evaluated_prompts = {eval_item['prompt'] for eval_item in st.session_state.evaluations}
            for i, prompt in enumerate(st.session_state.prompts):
                if prompt['prompt'] not in evaluated_prompts:
                    unrated_indices.append(i)
            
            if unrated_indices:
                st.session_state.current_index = unrated_indices[0]
                st.rerun()
            else:
                st.success("All prompts evaluated! 🎉")
        
        # Data storage indicator
        st.info("💾 Data Storage: JSON Files")
        
        # Statistics section
        st.header("📊 Analytics Dashboard")
        if st.session_state.evaluations:
            df_eval = pd.DataFrame(st.session_state.evaluations)
            
            # Average scores with color coding
            avg_helpfulness = df_eval['helpfulness_score'].mean()
            avg_truthfulness = df_eval['truthfulness_score'].mean()
            avg_harmlessness = df_eval['harmlessness_score'].mean()
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("🤝 Helpfulness", f"{avg_helpfulness:.2f}/5", 
                         delta=f"{avg_helpfulness-3:.2f}" if avg_helpfulness != 3 else None)
                st.metric("🛡️ Harmlessness", f"{avg_harmlessness:.2f}/5",
                         delta=f"{avg_harmlessness-3:.2f}" if avg_harmlessness != 3 else None)
            with col2:
                st.metric("✅ Truthfulness", f"{avg_truthfulness:.2f}/5",
                         delta=f"{avg_truthfulness-3:.2f}" if avg_truthfulness != 3 else None)
                st.metric("📝 Total Reviews", len(st.session_state.evaluations))
            
            # Score distribution chart
            st.subheader("📊 Score Distribution")
            scores_data = []
            for _, row in df_eval.iterrows():
                scores_data.extend([
                    {"Category": "Helpfulness", "Score": row['helpfulness_score']},
                    {"Category": "Truthfulness", "Score": row['truthfulness_score']},
                    {"Category": "Harmlessness", "Score": row['harmlessness_score']}
                ])
            
            if scores_data:
                scores_df = pd.DataFrame(scores_data)
                fig = px.histogram(scores_df, x="Score", color="Category", 
                                 title="Score Distribution by Category",
                                 nbins=5, range_x=[0.5, 5.5])
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
            
            # Recent evaluations
            st.subheader("🕒 Recent Evaluations")
            recent_evals = df_eval.tail(3)[['timestamp', 'helpfulness_score', 'truthfulness_score', 'harmlessness_score']].copy()
            
            # Fix timestamp formatting
            try:
                timestamps = pd.to_datetime(recent_evals['timestamp'])
                recent_evals['timestamp'] = timestamps.strftime('%m/%d %H:%M')
            except:
                recent_evals['timestamp'] = recent_evals['timestamp'].astype(str).str[:16]  # Fallback formatting
                
            st.dataframe(recent_evals, use_container_width=True, hide_index=True)
            
        else:
            st.info("📋 No evaluations yet - start rating to see analytics!")
    
    # Filter prompts based on selection
    prompts = st.session_state.prompts
    evaluated_prompts = {eval_item['prompt'] for eval_item in st.session_state.evaluations}
    
    if show_filter == "Unrated only":
        prompts = [p for p in prompts if p['prompt'] not in evaluated_prompts]
    elif show_filter == "Rated only":
        prompts = [p for p in prompts if p['prompt'] in evaluated_prompts]
    
    if not prompts:
        st.warning("No prompts match the current filter.")
        return
    
    # Navigation controls
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("⬅️ Previous", disabled=st.session_state.current_index <= 0):
            st.session_state.current_index = max(0, st.session_state.current_index - 1)
            st.rerun()
    
    with col2:
        st.markdown(f"**Prompt {st.session_state.current_index + 1} of {len(prompts)}**")
    
    with col3:
        if st.button("➡️ Next", disabled=st.session_state.current_index >= len(prompts) - 1):
            st.session_state.current_index = min(len(prompts) - 1, st.session_state.current_index + 1)
            st.rerun()
    
    # Ensure current index is valid
    if st.session_state.current_index >= len(prompts):
        st.session_state.current_index = 0
    
    current_prompt = prompts[st.session_state.current_index]
    
    # Display current prompt and response with improved styling
    st.markdown('<div class="prompt-card">', unsafe_allow_html=True)
    st.header("📝 Current Prompt")
    st.markdown(f"**Prompt #{st.session_state.current_index + 1}**")
    st.write(current_prompt['prompt'])
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Handle missing response with optional HF API integration
    response_text = current_prompt.get('response', '')
    
    if not response_text:
        st.warning("⚠️ No response available for this prompt.")
        
        # Optional: Generate response using Hugging Face API
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Generate Response with AI", use_container_width=True, type="secondary"):
                with st.spinner("🤖 Generating AI response..."):
                    try:
                        generated_response = get_completion_from_hf(current_prompt['prompt'])
                        if generated_response:
                            response_text = generated_response
                            # Update the prompt data and save to database
                            current_prompt['response'] = response_text
                            # Response updated in memory
                            st.success("✨ Response generated successfully!")
                            st.rerun()
                        else:
                            st.error("🔑 API key needed! Please set your Hugging Face API key to generate responses.")
                    except Exception as e:
                        st.error(f"❌ Error generating response: {str(e)}")
    
    if response_text:
        st.markdown('<div class="response-card">', unsafe_allow_html=True)
        st.header("🤖 GPT Response")
        st.write(response_text)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Check if this prompt has already been evaluated
        existing_eval = next(
            (eval_item for eval_item in st.session_state.evaluations 
             if eval_item['prompt'] == current_prompt['prompt']),
            None
        )
        
        if existing_eval:
            st.success("✅ This prompt has already been evaluated!")
            
            # Display existing evaluation in a nice format
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("🤝 Helpfulness", f"{existing_eval['helpfulness_score']}/5")
            with col2:
                st.metric("✅ Truthfulness", f"{existing_eval['truthfulness_score']}/5")
            with col3:
                st.metric("🛡️ Harmlessness", f"{existing_eval['harmlessness_score']}/5")
            
            if existing_eval.get('comments'):
                st.info(f"💬 **Comments:** {existing_eval['comments']}")
            
            eval_time = pd.to_datetime(existing_eval['timestamp']).strftime('%B %d, %Y at %I:%M %p')
            st.caption(f"🕒 Evaluated on {eval_time}")
            
        else:
            # Evaluation form with enhanced styling
            st.markdown('<div class="evaluation-form">', unsafe_allow_html=True)
            st.header("📊 Rate This Response")
            st.markdown("Please evaluate the GPT response across these three key dimensions:")
            
            with st.form("evaluation_form"):
                # Enhanced rating interface with descriptive labels
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("### 🤝 **Helpfulness**")
                    st.caption("How well does this response address the user's question or need?")
                    helpfulness = st.radio(
                        "Helpfulness Score",
                        options=[1, 2, 3, 4, 5],
                        format_func=lambda x: f"{x} - {'Poor' if x==1 else 'Fair' if x==2 else 'Good' if x==3 else 'Very Good' if x==4 else 'Excellent'}",
                        index=2,
                        key="helpfulness",
                        label_visibility="collapsed"
                    )
                
                with col2:
                    st.markdown("### ✅ **Truthfulness**")
                    st.caption("How accurate and factually correct is the information provided?")
                    truthfulness = st.radio(
                        "Truthfulness Score",
                        options=[1, 2, 3, 4, 5],
                        format_func=lambda x: f"{x} - {'Poor' if x==1 else 'Fair' if x==2 else 'Good' if x==3 else 'Very Good' if x==4 else 'Excellent'}",
                        index=2,
                        key="truthfulness",
                        label_visibility="collapsed"
                    )
                
                with col3:
                    st.markdown("### 🛡️ **Harmlessness**")
                    st.caption("How safe and free from harmful content is this response?")
                    harmlessness = st.radio(
                        "Harmlessness Score",
                        options=[1, 2, 3, 4, 5],
                        format_func=lambda x: f"{x} - {'Poor' if x==1 else 'Fair' if x==2 else 'Good' if x==3 else 'Very Good' if x==4 else 'Excellent'}",
                        index=2,
                        key="harmlessness",
                        label_visibility="collapsed"
                    )
                
                st.markdown("---")
                
                # Enhanced comments section
                comments = st.text_area(
                    "💬 Additional Comments (Optional)",
                    placeholder="Share any specific observations, concerns, or suggestions about this response...",
                    height=100
                )
                
                # Submit button with better styling
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.form_submit_button("🚀 Submit Evaluation", type="primary", use_container_width=True):
                        # Create evaluation record
                        evaluation = {
                            "prompt": current_prompt['prompt'],
                            "response": response_text,
                            "helpfulness_score": helpfulness,
                            "truthfulness_score": truthfulness,
                            "harmlessness_score": harmlessness,
                            "comments": comments,
                            "timestamp": datetime.now().isoformat()
                        }
                        
                        # Save evaluation
                        success = save_evaluation(evaluation)
                            
                        if success:
                            st.session_state.evaluations.append(evaluation)
                            st.success("🎉 Evaluation saved successfully!")
                            
                            # Auto-advance to next unrated prompt if available
                            if show_filter == "Unrated only" and st.session_state.current_index < len(prompts) - 1:
                                st.session_state.current_index += 1
                            
                            st.rerun()
                        else:
                            st.error("❌ Failed to save evaluation. Please try again.")
            
            st.markdown('</div>', unsafe_allow_html=True)

def generate_analysis_report(prompt, response, helpfulness, truthfulness, harmlessness, comments):
    """Generate a detailed analysis report."""
    report = f"""
GPT FEEDBACK ENGINE - ANALYSIS REPORT
=====================================
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

PROMPT ANALYSIS
--------------
Prompt: {prompt}
Word Count: {len(prompt.split())}
Character Count: {len(prompt)}
Has Question Mark: {'Yes' if '?' in prompt else 'No'}
Has Context: {'Yes' if any(word in prompt.lower() for word in ['for', 'as', 'like', 'example', 'please']) else 'No'}

RESPONSE ANALYSIS
----------------
Response: {response}
Word Count: {len(response.split())}
Character Count: {len(response)}
Sentences: {len([s for s in response.split('.') if s.strip()])}
Has Examples: {'Yes' if any(word in response.lower() for word in ['example', 'for instance', 'such as', 'like']) else 'No'}
Has Structure: {'Yes' if any(word in response.lower() for word in ['first', 'second', 'next', 'finally', '1.', '2.']) else 'No'}
Has Explanations: {'Yes' if any(word in response.lower() for word in ['because', 'therefore', 'this means', 'in other words']) else 'No'}

EVALUATION SCORES
----------------
Helpfulness: {helpfulness}/5
Truthfulness: {truthfulness}/5
Harmlessness: {harmlessness}/5
Overall Average: {(helpfulness + truthfulness + harmlessness) / 3:.2f}/5

ADDITIONAL COMMENTS
------------------
{comments if comments else 'No additional comments provided.'}

RECOMMENDATIONS
--------------
"""
    
    # Add recommendations based on scores
    if helpfulness < 3:
        report += "- Consider improving response relevance and usefulness\n"
    if truthfulness < 3:
        report += "- Verify factual accuracy and provide reliable sources\n"
    if harmlessness < 3:
        report += "- Review content for potential harmful or biased information\n"
    
    avg_score = (helpfulness + truthfulness + harmlessness) / 3
    if avg_score >= 4:
        report += "- Excellent response quality! Consider using as a template\n"
    elif avg_score >= 3:
        report += "- Good response with room for minor improvements\n"
    else:
        report += "- Response needs significant improvement in multiple areas\n"
    
    report += "\n---\nGenerated by GPT Feedback Engine"
    return report

def add_prompt_comparison_feature():
    """Add prompt comparison capabilities."""
    st.header("🔄 Prompt Comparison Lab")
    st.markdown("Compare different prompts and their responses side by side!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📝 Prompt A")
        prompt_a = st.text_area("First prompt:", height=100, key="prompt_a")
        response_a = st.text_area("Response A:", height=100, key="response_a")
    
    with col2:
        st.subheader("📝 Prompt B") 
        prompt_b = st.text_area("Second prompt:", height=100, key="prompt_b")
        response_b = st.text_area("Response B:", height=100, key="response_b")
    
    if prompt_a and response_a and prompt_b and response_b:
        if st.button("⚖️ Compare Prompts", type="primary", use_container_width=True):
            st.markdown("---")
            st.subheader("📊 Comparison Results")
            
            # Side by side metrics
            col_metrics1, col_metrics2 = st.columns(2)
            
            with col_metrics1:
                st.markdown("**📝 Prompt A Metrics**")
                st.metric("Words", len(prompt_a.split()))
                st.metric("Characters", len(prompt_a))
                st.metric("Response Words", len(response_a.split()))
            
            with col_metrics2:
                st.markdown("**📝 Prompt B Metrics**")
                st.metric("Words", len(prompt_b.split()))
                st.metric("Characters", len(prompt_b))
                st.metric("Response Words", len(response_b.split()))

if __name__ == "__main__":
    main()
