import streamlit as st
import openai
from streamlit_chat import message


openai.api_key = "Insert API Key"

# Set page title and header
st.set_page_config(page_title="App Selector")

################################################################################################

def gratitude_page(st):

    # Initialise session state variables
    if 'gratitude_generated' not in st.session_state:
        st.session_state['gratitude_generated'] = []
    if 'gratitude_past' not in st.session_state:
        st.session_state['gratitude_past'] = []
    if 'gratitude_messages' not in st.session_state:
        st.session_state['gratitude_messages'] = [
            {"role": "system", "content": "Hi ChatGPT, I'd like to start a gratitude exercise today. Can you help guide me through this process, asking me about what I'm grateful for and helping me explore why these things are meaningful to me? For example, if I say I'm grateful for the cup of coffee I had this morning, you might ask me why I'm grateful for it and help me connect it to deeper aspects of myself, such as how it might contribute to my productivity for the day. And when the conversations seems done, you can ask me if there's anything else I'm grateful for."},
        ]
    if 'gratitude_model_name' not in st.session_state:
        st.session_state['gratitude_model_name'] = []

    # Generate a response
    def generate_response(prompt):
        st.session_state['gratitude_messages'].append({"role": "user", "content": prompt})

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=st.session_state['gratitude_messages'],
            max_tokens=3000,
            temperature=0.6
        )
        response = completion.choices[0].message.content.strip()
        st.session_state['gratitude_messages'].append({"role": "system", "content": response})

        return response
    
    st.markdown('<div style="background-color: #F8E8EE; padding: 10px; border-radius: 10px; text-align: center;"><h1>Jamie the Grounded</h1></div>', unsafe_allow_html=True)
    st.markdown('')
    st.write('Gratitude is vital as it helps us focus on what truly matters in life and reduces anxiety, stress, and self-doubt. Studies have shown that practicing gratitude improves our mental health. To cultivate a grateful mindset, it is beneficial to engage in gratitude exercises.')
    st.write('Feel free to reach out to Jamie, and she will provide prompt responses to help you on your gratitude journey. Enjoy your time with her!')
    
    # Container for chat history
    response_container = st.container()
    # Container for text box
    container = st.container()

    

    with container:
        with st.form(key='my_form', clear_on_submit=True):
            user_input = st.text_area("You:", key='input', height=100)

            if st.form_submit_button("Send"):
                output = generate_response(user_input)
                st.session_state['gratitude_past'].append(user_input)
                st.session_state['gratitude_generated'].append(output)
                st.session_state['gratitude_model_name'].append("GPT-3.5")

        if st.button("New Session"):
            st.session_state['gratitude_generated'] = []
            st.session_state['gratitude_past'] = []
            st.session_state['gratitude_messages'] = [
                {"role": "system", "content": "Hi ChatGPT, I'd like to start a gratitude exercise today. Can you help guide me through this process, asking me about what I'm grateful for and helping me explore why these things are meaningful to me? For example, if I say I'm grateful for the cup of coffee I had this morning, you might ask me why I'm grateful for it and help me connect it to deeper aspects of myself, such as how it might contribute to my productivity for the day. And when the conversations seems done, you can ask me if there's anything else I'm grateful for."}
            ]
            st.session_state['gratitude_model_name'] = []

        if st.session_state['gratitude_generated']:
            with response_container:
                for i in range(len(st.session_state['gratitude_generated'])): 
                    if i < len(st.session_state["gratitude_past"]):
                        message(st.session_state["gratitude_past"][i], is_user=True, key=str(i) + '_user')
                    message(st.session_state["gratitude_generated"][i], key=str(i))

    if st.button('Go back'):
        st.session_state['selected_app'] = None
                    
############################################################################################################

def mental_app_page(st):
    # Initialise session state variables
    if 'mental_app_generated' not in st.session_state:
        st.session_state['mental_app_generated'] = []
    if 'mental_app_past' not in st.session_state:
        st.session_state['mental_app_past'] = []
    if 'mental_app_messages' not in st.session_state:
        st.session_state['mental_app_messages'] = [
            {"role": "system", "content": "Hi ChatGPT, I'd like you to act as an intelligent and empathetic psychotherapist for me today. Can you help guide me through a process of self-reflection, asking me questions that will help me better understand my own thoughts and feelings? I'd like you to gather as much information as possible about my mental state and current circumstances. Then, I'd like you to analyze this information and provide me with detailed insights, not a diagnosis, but a deeper understanding of my mental state. These insights should be expansive, precise, and supported by scientific evidence. I'd like our interaction to be conversational and comfortable."},
            {"role": "assistant", "content": "Hi! How are you feeling today? Is there something specific on your mind that you'd like to talk about?"}  # Add the initial message here
        ]
    if 'mental_app_model_name' not in st.session_state:
        st.session_state['mental_app_model_name'] = []
    if 'mental_app_analysis' not in st.session_state:
        st.session_state['mental_app_analysis'] = ""  # Add a session variable to store analysis result


    # Generate a response
    def generate_response(prompt):
        st.session_state['mental_app_messages'].append({"role": "user", "content": prompt})

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=st.session_state['mental_app_messages'],
            max_tokens=3000,
            temperature=0.6
        )
        response = completion.choices[0].message.content.strip()
        st.session_state['mental_app_messages'].append({"role": "assistant", "content": response})

        return response
    # Analyze user messages
    def generate_analysis():
        user_messages = st.session_state['mental_app_past'][-5:]  # Get the last 5 user messages
        merged_user_messages = " ".join(user_messages)  # Merge the user messages into a single prompt

        st.session_state['mental_app_messages'] = [
            {"role": "system", "content": "Hi ChatGPT, I'd like you to act as an intelligent and empathetic psychotherapist for me today. Can you help guide me through a process of self-reflection, asking me questions that will help me better understand my own thoughts and feelings? I'd like you to gather as much information as possible about my mental state and current circumstances. Then, I'd like you to analyze this information and provide me with detailed insights, not a diagnosis, but a deeper understanding of my mental state. These insights should be expansive, precise, and supported by scientific evidence. I'd like our interaction to be conversational and comfortable."},
            {"role": "user", "content": merged_user_messages},
            {"role": "system", "content": "Hi ChatGPT, let's imagine you're a psychotherapist who has just finished a therapy session with me. Now, I'd like you to review and analyze the information gathered during our session. Please take an objective and intelligent approach, using precise and technical language that I can still understand. Instead of offering a solution, I'd like you to provide a comprehensive analysis or report of my potential experiences and how various aspects are interconnected. I'd like you to mimic the behavior of a therapist who is attempting to comprehend and make sense of the situation after the session."}
        ]

        st.session_state['mental_app_analysis'] = generate_response("")  # Update the analysis session variable

    st.markdown('<div style="background-color: #E3F4F4; padding: 10px; border-radius: 10px;text-align: center;"><h1>Katie the Catalyst</h1></div>', unsafe_allow_html=True)
    st.markdown('')

    st.write("Gaining the ability to analyze your thoughts and emotions is a powerful way to enhance your mental well-being. Understanding the underlying reasons behind your feelings allows you to respond effectively and take appropriate actions. It's crucial to not only experience emotions but also objectively comprehend them, exploring why they arise and how to address them.")
    st.write("Katie is here to assist you in comprehending your own feelings. Feel free to begin a conversation with her, and she will respond promptly to help you navigate your emotional landscape.")

    # Container for chat history
    response_container = st.container()
    # Container for text box
    container = st.container()

    # New Session button
    if st.button("New Session"):
        st.session_state['mental_app_generated'] = []
        st.session_state['mental_app_past'] = []
        st.session_state['mental_app_messages'] = [
            {"role": "system", "content": "You are a psychotherapist, understand what I am going through. Allow me to express my feelings and be empathetic. Provide me assurance, and ask me follow up questions that I can better understand what I am feeling"}
        ]
        st.session_state['mental_app_model_name'] = []
        st.session_state['mental_app_analysis'] = ""  # Reset the analysis session variable

    with container:
        with st.form(key='my_form', clear_on_submit=True):
            user_input = st.text_area("You:", key='input', height=100)
            submit_button = st.form_submit_button(label='Send')

        if submit_button and user_input:
            output = generate_response(user_input)
            st.session_state['mental_app_past'].append(user_input)
            st.session_state['mental_app_generated'].append(output)
            st.session_state['mental_app_model_name'].append("GPT-3.5")

        st.write("When you are ready and have provided enough information to Katie, click the button below to generate an analysis.")

        # Replace the if condition for the analysis button with a permanent button
        analysis_button = st.button("Generate Analysis")
        if analysis_button:
            generate_analysis()

    if st.session_state['mental_app_generated']:
        with response_container:
            for i in range(len(st.session_state['mental_app_generated'])):
                if i < len(st.session_state["mental_app_past"]):
                    message(st.session_state["mental_app_past"][i], is_user=True, key=str(i) + '_user')
                message(st.session_state["mental_app_generated"][i], key=str(i))

    # Add a new section for displaying the analysis
    if st.session_state['mental_app_analysis']:
        st.markdown(f"## Analysis")
        st.markdown(st.session_state['mental_app_analysis'])

    if st.button('Go back'):
        st.session_state['selected_app'] = None

############################################################################################################

def encourager_page(st):
    # Initialise session state variables
    if 'encourager_generated' not in st.session_state:
        st.session_state['encourager_generated'] = []
    if 'encourager_past' not in st.session_state:
        st.session_state['encourager_past'] = []
    if 'encourager_messages' not in st.session_state:
        st.session_state['encourager_messages'] = [
            {"role": "system", "content": "Hi ChatGPT, I'd like you to act as a supportive life coach for me today. Can you help guide me through a process of self-encouragement, asking me questions that will help me focus on the positive aspects of my life and believe in myself? I'd like you to transform negative situations into positive ones, while maintaining a high level of empathy and sensitivity. I'd like our interaction to be conversational and comfortable, with you consistently posing questions that foster encouragement. For instance, you might ask about what I believe in about myself, and then affirm these beliefs and explain why they're beneficial. Your ultimate goal should be to provide unwavering support and optimism throughout our conversation. Be empathetic and don't just give lists of things to do."}
        ]
    if 'encourager_model_name' not in st.session_state:
        st.session_state['encourager_model_name'] = []

    # Generate a response
    def generate_response(prompt):
        st.session_state['encourager_messages'].append({"role": "user", "content": prompt})

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=st.session_state['encourager_messages'],
            max_tokens=3000,
            temperature=0.6
        )
        response = completion.choices[0].message.content.strip()
        st.session_state['encourager_messages'].append({"role": "system", "content": response})

        return response
    
    st.markdown('<div style="background-color: #FFFEC4; padding: 10px; border-radius: 10px;text-align: center;"><h1>Nathan the Coach</h1></div>', unsafe_allow_html=True)
    st.markdown('')

    st.write("Maintaining a positive mindset and receiving encouragement about your abilities can be incredibly valuable, especially when faced with life's challenges. Having someone who hypes you up and reminds you of your capabilities can make a significant difference.")
    st.write("That's where Nathan, your personal coach, comes in. Nathan will provide you with the motivation and encouragement you need. Feel free to start a conversation with Nathan, and he will respond promptly to provide you with an instant boost of support and positivity. Enjoy your chat with him!")

    # Container for chat history
    response_container = st.container()
    # Container for text box
    container = st.container()

    with container:
        with st.form(key='my_form', clear_on_submit=True):
            user_input = st.text_area("You:", key='input', height=100)

            if st.form_submit_button("Send"):
                output = generate_response(user_input)
                st.session_state['encourager_past'].append(user_input)
                st.session_state['encourager_generated'].append(output)
                st.session_state['encourager_model_name'].append("GPT-3.5")

        if st.button("New Session"):
            st.session_state['encourager_generated'] = []
            st.session_state['encourager_past'] = []
            st.session_state['encourager_messages'] = [
                {"role": "system", "content": "Hi ChatGPT, I'd like you to act as a supportive life coach for me today. Can you help guide me through a process of self-encouragement, asking me questions that will help me focus on the positive aspects of my life and believe in myself? I'd like you to transform negative situations into positive ones, while maintaining a high level of empathy and sensitivity. I'd like our interaction to be conversational and comfortable, with you consistently posing questions that foster encouragement. For instance, you might ask about what I believe in about myself, and then affirm these beliefs and explain why they're beneficial. Your ultimate goal should be to provide unwavering support and optimism throughout our conversation. Be empathetic and don't just give lists of things to do."}
            ]
            st.session_state['encourager_model_name'] = []

        if st.session_state['encourager_generated']:
            with response_container:
                for i in range(len(st.session_state['encourager_generated'])): 
                    if i < len(st.session_state["encourager_past"]):
                        message(st.session_state["encourager_past"][i], is_user=True, key=str(i) + '_user')
                    message(st.session_state["encourager_generated"][i], key=str(i))

    if st.button('Go back'):
        st.session_state['selected_app'] = None

############################################################################################################

# Create a dictionary to map app names to their corresponding functions
apps = {
    "Gratitude": gratitude_page,
    "Analyzer": mental_app_page,
    "Encourager": encourager_page
}

# Initialize session_state if it doesn't exist
if 'selected_app' not in st.session_state:
    st.session_state['selected_app'] = None

if st.session_state['selected_app'] is None:

    st.image('logo.png')
    st.write('**Introducing the resiliAInce, your AI powered mental health chatbot! Within this platform, you\'ll have the opportunity to chat with three chatbots: Jamie, Katie, and Nathan. These chatbots, powered by language models, are designed to support you in various aspects of your mental health.**')

    st.write('**While they can offer valuable assistance, it\'s crucial to remember that they are not a substitute for professional help. Seeking guidance from qualified mental health professionals is highly encouraged, as they underwent rigorous training and assessment.**')

    st.write('**This platform serves as a demonstration of how AI can complement mental health support, providing a starting point for those seeking assistance. Enjoy your experience and discover how this innovative tool can potentially aid you in your mental well-being journey.**')

    st.markdown("Developed by [Eys](https://www.linkedin.com/in/acecanacan/)", unsafe_allow_html=True)

    st.markdown('<div style="background-color: #F8E8EE; padding: 10px; border-radius: 10px;text-align: center;"><h1>Jamie the Grounded</h1></div>', unsafe_allow_html=True)
    st.write('Jamie the Grounded is your daily reminder of the good things in life. As a dedicated gratitude companion, she pushes you to engage in daily gratitude exercises to stay grounded and appreciative of what you have.')
    st.write('Her goal is to help you realize the positive aspects of your life consistently. With her, gratitude is not an occasional activity but a daily habit. Her ultimate aim is to help you cultivate a sense of appreciation that you can carry throughout your day')

    if st.button('Chat with Jamie'):
        st.session_state['selected_app'] = "Gratitude"

    st.markdown('<div style="background-color: #E3F4F4; padding: 10px; border-radius: 10px;text-align: center;"><h1>Katie the Catalyst</h1></div>', unsafe_allow_html=True)
    st.write('Katie the Catalyst is your supportive life coach with a knack for in-depth psychotherapeutic analysis. She drives your journey of self-discovery, focusing on the technical side of mental health.')
    st.write('Katie’s primary function is to thoroughly analyze and interpret your thoughts and feelings, revealing insights about your personality and emotional state. She serves as your guide, helping you comprehend what you are experiencing, and provides direction for facing your challenges')

    if st.button('Chat with Katie'):
        st.session_state['selected_app'] = "Analyzer"

    st.markdown('<div style="background-color: #FFFEC4; padding: 10px; border-radius: 10px;text-align: center;"><h1>Nathan the Coach</h1></div>', unsafe_allow_html=True)
    st.write('Nathan the Coach is your personal motivator, always there to bolster your self-belief. He champions your unique qualities, helping you recognize and embrace your individual potential. The primary goal of Nathan is to help you see what makes you distinct and amazing.')
    st.write('With him, every interaction is a celebration of your uniqueness, a step towards realizing your full potential. As an encourager, his primary function is to uplift, spotlight your strengths, and cheer you on in your journey of self-growth.')

    if st.button('Chat with Nathan'):
        st.session_state['selected_app'] = "Encourager"

elif st.session_state['selected_app'] == "Gratitude":
    gratitude_page(st)
elif st.session_state['selected_app'] == "Analyzer":
    mental_app_page(st)
elif st.session_state['selected_app'] == "Encourager":
    encourager_page(st)
